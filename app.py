# app.py
import os
import streamlit as st
from dotenv import load_dotenv
from chatbot import CareerChatbot
from profiles import load_profiles, save_profiles
from ui import sidebar_profile_manager, render_chat_ui

# ------------------ Config ------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
st.set_page_config(page_title="Career Guidance Bot", page_icon="🎯", layout="wide")

# ------------------ Init State ------------------
if "profiles" not in st.session_state:
    st.session_state.profiles = load_profiles()
if "active_profile" not in st.session_state:
    st.session_state.active_profile = None
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

chatbot = CareerChatbot(api_key=API_KEY)

# ------------------ Sidebar ------------------
st.sidebar.title("🧑‍🏫 Mentor Settings")
mentor_style = st.sidebar.selectbox(
    "Choose Mentor Style:",
    ["Supportive Mentor", "Strict Coach", "Practical Advisor"],
    index=0
)

st.sidebar.header("🎨 Theme")
if st.sidebar.button("Toggle Dark/Light Mode"):
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()

st.session_state.profiles, st.session_state.active_profile = sidebar_profile_manager(
    st.session_state.profiles, st.session_state.active_profile
)

# ------------------ Skill Gap & Resources ------------------
if st.session_state.active_profile:
    profile = st.session_state.profiles[st.session_state.active_profile]

    st.sidebar.header("🎯 Career Insights")
    if st.sidebar.button("🔍 Skill Gap Analysis"):
        result = chatbot.get_reply(
            profile, profile["chat_history"], mentor_mode=True,
            return_json_roadmap=True, task="skill_gap"
        )
        chat_entry = {"role": "assistant", "content": result["text"]}
        if result.get("roadmap"):
            chat_entry["roadmap"] = result["roadmap"]
            chat_entry["task"] = "skill_gap"
        profile["chat_history"].append(chat_entry)
        save_profiles(st.session_state.profiles)
        st.success("Skill Gap Analysis added to chat!")

    if st.sidebar.button("📚 Resource Recommendations"):
        result = chatbot.get_reply(
            profile, profile["chat_history"], mentor_mode=True,
            return_json_roadmap=True, task="resources"
        )
        chat_entry = {"role": "assistant", "content": result["text"]}
        if result.get("roadmap"):
            chat_entry["roadmap"] = result["roadmap"]
            chat_entry["task"] = "resources"
        profile["chat_history"].append(chat_entry)
        save_profiles(st.session_state.profiles)
        st.success("Resource Recommendations added to chat!")

# ------------------ Main Chat ------------------
if st.session_state.active_profile:
    profile = st.session_state.profiles[st.session_state.active_profile]
    render_chat_ui(profile, chatbot, mentor_mode=True)
else:
    st.info("Please select or create a profile to start chatting.")
