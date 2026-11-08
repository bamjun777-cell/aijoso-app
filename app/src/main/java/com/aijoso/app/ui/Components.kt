package com.aijoso.app.ui

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.LineBreak
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.aijoso.app.data.Item
import com.aijoso.app.data.difficultyLabel

/**
 * 한국어 줄바꿈: 단어(어절) 중간에서 끊기지 않도록 글자 사이에 '줄바꿈 금지' 문자(U+2060)를 넣는다.
 * 띄어쓰기와 '·' 뒤에서만 줄이 바뀐다. 화면 표시용 (복사용 글자에는 쓰지 않음).
 */
fun keepAll(s: String): String {
    val sb = StringBuilder(s.length * 2)
    for (i in s.indices) {
        val c = s[i]
        if (i > 0) {
            val p = s[i - 1]
            if (!p.isWhitespace() && !c.isWhitespace() && p != '·' && p != '/' && p != '→') sb.append('⁠')
        }
        sb.append(c)
    }
    return sb.toString()
}

/** 기본 글자 컴포넌트: 어절 단위 줄바꿈 + 제목은 줄 길이 균형(Heading) */
@Composable
fun KText(
    text: String,
    modifier: Modifier = Modifier,
    style: TextStyle = MaterialTheme.typography.bodyLarge,
    color: Color = Color.Unspecified,
    fontWeight: FontWeight? = null,
    heading: Boolean = false,
    maxLines: Int = Int.MAX_VALUE,
    textAlign: TextAlign? = null,
) {
    Text(
        text = keepAll(text),
        modifier = modifier,
        style = style.copy(lineBreak = if (heading) LineBreak.Heading else LineBreak.Paragraph),
        color = color,
        fontWeight = fontWeight,
        maxLines = maxLines,
        overflow = TextOverflow.Ellipsis,
        textAlign = textAlign,
    )
}

/** 선택형 알약 버튼 (필터·종류 선택) */
@Composable
fun Pill(text: String, selected: Boolean, modifier: Modifier = Modifier, onClick: () -> Unit) {
    val cs = MaterialTheme.colorScheme
    val shape = RoundedCornerShape(50)
    Box(
        modifier
            .clip(shape)
            .background(if (selected) cs.onBackground else cs.background)
            .border(1.5.dp, if (selected) cs.onBackground else cs.outline, shape)
            .clickable(onClick = onClick)
            .heightIn(min = 40.dp)
            .padding(horizontal = 14.dp, vertical = 9.dp),
        contentAlignment = Alignment.Center,
    ) {
        Text(keepAll(text), color = if (selected) cs.background else cs.onBackground, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.Bold)
    }
}

/** 작은 정보 표시 (분야·난이도·시간) */
@Composable
fun Tag(text: String, highlight: Boolean = false, dashed: Boolean = false) {
    val cs = MaterialTheme.colorScheme
    val shape = RoundedCornerShape(50)
    Box(
        Modifier
            .clip(shape)
            .background(if (highlight) Yellow else if (dashed) Color.Transparent else cs.surfaceVariant)
            .then(if (dashed) Modifier.border(1.dp, cs.onSurfaceVariant, shape) else Modifier)
            .padding(horizontal = 9.dp, vertical = 4.dp)
    ) {
        Text(text, style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.Bold, color = if (highlight) Ink else if (dashed) cs.onSurfaceVariant else cs.onBackground)
    }
}

@Composable
fun SectionHeader(title: String, aside: String = "") {
    Row(Modifier.fillMaxWidth().padding(start = 16.dp, end = 16.dp, top = 22.dp, bottom = 10.dp), verticalAlignment = Alignment.Bottom) {
        KText(title, Modifier.weight(1f), style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Black, heading = true)
        if (aside.isNotEmpty()) Text(aside, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

/** 매뉴얼 카드. 공개된 매뉴얼은 굵은 테두리, 준비 중은 흐리게 */
@Composable
fun ItemCard(item: Item, categoryName: String, requested: Boolean, onClick: () -> Unit) {
    val cs = MaterialTheme.colorScheme
    val pub = item.isPublished
    val shape = RoundedCornerShape(16.dp)
    Column(
        Modifier
            .padding(horizontal = 16.dp, vertical = 5.dp)
            .fillMaxWidth()
            .clip(shape)
            .border(if (pub) 2.dp else 1.5.dp, if (pub) cs.onBackground else cs.outline, shape)
            .clickable(onClick = onClick)
            .padding(14.dp)
    ) {
        KText(item.title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.ExtraBold, color = if (pub) cs.onBackground else cs.onSurfaceVariant, heading = true)
        if (pub && item.subtitle.isNotBlank()) {
            Spacer(Modifier.height(4.dp))
            KText(item.subtitle, style = MaterialTheme.typography.bodyMedium, color = cs.onSurfaceVariant, heading = true)
        }
        Spacer(Modifier.height(10.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
            Tag(categoryName)
            Tag(difficultyLabel(item.difficulty))
            if (pub) Tag("${item.timeBeforeMin}분 → ${item.timeAfterMin}분", highlight = true)
            else Tag(if (requested) "요청함" else "준비 중", dashed = true)
        }
    }
}

fun copyText(context: Context, label: String, text: String) {
    val cm = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
    cm.setPrimaryClip(ClipData.newPlainText(label, text))
}

fun shareText(context: Context, text: String) {
    val send = Intent(Intent.ACTION_SEND).apply {
        type = "text/plain"
        putExtra(Intent.EXTRA_TEXT, text)
    }
    context.startActivity(Intent.createChooser(send, "공유하기"))
}
