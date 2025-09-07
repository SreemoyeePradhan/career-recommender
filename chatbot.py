import google.generativeai as genai
import os
import json
import plotly.graph_objects as go

SYSTEM_PROMPT = """
You are a warm, empathetic career guidance coach.
Always personalise responses by:
- Referring to the user by their name
- Connecting advice to their education, interests, and strengths
- Giving encouragement and motivation
- Providing actionable next steps
"""

class CareerChatbot:
    def __init__(self, api_key: str, model: str = "models/gemini-1.5-flash"):
        if not api_key:
            raise ValueError("Google API key missing. Set GOOGLE_API_KEY in environment.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def build_conversation_context(
        self, profile: dict, messages: list,
        mentor_mode: bool = True, task: str = None, language: str = "English"
    ) -> str:
        """Build prompt with system prompt, profile info, and recent conversation."""
        profile_text = f"""
User Profile:
Name: {profile.get('name')}
Education: {profile.get('education')}
Interests: {', '.join(profile.get('interests', []))}
Strengths: {', '.join(profile.get('strengths', []))}
Goal: {profile.get('goal')}
"""
        history = "\n".join([f"{m['role'].title()}: {m['content']}" for m in messages[-6:]]) if messages else "No prior conversation."

        style_instruction = (
            "Provide a warm, detailed, mentor-like response with encouragement."
            if mentor_mode else "Provide a short, direct answer."
        )

        task_instruction = ""
        if task == "skill_gap":
            task_instruction = """
Focus on identifying the **skill gaps** between the user's current strengths/education and their career goal.
Return both:
1. A short mentor-style explanation.
2. A JSON object like:
{
 "Skill A": "Gap level or missing detail",
 "Skill B": "Gap level or missing detail"
}
"""
        elif task == "resources":
            task_instruction = """
Recommend practical **resources** (courses, books, websites, mentors) to fill gaps.
Return both:
1. A short mentor-style explanation.
2. A JSON object like:
{
 "Week 1": "Resource A",
 "Week 2": "Resource B",
 ...
}
"""

        return f"""{SYSTEM_PROMPT}

{profile_text}

Conversation so far:
{history}

Task: {task_instruction}

Language: Respond in {language}.

Now continue the conversation.
{style_instruction}
"""

    def _force_translate(self, text: str, target_lang: str) -> str:
        """Forcefully translate text to target language, ignoring JSON blocks."""
        if target_lang.lower() == "english":
            return text  # no need to translate

        # Separate JSON (if any) from text
        json_part = ""
        if "{" in text and "}" in text:
            try:
                start = text.find("{")
                end = text.rfind("}") + 1
                json_part = text[start:end]
                text = text[:start] + text[end:]
            except Exception:
                pass

        # Strict translation step
        translate_prompt = f"""
You are a professional translator.
Translate ONLY the following text into {target_lang}.
Do NOT add explanations.
Do NOT output anything other than the translated text.
Keep emojis and formatting intact.

Text to translate:
{text}
"""
        try:
            response = self.model.generate_content(translate_prompt)
            translated_text = response.text.strip()
        except Exception:
            translated_text = text  # fallback

        # Recombine translated text + untouched JSON
        return translated_text + ("\n\n" + json_part if json_part else "")

    def get_reply(
        self, profile: dict, messages: list, mentor_mode: bool = True,
        return_json_roadmap: bool = False, task: str = None, language: str = "English"
    ) -> dict:
        """
        Generates a reply using Gemini, optionally extracting roadmap JSON.
        Returns: {"text": str, "roadmap": dict or None, "task": str or None}
        """
        prompt = self.build_conversation_context(profile, messages, mentor_mode, task, language)
        response = self.model.generate_content(prompt)
        text = response.text.strip()

        roadmap = None
        if return_json_roadmap and "{" in text and "}" in text:
            try:
                start = text.find("{")
                end = text.rfind("}") + 1
                roadmap_json = text[start:end]
                roadmap = json.loads(roadmap_json)
            except Exception:
                roadmap = None

        # Ensure final output is in the selected language
        final_text = self._force_translate(text, language)

        return {"text": final_text, "roadmap": roadmap, "task": task}


# ------------------- Helpers for Visualization -------------------

def generate_roadmap_chart(roadmap, task="skill_gap"):
    """Generate a horizontal roadmap chart for skills or resources."""
    weeks = list(roadmap.keys())

    fig = go.Figure()

    for i, week in enumerate(weeks):
        items = roadmap[week]

        # If it's a list of dicts (resource recommendations), stringify nicely
        if isinstance(items, list) and all(isinstance(x, dict) for x in items):
            res_texts = [
                f"Topic: {x.get('Topic','')}\nResource: {x.get('Resource','')}\nAction: {x.get('Action','')}"
                for x in items
            ]
        # If it's a simple list of strings (skill gap tasks)
        elif isinstance(items, list):
            res_texts = [str(x) for x in items]
        # Single value
        else:
            res_texts = [str(items)]

        # Add bars for each item in that week
        for res in res_texts:
            fig.add_trace(go.Bar(
                x=[1], y=[week], orientation="h",
                text=res, textposition="auto", marker_color="lightgreen"
            ))

    fig.update_layout(
        title="📊 Career Roadmap" if task == "skill_gap" else "📚 Resource Plan",
        xaxis=dict(showticklabels=False),
        yaxis=dict(title="Weeks"),
        height=400 + 30 * len(weeks)
    )
    return fig
