@file:OptIn(ExperimentalMaterial3Api::class)

package com.aijoso.app.ui

import com.aijoso.app.data.AI_SITES
import androidx.compose.foundation.clickable
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.platform.LocalContext
import com.aijoso.app.data.LocalUi
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.aijoso.app.data.AppStore
import com.aijoso.app.data.ContentFile
import com.aijoso.app.data.Item
import com.aijoso.app.data.Moderator

/** 의견 남기기: 욕설·비속어·개인정보가 있으면 [보내기]가 잠긴다 */
@Composable
fun FeedbackSheet(item: Item, c: ContentFile, moderator: Moderator, onDismiss: () -> Unit, onSend: (type: String, text: String) -> Unit) {
    val state = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val cs = MaterialTheme.colorScheme
    var type by rememberSaveable { mutableStateOf(c.feedback.types.firstOrNull()?.id ?: "error") }
    var text by rememberSaveable { mutableStateOf("") }
    val ui = LocalUi.current
    val result = remember(text) { moderator.check(text) }
    val typed = text.isNotBlank()
    val showError = typed && !result.ok && result.reason != "short"

    ModalBottomSheet(onDismissRequest = onDismiss, sheetState = state, containerColor = cs.background) {
        Column(Modifier.padding(horizontal = 16.dp).padding(bottom = 24.dp).imePadding()) {
            Text(ui.t("fbs.title"), style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Black)
            KText(item.title, style = MaterialTheme.typography.bodySmall, color = cs.onSurfaceVariant)
            Spacer(Modifier.height(12.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                c.feedback.types.take(2).forEach { t -> Pill(t.label, type == t.id) { type = t.id } }
            }
            Spacer(Modifier.height(6.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                c.feedback.types.drop(2).forEach { t -> Pill(t.label, type == t.id) { type = t.id } }
            }
            Spacer(Modifier.height(12.dp))
            OutlinedTextField(
                value = text,
                onValueChange = { if (it.length <= c.feedback.maxLength) text = it },
                label = { Text(ui.t("fbs.content")) },
                placeholder = { Text(ui.t("fbs.placeholder")) },
                minLines = 4,
                isError = showError,
                supportingText = {
                    Row(Modifier.fillMaxWidth()) {
                        Text(if (typed && !result.ok) ui.t("mod.${result.reason}", "min" to c.moderation.minLength, "max" to c.moderation.maxLength) else "", Modifier.weight(1f), fontWeight = if (showError) FontWeight.Bold else null)
                        Text("${text.length}/${c.feedback.maxLength}")
                    }
                },
                modifier = Modifier.fillMaxWidth().heightIn(min = 120.dp),
                shape = RoundedCornerShape(12.dp),
            )
            Text(ui.t("fbs.notice"), style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant)
            Spacer(Modifier.height(12.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedButton(onClick = onDismiss, modifier = Modifier.weight(1f).height(48.dp), shape = RoundedCornerShape(12.dp)) { Text(ui.t("fbs.cancel"), fontWeight = FontWeight.Bold) }
                Button(
                    onClick = { if (moderator.check(text).ok) onSend(type, text) },
                    enabled = result.ok,
                    modifier = Modifier.weight(1f).height(48.dp), shape = RoundedCornerShape(12.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Yellow, contentColor = Ink),
                ) { Text(ui.t("fbs.send"), fontWeight = FontWeight.ExtraBold) }
            }
        }
    }
}

/** 준비 중 매뉴얼 요청 */
@Composable
fun RequestSheet(item: Item, requested: Boolean, onDismiss: () -> Unit, onToggle: () -> Unit) {
    val state = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val ui = LocalUi.current
    ModalBottomSheet(onDismissRequest = onDismiss, sheetState = state, containerColor = MaterialTheme.colorScheme.background) {
        Column(Modifier.padding(horizontal = 16.dp).padding(bottom = 24.dp)) {
            Text(ui.t("req.title"), style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Black)
            Spacer(Modifier.height(6.dp))
            KText(item.title, fontWeight = FontWeight.ExtraBold)
            KText(ui.t("req.note"), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            Spacer(Modifier.height(14.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedButton(onClick = onDismiss, modifier = Modifier.weight(1f).height(48.dp), shape = RoundedCornerShape(12.dp)) { Text(ui.t("req.close"), fontWeight = FontWeight.Bold) }
                CopyButton(if (requested) ui.t("req.cancel") else ui.t("req.want"), Modifier.weight(1f), onToggle)
            }
        }
    }
}

/** 설정: 언어, 글자 크기, 버전, 비제휴 고지 */
@Composable
fun SettingsSheet(c: ContentFile, store: AppStore, onDismiss: () -> Unit) {
    val state = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val cs = MaterialTheme.colorScheme
    val ui = LocalUi.current
    ModalBottomSheet(onDismissRequest = onDismiss, sheetState = state, containerColor = cs.background) {
        Column(Modifier.padding(horizontal = 16.dp).padding(bottom = 24.dp)) {
            Text(ui.t("set.title"), style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Black)
            Spacer(Modifier.height(12.dp))
            Text(ui.t("set.lang"), fontWeight = FontWeight.Bold)
            Spacer(Modifier.height(6.dp))
            // 언어: 휴대폰 설정 따르기 + 5개 언어 (2줄로 나눠 좁은 화면에서도 보이게)
            val langOptions = listOf("" to ui.t("set.langAuto")) + ui.langs.map { it to ui.langName(it) }
            langOptions.chunked(3).forEach { row ->
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.padding(bottom = 6.dp)) {
                    row.forEach { (code, label) -> Pill(label, store.lang == code, Modifier.weight(1f)) { store.updateLang(code) } }
                    repeat(3 - row.size) { Spacer(Modifier.weight(1f)) }
                }
            }
            Spacer(Modifier.height(8.dp))
            Text(ui.t("ai.default"), fontWeight = FontWeight.Bold)
            Spacer(Modifier.height(6.dp))
            // 프롬프트를 붙여넣을 AI: 매번 고르기 / Claude / ChatGPT / Gemini
            val aiOptions = listOf("" to ui.t("ai.ask")) + AI_SITES.map { it.id to it.name }
            aiOptions.chunked(2).forEach { row ->
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.padding(bottom = 6.dp)) {
                    row.forEach { (id, label) -> Pill(label, store.ai == id, Modifier.weight(1f)) { store.updateAi(id) } }
                }
            }
            Spacer(Modifier.height(8.dp))
            Text(ui.t("set.font"), fontWeight = FontWeight.Bold)
            Spacer(Modifier.height(6.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                listOf(0.9f to ui.t("set.small"), 1f to ui.t("set.normal"), 1.15f to ui.t("set.large")).forEach { (v, label) ->
                    Pill(label, store.fontScale == v, Modifier.weight(1f)) { store.updateFontScale(v) }
                }
            }
            Spacer(Modifier.height(12.dp))
            HorizontalDivider(color = cs.outline)
            SettingRow(ui.t("set.contentVer"), c.contentVersion)
            val ctx = LocalContext.current
            val ver = remember { runCatching { ctx.packageManager.getPackageInfo(ctx.packageName, 0).versionName }.getOrNull() ?: "" }
            SettingRow(ui.t("set.appVer"), ver)
            val uri = LocalUriHandler.current
            SettingRow(ui.t("set.privacy"), ui.t("pp.link")) { uri.openUri(privacyUrl(ui.lang)) }
            HorizontalDivider(color = cs.outline)
            Spacer(Modifier.height(10.dp))
            KText(ui.t("disclaimer"),
                style = MaterialTheme.typography.bodySmall, color = cs.onSurfaceVariant)
            Spacer(Modifier.height(12.dp))
            CopyButton(ui.t("set.close"), Modifier.fillMaxWidth(), onDismiss)
        }
    }
}

/** 웹에 게시한 언어별 개인정보처리방침 주소 */
fun privacyUrl(lang: String): String {
    val pre = mapOf("ko" to "", "en" to "en/", "ja" to "ja/", "zh-Hans" to "zh-hans/", "zh-Hant" to "zh-hant/")[lang] ?: "en/"
    return "https://bamjun777-cell.github.io/ai-work-recipe/${pre}privacy.html"
}

@Composable
private fun SettingRow(label: String, value: String, onClick: (() -> Unit)? = null) {
    Row(Modifier.fillMaxWidth().then(if (onClick != null) Modifier.clickable(onClick = onClick) else Modifier).padding(vertical = 12.dp), verticalAlignment = Alignment.CenterVertically) {
        Text(label, Modifier.weight(1f))
        Text(value, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}
