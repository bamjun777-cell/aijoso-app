package com.aijoso.app.data

import android.content.Context
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import kotlinx.serialization.KSerializer
import kotlinx.serialization.Serializable
import kotlinx.serialization.builtins.ListSerializer
import kotlinx.serialization.builtins.MapSerializer
import kotlinx.serialization.builtins.serializer
import java.time.LocalDate
import java.util.UUID

/** 내가 보낸 의견. status: pending(전송 대기) / sent(접수됨). 반영 여부는 content.json의 resolvedFeedback으로 판단 */
@Serializable
data class MyFeedback(
    val id: String,
    val contentId: String,
    val type: String,
    val text: String,
    val date: String,
    val status: String = "pending",
)

/** 회원가입 없이 모든 개인 데이터는 이 휴대폰에만 저장 (SharedPreferences) */
class AppStore(context: Context) {
    private val sp = context.getSharedPreferences("aijoso", Context.MODE_PRIVATE)
    private val strList = ListSerializer(String.serializer())
    private val strMap = MapSerializer(String.serializer(), String.serializer())
    private val fbList = ListSerializer(MyFeedback.serializer())

    val favs = mutableStateListOf<String>().apply { addAll(read("favs", strList) ?: emptyList()) }
    val recent = mutableStateListOf<String>().apply { addAll(read("recent", strList) ?: emptyList()) }
    val requests = mutableStateListOf<String>().apply { addAll(read("reqs", strList) ?: emptyList()) }
    val values = mutableStateMapOf<String, String>().apply { putAll(read("vals", strMap) ?: emptyMap()) }
    val reactions = mutableStateMapOf<String, String>().apply { putAll(read("react", strMap) ?: emptyMap()) }
    val myFeedback = mutableStateListOf<MyFeedback>().apply { addAll(read("myfb", fbList) ?: emptyList()) }
    var fontScale by mutableFloatStateOf(sp.getFloat("fontScale", 1f))
        private set
    /** 화면 언어. "" = 휴대폰 설정 따르기 */
    var lang by mutableStateOf(sp.getString("lang", "") ?: "")
        private set

    fun updateLang(v: String) { lang = v; sp.edit().putString("lang", v).apply() }

    /** 프롬프트를 붙여넣을 기본 AI. "" = 매번 고르기 */
    var ai by mutableStateOf(sp.getString("ai", "") ?: "")
        private set

    fun updateAi(v: String) { ai = v; sp.edit().putString("ai", v).apply() }

    private fun <T> read(key: String, s: KSerializer<T>): T? =
        sp.getString(key, null)?.let { runCatching { ContentJson.decodeFromString(s, it) }.getOrNull() }

    private fun <T> write(key: String, s: KSerializer<T>, v: T) {
        sp.edit().putString(key, ContentJson.encodeToString(s, v)).apply()
    }

    fun toggleFav(id: String) {
        if (!favs.remove(id)) favs.add(0, id)
        write("favs", strList, favs.toList())
    }

    fun touchRecent(id: String) {
        recent.remove(id); recent.add(0, id)
        while (recent.size > 20) recent.removeAt(recent.lastIndex)
        write("recent", strList, recent.toList())
    }

    fun toggleRequest(id: String): Boolean {
        val added = if (requests.remove(id)) false else { requests.add(id); true }
        write("reqs", strList, requests.toList())
        return added
    }

    fun setValue(key: String, v: String) {
        values[key] = v
        write("vals", strMap, values.toMap())
    }

    /** 같은 버튼을 다시 누르면 취소. 반환값: 현재 선택 */
    fun react(id: String, kind: String): String? {
        if (reactions[id] == kind) reactions.remove(id) else reactions[id] = kind
        write("react", strMap, reactions.toMap())
        return reactions[id]
    }

    fun addFeedback(contentId: String, type: String, text: String): MyFeedback {
        val fb = MyFeedback(
            id = "fb-" + UUID.randomUUID().toString().take(12),   // 사람을 알 수 없는 무작위 번호
            contentId = contentId, type = type, text = text.trim(),
            date = LocalDate.now().toString(),
        )
        myFeedback.add(fb)
        write("myfb", fbList, myFeedback.toList())
        return fb
    }

    fun updateFontScale(v: Float) {
        fontScale = v
        sp.edit().putFloat("fontScale", v).apply()
    }
}
