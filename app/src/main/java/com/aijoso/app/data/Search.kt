package com.aijoso.app.data

/** 서버·AI 없는 검색: 제목·태그·동의어 사전으로 점수를 매긴다. 문장으로 검색해도 동작. */
class Searcher(private val c: ContentFile) {
    private val splitter = Regex("""[\s·,()+→↔:/]+""")
    private val stop = setOf("the", "and", "for", "with", "from", "into", "your", "you", "all", "one", "out", "get", "how", "what", "are", "can", "this", "that", "takes", "forever")

    private fun ascii(w: String) = w.all { it.code < 128 }
    /** 영어 단어는 단어 처음부터 맞을 때만 (pay → payroll O, ar → car X). 한·중·일은 포함 여부 */
    private fun hit(term: String, text: String): Boolean =
        if (ascii(term)) Regex("(^|[^a-z0-9])" + Regex.escape(term) + if (term.length <= 3) "($|[^a-z0-9])" else "").containsMatchIn(text)
        else text.contains(term)
    private fun useful(w: String) = w.length > 1 && !(ascii(w) && (w.length < 3 || w in stop))
    private val termsById: Map<String, List<String>> = c.items.associate { item -> item.id to termsOf(item) }

    private fun termsOf(item: Item): List<String> {
        val t = linkedSetOf<String>()
        t.addAll(item.tags)
        item.title.lowercase().split(splitter).filter { w -> useful(w) }.forEach { w -> t.add(w) }
        for ((key, values) in c.synonyms) {
            val group = listOf(key) + values
            if (group.any { w -> w.lowercase() in t || hit(w.lowercase(), item.title.lowercase()) }) {
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
            if ((lw.length > 1 || lw == q) && (hit(lw, q) || (!ascii(lw) && qs.contains(lw)))) s += if (hit(lw, title)) 3 else 2
        }
        for (w in q.split(Regex("""\s+"""))) if (useful(w) && hit(w, title)) s += 2
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
