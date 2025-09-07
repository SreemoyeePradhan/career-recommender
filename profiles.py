# profiles.py
import os
import json

PROFILE_FILE = "profiles.json"


def load_profiles():
    """Load all profiles from JSON file safely."""
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                profiles = json.load(f)

                # Ensure backward compatibility: add "language" if missing
                for profile in profiles.values():
                    if "language" not in profile:
                        profile["language"] = "English"
                return profiles
        except json.JSONDecodeError:
            return {}
    return {}


def save_profiles(profiles):
    """Save all profiles to JSON file."""
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2)


def create_profile(profiles, name, education="", interests=None, strengths=None, goal="", language="English"):
    """Create a new profile and return updated dict."""
    if not name.strip():
        return profiles

    profiles[name] = {
        "name": name,
        "education": education,
        "interests": interests or [],
        "strengths": strengths or [],
        "goal": goal,
        "chat_history": [],
        "language": language,  # ✅ New field
    }
    save_profiles(profiles)
    return profiles
