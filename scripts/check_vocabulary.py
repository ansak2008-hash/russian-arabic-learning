#!/usr/bin/env python3
"""Check that words in lesson 'new vocabulary' tables have not appeared earlier."""
import csv
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "vocabulary" / "token-ledger.csv"
LESSONS = sorted((ROOT / "lessons").glob("*.md"))

def normalize(token: str) -> str:
    token = unicodedata.normalize("NFD", token.casefold())
    token = "".join(ch for ch in token if unicodedata.category(ch) != "Mn")
    token = token.replace("ـ", "")
    token = token.translate(str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ؤ": "و", "ئ": "ي"}))
    if re.fullmatch(r"[\u0600-\u06FF]+", token) and token.startswith("ال") and len(token) > 4:
        token = token[2:]
    return token

def words(text: str):
    return re.findall(r"[\w\u0600-\u06FF]+", text, flags=re.UNICODE)

with LEDGER.open(encoding="utf-8-sig", newline="") as handle:
    records = list(csv.DictReader(handle))
known = {}
for row in records:
    key = (row["language"], row["normalized"])
    old = known.get(key)
    if old is None or row["first_lesson"] < old:
        known[key] = row["first_lesson"]

errors = []
checked = 0
for lesson in LESSONS:
    lesson_id = lesson.stem
    language = None
    in_new_vocab = False
    lesson_seen = set()
    for line_no, line in enumerate(lesson.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("## 1. الروسية للعرب"):
            language, in_new_vocab = "ru", False
            continue
        if line.startswith("## 2. العربية للروس"):
            language, in_new_vocab = "ar", False
            continue
        if line.startswith("### مفردات جديدة / Новая лексика"):
            in_new_vocab = True
            continue
        if line.startswith("## ") or (line.startswith("### ") and in_new_vocab):
            in_new_vocab = False
        if not in_new_vocab or not line.startswith("|") or line.startswith("|---") or "النطق" in line or "الروسية" in line or "العربية" in line:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2 or not cells[0]:
            continue
        term = cells[0]
        checked += 1
        for token in words(term):
            normalized = normalize(token)
            key = (language, normalized)
            first_lesson = known.get(key)
            if first_lesson and first_lesson != lesson_id:
                errors.append(f"{lesson.name}:{line_no}: repeated {language} word '{token}' (first used in {first_lesson})")
            if key in lesson_seen:
                errors.append(f"{lesson.name}:{line_no}: repeated word '{token}' inside this lesson's new vocabulary")
            lesson_seen.add(key)

if errors:
    print("Vocabulary repetition check FAILED:")
    print("\n".join(f"- {error}" for error in errors))
    sys.exit(1)
print(f"Vocabulary repetition check passed: inspected {checked} new-vocabulary entries across {len(LESSONS)} lessons.")
print("Note: words reused in example sentences and dialogues are allowed for review.")
