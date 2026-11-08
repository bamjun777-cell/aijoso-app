package com.aijoso.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Share
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.LineBreak
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import com.aijoso.app.data.AppStore
import com.aijoso.app.data.ContentFile
import com.aijoso.app.data.Item
import com.aijoso.app.data.Prompt
import com.aijoso.app.data.fillPrompt
import com.aijoso.app.data.frequencyLabel
import com.aijoso.app.data.promptSegments

@Composable
fun DetailScreen(manual: Item, c: ContentFile, store: AppStore, toast: (String) -> Unit, onFeedback: () -> Unit) {
    val ctx = LocalContext.current
    val uri = LocalUriHandler.current
    val cs = MaterialTheme.colorScheme
    val fav = store.favs.contains(manual.id)
    // 블록 번호는 미리 계산 (지연 목록 안에서 증가시키면 다시 그릴 때 번호가 바뀜)
    val sections = buildList {
        add("prob"); add("how"); add("prep"); if (manual.project != null) add("proj"); add("prompt")
        add("steps"); if (manual.result != null) add("result"); add("caution"); add("ref"); add("fb")
    }
    fun no(k: String) = (sections.indexOf(k) + 1).toString()

    LazyColumn(Modifier.fillMaxSize()) {
        // 요약
        item {
            Column(Modifier.fillMaxWidth().background(cs.primaryContainer).padding(16.dp)) {
                Text("${c.categoryName(manual.category)} · 검증일 ${manual.verifiedAt}", style = MaterialTheme.typography.labelMedium, color = cs.onSurfaceVariant, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(4.dp))
                KText(manual.title, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Black, heading = true)
                Spacer(Modifier.height(4.dp))
                KText(manual.subtitle, style = MaterialTheme.typography.bodyMedium, color = cs.onSurfaceVariant, heading = true)
                Spacer(Modifier.height(12.dp))
                Row(
                    Modifier.fillMaxWidth().clip(RoundedCornerShape(14.dp)).background(cs.background)
                        .border(2.dp, cs.onBackground, RoundedCornerShape(14.dp)).padding(12.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    TimeBox("지금", "${manual.timeBeforeMin}분", strike = true, Modifier.weight(1f))
                    Text("→", fontWeight = FontWeight.Bold)
                    TimeBox("AI 적용 후", "${manual.timeAfterMin}분", strike = false, Modifier.weight(1f))
                }
                Spacer(Modifier.height(8.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    Fact("난이도", mapOf("easy" to "쉬움", "normal" to "보통", "hard" to "어려움")[manual.difficulty] ?: manual.difficulty, Modifier.weight(1f))
                    Fact("반복", frequencyLabel(manual.frequency), Modifier.weight(1f))
                    Fact("무료 플랜", if (manual.freePlanOk) "가능" else "유료", Modifier.weight(1f))
                }
                Text("* 시간은 추정치", style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant, modifier = Modifier.padding(top = 6.dp))
            }
        }
        item { Block(no("prob"), "이런 문제, 있으시죠?") { KText(manual.problem) } }
        item {
            Block(no("how"), "이렇게 바뀝니다") {
                LabeledBox("지금 방식", manual.before, cs.surfaceVariant)
                Spacer(Modifier.height(8.dp))
                LabeledBox("AI 적용 후", manual.after, cs.primaryContainer)
            }
        }
        item {
            Block(no("prep"), "필요한 것과 준비") {
                manual.tools.forEach { t ->
                    Row(Modifier.padding(vertical = 4.dp), verticalAlignment = Alignment.CenterVertically) {
                        Tag(if (t.free) "무료" else "보유", highlight = t.free)
                        Spacer(Modifier.width(8.dp))
                        Column { KText(t.name, fontWeight = FontWeight.Bold); KText(t.note, style = MaterialTheme.typography.bodySmall, color = cs.onSurfaceVariant) }
                    }
                }
                Spacer(Modifier.height(6.dp))
                manual.prepare.forEach { p -> Bullet(p) }
            }
        }
        manual.project?.let { pr ->
            item {
                Block(no("proj"), "Claude 프로젝트로 만들어 두기") {
                    KText("매달 반복된다면 '${pr.name}' 프로젝트를 만들고 아래 지침을 붙여넣으세요")
                    Spacer(Modifier.height(8.dp))
                    Box(Modifier.fillMaxWidth().clip(RoundedCornerShape(12.dp)).background(cs.surfaceVariant).padding(12.dp)) {
                        Text(pr.instructions, style = MaterialTheme.typography.bodySmall)
                    }
                    if (pr.knowledge.isNotEmpty()) KText("올릴 파일: " + pr.knowledge.joinToString(", "), Modifier.padding(top = 6.dp), style = MaterialTheme.typography.bodySmall, color = cs.onSurfaceVariant)
                    Spacer(Modifier.height(8.dp))
                    OutlinedButton(onClick = { copyText(ctx, "프로젝트 지침", pr.instructions); toast("지침을 복사했어요") }, shape = RoundedCornerShape(12.dp), modifier = Modifier.fillMaxWidth()) {
                        Text("지침 복사", fontWeight = FontWeight.Bold)
                    }
                }
            }
        }
        item { Block(no("prompt"), "복사해서 쓰는 프롬프트") { KText("빈칸을 채우면 바로 반영돼요", style = MaterialTheme.typography.bodySmall, color = cs.onSurfaceVariant) } }
        itemsIndexed(manual.prompts, key = { _, p -> "p-" + p.id }) { _, p ->
            PromptCard(manual, p, store,
                onCopy = { copyText(ctx, p.title, fillPrompt(manual.id, p, store.values)); toast("복사했어요! Claude에 붙여넣으세요") },
                onOpenClaude = { uri.openUri("https://claude.ai/new") })
        }
        item {
            Block(no("steps"), "순서대로 따라 하기") {
                manual.steps.forEachIndexed { i, s ->
                    Row(Modifier.padding(vertical = 5.dp)) {
                        Box(Modifier.size(28.dp).clip(CircleShape).background(Yellow), contentAlignment = Alignment.Center) {
                            Text("${i + 1}", color = Ink, fontWeight = FontWeight.Black)
                        }
                        Spacer(Modifier.width(10.dp))
                        Column(Modifier.weight(1f)) {
                            KText(s.title, fontWeight = FontWeight.ExtraBold)
                            KText(s.body)
                            if (s.check.isNotBlank()) {
                                Spacer(Modifier.height(4.dp))
                                KText("확인 · " + s.check, Modifier.clip(RoundedCornerShape(8.dp)).background(cs.errorContainer).padding(horizontal = 8.dp, vertical = 4.dp),
                                    style = MaterialTheme.typography.bodySmall, color = cs.onErrorContainer)
                            }
                        }
                    }
                }
            }
        }
        manual.result?.let { r ->
            item {
                Block(no("result"), "이런 결과가 나와요") {
                    KText(r.summary, fontWeight = FontWeight.Bold, heading = true)
                    Spacer(Modifier.height(8.dp))
                    Box(Modifier.fillMaxWidth().clip(RoundedCornerShape(12.dp)).background(cs.surfaceVariant).padding(12.dp)) { KText(r.example, style = MaterialTheme.typography.bodyMedium) }
                    Text("A4 출력 미리보기는 다음 단계에서 연결돼요", style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant, modifier = Modifier.padding(top = 6.dp))
                }
            }
        }
        item {
            Block(no("caution"), "꼭 지켜 주세요") {
                Column(Modifier.fillMaxWidth().clip(RoundedCornerShape(12.dp)).background(cs.errorContainer).padding(12.dp)) {
                    manual.cautions.forEach { Bullet(it, cs.onErrorContainer) }
                }
                manual.legal?.let { l ->
                    Spacer(Modifier.height(8.dp))
                    KText("법령 기준 · ${l.note}\n확인일 ${l.checkedAt} · ${l.disclaimer}", style = MaterialTheme.typography.bodySmall, color = cs.onSurfaceVariant)
                }
            }
        }
        item {
            Block(no("ref"), "더 알아보기") {
                KText("관련 영상은 확인 후 올려요", style = MaterialTheme.typography.bodySmall, color = cs.onSurfaceVariant)
                manual.docs.forEach { d ->
                    Column(Modifier.fillMaxWidth().clickable { uri.openUri(d.url) }.padding(vertical = 10.dp)) {
                        Text(d.title, fontWeight = FontWeight.Bold, textDecoration = TextDecoration.Underline)
                        Text("${d.publisher} · 검증일 ${d.verifiedAt}", style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant)
                    }
                }
            }
        }
        item {
            Block(no("fb"), "이 매뉴얼, 어땠나요?") {
                val r = store.reactions[manual.id]
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Pill("도움 됐어요", r == "good", Modifier.weight(1f)) {
                        if (store.react(manual.id, "good") == "good") toast("도움이 됐다니 다행이에요")
                    }
                    Pill("아쉬워요", r == "bad", Modifier.weight(1f)) {
                        if (store.react(manual.id, "bad") == "bad") onFeedback()
                    }
                }
                Spacer(Modifier.height(10.dp))
                OutlinedButton(onClick = onFeedback, modifier = Modifier.fillMaxWidth().height(48.dp), shape = RoundedCornerShape(12.dp)) {
                    Text("틀린 내용 신고 · 추가 요청", fontWeight = FontWeight.Bold)
                }
                val sent = store.myFeedback.count { it.contentId == manual.id }
                if (sent > 0) Text("보낸 의견 ${sent}건 · 보관함에서 확인", style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant, modifier = Modifier.padding(top = 6.dp))
            }
        }
        item {
            Row(Modifier.padding(16.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                CopyButton(if (fav) "보관함에 있음" else "보관함에 담기", Modifier.weight(1f)) {
                    store.toggleFav(manual.id); toast(if (fav) "보관함에서 뺐어요" else "보관함에 담았어요")
                }
                OutlinedButton(onClick = { shareText(ctx, "[AI 좋소] ${manual.title}\n${manual.subtitle}") }, modifier = Modifier.weight(1f).height(48.dp), shape = RoundedCornerShape(12.dp)) {
                    Icon(Icons.Filled.Share, contentDescription = null); Spacer(Modifier.width(6.dp)); Text("PC로 보내기", fontWeight = FontWeight.Bold)
                }
            }
            Spacer(Modifier.height(16.dp))
        }
    }
}

@Composable
private fun PromptCard(item: Item, p: Prompt, store: AppStore, onCopy: () -> Unit, onOpenClaude: () -> Unit) {
    val cs = MaterialTheme.colorScheme
    val shape = RoundedCornerShape(16.dp)
    Column(Modifier.padding(horizontal = 16.dp, vertical = 6.dp).fillMaxWidth().clip(shape).border(2.dp, cs.onBackground, shape)) {
        Column(Modifier.fillMaxWidth().background(cs.onBackground).padding(12.dp)) {
            KText(p.title, color = cs.background, fontWeight = FontWeight.ExtraBold)
            KText(p.howTo, color = cs.background.copy(alpha = .8f), style = MaterialTheme.typography.bodySmall)
        }
        Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            p.variables.forEach { v ->
                val key = "${item.id}.${v.key}"
                OutlinedTextField(
                    value = store.values[key] ?: "", onValueChange = { store.setValue(key, it) },
                    label = { Text(v.label) }, placeholder = { Text("예) ${v.example}") },
                    singleLine = v.example.length < 40, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(10.dp),
                )
            }
            val preview = buildAnnotatedString {
                promptSegments(item.id, p, store.values).forEach { (text, filled) ->
                    if (filled) withStyle(SpanStyle(background = Mark, color = Ink, fontWeight = FontWeight.Bold)) { append(text) } else append(text)
                }
            }
            Box(Modifier.fillMaxWidth().clip(RoundedCornerShape(12.dp)).background(cs.surfaceVariant).padding(12.dp)) {
                Text(preview, style = MaterialTheme.typography.bodySmall.copy(lineBreak = LineBreak.Paragraph))
            }
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                CopyButton("복사하기", Modifier.weight(1f), onCopy)
                OutlinedButton(onClick = onOpenClaude, modifier = Modifier.weight(1f).height(48.dp), shape = RoundedCornerShape(12.dp)) {
                    Text("Claude 열기", fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}

@Composable
private fun Block(number: String, title: String, body: @Composable () -> Unit) {
    Column(Modifier.fillMaxWidth().padding(start = 16.dp, end = 16.dp, top = 20.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Box(Modifier.clip(RoundedCornerShape(6.dp)).background(MaterialTheme.colorScheme.onBackground).padding(horizontal = 7.dp, vertical = 1.dp)) {
                Text(number, color = MaterialTheme.colorScheme.background, fontWeight = FontWeight.Black)
            }
            Spacer(Modifier.width(8.dp))
            KText(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.ExtraBold, heading = true)
        }
        Spacer(Modifier.height(8.dp))
        body()
    }
}

@Composable
private fun TimeBox(label: String, value: String, strike: Boolean, modifier: Modifier) {
    Column(modifier, horizontalAlignment = Alignment.CenterHorizontally) {
        Text(label, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold)
        Text(value, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Black,
            textDecoration = if (strike) TextDecoration.LineThrough else null,
            color = if (strike) MaterialTheme.colorScheme.onSurfaceVariant else MaterialTheme.colorScheme.onBackground)
    }
}

@Composable
private fun Fact(label: String, value: String, modifier: Modifier) {
    Column(modifier.clip(RoundedCornerShape(10.dp)).background(MaterialTheme.colorScheme.background).padding(vertical = 8.dp), horizontalAlignment = Alignment.CenterHorizontally) {
        Text(label, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        Text(value, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.Bold)
    }
}

@Composable
private fun LabeledBox(label: String, text: String, bg: androidx.compose.ui.graphics.Color) {
    Column(Modifier.fillMaxWidth().clip(RoundedCornerShape(12.dp)).background(bg).padding(12.dp)) {
        Text(label, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold)
        KText(text)
    }
}

@Composable
private fun Bullet(text: String, color: androidx.compose.ui.graphics.Color = androidx.compose.ui.graphics.Color.Unspecified) {
    Row(Modifier.padding(vertical = 2.dp)) {
        Text("•  ", color = color)
        KText(text, color = color)
    }
}
