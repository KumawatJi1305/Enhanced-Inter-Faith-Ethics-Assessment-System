# ethics_api.py
import requests
import json
import re
from typing import Any, Dict, List

# --- Configure your OpenRouter key/model ---
API_KEY = "Enter your API key"
API_URL = "Enter your url"
MODEL = "Enter your model"  # Keep your current model

def _default_payload(user_input: str) -> Dict[str, Any]:
    """
    Minimal safe fallback payload if the model output can't be parsed.
    Keeps your UI working rather than crashing.
    """
    return {
        "score": 0.0,
        "suggestion": "We could not generate a complete analysis for this input. Please try again.",
        "insights": {
            "religious": {
                "highest": {"tradition": "—", "score": 0.0},
                "lowest":  {"tradition": "—", "score": 0.0},
                "consensus": 0.0
            },
            "classification": {
                "primary_context": "General",
                "scores": [
                    {"label": "General", "score": 1.0}
                ]
            },
            "framework_summary": "No framework summary available.",
            "assessment": {
                "concern": "Insufficient data.",
                "recommendation": "Please resubmit the scenario."
            }
        },
        "scoring": [
            {"religion": "Hinduism", "score": 0.0},
            {"religion": "Islam", "score": 0.0},
            {"religion": "Christianity", "score": 0.0},
            {"religion": "Sikhism", "score": 0.0},
            {"religion": "Buddhism", "score": 0.0},
            {"religion": "Judaism", "score": 0.0}
        ]
    }

def _extract_json_block(text: str) -> str:
    """
    Extract the first JSON object from a text response.
    Handles cases with code fences and extra prose.
    """
    # Strip code fences if present
    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if fenced:
        return fenced.group(1).strip()

    # Fallback: first {...} block (non-greedy)
    curly = re.search(r"\{[\s\S]*\}", text)
    if curly:
        return curly.group(0).strip()

    return ""

def _coerce_float(v: Any, default: float = 0.0) -> float:
    try:
        return float(v)
    except Exception:
        return default

def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))

def evaluate_ethics(user_input: str) -> Dict[str, Any]:
    """
    Calls the model and returns a dict with the shape required by your result page:

    {
      "score": 0..10 (float),
      "suggestion": str,
      "insights": {
        "religious": {
          "highest": {"tradition": str, "score": 0..1},
          "lowest":  {"tradition": str, "score": 0..1},
          "consensus": 0..1
        },
        "classification": {
          "primary_context": str,
          "scores": [{"label": str, "score": float}, ...]
        },
        "framework_summary": str,
        "assessment": {"concern": str, "recommendation": str}
      },
      "scoring": [{"religion": str, "score": 0..1}, ...]
    }
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        # OpenRouter asks for these for attribution/rate-limiting
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "EthicsAI Project"
    }

    # Instruct the model to return JSON ONLY in the exact schema we need.
    prompt = f"""
You are an AI ethicist. Analyze the user's scenario below and return ONLY a JSON object
in the EXACT schema that follows. No explanations, no markdown, no extra text.

USER_SCENARIO:
\"\"\"{user_input}\"\"\"

REQUIREMENTS:
- "score" is an overall ethical score on a 0–10 scale (float).
- "scoring" contains alignment scores per religion on a 0–1 scale (floats). Include at least:
  Hinduism, Islam, Christianity, Sikhism, Buddhism, Judaism.
- "insights.religious.highest"/"lowest" identify the traditions with the highest/lowest alignment,
  with their 0–1 scores.
- "insights.religious.consensus" is a 0–1 value (0=high disagreement, 1=high agreement across traditions).
- "insights.classification.primary_context" is a short label like "Medical", "AI Technology",
  "Education", "Legal", etc. Also provide a small list "scores" with labels and floats.
- "insights.framework_summary" is 1–3 sentences summarizing ethical frameworks relevant here.
- "insights.assessment.concern" and "insights.assessment.recommendation" are concise bullet-style strings.

Return JSON ONLY in this schema (example values shown):

{{
  "score": 2.9,
  "suggestion": "Give a succinct, practical recommendation that respects multiple traditions.",
  "insights": {{
    "religious": {{
      "highest": {{ "tradition": "Hinduism", "score": 0.334 }},
      "lowest":  {{ "tradition": "Judaism",  "score": 0.314 }},
      "consensus": 0.975
    }},
    "classification": {{
      "primary_context": "Medical",
      "scores": [
        {{ "label": "Medical", "score": 0.29 }},
        {{ "label": "AI Technology", "score": 0.17 }}
      ]
    }},
    "framework_summary": "Brief comparison of deontological, consequentialist, virtue, care, justice, etc.",
    "assessment": {{
      "concern": "Concerning: Low ethical alignment across traditions",
      "recommendation": "Major ethical concerns require addressing"
    }}
  }},
}}
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a careful, structured AI ethics evaluator who only outputs valid JSON when asked."},
            {"role": "user", "content": prompt.strip()}
        ],
        "temperature": 0.4,
    }

    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=90)
        if resp.status_code != 200:
            # Keep UI alive with a fallback object
            fallback = _default_payload(user_input)
            fallback["suggestion"] = f"API Error {resp.status_code}: {resp.text}"
            return fallback

        data = resp.json()
        content = data["choices"][0]["message"]["content"]

        json_text = _extract_json_block(content)
        if not json_text:
            fallback = _default_payload(user_input)
            fallback["suggestion"] = "Could not find JSON in the AI response."
            return fallback

        try:
            parsed = json.loads(json_text)
        except Exception as e:
            # Try to repair common trailing commas or single quotes if needed
            repaired = json_text.replace("'", '"')
            repaired = re.sub(r",\s*([}\]])", r"\1", repaired)  # remove trailing commas
            try:
                parsed = json.loads(repaired)
            except Exception:
                fallback = _default_payload(user_input)
                fallback["suggestion"] = f"JSON parse error: {str(e)}"
                return fallback

        # --- Sanity & type checks so the template never breaks ---
        result = _default_payload(user_input)

        # Score 0..10
        result["score"] = _clamp(_coerce_float(parsed.get("score", 0.0)), 0.0, 10.0)

        # Suggestion
        result["suggestion"] = str(parsed.get("suggestion", result["suggestion"]))

        # Insights -> Religious
        insights = parsed.get("insights", {}) or {}
        religious = insights.get("religious", {}) or {}
        highest = religious.get("highest", {}) or {}
        lowest = religious.get("lowest", {}) or {}

        result["insights"]["religious"]["highest"]["tradition"] = str(highest.get("tradition", "—"))
        result["insights"]["religious"]["highest"]["score"] = _clamp(_coerce_float(highest.get("score", 0.0)), 0.0, 1.0)
        result["insights"]["religious"]["lowest"]["tradition"] = str(lowest.get("tradition", "—"))
        result["insights"]["religious"]["lowest"]["score"] = _clamp(_coerce_float(lowest.get("score", 0.0)), 0.0, 1.0)
        result["insights"]["religious"]["consensus"] = _clamp(_coerce_float(religious.get("consensus", 0.0)), 0.0, 1.0)

        # Insights -> Classification
        classification = insights.get("classification", {}) or {}
        result["insights"]["classification"]["primary_context"] = str(classification.get("primary_context", "General"))

        cls_scores_in = classification.get("scores", []) or []
        cls_scores_out: List[Dict[str, Any]] = []
        for s in cls_scores_in:
            try:
                label = str(s.get("label", "Other"))
                score = _coerce_float(s.get("score", 0.0))
                cls_scores_out.append({"label": label, "score": score})
            except Exception:
                continue
        if cls_scores_out:
            result["insights"]["classification"]["scores"] = cls_scores_out

        # Framework + assessment
        result["insights"]["framework_summary"] = str(insights.get("framework_summary", result["insights"]["framework_summary"]))
        assessment = insights.get("assessment", {}) or {}
        result["insights"]["assessment"]["concern"] = str(assessment.get("concern", result["insights"]["assessment"]["concern"]))
        result["insights"]["assessment"]["recommendation"] = str(assessment.get("recommendation", result["insights"]["assessment"]["recommendation"]))

        # Detailed scoring list (for table + pie)
        scoring_in = parsed.get("scoring", []) or []
        scoring_out: List[Dict[str, Any]] = []
        for row in scoring_in:
            try:
                religion = str(row.get("religion", "")).strip() or "Unknown"
                score01 = _clamp(_coerce_float(row.get("score", 0.0)), 0.0, 1.0)
                scoring_out.append({"religion": religion, "score": score01})
            except Exception:
                continue

        # Ensure the six standard traditions exist (even if 0s) so the pie/table render consistently
        required = ["Hinduism", "Islam", "Christianity", "Sikhism", "Buddhism", "Judaism"]
        present = {r["religion"] for r in scoring_out}
        for name in required:
            if name not in present:
                scoring_out.append({"religion": name, "score": 0.0})

        # Deduplicate by keeping the first occurrence
        seen = set()
        deduped = []
        for r in scoring_out:
            if r["religion"] in seen:
                continue
            seen.add(r["religion"])
            deduped.append(r)

        return result

    except Exception as e:
        fallback = _default_payload(user_input)
        fallback["suggestion"] = f"Error: {str(e)}"
        return fallback
