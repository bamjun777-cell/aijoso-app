package com.aijoso.app.ui

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Density
import androidx.compose.ui.unit.dp
import com.aijoso.app.data.AppStore
import com.aijoso.app.data.ContentFile
import com.aijoso.app.data.Item
import com.aijoso.app.data.Moderator
import com.aijoso.app.data.Searcher
import kotlinx.coroutines.launch

private data class TabDef(val label: String, val icon: ImageVector)
private val TABS = listOf(TabDef("홈", Icons.Filled.Home), TabDef("찾기", Icons.Filled.Search), TabDef("프롬프트", Icons.Filled.Edit), TabDef("보관함", Icons.Filled.Star))

@Composable
fun AppRoot(content: ContentFile, store: AppStore) {
    val searcher = remember(content) { Searcher(content) }
    val moderator = remember(content) { Moderator(content.moderation) }
    var tab by rememberSaveable { mutableIntStateOf(0) }
    var detailId by rememberSaveable { mutableStateOf<String?>(null) }
    var query by rememberSaveable { mutableStateOf("") }
    var category by rememberSaveable { mutableStateOf<String?>(null) }
    var difficulty by rememberSaveable { mutableStateOf<String?>(null) }
    var sheet by remember { mutableStateOf<Sheet?>(null) }
    val snackbar = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()
    val toast: (String) -> Unit = { msg ->
        scope.launch { snackbar.currentSnackbarData?.dismiss(); snackbar.showSnackbar(msg) }
    }
    val open: (Item) -> Unit = { item ->
        if (item.isPublished) { store.touchRecent(item.id); detailId = item.id } else sheet = Sheet.Request(item)
    }

    BackHandler(enabled = detailId != null) { detailId = null }

    val density = LocalDensity.current
    CompositionLocalProvider(LocalDensity provides Density(density.density, density.fontScale * store.fontScale)) {
        Scaffold(
            topBar = {
                TopBar(
                    title = detailId?.let { id -> content.item(id)?.let { content.categoryName(it.category) } },
                    onBack = if (detailId != null) ({ detailId = null }) else null,
                    onSettings = { sheet = Sheet.Settings },
                )
            },
            bottomBar = {
                Column {
                    AdSlot()
                    NavigationBar(containerColor = MaterialTheme.colorScheme.background) {
                        TABS.forEachIndexed { i, t ->
                            NavigationBarItem(
                                selected = detailId == null && tab == i,
                                onClick = { tab = i; detailId = null },
                                icon = { Icon(t.icon, contentDescription = null) },
                                label = { Text(t.label, fontWeight = FontWeight.Bold) },
                                colors = NavigationBarItemDefaults.colors(indicatorColor = Yellow, selectedIconColor = Ink),
                            )
                        }
                    }
                }
            },
            snackbarHost = { SnackbarHost(snackbar) },
            containerColor = MaterialTheme.colorScheme.background,
        ) { pad ->
            Box(Modifier.padding(pad).fillMaxSize()) {
                val item = detailId?.let { content.item(it) }
                when {
                    item != null -> DetailScreen(item, content, store, toast, onFeedback = { sheet = Sheet.Feedback(item) })
                    tab == 0 -> HomeScreen(content, store, onOpen = open,
                        onSearch = { q -> query = q; category = null; difficulty = null; tab = 1 },
                        onCategory = { c -> category = c; query = ""; tab = 1 })
                    tab == 1 -> SearchScreen(content, searcher, store, query, { query = it }, category, { category = it }, difficulty, { difficulty = it }, open)
                    tab == 2 -> PromptsScreen(content, store, toast, onOpen = open)
                    else -> SavedScreen(content, store, onOpen = open)
                }
            }
        }

        when (val s = sheet) {
            is Sheet.Feedback -> FeedbackSheet(s.item, content, moderator, onDismiss = { sheet = null }) { type, text ->
                store.addFeedback(s.item.id, type, text)
                sheet = null
                toast("고마워요! 반영되면 알려 드릴게요")
            }
            is Sheet.Request -> RequestSheet(s.item, store.requests.contains(s.item.id), onDismiss = { sheet = null }) {
                val added = store.toggleRequest(s.item.id)
                sheet = null
                toast(if (added) "요청했어요! 올라오면 알려 드릴게요" else "요청을 취소했어요")
            }
            Sheet.Settings -> SettingsSheet(content, store, onDismiss = { sheet = null })
            null -> Unit
        }
    }
}

sealed interface Sheet {
    data class Feedback(val item: Item) : Sheet
    data class Request(val item: Item) : Sheet
    data object Settings : Sheet
}

@Composable
private fun TopBar(title: String?, onBack: (() -> Unit)?, onSettings: () -> Unit) {
    Column(Modifier.background(Yellow).windowInsetsPadding(WindowInsets.statusBars)) {
        Row(Modifier.fillMaxWidth().height(56.dp).padding(horizontal = 8.dp), verticalAlignment = Alignment.CenterVertically) {
            if (onBack != null) {
                IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "뒤로", tint = Ink) }
                Text(title ?: "", color = Ink, fontWeight = FontWeight.ExtraBold, style = MaterialTheme.typography.titleMedium, modifier = Modifier.weight(1f))
            } else {
                Column(Modifier.weight(1f).padding(start = 8.dp)) {
                    Text("AI 좋소", color = Ink, fontWeight = FontWeight.Black, style = MaterialTheme.typography.titleLarge)
                    Text("작은 회사의 큰 업무를 가볍게", color = Ink, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.labelSmall)
                }
            }
            IconButton(onClick = onSettings) { Icon(Icons.Filled.Settings, contentDescription = "설정", tint = Ink) }
        }
        HorizontalDivider(thickness = 2.dp, color = Ink)
    }
}

/** 광고 자리 (다음 단계에서 AdMob 테스트 배너로 교체) */
@Composable
private fun AdSlot() {
    val cs = MaterialTheme.colorScheme
    Box(Modifier.fillMaxWidth().height(50.dp).background(cs.surfaceVariant), contentAlignment = Alignment.Center) {
        Text("광고 영역 · 다음 단계에서 AdMob 연결", style = MaterialTheme.typography.labelMedium, color = cs.onSurfaceVariant)
    }
    HorizontalDivider(color = cs.outline)
}
