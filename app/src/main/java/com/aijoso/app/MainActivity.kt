package com.aijoso.app

import android.graphics.Color
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.SystemBarStyle
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.aijoso.app.data.AppStore
import com.aijoso.app.data.parseUi
import com.aijoso.app.ui.AppEntry
import com.aijoso.app.ui.AppTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // 상단 바가 노랑이라 상태 표시줄 아이콘은 항상 어둡게
        enableEdgeToEdge(statusBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.TRANSPARENT))
        // 콘텐츠·화면 문구는 앱 안에 내장 → 인터넷 없이도 전부 볼 수 있음 (언어별 파일)
        val read: (String) -> String = { name -> assets.open(name).bufferedReader(Charsets.UTF_8).use { it.readText() } }
        val ui = parseUi(read("ui.json"))
        val store = AppStore(applicationContext)
        setContent { AppTheme { AppEntry(store, ui, read) } }
    }
}
