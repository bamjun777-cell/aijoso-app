package com.aijoso.app.ui

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

// 브랜드 색: 간판 노랑 + 먹색 ("쌈마이" 톤). 노랑 위 글자는 항상 먹색.
val Yellow = Color(0xFFFFD23F)
val Ink = Color(0xFF1C1B17)
val Mark = Color(0xFFFFE58A)

private val LightColors = lightColorScheme(
    primary = Ink, onPrimary = Yellow,
    secondary = Yellow, onSecondary = Ink,
    background = Color.White, onBackground = Ink,
    surface = Color.White, onSurface = Ink,
    surfaceVariant = Color(0xFFF6F5F0), onSurfaceVariant = Color(0xFF5F5B51),
    outline = Color(0xFFE4E1D6),
    primaryContainer = Color(0xFFFFF4C2), onPrimaryContainer = Ink,
    tertiary = Color(0xFF1F7A4D),
    error = Color(0xFF9A4F00), errorContainer = Color(0xFFFFF0DB), onErrorContainer = Color(0xFF6B3700),
)

private val DarkColors = darkColorScheme(
    primary = Yellow, onPrimary = Ink,
    secondary = Yellow, onSecondary = Ink,
    background = Color(0xFF141412), onBackground = Color(0xFFF2EFE6),
    surface = Color(0xFF141412), onSurface = Color(0xFFF2EFE6),
    surfaceVariant = Color(0xFF1F1E1A), onSurfaceVariant = Color(0xFFB3AEA0),
    outline = Color(0xFF3A3830),
    primaryContainer = Color(0xFF3A3318), onPrimaryContainer = Color(0xFFF2EFE6),
    tertiary = Color(0xFF5CC48E),
    error = Color(0xFFF2A64A), errorContainer = Color(0xFF3A2A14), onErrorContainer = Color(0xFFFFD9A8),
)

@Composable
fun AppTheme(content: @Composable () -> Unit) {
    MaterialTheme(colorScheme = if (isSystemInDarkTheme()) DarkColors else LightColors, content = content)
}
