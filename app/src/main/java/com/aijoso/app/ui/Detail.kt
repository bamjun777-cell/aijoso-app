package com.aijoso.app.ui

import com.aijoso.app.data.LocalUi
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
import com.aijoso.app.data.promptSegments

@Composable
fun DetailScreen(manual: Item, c: ContentFile, store: AppStore, toast: (String) -> Unit, onFeedback: () -> Unit) {
    val ctx = LocalContext.current
    val uri = LocalUriHandler.current
    val cs = MaterialTheme.colorScheme
    val ui = LocalUi.current
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
                Text("${c.categoryName(manual.category)} · " + ui.t("detail.verified", "d" to manual.verifiedAt), style = MaterialTheme.typography.labelMedium, color = cs.onSurfaceVariant, fontWeight = FontWeight.Bold)
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
                    TimeBox(ui.t("detail.now"), ui.t("min.n", "n" to manual.timeBeforeMin), strike = true, Modifier.weight(1f))
                    Text("→", fontWeight = FontWeight.Bold)
                    TimeBox(ui.t("detail.after"), ui.t("min.n", "n" to manual.timeAfterMin), strike = false, Modifier.weight(1f))
                }
                Spacer(Modifier.height(8.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    Fact(ui.t("diff.label"), ui.difficulty(manual.difficulty), Modifier.weight(1f))
                    Fact(ui.t("detail.repeat"), ui.frequency(manual.frequency), Modifier.weight(1f))
                    Fact(ui.t("detail.freePlan"), if (manual.freePlanOk) ui.t("detail.freeYes") else ui.t("detail.freeNo"), Modifier.weight(1f))
                }
                Text(ui.t("detail.estimate"), style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant, modifier = Modifier.padding(top = 6.dp))
            }
        }
        item { Block(no("prob"), ui.t("sec.prob")) { KText(manual.problem) } }
        item {
            Block(no("how"), ui.t("sec.how")) {
                LabeledBox(ui.t("how.before"), manual.before, cs.surfaceVariant)
                Spacer(Modifier.height(8.dp))
                LabeledBox(ui.t("detail.after"), manual.after, cs.primaryContainer)
            }
        }
        item {
            Block(no("prep"), ui.t("sec.prep")) {
                manual.tools.forEach { t ->
                    Row(Modifier.padding(vertical = 4.dp), verticalAlignment = Alignment.CenterVertically) {
                        Tag(if (t.free) ui.t("tool.free") else ui.t("tool.own"), highlight = t.free)
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
                Block(no("proj"), ui.t("sec.proj")) {
                    KText(ui.t("proj.intro", "name" to pr.name))
                    Spacer(Modifier.height(8.dp))
                    Box(Modifier.fillMaxWidth().clip(RoundedCornerShape(12.dp)).background(cs.surfaceVariant).padding(12.dp)) {
                        Text(pr.instructions, style = MaterialTheme.typography.bodySmall)
                    }
                    if (pr.knowledge.isNotEmpty()) KText(ui.t("proj.knowledge", "name" to pr.knowledge.joinToString(", ")), Modifier.padding(top = 6.dp), style = MaterialTheme.typography.bodySmall, color = cs.onSurfaceVariant)
                    Spacer(Modifier.height(8.dp))
                    OutlinedButton(onClick = { copyText(ctx, pr.name, pr.instructions); toast(ui.t("proj.copied")) }, shape = RoundedCornerShape(12.dp), modifier = Modifier.fillMaxWidth()) {
                        Text(ui.t("proj.copy"), fontWeight = FontWeight.Bold)
                    }
                }
            }
        }
        item { Block(no("prompt"), ui.t("sec.prompt")) { KText(ui.t("prompt.hint"), style = MaterialTheme.typography.bodySmall, color = cs.onSurfaceVariant) } }
        itemsIndexed(manual.prompts, key = { _, p -> "p-" + p.id }) { _, p ->
            PromptCard(manual, p, store,
                onCopy = { copyText(ctx, p.title, fillPrompt(manual.id, p, store.values)); toast(ui.t("prompt.copied")) },
                onOpenClaude = { uri.openUri("https://claude.ai/new") })
        }
        item {
            Block(no("steps"), ui.t("sec.steps")) {
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
                                KText(ui.t("step.check", "name" to s.check), Modifier.clip(RoundedCornerShape(8.dp)).background(cs.errorContainer).padding(horizontal = 8.dp, vertical = 4.dp),
                                    style = MaterialTheme.typography.bodySmall, color = cs.onErrorContainer)
                            }
                        }
                    }
                }
            }
        }
        manual.result?.let { r ->
            item {
                Block(no("result"), ui.t("sec.result")) {
                    KText(r.summary, fontWeight = FontWeight.Bold, heading = true)
                    Spacer(Modifier.height(8.dp))
                    Box(Modifier.fillMaxWidth().clip(RoundedCornerShape(12.dp)).background(cs.surfaceVariant).padding(12.dp)) { KText(r.example, style = MaterialTheme.typography.bodyMedium) }
                    if (manual.printSample != null) Text(ui.t("result.printLater"), style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant, modifier = Modifier.padding(top = 6.dp))
                }
            }
        }
        item {
            Block(no("caution"), ui.t("sec.caution")) {
                Column(Modifier.fillMaxWidth().clip(RoundedCornerShape(12.dp)).background(cs.errorContainer).padding(12.dp)) {
                    manual.cautions.forEach { Bullet(it, cs.onErrorContainer) }
                }
                manual.legal?.let { l ->
                    Spacer(Modifier.height(8.dp))
                    KText(ui.t("legal.label") + " · ${l.note}\n" + ui.t("legal.checked", "d" to l.checkedAt) + " · ${l.disclaimer}", style = MaterialTheme.typography.bodySmall, color = cs.onSurfaceVariant)
                }
            }
        }
        item {
            Block(no("ref"), ui.t("sec.ref")) {
                KText(ui.t("ref.videos"), style = MaterialTheme.typography.bodySmall, color = cs.onSurfaceVariant)
                manual.docs.forEach { d ->
                    Column(Modifier.fillMaxWidth().clickable { uri.openUri(d.url) }.padding(vertical = 10.dp)) {
                        Text(d.title, fontWeight = FontWeight.Bold, textDecoration = TextDecoration.Underline)
                        Text("${d.publisher} · " + ui.t("detail.verified", "d" to d.verifiedAt), style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant)
                    }
                }
            }
        }
        item {
            Block(no("fb"), ui.t("sec.fb")) {
                val r = store.reactions[manual.id]
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Pill(ui.t("react.good"), r == "good", Modifier.weight(1f)) {
                        if (store.react(manual.id, "good") == "good") toast(ui.t("react.goodToast"))
                    }
                    Pill(ui.t("react.bad"), r == "bad", Modifier.weight(1f)) {
                        if (store.react(manual.id, "bad") == "bad") onFeedback()
                    }
                }
                Spacer(Modifier.height(10.dp))
                OutlinedButton(onClick = onFeedback, modifier = Modifier.fillMaxWidth().height(48.dp), shape = RoundedCornerShape(12.dp)) {
                    Text(ui.t("fb.open"), fontWeight = FontWeight.Bold)
                }
                val sent = store.myFeedback.count { it.contentId == manual.id }
                if (sent > 0) Text(ui.t("fb.sentCount", "n" to sent), style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant, modifier = Modifier.padding(top = 6.dp))
            }
        }
        item {
            Row(Modifier.padding(16.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                CopyButton(if (fav) ui.t("fav.has") else ui.t("fav.add"), Modifier.weight(1f)) {
                    store.toggleFav(manual.id); toast(if (fav) ui.t("fav.removed") else ui.t("fav.added"))
                }
                OutlinedButton(onClick = { shareText(ctx, "[" + ui.t("app.name") + "] ${manual.title}\n${manual.subtitle}", ui.t("share.chooser")) }, modifier = Modifier.weight(1f).height(48.dp), shape = RoundedCornerShape(12.dp)) {
                    Icon(Icons.Filled.Share, contentDescription = null); Spacer(Modifier.width(6.dp)); Text(ui.t("share.pc"), fontWeight = FontWeight.Bold)
                }
            }
            Spacer(Modifier.height(16.dp))
        }
    }
}

@Composable
private fun PromptCard(item: Item, p: Prompt, store: AppStore, onCopy: () -> Unit, onOpenClaude: () -> Unit) {
    val cs = MaterialTheme.colorScheme
    val ui = LocalUi.current
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
                    label = { Text(v.label) }, placeholder = { Text(ui.t("prompt.example", "name" to v.example)) },
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
                CopyButton(ui.t("prompt.copy"), Modifier.weight(1f), onCopy)
                OutlinedButton(onClick = onOpenClaude, modifier = Modifier.weight(1f).height(48.dp), shape = RoundedCornerShape(12.dp)) {
                    Text(ui.t("prompt.openClaude"), fontWeight = FontWeight.Bold)
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
