package com.aijoso.app.data

import java.text.Normalizer

/**
 * 의견 입력 검사 (욕설·비속어·개인정보·길이).
 * 시안(moderation.js)·저장소 규칙(firestore.rules)과 같은 규칙. 목록은 content.json에서 받아 앱 업데이트 없이 바꿀 수 있다.
 */
class Moderator(m: Moderation) {
    data class Check(val ok: Boolean, val reason: String = "", val message: String = "")

    private val minLength = m.minLength
    private val maxLength = m.maxLength
    private val strip = Regex("[^가-힣ㄱ-ㅎㅏ-ㅣa-z]")
    private val allow = m.allow.map { it.lowercase() }
    private val banned = m.banned.map { strip.replace(it.lowercase(), "") }.filter { it.isNotEmpty() }
    private val phone = Regex("""01[016789][\s.\-]?\d{3,4}[\s.\-]?\d{4}""")
    private val email = Regex("""[\w.+-]+@[\w-]+\.[\w.]+""")
    private val rrn = Regex("""\d{6}[\s\-]?[1-8]\d{6}""")
    private val spaces = Regex("""\s+""")

    fun check(raw: String): Check {
        val text = Normalizer.normalize(raw.lowercase(), Normalizer.Form.NFC)
        val len = raw.trim().length
        if (len < minLength) return Check(false, "short", "${minLength}자 이상 적어 주세요")
        if (len > maxLength) return Check(false, "long", "${maxLength}자까지 쓸 수 있어요")
        if (phone.containsMatchIn(text) || email.containsMatchIn(text) || rrn.containsMatchIn(text))
            return Check(false, "pii", "전화번호·이메일·주민번호는 적지 말아 주세요")
        var s = text
        for (a in allow) s = s.replace(a, " ")                 // 허용 단어(시발점 등) 먼저 제외 → 오탐 방지
        val tokens = s.split(spaces).map { strip.replace(it, "") }.filter { it.isNotEmpty() }
        val candidates = tokens.toMutableList()
        // 한 글자씩 띄어 쓴 우회(씨 발, 개 새 끼)만 이어 붙여 검사. "다시 발표"처럼 두 글자 이상 단어는 붙이지 않음
        val run = StringBuilder()
        for (w in tokens + "##") {
            if (w.length == 1) run.append(w) else { if (run.length > 1) candidates += run.toString(); run.clear() }
        }
        if (candidates.any { c -> banned.any { b -> c.contains(b) } })
            return Check(false, "abuse", "욕설·비속어가 있어 보낼 수 없어요")
        return Check(true)
    }
}
