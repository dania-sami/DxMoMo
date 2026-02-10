# MoMo Daily Reflection Demo

Hi,

My name is Dania and this is a small personal demo I built to explore ideas that are close to MoMo’s vision: short daily check‑ins, emotional patterns, and gentle habit support.

The goal of this project is not to be a full product, but to show how I think about:

- keeping interactions short and low‑friction
- reflecting emotional tone and patterns back to the user
- suggesting small, realistic next steps instead of generic advice

Everything is intentionally transparent and simple so it is easy to discuss, critique and extend.

## What the demo does

The script acts like a tiny text‑based “pocket coach”:

1. **Daily check‑in**

   It asks a few very short questions, for example:

   - “How is your energy today on a scale from 1–5?”
   - “What is on your mind right now?”
   - “One thing that went well today?”
   - “One thing that felt difficult?”
   - “Is there one small step you want to take tomorrow?”

   The answers are stored in a local CSV file on disk (no network calls, no external services).

2. **Lightweight emotional analysis**

   The script uses a very small, transparent word list to estimate:

   - a rough “mood score”
   - whether the day feels more positive, neutral or strained
   - a simple “stress hint” if many “overwhelmed”, “tired”, “worried” type words appear

   This is intentionally basic and easy to read in the code. The idea is to keep it explainable rather than “magical”.

3. **Patterns over time**

   When you choose “View summary”, the script:

   - loads previous reflections from the CSV file
   - calculates average energy
   - counts how many days looked positive, neutral or strained
   - shows recurring keywords that appear in the free text (for example sleep, work, study, friends)
   - prints a short reflection summary, such as:

     - “You have described several days as ‘tired’ or ‘drained’.”
     - “The word ‘sleep’ appeared multiple times this week.”
     - “You mention ‘progress’ and ‘learning’ often.”

   This is meant to echo MoMo’s focus on emotional patterns and gentle awareness.

## How to run

1. Make sure you have Python 3.8 or later installed.

2. (Optional but recommended) create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies (there are no external libraries, but this keeps the workflow familiar):

   ```bash
   pip install -r requirements.txt
   ```

4. Run the demo:

   ```bash
   python main.py
   ```

5. You will see a small menu:

   - `1` – New reflection
   - `2` – View summary
   - `3` – Exit

   Start by entering a new reflection, then try “View summary” after a few entries (or pre‑populate the CSV with sample days).

## Data and privacy

- All data is stored in a single local file: `reflections.csv` in the same folder.
- There are no network calls and no external services.
- The format is simple CSV so it can be inspected and deleted easily.

## Files

- `main.py` – the main script with the interaction loop, reflection capture and summary logic.
- `requirements.txt` – included for completeness, but the project uses only the Python standard library.
- `reflections.csv` – created automatically after the first reflection.

## Closing note

This demo is a small way for me to explore how a mindful pocket coach can:

- stay light and friendly
- surface emotional trends
- and nudge the user toward one small, realistic step at a time

I would be happy to walk through the code and design choices live if that is useful.

Best regards,  
Dania
