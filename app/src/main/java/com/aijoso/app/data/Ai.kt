package com.aijoso.app.data

/** 프롬프트를 붙여넣을 AI. 주소는 각 서비스의 새 대화 화면 (앱이 깔려 있으면 앱으로 열림) */
data class AiSite(val id: String, val name: String, val url: String)

val AI_SITES = listOf(
    AiSite("claude", "Claude", "https://claude.ai/new"),
    AiSite("chatgpt", "ChatGPT", "https://chatgpt.com/"),
    AiSite("gemini", "Gemini", "https://gemini.google.com/app"),
)

fun aiSite(id: String): AiSite? = AI_SITES.firstOrNull { it.id == id }
