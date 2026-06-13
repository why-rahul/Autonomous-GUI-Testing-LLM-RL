import json
from llm.ollama_client import query_llm


def generate_test_plan(user_input, html=None):

    # 🔥 If HTML available → smarter prompt
    if html:
        prompt = f"""
You are an expert UI testing agent.

TASK:
Generate a test plan using REAL HTML.

RULES:
- Output ONLY valid JSON list
- No explanation
- Use VALID XPath from given HTML
- Steps: open_url, type, click, verify

HTML:
{html[:8000]}

USER REQUEST:
{user_input}

OUTPUT FORMAT:
[
  {{"action": "open_url", "target": "login_page", "value": ""}},
  {{"action": "type", "target": "//input[@name='username']", "value": "Admin"}},
  {{"action": "type", "target": "//input[@name='password']", "value": "admin123"}},
  {{"action": "click", "target": "//button[@type='submit']", "value": ""}},
  {{"action": "verify", "target": "dashboard", "value": ""}}
]
"""
    else:
        # fallback
        prompt = f"""
Generate UI test steps in JSON.
Instruction: {user_input}
"""

    response = query_llm(prompt)

    try:
        start = response.find("[")
        end = response.rfind("]") + 1
        json_str = response[start:end]

        plan = json.loads(json_str)

        cleaned_plan = []
        for step in plan:
            cleaned_plan.append({
                "action": step.get("action", "").strip(),
                "target": step.get("target", "").strip(),
                "value": step.get("value", "").strip()
            })

        return cleaned_plan

    except Exception as e:
        print("❌ Parsing Error:", e)
        print("RAW:", response)
        return None