package com.aijoso.app

import com.aijoso.app.data.ContentFile
import com.aijoso.app.data.Moderator
import com.aijoso.app.data.Searcher
import com.aijoso.app.data.fillPrompt
import com.aijoso.app.data.parseContent
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File

/** 빌드할 때마다 자동으로 도는 검사: 콘텐츠 파일, 검색, 비속어 필터 */
class LogicTest {
    private val content: ContentFile = parseContent(File("src/main/assets/content.json").readText())

    @Test fun contentLoads() {
        assertEquals(30, content.items.size)
        assertEquals(30, content.published.size)
        assertEquals(6, content.featuredItems.size)
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
