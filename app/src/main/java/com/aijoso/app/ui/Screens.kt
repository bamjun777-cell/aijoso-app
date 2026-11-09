package com.aijoso.app.ui

import com.aijoso.app.data.LocalUi
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
import androidx.compose.foundation.lazy.rememberLazyListState
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
import androidx.compose.runtime.rememberCoroutineScope
import kotlinx.coroutines.launch
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
    val ui = LocalUi.current
    var q by rememberSaveable { mutableStateOf("") }
    val drafts = remember(c) { c.items.filter { !it.isPublished } }
    // 분야별 묶음: 공개 매뉴얼 전부를 분야 순서대로
    val groups = remember(c) {
        c.categories.sortedBy { it.order }.map { cat -> cat to c.published.filter { it.category == cat.id } }.filter { it.second.isNotEmpty() }
    }
    // 분야 타일을 누르면 홈 안에서 해당 분야 제목으로 이동 (앞: 검색창·분야 제목·타일·전체 제목 = 4칸)
    val groupIndex = remember(groups) {
        var i = 4
        groups.associate { (cat, its) -> (cat.id to i).also { i += 1 + its.size } }
    }
    val listState = rememberLazyListState()
    val scope = rememberCoroutineScope()
    LazyColumn(Modifier.fillMaxSize(), state = listState) {
        item {
            Column(Modifier.fillMaxWidth().background(Yellow).padding(16.dp)) {
                KText(ui.t("hero.title"), style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Black, color = Ink, heading = true)
                Spacer(Modifier.height(4.dp))
                KText(ui.t("hero.sub"), fontWeight = FontWeight.Bold, color = Ink)
                Spacer(Modifier.height(12.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    OutlinedTextField(
                        value = q, onValueChange = { q = it }, singleLine = true,
                        modifier = Modifier.weight(1f),
                        placeholder = { Text(ui.t("hero.placeholder")) },
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
                    ) { Text(ui.t("search.button"), fontWeight = FontWeight.Bold) }
                }
                Spacer(Modifier.height(10.dp))
                Row(Modifier.horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    ui.chips.forEach { s ->
                        Box(
                            Modifier.clip(RoundedCornerShape(50)).background(Color.White.copy(alpha = .55f))
                                .border(1.5.dp, Ink, RoundedCornerShape(50)).clickable { onSearch(s) }
                                .heightIn(min = 40.dp).padding(horizontal = 12.dp, vertical = 9.dp)
                        ) { Text(s, color = Ink, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.labelLarge) }
                    }
                }
            }
        }
        item { SectionHeader(ui.t("home.byCategory"), ui.t("home.byCategoryHint")) }
        item {
            CategoryGrid(c) { id ->
                val idx = groupIndex[id]
                if (idx != null) scope.launch { listState.animateScrollToItem(idx) } else onCategory(id)
            }
        }
        item { SectionHeader(ui.t("home.all"), ui.t("home.total", "n" to c.published.size)) }
        groups.forEach { (cat, its) ->
            item(key = "h-" + cat.id) {
                Row(
                    Modifier.padding(start = 16.dp, end = 16.dp, top = 14.dp, bottom = 4.dp).fillMaxWidth()
                        .clip(RoundedCornerShape(12.dp)).background(MaterialTheme.colorScheme.primaryContainer)
                        .padding(horizontal = 14.dp, vertical = 10.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    KText(cat.name, Modifier.weight(1f), style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Black, heading = true,
                        color = MaterialTheme.colorScheme.onPrimaryContainer)
                    Text(ui.t("count.n", "n" to its.size), style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
            items(its, key = { "r-" + it.id }) { ItemCard(it, "", false) { onOpen(it) } }
        }
        if (c.changelog.isNotEmpty()) {
            item { SectionHeader(ui.t("home.news"), ui.t("home.newsAside")) }
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
        if (drafts.isNotEmpty()) {
            item { SectionHeader(ui.t("home.drafts"), ui.t("home.draftsAside", "n" to drafts.size)) }
            items(drafts.take(4), key = { "d-" + it.id }) { ItemCard(it, c.categoryName(it.category), store.requests.contains(it.id)) { onOpen(it) } }
        }
        item { Spacer(Modifier.height(24.dp)) }
    }
}

@Composable
private fun CategoryGrid(c: ContentFile, onCategory: (String) -> Unit) {
    val cs = MaterialTheme.colorScheme
    val ui = LocalUi.current
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
                        Text(ui.t("count.n", "n" to n), style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant)
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
    val ui = LocalUi.current
    val results = remember(query, category, difficulty) { searcher.search(query, category, difficulty) }
    LazyColumn(Modifier.fillMaxSize()) {
        item {
            OutlinedTextField(
                value = query, onValueChange = onQuery, singleLine = true,
                modifier = Modifier.fillMaxWidth().padding(16.dp),
                leadingIcon = { Icon(Icons.Filled.Search, contentDescription = null) },
                placeholder = { Text(ui.t("search.placeholder")) },
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                keyboardActions = KeyboardActions(onSearch = { focus.clearFocus() }),
                shape = RoundedCornerShape(12.dp),
            )
        }
        item {
            Row(Modifier.horizontalScroll(rememberScrollState()).padding(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                Pill(ui.t("filter.all"), category == null) { onCategory(null) }
                c.categories.sortedBy { it.order }.forEach { cat -> Pill(cat.name, category == cat.id) { onCategory(cat.id) } }
            }
            Spacer(Modifier.height(6.dp))
            Row(Modifier.horizontalScroll(rememberScrollState()).padding(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                listOf(null to ui.t("diff.all"), "easy" to ui.t("diff.easy"), "normal" to ui.t("diff.normal"), "hard" to ui.t("diff.hard")).forEach { (k, label) ->
                    Pill(label, difficulty == k) { onDifficulty(k) }
                }
            }
        }
        item {
            Text(
                if (query.isNotBlank()) ui.t("search.results", "q" to query, "n" to results.size) else ui.t("home.total", "n" to results.size),
                style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
            )
        }
        if (results.isEmpty()) item { EmptyState(ui.t("search.emptyTitle"), ui.t("search.emptyBody")) }
        items(results, key = { it.id }) { ItemCard(it, c.categoryName(it.category), store.requests.contains(it.id)) { onOpen(it) } }
        item { Spacer(Modifier.height(24.dp)) }
    }
}

// ───────────────────────── 프롬프트 보관함 ─────────────────────────
@Composable
fun PromptsScreen(c: ContentFile, store: AppStore, toast: (String) -> Unit, onOpen: (Item) -> Unit) {
    val ctx = LocalContext.current
    val cs = MaterialTheme.colorScheme
    val ui = LocalUi.current
    LazyColumn(Modifier.fillMaxSize()) {
        item { SectionHeader(ui.t("prompts.title"), ui.t("count.n", "n" to c.published.sumOf { it.prompts.size })) }
        item { KText(ui.t("prompts.note"), Modifier.padding(horizontal = 16.dp), style = MaterialTheme.typography.bodySmall, color = cs.onSurfaceVariant) }
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
                                CopyButton(ui.t("prompt.copyShort"), Modifier.weight(1f)) {
                                    copyText(ctx, p.title, fillPrompt(it0.id, p, store.values)); toast(ui.t("prompt.copied"))
                                }
                                OutlinedButton(onClick = { onOpen(it0) }, modifier = Modifier.weight(1f).height(44.dp), shape = RoundedCornerShape(12.dp)) {
                                    Text(ui.t("prompt.fill"), fontWeight = FontWeight.Bold)
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
    val ui = LocalUi.current
    LazyColumn(Modifier.fillMaxSize()) {
        item {
            Row(Modifier.padding(16.dp), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                Pill(ui.t("saved.fav") + " ${store.favs.size}", seg == "fav", Modifier.weight(1f)) { seg = "fav" }
                Pill(ui.t("saved.recent") + " ${store.recent.size}", seg == "recent", Modifier.weight(1f)) { seg = "recent" }
                Pill(ui.t("saved.fb") + " ${store.myFeedback.size}", seg == "fb", Modifier.weight(1f)) { seg = "fb" }
            }
        }
        when (seg) {
            "fb" -> {
                val list = store.myFeedback.reversed()
                if (list.isEmpty()) item { EmptyState(ui.t("saved.noFbTitle"), ui.t("saved.noFbBody")) }
                val types = c.feedback.types.associate { it.id to it.label }
                items(list, key = { it.id }) { f ->
                    val resolved = c.resolvedFeedback.contains(f.id)
                    Column(
                        Modifier.padding(horizontal = 16.dp, vertical = 5.dp).fillMaxWidth().clip(RoundedCornerShape(14.dp))
                            .border(1.5.dp, cs.outline, RoundedCornerShape(14.dp)).padding(12.dp)
                    ) {
                        Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                            Tag(if (resolved) ui.t("saved.resolved") else if (f.status == "sent") ui.t("saved.received") else ui.t("saved.pending"), highlight = resolved)
                            Tag(types[f.type] ?: f.type)
                            Text(f.date, style = MaterialTheme.typography.labelSmall, color = cs.onSurfaceVariant)
                        }
                        Spacer(Modifier.height(6.dp))
                        KText(c.item(f.contentId)?.title ?: "", fontWeight = FontWeight.ExtraBold, style = MaterialTheme.typography.bodyMedium)
                        KText(f.text, style = MaterialTheme.typography.bodyMedium)
                    }
                }
                item { KText(ui.t("saved.fbPendingNote"), Modifier.padding(16.dp), style = MaterialTheme.typography.bodySmall, color = cs.onSurfaceVariant) }
            }
            else -> {
                val ids = if (seg == "fav") store.favs.toList() else store.recent.toList()
                val its = ids.mapNotNull { c.item(it) }
                if (its.isEmpty()) item {
                    if (seg == "fav") EmptyState(ui.t("saved.noFavTitle"), ui.t("saved.noFavBody"))
                    else EmptyState(ui.t("saved.noRecentTitle"), ui.t("saved.noRecentBody"))
                }
                items(its, key = { seg + it.id }) { ItemCard(it, c.categoryName(it.category), false) { onOpen(it) } }
                item { KText(ui.t("saved.noteApp"), Modifier.padding(16.dp), style = MaterialTheme.typography.bodySmall, color = cs.onSurfaceVariant) }
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
