package com.aijoso.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.aijoso.app.data.AppStore
import com.aijoso.app.data.ContentFile
import com.aijoso.app.data.Item
import com.aijoso.app.data.Searcher
import com.aijoso.app.data.fillPrompt

// ───────────────────────── 홈 ─────────────────────────
@Composable
fun HomeScreen(c: ContentFile, store: AppStore, onOpen: (Item) -> Unit, onSearch: (String) -> Unit, onCategory: (String) -> Unit) {
    var q by rememberSaveable { mutableStateOf("") }
    val recommended = remember(c) { c.published }
    val drafts = remember(c) { c.items.filter { !it.isPublished } }
    LazyColumn(Modifier.fillMaxSize()) {
        item {
            Column(Modifier.fillMaxWidth().background(Yellow).padding(16.dp)) {
                KText("사람은 없고\n일은 많죠?", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Black, color = Ink, heading = true)
                Spacer(Modifier.height(4.dp))
                KText("힘든 업무를 문장으로 적어 보세요", fontWeight = FontWeight.Bold, color = Ink)
                Spacer(Modifier.height(12.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    OutlinedTextField(
                        value = q, onValueChange = { q = it }, singleLine = true,
                        modifier = Modifier.weight(1f),
                        placeholder = { Text("예) 급여 비교가 오래 걸려요") },
                        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                        keyboardActions = KeyboardActions(onSearch = { onSearch(q) }),
                        shape = RoundedCornerShape(12.dp),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedContainerColor = Color.White, unfocusedContainerColor = Color.White,
                            focusedTextColor = Ink, unfocusedTextColor = Ink,
                            focusedBorderColor = Ink, unfocusedBorderColor = Ink,
                            focusedPlaceholderColor = Color(0xFF6B675C), unfocusedPlaceholderColor = Color(0xFF6B675C),
                            cursorColor = Ink,
                        ),
                    )
                    Spacer(Modifier.padding(4.dp))
                    Button(
                        onClick = { onSearch(q) }, shape = RoundedCornerShape(12.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Ink, contentColor = Yellow),
                        modifier = Modifier.height(56.dp),
                    ) { Text("찾기", fontWeight = FontWeight.Bold) }
                }
                Spacer(Modifier.height(10.dp))
                Row(Modifier.horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    listOf("지점 엑셀 합치기", "급여 전월 비교", "보고서 1장 요약").forEach { s ->
                        Box(
                            Modifier.clip(RoundedCornerShape(50)).background(Color.White.copy(alpha = .55f))
                                .border(1.5.dp, Ink, RoundedCornerShape(50)).clickable { onSearch(s) }
                                .heightIn(min = 40.dp).padding(horizontal = 12.dp, vertical = 9.dp)
                        ) { Text(s, color = Ink, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.labelLarge) }
                    }
                }
            }
        }
        item { SectionHeader("분야별로 찾기", "${c.categories.size}개 분야") }
        item { CategoryGrid(c, onCategory) }
        item { SectionHeader("추천 매뉴얼", "${recommended.size}개 공개") }
        items(recommended, key = { "r-" + it.id }) { ItemCard(it, c.categoryName(it.category), false) { onOpen(it) } }
        if (c.changelog.isNotEmpty()) {
            item { SectionHeader("여러분 의견으로 바뀌었어요", "업데이트 소식") }
            items(c.changelog) { ch ->
                Row(
                    Modifier.padding(horizontal = 16.dp, vertical = 3.dp).fillMaxWidth().clip(RoundedCornerShape(12.dp))
                        .background(MaterialTheme.colorScheme.surfaceVariant).padding(12.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text(ch.date.drop(5).replace('-', '.'), style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold)
                    Spacer(Modifier.padding(5.dp))
                    KText(ch.text, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.bodyMedium)
                }
            }
        }
        item { SectionHeader("곧 올라올 매뉴얼", "${drafts.size}개 준비 중") }
        items(drafts.take(4), key = { "d-" + it.id }) { ItemCard(it, c.categoryName(it.category), store.requests.contains(it.id)) { onOpen(it) } }
        item { Spacer(Modifier.height(24.dp)) }
    }
}

@Composable
private fun CategoryGrid(c: ContentFile, onCategory: (String) -> Unit) {
    val cs = MaterialTheme.colorScheme
    Column(Modifier.padding(horizontal = 16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
        c.categories.sortedBy { it.order }.chunked(4).forEach { row ->
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                row.forEach { cat ->
                    val n = c.items.count { it.category == cat.id }
                    Column(
                        Modifier.weight(1f).heightIn(min = 76.dp).clip(RoundedCornerShape(14.dp)).background(cs.surfaceVariant)
                            .clickable { onCategory(cat.id) }.padding(vertical = 12.dp, horizontal = 4.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center,
                    ) {
                        KText(cat.name, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.Bold, textAlign = TextAlign.Center, heading = true)
                        Text("${n}개", style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant)
                    }
                }
                repeat(4 - row.size) { Spacer(Modifier.weight(1f)) }
            }
        }
    }
}

// ───────────────────────── 찾기 ─────────────────────────
@Composable
fun SearchScreen(
    c: ContentFile, searcher: Searcher, store: AppStore,
    query: String, onQuery: (String) -> Unit,
    category: String?, onCategory: (String?) -> Unit,
    difficulty: String?, onDifficulty: (String?) -> Unit,
    onOpen: (Item) -> Unit,
) {
    val focus = LocalFocusManager.current
    val results = remember(query, category, difficulty) { searcher.search(query, category, difficulty) }
    LazyColumn(Modifier.fillMaxSize()) {
        item {
            OutlinedTextField(
                value = query, onValueChange = onQuery, singleLine = true,
                modifier = Modifier.fillMaxWidth().padding(16.dp),
                leadingIcon = { Icon(Icons.Filled.Search, contentDescription = null) },
                placeholder = { Text("업무 이름이나 문장으로 검색") },
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                keyboardActions = KeyboardActions(onSearch = { focus.clearFocus() }),
                shape = RoundedCornerShape(12.dp),
            )
        }
        item {
            Row(Modifier.horizontalScroll(rememberScrollState()).padding(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                Pill("전체", category == null) { onCategory(null) }
                c.categories.sortedBy { it.order }.forEach { cat -> Pill(cat.name, category == cat.id) { onCategory(cat.id) } }
            }
            Spacer(Modifier.height(6.dp))
            Row(Modifier.horizontalScroll(rememberScrollState()).padding(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                listOf(null to "난이도 전체", "easy" to "쉬움", "normal" to "보통", "hard" to "어려움").forEach { (k, label) ->
                    Pill(label, difficulty == k) { onDifficulty(k) }
                }
            }
        }
        item {
            Text(
                (if (query.isNotBlank()) "'$query' 검색 결과 " else "") + "${results.size}개",
                style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
            )
        }
        if (results.isEmpty()) item { EmptyState("아직 없는 업무예요", "다른 말로 찾거나 분야를 골라 보세요") }
        items(results, key = { it.id }) { ItemCard(it, c.categoryName(it.category), store.requests.contains(it.id)) { onOpen(it) } }
        item { Spacer(Modifier.height(24.dp)) }
    }
}

// ───────────────────────── 프롬프트 보관함 ─────────────────────────
@Composable
fun PromptsScreen(c: ContentFile, store: AppStore, toast: (String) -> Unit, onOpen: (Item) -> Unit) {
    val ctx = LocalContext.current
    val cs = MaterialTheme.colorScheme
    LazyColumn(Modifier.fillMaxSize()) {
        item { SectionHeader("프롬프트 보관함", "${c.published.sumOf { it.prompts.size }}개") }
        item { KText("빈칸은 입력한 값, 없으면 예시로 복사돼요", Modifier.padding(horizontal = 16.dp), style = MaterialTheme.typography.bodySmall, color = cs.onSurfaceVariant) }
        c.categories.sortedBy { it.order }.forEach { cat ->
            val its = c.published.filter { it.category == cat.id }
            if (its.isNotEmpty()) {
                item(key = "h-" + cat.id) { SectionHeader(cat.name) }
                its.forEach { it0 ->
                    items(it0.prompts, key = { p -> it0.id + "/" + p.id }) { p ->
                        Column(
                            Modifier.padding(horizontal = 16.dp, vertical = 5.dp).fillMaxWidth().clip(RoundedCornerShape(14.dp))
                                .border(1.5.dp, cs.outline, RoundedCornerShape(14.dp)).padding(12.dp)
                        ) {
                            KText(p.title, fontWeight = FontWeight.ExtraBold, heading = true)
                            KText("${it0.title} · ${p.howTo}", style = MaterialTheme.typography.bodySmall, color = cs.onSurfaceVariant, maxLines = 2)
                            Spacer(Modifier.height(8.dp))
                            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                CopyButton("복사", Modifier.weight(1f)) {
                                    copyText(ctx, p.title, fillPrompt(it0.id, p, store.values)); toast("복사했어요! Claude에 붙여넣으세요")
                                }
                                OutlinedButton(onClick = { onOpen(it0) }, modifier = Modifier.weight(1f).height(44.dp), shape = RoundedCornerShape(12.dp)) {
                                    Text("빈칸 채우기", fontWeight = FontWeight.Bold)
                                }
                            }
                        }
                    }
                }
            }
        }
        item { Spacer(Modifier.height(24.dp)) }
    }
}

// ───────────────────────── 보관함 ─────────────────────────
@Composable
fun SavedScreen(c: ContentFile, store: AppStore, onOpen: (Item) -> Unit) {
    var seg by rememberSaveable { mutableStateOf("fav") }
    val cs = MaterialTheme.colorScheme
    LazyColumn(Modifier.fillMaxSize()) {
        item {
            Row(Modifier.padding(16.dp), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                Pill("즐겨찾기 ${store.favs.size}", seg == "fav", Modifier.weight(1f)) { seg = "fav" }
                Pill("최근 본 ${store.recent.size}", seg == "recent", Modifier.weight(1f)) { seg = "recent" }
                Pill("내 의견 ${store.myFeedback.size}", seg == "fb", Modifier.weight(1f)) { seg = "fb" }
            }
        }
        when (seg) {
            "fb" -> {
                val list = store.myFeedback.reversed()
                if (list.isEmpty()) item { EmptyState("보낸 의견이 없어요", "매뉴얼 맨 아래에서 남길 수 있어요") }
                val types = c.feedback.types.associate { it.id to it.label }
                items(list, key = { it.id }) { f ->
                    val resolved = c.resolvedFeedback.contains(f.id)
                    Column(
                        Modifier.padding(horizontal = 16.dp, vertical = 5.dp).fillMaxWidth().clip(RoundedCornerShape(14.dp))
                            .border(1.5.dp, cs.outline, RoundedCornerShape(14.dp)).padding(12.dp)
                    ) {
                        Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                            Tag(if (resolved) "반영됨" else if (f.status == "sent") "접수됨" else "전송 대기", highlight = resolved)
                            Tag(types[f.type] ?: f.type)
                            Text(f.date, style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant)
                        }
                        Spacer(Modifier.height(6.dp))
                        KText(c.item(f.contentId)?.title ?: "", fontWeight = FontWeight.ExtraBold, style = MaterialTheme.typography.bodyMedium)
                        KText(f.text, style = MaterialTheme.typography.bodyMedium)
                    }
                }
                item { KText("의견 전송은 다음 단계에서 연결돼요. 반영되면 '반영됨'으로 바뀌어요", Modifier.padding(16.dp), style = MaterialTheme.typography.bodySmall, color = cs.onSurfaceVariant) }
            }
            else -> {
                val ids = if (seg == "fav") store.favs.toList() else store.recent.toList()
                val its = ids.mapNotNull { c.item(it) }
                if (its.isEmpty()) item {
                    if (seg == "fav") EmptyState("담아 둔 매뉴얼이 없어요", "매뉴얼에서 [보관함에 담기]를 눌러 보세요")
                    else EmptyState("아직 본 매뉴얼이 없어요", "매뉴얼을 열면 여기 남아요")
                }
                items(its, key = { seg + it.id }) { ItemCard(it, c.categoryName(it.category), false) { onOpen(it) } }
                item { KText("보관함은 이 휴대폰에만 저장돼요", Modifier.padding(16.dp), style = MaterialTheme.typography.bodySmall, color = cs.onSurfaceVariant) }
            }
        }
    }
}

@Composable
fun EmptyState(title: String, body: String) {
    Column(Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 36.dp), horizontalAlignment = Alignment.CenterHorizontally) {
        KText(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Black, heading = true)
        Spacer(Modifier.height(4.dp))
        KText(body, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, textAlign = TextAlign.Center, heading = true)
    }
}

/** 노랑 복사 버튼 (핵심 동작이라 가장 눈에 띄게) */
@Composable
fun CopyButton(label: String, modifier: Modifier = Modifier, onClick: () -> Unit) {
    Button(
        onClick = onClick, modifier = modifier.height(48.dp), shape = RoundedCornerShape(12.dp),
        colors = ButtonDefaults.buttonColors(containerColor = Yellow, contentColor = Ink),
    ) { Text(label, fontWeight = FontWeight.ExtraBold) }
}
