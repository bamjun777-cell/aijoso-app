package com.aijoso.app

import com.aijoso.app.data.ContentFile
import com.aijoso.app.data.Moderator
import com.aijoso.app.data.Searcher
import com.aijoso.app.data.fillPrompt
import com.aijoso.app.data.parseContent
import com.aijoso.app.data.parseUi
import com.aijoso.app.data.Ui
import com.aijoso.app.data.resolveLang
import com.aijoso.app.data.contentAsset
import java.util.Locale
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File

/** 빌드할 때마다 자동으로 도는 검사: 콘텐츠 파일, 검색, 비속어 필터 */
class LogicTest {
    private val content: ContentFile = parseContent(File("src/main/assets/content.json").readText())
    private val langs = listOf("ko", "en", "ja", "zh-Hans", "zh-Hant")
    private fun load(lang: String) = parseContent(File("src/main/assets/" + contentAsset(lang)).readText())
    private val uiFile = parseUi(File("src/main/assets/ui.json").readText())

    @Test fun everyLanguageHasAllManuals() {
        val ids = content.items.map { it.id }
        for (l in langs) {
            val c = load(l)
            // 한국어판은 전체, 외국어판은 번역된 매뉴얼만 (한국어판 순서와 같게)
            if (l == "ko") assertEquals(ids, c.items.map { it.id }) else assertEquals(l, ids.filter { it in c.items.map { i -> i.id } }, c.items.map { it.id })
            assertTrue(l, c.published.size >= 30)
            assertEquals(l, 8, c.categories.size)
            // 파일을 만드는 매뉴얼 표시(AI별 파일 기능 안내)는 언어마다 같아야 함
            val ko = content.items.associate { it.id to it.fileOutput }
            for (item in c.items) assertEquals("$l/${item.id} fileOutput", ko[item.id], item.fileOutput)
            // 빈칸과 입력칸이 맞는지 (언어마다)
            val re = Regex("""\{\{(.+?)\}\}""")
            for (item in c.items) for (p in item.prompts)
                assertEquals("$l/${item.id}/${p.id}", p.variables.map { it.key }.toSet(), re.findAll(p.body).map { it.groupValues[1] }.toSet())
        }
    }

    @Test fun everyScreenTextIsTranslated() {
        assertEquals(langs, uiFile.langs)
        for ((key, m) in uiFile.strings) for (l in langs) assertTrue("$key/$l", !m[l].isNullOrBlank())
        for (l in langs) assertEquals(l, 3, uiFile.chips[l]?.size)
        assertEquals("3개", Ui("ko", uiFile).t("count.n", "n" to 3))
        assertEquals("12 min", Ui("en", uiFile).t("min.n", "n" to 12))
    }

    @Test fun deviceLanguagePicksContent() {
        assertEquals("ko", resolveLang("", Locale.KOREA))
        assertEquals("ja", resolveLang("", Locale.JAPAN))
        assertEquals("zh-Hant", resolveLang("", Locale.TAIWAN))
        assertEquals("zh-Hans", resolveLang("", Locale.SIMPLIFIED_CHINESE))
        assertEquals("en", resolveLang("", Locale.GERMANY))
        assertEquals("ja", resolveLang("ja", Locale.KOREA))   // 앱에서 고른 언어가 우선
    }

    @Test fun searchWorksInEveryLanguage() {
        val cases = mapOf(
            "en" to mapOf("Comparing payroll every month takes forever" to "payroll-variance-check", "merge branch excel files" to "excel-merge-files", "overtime hours" to "hr-attendance-overtime", "decline email" to "report-email", "vlookup error" to "excel-formula"),
            "ja" to mapOf("毎月の給与比較に時間がかかる" to "payroll-variance-check", "支店のExcelをまとめる" to "excel-merge-files", "有給の残日数" to "hr-annual-leave", "お断りのメール" to "report-email"),
            "zh-Hans" to mapOf("工资环比核对" to "payroll-variance-check", "合并分店 Excel" to "excel-merge-files", "加班费怎么算" to "hr-attendance-overtime", "宏" to "excel-vba"),
            "zh-Hant" to mapOf("薪資環比核對" to "payroll-variance-check", "特休" to "hr-annual-leave", "盤點庫存" to "logistics-stock"),
        )
        for ((l, qs) in cases) { val s = Searcher(load(l)); for ((q, id) in qs) assertEquals("$l: $q", id, s.search(q).firstOrNull()?.id) }
    }

    @Test fun moderationOtherLanguages() {
        val en = Moderator(load("en").moderation)
        listOf("The pivot steps were really helpful, thanks", "Please add an assessment template", "Scunthorpe branch uses this", "Step 2 changed on 2026-11-09").forEach { assertTrue("pass: $it", en.check(it).ok) }
        listOf("this is fucking useless", "what a piece of s h i t app", "call me at +1 (415) 555-0132", "my SSN is 123-45-6789").forEach { assertFalse("block: $it", en.check(it).ok) }
        val ja = Moderator(load("ja").moderation)
        assertTrue(ja.check("手順3のメニュー名が違います").ok)
        assertFalse(ja.check("こんなアプリ死ねばいい").ok)
        assertFalse(ja.check("電話は090-1234-5678です").ok)
        val zh = Moderator(load("zh-Hans").moderation)
        assertTrue(zh.check("第二步的菜单名称不一样").ok)
        assertFalse(zh.check("这个傻逼应用").ok)
        val tw = Moderator(load("zh-Hant").moderation)
        assertFalse(tw.check("幹你娘 這什麼爛東西").ok)
        assertFalse(tw.check("我的電話 0912-345-678").ok)
    }

    @Test fun contentLoads() {
        assertEquals(72, content.items.size)
        assertEquals(72, content.published.size)
        // 분야마다 9개
        content.categories.forEach { cat -> assertEquals(cat.id, 9, content.published.count { it.category == cat.id }) }
        assertEquals(6, content.featuredItems.size)
        // 홈은 분야별로 묶어 모두 보여 주므로, 모든 공개 매뉴얼이 실제 분야에 속해야 함
        assertTrue(content.published.all { p -> content.categories.any { it.id == p.category } })
        assertEquals(8, content.categories.size)
    }

    @Test fun everyPromptBlankHasAnInput() {
        val re = Regex("""\{\{(.+?)\}\}""")
        for (item in content.items) for (p in item.prompts) {
            val keys = re.findAll(p.body).map { it.groupValues[1] }.toSet()
            assertEquals("${item.id}/${p.id}", p.variables.map { it.key }.toSet(), keys)
        }
    }

    @Test fun fillUsesInputThenExample() {
        val item = content.item("payroll-variance-check")!!
        val p = item.prompts.first { it.id == "main" }
        val filled = fillPrompt(item.id, p, mapOf("${item.id}.전월" to "2026년 8월"))
        assertTrue(filled.contains("2026년 8월 급여대장"))
        assertTrue(filled.contains("10320"))          // 입력 안 한 빈칸은 예시값
        assertFalse(filled.contains("{{"))
    }

    @Test fun sentenceSearchFindsPayroll() {
        val s = Searcher(content)
        assertEquals("payroll-variance-check", s.search("매달 급여 비교하는 게 오래 걸려요").first().id)
        assertEquals("excel-merge-files", s.search("지점 엑셀 합치기").first().id)
        assertEquals("one-page-exec-report", s.search("보고서 1장 요약").first().id)
        assertEquals("hr-severance", s.search("퇴직금 계산").first().id)
        assertEquals("account-vat-prep", s.search("부가세 신고 준비").first().id)
        assertEquals("logistics-freight-audit", s.search("택배비 청구서 검증").first().id)
        assertTrue(s.search("급여", category = "excel").none { it.category != "excel" })
    }

    @Test fun moderationCases() {
        val m = Moderator(content.moderation)
        val pass = listOf(
            "엑셀 취합 단계에서 파일이 20개 넘으면 어떻게 하나요?", "시발점부터 다시 설명해 주세요", "다시 발표 자료 예시도 넣어 주세요",
            "화면이 꺼져서 복사가 안 돼요", "새끼손가락으로 눌러도 버튼이 작아요", "새끼 고양이처럼 귀여운 아이콘이면 좋겠어요",
            "현장 아시바 발주 관리 매뉴얼도 추가해 주세요", "AI 좋소 앱 너무 좋아요 급여 매뉴얼 더 주세요", "최저시급이 2027년 값으로 안 바뀌어 있어요",
        )
        val block = listOf(
            "이거 시발 왜 안돼", "씨 1 발 오류남", "ㅅㅂ 복사가 안됨", "존나 느려요", "병1신같은 설명", "개 새 끼 같은 앱",
            "좆소 다니는 사람용 앱이네", "fuck this app", "급식충도 알아듣게 써 주세요",
            "010-1234-5678로 연락 주세요", "답변은 abc@test.com 으로 주세요", "제 주민번호 900101-1234567 예시로", "좋아요",
        )
        pass.forEach { assertTrue("통과해야 함: $it", m.check(it).ok) }
        block.forEach { assertFalse("막혀야 함: $it", m.check(it).ok) }
    }
}
