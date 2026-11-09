package com.aijoso.app.data

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement

/** content.json 구조. 화면 코드는 이 데이터만 보고 그린다 (콘텐츠 추가 시 코드 수정 불필요). */
@Serializable
data class ContentFile(
    val schemaVersion: Int = 1,
    val contentVersion: String = "",
    val updatedAt: String = "",
    val categories: List<Category> = emptyList(),
    val synonyms: Map<String, List<String>> = emptyMap(),
    val items: List<Item> = emptyList(),
    val featured: List<String> = emptyList(),
    val feedback: FeedbackConfig = FeedbackConfig(),
    val moderation: Moderation = Moderation(),
    val changelog: List<Change> = emptyList(),
    val resolvedFeedback: List<String> = emptyList(),
) {
    fun categoryName(id: String): String = categories.firstOrNull { it.id == id }?.name ?: id
    fun item(id: String): Item? = items.firstOrNull { it.id == id }
    val published: List<Item> get() = items.filter { it.isPublished }
    /** 홈 추천: featured 목록 순서대로, 없으면 공개 매뉴얼 앞 6개 */
    val featuredItems: List<Item> get() = featured.mapNotNull { item(it) }.filter { it.isPublished }.ifEmpty { published.take(6) }
}

@Serializable
data class Category(val id: String, val name: String, val order: Int = 0)

@Serializable
data class Item(
    val id: String,
    val status: String = "draft",
    val lang: String = "ko",
    val title: String,
    val subtitle: String = "",
    val category: String = "",
    val tags: List<String> = emptyList(),
    val difficulty: String = "easy",
    val frequency: String = "",
    val timeBeforeMin: Int = 0,
    val timeAfterMin: Int = 0,
    val freePlanOk: Boolean = true,
    val tools: List<Tool> = emptyList(),
    val problem: String = "",
    val before: String = "",
    val after: String = "",
    val prepare: List<String> = emptyList(),
    val project: Project? = null,
    val prompts: List<Prompt> = emptyList(),
    val steps: List<Step> = emptyList(),
    val result: ResultInfo? = null,
    val cautions: List<String> = emptyList(),
    val videos: List<JsonElement> = emptyList(),
    val docs: List<Doc> = emptyList(),
    val legal: Legal? = null,
    val verifiedAt: String = "",
    val updatedAt: String = "",
    val printSample: JsonElement? = null,
) {
    val isPublished: Boolean get() = status == "published"
}

@Serializable data class Tool(val name: String, val free: Boolean = true, val note: String = "")
@Serializable data class Project(val recommended: Boolean = false, val name: String = "", val instructions: String = "", val knowledge: List<String> = emptyList())
@Serializable data class Prompt(val id: String, val title: String, val howTo: String = "", val body: String, val variables: List<Variable> = emptyList())
@Serializable data class Variable(val key: String, val label: String, val example: String = "")
@Serializable data class Step(val title: String, val body: String = "", val check: String = "")
@Serializable data class ResultInfo(val summary: String = "", val example: String = "")
@Serializable data class Doc(val title: String, val publisher: String = "", val url: String, val verifiedAt: String = "")
@Serializable data class Legal(val note: String = "", val checkedAt: String = "", val disclaimer: String = "")
@Serializable data class FeedbackType(val id: String, val label: String)
@Serializable data class FeedbackConfig(val types: List<FeedbackType> = emptyList(), val minLength: Int = 5, val maxLength: Int = 300, val storage: String = "")
@Serializable data class Moderation(val minLength: Int = 5, val maxLength: Int = 300, val banned: List<String> = emptyList(), val allow: List<String> = emptyList(), val checkedAt: String = "")
@Serializable data class Change(val date: String, val contentId: String? = null, val text: String, val source: String = "")

val ContentJson = Json {
    ignoreUnknownKeys = true
    coerceInputValues = true
    explicitNulls = false
    isLenient = true
}

fun parseContent(text: String): ContentFile = ContentJson.decodeFromString(ContentFile.serializer(), text)

fun difficultyLabel(d: String): String = when (d) {
    "easy" -> "난이도 하"
    "normal" -> "난이도 중"
    "hard" -> "난이도 상"
    else -> d
}

fun frequencyLabel(f: String): String = if (f == "수시" || f.isBlank()) "수시" else "매$f"

private val VAR = Regex("""\{\{(.+?)\}\}""")

/** 프롬프트 빈칸 채우기: 사용자가 입력한 값, 없으면 예시값 */
fun fillPrompt(itemId: String, p: Prompt, values: Map<String, String>): String =
    VAR.replace(p.body) { m -> valueFor(itemId, p, m.groupValues[1], values) }

fun valueFor(itemId: String, p: Prompt, key: String, values: Map<String, String>): String =
    values["$itemId.$key"]?.trim()?.takeIf { it.isNotEmpty() }
        ?: p.variables.firstOrNull { it.key == key }?.example
        ?: key

/** 화면 미리보기용: (글자, 빈칸에서 온 값인지) 조각 목록 */
fun promptSegments(itemId: String, p: Prompt, values: Map<String, String>): List<Pair<String, Boolean>> {
    val out = mutableListOf<Pair<String, Boolean>>()
    var last = 0
    for (m in VAR.findAll(p.body)) {
        if (m.range.first > last) out += p.body.substring(last, m.range.first) to false
        out += valueFor(itemId, p, m.groupValues[1], values) to true
        last = m.range.last + 1
    }
    if (last < p.body.length) out += p.body.substring(last) to false
    return out
}
