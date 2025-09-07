# ui.py
import streamlit as st
from profiles import save_profiles
from chatbot import generate_roadmap_chart

# ------------------- Profile Sidebar -------------------
def sidebar_profile_manager(profiles, active_profile):
    """Sidebar UI for managing profiles."""
    st.sidebar.title("👤 Profile Manager")

    profile_names = list(profiles.keys())
    selected_profile = st.sidebar.selectbox("Select Profile", ["-- None --"] + profile_names)

    if selected_profile != "-- None --":
        active_profile = selected_profile

    # --- Delete Profile Button ---
    if active_profile:
        if st.sidebar.button("🗑️ Delete Profile"):
            profiles.pop(active_profile)
            save_profiles(profiles)
            st.sidebar.success(f"Profile '{active_profile}' deleted!")
            active_profile = None

    with st.sidebar.expander("➕ Create New Profile"):
        new_name = st.text_input("Profile Name")
        education = st.text_input("Education")
        interests = st.text_area("Interests (comma separated)")
        strengths = st.text_area("Strengths (comma separated)")
        goal = st.text_area("Career Goal")
        language = st.selectbox(
            "Preferred Language",
            ["English", "Hindi", "Spanish", "French", "German"],
            index=0
        )

        if st.button("Save Profile"):
            if new_name.strip():
                profiles[new_name] = {
                    "name": new_name,
                    "education": education,
                    "interests": [i.strip() for i in interests.split(",") if i.strip()],
                    "strengths": [s.strip() for s in strengths.split(",") if s.strip()],
                    "goal": goal,
                    "language": language,
                    "chat_history": [],
                }
                save_profiles(profiles)
                st.success(f"Profile '{new_name}' created!")

    return profiles, active_profile


# ------------------- Main Chat UI -------------------
def render_chat_ui(profile, chatbot, mentor_mode):
    """Main chat area for conversation with visual roadmap integration."""

    # Dark/Light Theme
    dark_mode = st.session_state.get("dark_mode", True)
    user_bg = "#DCF8C6" if dark_mode else "#E1FFC7"
    user_color = "#000000"
    bot_bg = "#1E1E1E" if dark_mode else "#F1F0F0"
    bot_color = "#FFFFFF" if dark_mode else "#000000"
    theme_bg = "#121212" if dark_mode else "#FFFFFF"

    # Custom CSS
    st.markdown(
        f"""
        <style>
        .user-bubble {{
            background-color: {user_bg};
            color: {user_color};
            padding: 10px; border-radius: 16px; margin: 5px 0;
            text-align: right; max-width: 75%; float: right; clear: both;
        }}
        .bot-bubble {{
            background-color: {bot_bg};
            color: {bot_color};
            padding: 10px; border-radius: 16px; margin: 5px 0;
            text-align: left; max-width: 75%; float: left; clear: both;
        }}
        .chat-container {{
            background-color: {theme_bg};
            padding: 10px; border-radius: 10px; height: 500px; overflow-y: auto;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🎯 Personalized Career Guidance Chatbot")
    st.subheader(f"💡 Active Profile: {profile['name']} ({profile.get('language', 'English')})")

    # Chat Container
    chat_container = st.container()
    with chat_container:
        for msg in profile["chat_history"]:
            bubble_class = "user-bubble" if msg["role"] == "user" else "bot-bubble"
            st.markdown(f"<div class='{bubble_class}'>{msg['content']}</div>", unsafe_allow_html=True)
            if msg.get("roadmap"):
                fig = generate_roadmap_chart(msg["roadmap"], task=msg.get("task"))
                if fig:
                    st.plotly_chart(fig, use_container_width=True)

    # Chat Input
    if prompt := st.chat_input("Ask about careers, skills, or roadmaps..."):
        profile["chat_history"].append({"role": "user", "content": prompt})
        save_profiles(st.session_state.profiles)

        with chat_container:
            st.markdown(f"<div class='user-bubble'>{prompt}</div>", unsafe_allow_html=True)

        with st.spinner("Thinking..."):
            reply_result = chatbot.get_reply(
                profile=profile,
                messages=profile["chat_history"],
                mentor_mode=mentor_mode,
                return_json_roadmap=True
            )

        text_reply = reply_result["text"]
        roadmap_data = reply_result.get("roadmap")

        with chat_container:
            st.markdown(f"<div class='bot-bubble'>{text_reply}</div>", unsafe_allow_html=True)
            if roadmap_data:
                fig = generate_roadmap_chart(roadmap_data, task=reply_result.get("task"))
                if fig:
                    st.plotly_chart(fig, use_container_width=True)

        chat_entry = {"role": "assistant", "content": text_reply}
        if roadmap_data:
            chat_entry["roadmap"] = roadmap_data
            chat_entry["task"] = reply_result.get("task")
        profile["chat_history"].append(chat_entry)

        save_profiles(st.session_state.profiles)
        st.rerun()
