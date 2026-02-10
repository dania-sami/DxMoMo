import csv
import datetime as dt
import os
import string
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple


REFLECTIONS_FILE = "reflections.csv"


POSITIVE_WORDS = {
    "calm", "grateful", "happy", "good", "hopeful", "relaxed", "progress",
    "energy", "energised", "energized", "proud", "excited", "okay", "better"
}

NEGATIVE_WORDS = {
    "tired", "exhausted", "anxious", "worried", "stressed", "overwhelmed",
    "low", "drained", "sad", "down", "frustrated", "angry", "tense"
}

STOPWORDS = {
    "the", "and", "a", "an", "to", "for", "in", "on", "of", "at", "it",
    "is", "was", "am", "are", "this", "that", "with", "but", "so", "just",
    "have", "had", "been", "from", "today", "yesterday", "tomorrow"
}


@dataclass
class Reflection:
    timestamp: str
    energy: int
    tone: str
    mood_score: int
    stress_hint: str
    on_mind: str
    went_well: str
    difficult: str
    small_step: str


def prompt_int(prompt: str, minimum: int, maximum: int) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if minimum <= value <= maximum:
                return value
        except ValueError:
            pass
        print(f"Please enter a number between {minimum} and {maximum}.")


def capture_reflection() -> Reflection:
    print()
    print("New daily reflection")
    print("-" * 40)

    energy = prompt_int(
        "How is your energy today on a scale from 1 (very low) to 5 (very high)? ",
        1,
        5,
    )
    on_mind = input("What is on your mind right now? ").strip()
    went_well = input("One thing that went well today? ").strip()
    difficult = input("One thing that felt difficult today? ").strip()
    small_step = input("Is there one small step you want to take tomorrow? ").strip()

    combined_text = " ".join([on_mind, went_well, difficult]).lower()
    mood_score, tone = analyse_mood(combined_text, energy)
    stress_hint = build_stress_hint(combined_text)

    ts = dt.datetime.now().isoformat(timespec="seconds")

    print()
    print("Thank you. Here is a short reflection summary for today:")
    print(f"- Energy: {energy}/5")
    print(f"- Overall tone: {tone} (mood score {mood_score})")
    if stress_hint:
        print(f"- Noticed: {stress_hint}")
    if small_step:
        print(f"- Tomorrow's small step: {small_step}")
    print()

    return Reflection(
        timestamp=ts,
        energy=energy,
        tone=tone,
        mood_score=mood_score,
        stress_hint=stress_hint,
        on_mind=on_mind,
        went_well=went_well,
        difficult=difficult,
        small_step=small_step,
    )


def analyse_mood(text: str, energy: int) -> Tuple[int, str]:
    tokens = [t.strip(string.punctuation) for t in text.split()]
    pos = sum(1 for t in tokens if t in POSITIVE_WORDS)
    neg = sum(1 for t in tokens if t in NEGATIVE_WORDS)
    mood_score = pos - neg + (energy - 3)

    if mood_score >= 2:
        tone = "positive"
    elif mood_score <= -2:
        tone = "strained"
    else:
        tone = "neutral"
    return mood_score, tone


def build_stress_hint(text: str) -> str:
    tokens = [t.strip(string.punctuation) for t in text.split()]
    negatives = [t for t in tokens if t in NEGATIVE_WORDS]
    if len(negatives) >= 3:
        unique_neg = sorted(set(negatives))
        joined = ", ".join(unique_neg)
        return f"many mentions of {joined}"
    if "tired" in negatives or "exhausted" in negatives:
        return "several mentions of being tired or low on energy"
    if "worried" in negatives or "anxious" in negatives:
        return "worry and anxiety showed up more than once"
    return ""


def ensure_file_exists(path: str) -> None:
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "timestamp",
                    "energy",
                    "tone",
                    "mood_score",
                    "stress_hint",
                    "on_mind",
                    "went_well",
                    "difficult",
                    "small_step",
                ]
            )


def save_reflection(reflection: Reflection) -> None:
    ensure_file_exists(REFLECTIONS_FILE)
    with open(REFLECTIONS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(reflection).keys()))
        writer.writerow(asdict(reflection))


def load_reflections() -> List[Reflection]:
    if not os.path.exists(REFLECTIONS_FILE):
        return []
    reflections: List[Reflection] = []
    with open(REFLECTIONS_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            reflections.append(
                Reflection(
                    timestamp=row["timestamp"],
                    energy=int(row["energy"]),
                    tone=row["tone"],
                    mood_score=int(row["mood_score"]),
                    stress_hint=row["stress_hint"],
                    on_mind=row["on_mind"],
                    went_well=row["went_well"],
                    difficult=row["difficult"],
                    small_step=row["small_step"],
                )
            )
    return reflections


def summarise_keywords(reflections: List[Reflection]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for ref in reflections:
        text = " ".join([ref.on_mind, ref.went_well, ref.difficult]).lower()
        tokens = [t.strip(string.punctuation) for t in text.split()]
        for token in tokens:
            if not token or token in STOPWORDS:
                continue
            counts[token] = counts.get(token, 0) + 1
    return counts


def view_summary() -> None:
    reflections = load_reflections()
    if not reflections:
        print()
        print("No reflections found yet. Add at least one day first.")
        print()
        return

    print()
    print("Reflection summary")
    print("-" * 40)
    print(f"Total days recorded: {len(reflections)}")

    avg_energy = sum(r.energy for r in reflections) / len(reflections)
    print(f"Average energy: {avg_energy:.1f} / 5")

    tone_counts: Dict[str, int] = {}
    for r in reflections:
        tone_counts[r.tone] = tone_counts.get(r.tone, 0) + 1

    for tone in ["positive", "neutral", "strained"]:
        if tone in tone_counts:
            print(f"Days that felt {tone}: {tone_counts[tone]}")

    keywords = summarise_keywords(reflections)
    if keywords:
        sorted_keywords = sorted(keywords.items(), key=lambda kv: kv[1], reverse=True)
        top_keywords = [f"{word} ({count})" for word, count in sorted_keywords[:6]]
        print()
        print("Words that keep showing up in your reflections:")
        print(", ".join(top_keywords))

    print()
    print("Gentle observations:")
    if tone_counts.get("strained", 0) >= 3:
        print("- There have been several strained days. It might help to notice what repeats on those days.")
    if any(k in keywords for k in ["sleep", "tired", "exhausted"]):
        print("- Sleep and energy show up often. It could be worth giving them a bit of extra attention.")
    if any(k in keywords for k in ["progress", "learning", "study", "project"]):
        print("- You mention progress and learning quite a lot. That might be a quiet strength to build on.")

    print()
    print("You can always add one small step for tomorrow rather than trying to fix everything at once.")
    print()


def main() -> None:
    while True:
        print("MoMo Daily Reflection Demo")
        print("-" * 40)
        print("1) New reflection")
        print("2) View summary")
        print("3) Exit")
        choice = input("Choose an option (1–3): ").strip()

        if choice == "1":
            reflection = capture_reflection()
            save_reflection(reflection)
        elif choice == "2":
            view_summary()
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Please choose 1, 2 or 3.")
        print()


if __name__ == "__main__":
    main()
