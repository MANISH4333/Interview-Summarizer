# Prompt Iterations

This document tracks the evolution of the prompt used in the Interview Summarizer tool, highlighting the improvements made to achieve the desired output structure and quality.

---

## Iteration 1 (Initial Draft)
**Prompt:**
```text
Read this transcript and summarize it. Tell me the topics, what role the candidate fits, and a general summary of the candidate.
```
**Issues identified:**
- The model returned a long, unstructured essay.
- The topics were generic (e.g., "Experience", "Background") rather than specific to the candidate's actual work.
- The role recommendation lacked a seniority level and clear justification based on the transcript.

---

## Iteration 2 (Adding Structure)
**Prompt:**
```text
You are an HR analyst. Read the transcript and output exactly three sections:
1. Topics Covered
2. Candidate Profile
3. Candidate Summary
```
**Issues identified:**
- Better structure, but the model still included conversational filler before and after the summary (e.g., "Here is the summary you requested:").
- Topics were sometimes listed as paragraphs instead of bullet points.
- The candidate summary was occasionally too brief or missed critical concerns mentioned by the interviewer.

---

## Iteration 3 (Final Version)
**Prompt:**
```text
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
```

**Why this final version works best:**
1. **Role Context:** Assigning the persona of an "expert HR analyst" anchors the tone of the response.
2. **Strict Formatting:** The instruction "Do not add any extra sections or commentary" successfully stops the model from outputting conversational filler.
3. **Clear Constraints:** Specifying exact sentence counts (3–6 sentences) and bullet point targets (4–8) keeps the output uniform, concise, and predictable.
4. **Evidence-Based Justification:** Explicitly requiring the model to justify the profile "based on specific evidence" drastically improves the quality and reliability of the Candidate Profile section.
