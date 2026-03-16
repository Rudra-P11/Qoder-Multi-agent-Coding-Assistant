"""
AmbiguityAnalyzer — scores a task for underspecification before planning begins.

Dimensions scored (0.0–1.0 each, averaged):
  goal_clarity       — is the deliverable obvious? (file? API? CLI? UI?)
  technical_stack    — is language/library/framework specified or freely chosen?
  scope_bounds       — is the task bounded or open-ended?
  dependencies       — does it need credentials, external data, or existing code?

If mean score ≥ THRESHOLD, returns up to 3 targeted questions as multiple-choice options.
"""
import json
from app.llm.ollama_client import ollama_client
from app.llm.prompts import AMBIGUITY_ANALYZER_PROMPT

THRESHOLD = 0.55  # tunable — lower = ask more questions, higher = ask less


class AmbiguityAnalyzer:

    def analyze(self, task: str) -> dict:
        """
        Returns:
          {
            "needs_clarification": bool,
            "score": float,
            "questions": [
              {
                "id": "q1",
                "question": "What language should the script use?",
                "options": ["Python", "JavaScript", "Any — agent decides"]
              },
              ...
            ]
          }
        """
        prompt = AMBIGUITY_ANALYZER_PROMPT.format(task=task)

        try:
            raw = ollama_client.generate_json(prompt)

            data = json.loads(raw)

            scores = data.get("scores", {})
            raw_questions = data.get("questions", [])

            # Calculate mean ambiguity score
            score_values = [v for v in scores.values() if isinstance(v, (int, float))]
            mean_score = sum(score_values) / len(score_values) if score_values else 0.0

            # Only surface questions if score exceeds threshold AND questions were generated
            needs_clarification = mean_score >= THRESHOLD and len(raw_questions) > 0

            # Cap at 3 questions, validate structure
            questions = []
            for q in raw_questions[:3]:
                if "question" in q and "options" in q and len(q["options"]) >= 2:
                    questions.append({
                        "id": q.get("id", f"q{len(questions)+1}"),
                        "question": q["question"],
                        "options": q["options"][:3]  # max 3 options
                    })

            return {
                "needs_clarification": needs_clarification,
                "score": round(mean_score, 2),
                "questions": questions if needs_clarification else []
            }

        except Exception as e:
            # On any failure, proceed without clarification (fail open)
            return {
                "needs_clarification": False,
                "score": 0.0,
                "questions": [],
                "error": str(e)
            }


ambiguity_analyzer = AmbiguityAnalyzer()
