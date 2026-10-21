---
applyTo: "lessons/**/*.md"
---

# Bilingual lesson authoring rules

- Every lesson must teach both directions: Russian for Arabic speakers and Arabic for Russian speakers.
- Include a dedicated `### مفردات جديدة / Новая лексика` table under each language direction. List only genuinely new target words or expressions there.
- Reuse prior words in examples, natural sentences, and dialogues when needed, but treat them as review; never label them as new again.
- Add every new term to `vocabulary/word-ledger.csv` and every new lexical token to `vocabulary/token-ledger.csv`.
- Run `python scripts/check_vocabulary.py` before publishing. The GitHub Actions workflow also runs the check on lesson or vocabulary changes.
- Do not copy lesson text from external sites. Use them for syllabus structure, sequencing, pronunciation references, and teaching-method inspiration; write original examples.
- Verify translations, stress marks, Arabic gender/address forms, and the naturalness of both dialogues.
- Keep each lesson short enough to study in one sitting, but include full sentences and a practical dialogue.
