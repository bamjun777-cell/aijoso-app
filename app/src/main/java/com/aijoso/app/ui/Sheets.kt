@file:OptIn(ExperimentalMaterial3Api::class)

package com.aijoso.app.ui

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
    val result = remember(text) { moderator.check(text) }
    val typed = text.isNotBlank()
    val showError = typed && !result.ok && result.reason != "short"

    ModalBottomSheet(onDismissRequest = onDismiss, sheetState = state, containerColor = cs.background) {
        Column(Modifier.padding(horizontal = 16.dp).padding(bottom = 24.dp).imePadding()) {
            Text("의견 남기기", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Black)
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
                label = { Text("내용") },
                placeholder = { Text("예) 2단계 메뉴 이름이 달라요") },
                minLines = 4,
                isError = showError,
                supportingText = {
                    Row(Modifier.fillMaxWidth()) {
                        Text(if (typed && !result.ok) result.message else "", Modifier.weight(1f), fontWeight = if (showError) FontWeight.Bold else null)
                        Text("${text.length}/${c.feedback.maxLength}")
                    }
                },
                modifier = Modifier.fillMaxWidth().heightIn(min = 120.dp),
                shape = RoundedCornerShape(12.dp),
            )
            Text("욕설·비속어, 개인정보는 보낼 수 없어요", style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant)
            Spacer(Modifier.height(12.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedButton(onClick = onDismiss, modifier = Modifier.weight(1f).height(48.dp), shape = RoundedCornerShape(12.dp)) { Text("취소", fontWeight = FontWeight.Bold) }
                Button(
                    onClick = { if (moderator.check(text).ok) onSend(type, text) },
                    enabled = result.ok,
                    modifier = Modifier.weight(1f).height(48.dp), shape = RoundedCornerShape(12.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Yellow, contentColor = Ink),
                ) { Text("보내기", fontWeight = FontWeight.ExtraBold) }
            }
        }
    }
}

/** 준비 중 매뉴얼 요청 */
@Composable
fun RequestSheet(item: Item, requested: Boolean, onDismiss: () -> Unit, onToggle: () -> Unit) {
    val state = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    ModalBottomSheet(onDismissRequest = onDismiss, sheetState = state, containerColor = MaterialTheme.colorScheme.background) {
        Column(Modifier.padding(horizontal = 16.dp).padding(bottom = 24.dp)) {
            Text("지금 쓰고 있는 매뉴얼이에요", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Black)
            Spacer(Modifier.height(6.dp))
            KText(item.title, fontWeight = FontWeight.ExtraBold)
            KText("요청이 많은 매뉴얼부터 올려요", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            Spacer(Modifier.height(14.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedButton(onClick = onDismiss, modifier = Modifier.weight(1f).height(48.dp), shape = RoundedCornerShape(12.dp)) { Text("닫기", fontWeight = FontWeight.Bold) }
                CopyButton(if (requested) "요청 취소" else "먼저 보고 싶어요", Modifier.weight(1f), onToggle)
            }
        }
    }
}

/** 설정: 글자 크기, 버전, 비제휴 고지 */
@Composable
fun SettingsSheet(c: ContentFile, store: AppStore, onDismiss: () -> Unit) {
    val state = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val cs = MaterialTheme.colorScheme
    ModalBottomSheet(onDismissRequest = onDismiss, sheetState = state, containerColor = cs.background) {
        Column(Modifier.padding(horizontal = 16.dp).padding(bottom = 24.dp)) {
            Text("설정", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Black)
            Spacer(Modifier.height(12.dp))
            Text("글자 크기", fontWeight = FontWeight.Bold)
            Spacer(Modifier.height(6.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                listOf(0.9f to "작게", 1f to "보통", 1.15f to "크게").forEach { (v, label) ->
                    Pill(label, store.fontScale == v, Modifier.weight(1f)) { store.updateFontScale(v) }
                }
            }
            Spacer(Modifier.height(12.dp))
            HorizontalDivider(color = cs.outline)
            SettingRow("콘텐츠 버전", c.contentVersion)
            SettingRow("앱 버전", "0.1.0 (테스트)")
            SettingRow("개인정보처리방침", "출시 전 게시 예정")
            HorizontalDivider(color = cs.outline)
            Spacer(Modifier.height(10.dp))
            KText("AI 좋소는 Claude 등 AI 도구 활용법을 안내하는 독립 앱입니다. Anthropic·OpenAI·Google 등 AI 회사와 제휴하거나 승인받은 관계가 없습니다.",
                style = MaterialTheme.typography.bodySmall, color = cs.onSurfaceVariant)
            Spacer(Modifier.height(12.dp))
            CopyButton("닫기", Modifier.fillMaxWidth(), onDismiss)
        }
    }
}

@Composable
private fun SettingRow(label: String, value: String) {
    Row(Modifier.fillMaxWidth().padding(vertical = 12.dp), verticalAlignment = Alignment.CenterVertically) {
        Text(label, Modifier.weight(1f))
        Text(value, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}
