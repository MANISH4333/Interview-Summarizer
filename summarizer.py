import sys
import os
from groq import Groq
from dotenv import load_dotenv

# ── Load environment variables ──────────────────────────────────────────────
load_dotenv()

PROMPT_TEMPLATE = """
You are an expert HR analyst. Carefully read the interview transcript below and produce a structured summary with exactly three sections.

---

TRANSCRIPT:
{transcript}

---

Now generate the summary in the following format. Do not add any extra sections or commentary outside of this structure.

## 1. Topics Covered
List the main themes discussed in the interview as bullet points. Be specific — use the actual subject matter from the transcript, not generic labels. Aim for 4–8 distinct topics.

## 2. Candidate Profile
State the role and seniority level this candidate best fits (e.g., "Backend Engineer — mid-level", "Program Manager — senior").
Then write 2–3 sentences justifying this based on specific evidence from the transcript.

## 3. Candidate Summary
Write a short paragraph of 3–6 sentences covering their background, strengths, concerns, and overall impression. If anything is unclear from the transcript, say so rather than guessing.
"""


def load_api_key() -> str:
    """Load and validate the Groq API key from environment."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY is not set.")
        print("Create a .env file in this directory with the following content:")
        print("  GROQ_API_KEY=your_groq_api_key_here")
        sys.exit(1)
    return api_key


def load_transcript(filepath: str) -> str:
    """Read and return the transcript text from the given file path."""
    if not os.path.isfile(filepath):
        print(f"Error: File not found — '{filepath}'")
        print("Usage: python summarizer.py <transcript.txt>")
        sys.exit(1)

    if not filepath.lower().endswith(".txt"):
        print(f"Warning: '{filepath}' does not have a .txt extension. Proceeding anyway...")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except OSError as e:
        print(f"Error: Could not read file '{filepath}': {e}")
        sys.exit(1)

    if not content:
        print(f"Error: The transcript file '{filepath}' is empty.")
        sys.exit(1)

    return content


def summarize_transcript(transcript: str, api_key: str) -> str:
    """Send the transcript to Groq and return the structured summary."""
    client = Groq(api_key=api_key)

    prompt = PROMPT_TEMPLATE.format(transcript=transcript)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: Groq API call failed — {e}")
        sys.exit(1)


def save_summary(summary: str, output_path: str = "transcript_summary.txt") -> None:
    """Write the summary to a text file."""
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"\nSuccess! Summary saved to '{output_path}'")
    except OSError as e:
        print(f"Warning: Could not save summary to file — {e}")


def main():
    # ── Validate CLI arguments ───────────────────────────────────────────────
    if len(sys.argv) != 2:
        print("Usage: python summarizer.py <transcript.txt>")
        sys.exit(1)

    transcript_path = sys.argv[1]

    # ── Load resources ───────────────────────────────────────────────────────
    api_key    = load_api_key()
    transcript = load_transcript(transcript_path)

    print(f"Processing transcript: '{transcript_path}' …\n")

    # ── Generate summary ─────────────────────────────────────────────────────
    summary = summarize_transcript(transcript, api_key)

    # ── Output ───────────────────────────────────────────────────────────────
    print("=" * 60)
    print(summary)
    print("=" * 60)

    save_summary(summary)


if __name__ == "__main__":
    main()
