package com.aijoso.app.data

/** 서버·AI 없는 검색: 제목·태그·동의어 사전으로 점수를 매긴다. 문장으로 검색해도 동작. */
class Searcher(private val c: ContentFile) {
    private val splitter = Regex("""[\s·,()+→↔]+""")
    private val termsById: Map<String, List<String>> = c.items.associate { item -> item.id to termsOf(item) }

    private fun termsOf(item: Item): List<String> {
        val t = linkedSetOf<String>()
        t.addAll(item.tags)
        item.title.split(splitter).filter { w -> w.length > 1 }.forEach { w -> t.add(w) }
        for ((key, values) in c.synonyms) {
            val group = listOf(key) + values
            if (group.any { w -> w in t || item.title.contains(w) }) {
                t.add(key); t.addAll(values)
            }
        }
        return t.toList()
    }

    fun score(item: Item, query: String): Double {
        val q = query.trim().lowercase()
        if (q.isEmpty()) return 1.0
        val qs = q.replace(Regex("""\s+"""), "")
        var s = 0.0
        val title = item.title.lowercase()
        for (w in termsById[item.id].orEmpty()) {
            val lw = w.lowercase()
            if (lw.length > 1 && (q.contains(lw) || qs.contains(lw))) s += if (title.contains(lw)) 3 else 2
        }
        for (w in q.split(Regex("""\s+"""))) if (w.length > 1 && item.title.contains(w)) s += 2
        if (item.isPublished && s > 0) s += 0.5
        return s
    }

    fun search(query: String, category: String? = null, difficulty: String? = null): List<Item> =
        c.items
            .map { it to score(it, query) }
            .filter { (item, s) -> s > 0 && (category == null || item.category == category) && (difficulty == null || item.difficulty == difficulty) }
            .sortedWith(compareByDescending<Pair<Item, Double>> { it.second }.thenBy { if (it.first.isPublished) 0 else 1 })
            .map { it.first }
}
