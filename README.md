# AmbitionBot – AI-Powered Career Guidance Chatbot

**AmbitionBot** is an AI-powered, personalized career guidance chatbot that acts as a one-stop solution for all career-related needs. It helps users explore career paths, identify skill gaps, get resource recommendations, and plan actionable roadmaps to achieve their professional goals.

---

## 🌟 Features

- Personalized career guidance based on user profile (education, interests, strengths, goals).  
- Skill gap analysis to identify missing or underdeveloped skills.  
- Actionable resource recommendations (courses, books, websites, mentors).  
- Interactive 12-week or custom roadmap visualization.  
- Multilingual support (English, German, Hindi) for both prompts and responses. (As of now, prompts can be given in any language based on individual preference. However the bot replies in English.)
- User profile management:
  - Create, save, and switch between multiple profiles.
  - Delete profiles when needed.  
- Conversational chat interface with mentor-style responses.  
- Automatic translation fallback if AI outputs in a different language.  
- Dark/Light mode for better readability.  

---

## 🛠️ Tech Stack & Libraries

- **Frontend:** Streamlit  
- **Backend / AI:** Google Gemini API (Generative AI model)  
- **Visualization:** Plotly (roadmap and resource charts)  
- **Data Storage:** JSON files for user profiles  
- **Python Libraries:**  
  - `google-generativeai` – for AI-powered career guidance  
  - `streamlit` – web application interface  
  - `plotly` – charts and visualizations  
  - `deep_translator` – translation of text into selected language  

---

## ⚙️ How It Works

1. **User Profile Creation:**  
   - On first visit, the user creates a profile with their name, education, interests, strengths, and career goal.  
   - Multiple profiles can be managed simultaneously.  

2. **Chat Interaction:**  
   - Users can type questions or requests regarding careers, skill gaps, or learning resources.  
   - Users can select their preferred language (English, German, Hindi).  

3. **AI Response:**  
   - AmbitionBot generates personalized responses using the Gemini AI model.  
   - Skill gaps and resource recommendations are returned as both text and interactive visual roadmaps.  
   - If AI output is in English but the user prefers another language, AmbitionBot automatically translates it.  

4. **Visual Roadmap:**  
   - Skill gaps or recommended resources are displayed as horizontal charts for clear visualization.  

5. **Profile Management:**  
   - Users can create new profiles, switch between profiles, or delete profiles from the sidebar.  

---

## 🚀 How to Use

1. Visit the application and create a new profile with your career details.  
2. Type a question or request in the chat input (e.g., "What skills do I need for a data scientist role?").  
3. Choose your preferred language for responses.  
4. View personalized guidance, skill gap analysis, or resource recommendations.  
5. Repeat the process as needed for continuous career planning.  

---

**AmbitionBot** simplifies career planning by combining AI-powered guidance, multilingual support, and interactive visualizations — all in one platform!
