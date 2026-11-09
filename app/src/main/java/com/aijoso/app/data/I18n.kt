package com.aijoso.app.data

import androidx.compose.runtime.staticCompositionLocalOf
import kotlinx.serialization.Serializable
import java.util.Locale

/**
 * 화면 문구 (ui.json, 웹과 공통). 언어: ko · en · ja · zh-Hans · zh-Hant
 * 문구가 없으면 영어 → 한국어 순으로 대신 보여 준다.
 */
@Serializable
data class UiFile(
    val langs: List<String> = emptyList(),
    val names: Map<String, String> = emptyMap(),
    val chips: Map<String, List<String>> = emptyMap(),
    val strings: Map<String, Map<String, String>> = emptyMap(),
)

class Ui(val lang: String, private val file: UiFile) {
    val langs get() = file.langs
    fun langName(code: String) = file.names[code] ?: code
    val chips: List<String> get() = file.chips[lang] ?: file.chips["en"].orEmpty()

    /** t("count.n", "n" to 3) → "3개" */
    fun t(key: String, vararg args: Pair<String, Any>): String {
        val m = file.strings[key] ?: return key
        var s = m[lang] ?: m["en"] ?: m["ko"] ?: key
        for ((k, v) in args) s = s.replace("{$k}", v.toString())
        return s
    }

    fun difficulty(d: String) = t("diff.$d")
    fun frequency(f: String) = t("freq.${f.ifBlank { "수시" }}")
}

val LocalUi = staticCompositionLocalOf<Ui> { error("Ui not provided") }

fun parseUi(text: String): UiFile = ContentJson.decodeFromString(UiFile.serializer(), text)

/** 저장된 선택("" = 휴대폰 설정 따르기)과 기기 언어로 실제 언어를 정한다. 한국어·일본어·중국어 외에는 영어 */
fun resolveLang(pref: String, locale: Locale = Locale.getDefault()): String {
    if (pref.isNotBlank()) return pref
    return when (locale.language) {
        "ko" -> "ko"
        "ja" -> "ja"
        "zh" -> if (locale.script == "Hant" || locale.country in setOf("TW", "HK", "MO")) "zh-Hant" else "zh-Hans"
        else -> "en"
    }
}

/** 언어별 콘텐츠 파일 이름 */
fun contentAsset(lang: String) = if (lang == "ko") "content.json" else "content.$lang.json"
