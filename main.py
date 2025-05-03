
import streamlit as st
import time
import google.generativeai as genai
from datetime import datetime, timedelta
import io
import speech_recognition as sr
from pydub import AudioSegment
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(page_title="RoofTop Gardening", layout="wide")

# Apply custom CSS for beautiful background image
st.markdown(
"""
 <style>
 body {
 background-image: url("https://sl.bing.net/df80MIH7xYq");
 background-size: cover;
 background-repeat: no-repeat;
 background-attachment: fixed;
 }
 .stApp {
 padding: 20px;
 border-radius: 10px;
 }
 </style>
 """,
unsafe_allow_html=True
)

# Initialize session state variables
def init_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "water_start_time" not in st.session_state:
        st.session_state.water_start_time = None
    if "fertilizer_start_time" not in st.session_state:
        st.session_state.fertilizer_start_time = None
    if "forum_data" not in st.session_state:
        st.session_state.forum_data = []
    if "replying" not in st.session_state:
        st.session_state.replying = {}

init_session_state()

# Authentication functionality
def login(username, password):
    valid_users = ["sanketh", "nikhil", "karthik", "shiva"]
    if username in valid_users and password == "rooftop":
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.water_start_time = datetime.now()
        st.session_state.fertilizer_start_time = datetime.now()
        return True
    return False

# Calculate progress for timer reminders
def calculate_progress(start_time, total_duration):
    if start_time is None:
        return 0, "Login Required"
    elapsed_time = datetime.now() - start_time
    remaining_time = total_duration - elapsed_time.total_seconds()
    if remaining_time <= 0:
        return 100, "Time to water/fertilize!"
    progress = (elapsed_time.total_seconds() / total_duration) * 100
    return min(progress, 100), f"Time left: {timedelta(seconds=int(remaining_time))}"

# Format datetime for forum posts
def format_datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

# Initialize Gemini AI model
def setup_gemini():
    # Get API key from environment variable or Streamlit secrets
    api_key = None
    
    # First try to get from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    
    # If not found in environment, try Streamlit secrets
    if not api_key and 'GEMINI_API_KEY' in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    
    # If still not found, allow user input (for development/testing only)
    if not api_key:
        api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
        if not api_key:
            st.sidebar.warning("Please enter a valid API key to use the chatbot.")
            return None
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model

# Audio processing function for speech-to-text
def process_audio(audio_file):
    try:
        # Save the uploaded file to a temporary file
        audio_bytes = audio_file.getvalue()
        # Convert the audio to WAV format using pydub
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        wav_audio = io.BytesIO()
        audio.export(wav_audio, format="wav")
        wav_audio.seek(0)
        # Use speech recognition to convert to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_audio) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        return text
    except Exception as e:
        st.error(f"Error processing audio: {e}")
        return None

# Main application UI
def main():
    # Layout for Reminders and Login Form
    col1, col2 = st.columns([3, 1])
    
    # Reminders in the Left Column
    with col1:
        st.write("🌿 Reminders")
        water_progress, water_message = calculate_progress(st.session_state.water_start_time, 24 * 3600) # 24 hours
        fertilizer_progress, fertilizer_message = calculate_progress(st.session_state.fertilizer_start_time, 48 * 3600) # 48 hours
        
        # Display dynamic updates
        water_placeholder = st.empty()
        fertilizer_placeholder = st.empty()
        water_placeholder.progress(water_progress / 100)
        water_placeholder.write(f"💧 Water Reminder: {water_message}")
        fertilizer_placeholder.progress(fertilizer_progress / 100)
        fertilizer_placeholder.write(f"🌱 Fertilizer Reminder: {fertilizer_message}")
    
    # Login Form in the Right Column
    with col2:
        if st.session_state.logged_in:
            st.success(f"Welcome, {st.session_state.username}!")
        else:
            with st.expander("🔑 Login"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", placeholder="Enter your password", type="password")
                login_button = st.button("Login")
                if login_button:
                    if login(username, password):
                        st.success(f"Welcome, {username}!")
                        st.rerun()
                    else:
                        st.error("Login unsuccessful. Please check your credentials.")
    
    # Sidebar Navigation
    st.sidebar.title("🌿 Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Chatbot", "Prompts", "Forum"])
    
    # Page content based on selection
    if page == "Home":
        render_home_page()
    elif page == "Chatbot":
        render_chatbot_page()
    elif page == "Prompts":
        render_prompts_page()
    elif page == "Forum":
        render_forum_page()

# Home Page Content
def render_home_page():
    st.title("🌿 Welcome to Our RoofTop Gardening Web App!")
    st.markdown("""
     RoofTop gardening transforms underutilized rooftop spaces into thriving green areas.
     This web app serves as your **go-to guide** for starting and maintaining a **cost-effective, sustainable** garden right on your terrace.
     With easy-to-follow tips and expert recommendations, you can enjoy **fresh, organic produce** while contributing to a greener environment.
     """)
    st.header("🌱 Why RoofTop Gardening?")
    st.markdown("""
     - **Utilize Your Space:** Convert rooftops into lush gardens.
     - **Grow Fresh & Organic:** Enjoy pesticide-free, home-grown produce.
     - **Cost-Effective Solutions:** Gardening tips that don't break the bank.
     - **Health & Well-being:** Gardening reduces stress and promotes a healthier lifestyle.
     - **Eco-Friendly Choice:** Green spaces help lower urban heat and improve air quality.
     """)
    st.header("🚀 What You'll Find Here")
    st.markdown("""
     ✅ **Step-by-step gardening guides** ✅ **Best plants for rooftop gardening** ✅ **DIY solutions for low-cost gardening** ✅ **Organic farming techniques** ✅ **Community & expert advice** """)
    st.info("🌍 Start your RoofTop gardening journey today and make a positive impact on your health and the environment!")

# Chatbot Page Content
def render_chatbot_page():
    st.title("🤖 Gardening Assistant Chatbot")
    st.markdown("Ask anything about **RoofTop gardening** and get instant responses powered by **Gemini Flash 2 AI**!")
    
    try:
        model = setup_gemini()
        if model:
            # Chat input options - text or audio
            input_method = st.radio("Choose input method:", ["Text", "Audio"])
            user_input = ""
            
            if input_method == "Text":
                user_input = st.text_area("Type your question here...", height=100)
            else:
                st.write("### 🎤 Upload Audio")
                audio_file = st.file_uploader("Upload an audio file to ask your question", type=["mp3", "wav", "ogg"])
                
                if audio_file is not None:
                    st.audio(audio_file, format="audio/*")
                    if st.button("Transcribe Audio"):
                        with st.spinner("Transcribing audio..."):
                            user_input = process_audio(audio_file)
                            if user_input:
                                st.success("Transcription successful!")
                                st.write(f"Your question: {user_input}")
                            else:
                                st.error("Could not transcribe audio. Please try again.")
            
            # Generate response
            if st.button("Generate Response 🌿"):
                if user_input:
                    with st.spinner("Thinking... 💡"):
                        try:
                            response = model.generate_content(user_input)
                            st.subheader("🤖 AI Response:")
                            st.markdown(f"**{response.text}**")
                        except Exception as e:
                            st.error(f"⚠️ Error: Could not process your request. {e}")
                else:
                    st.warning("⚠️ Please enter a question before submitting.")
        else:
            st.warning("⚠️ API key not configured. Please set up your API key to use the chatbot.")
    except Exception as e:
        st.error(f"⚠️ Error initializing the Chatbot: {e}. Please ensure your Gemini API key is correctly set.")

# Prompts Page Content
def render_prompts_page():
    st.title("📝 RoofTop Gardening Prompts")
    st.markdown("Explore a comprehensive list of prompts to guide your rooftop gardening journey.")
    
    # Prompts categories and expandable sections
    categories = {
        "🌿 How to Design Rooftop Gardening": [
            "How to Design Rooftop Gardening",
            "What are the key considerations for designing a rooftop garden?",
            "How can I create a layout for my rooftop garden?",
            "What types of containers are best for rooftop gardening?",
            "How do I choose the right plants for my rooftop garden design?",
            "What are the best materials for building raised beds on a rooftop?",
            "How can I incorporate vertical gardening into my rooftop design?",
            "What are some creative ways to use space in a small rooftop garden?",
            "How can I design a rooftop garden that is aesthetically pleasing?",
            "What are the best practices for ensuring proper drainage in a rooftop garden?",
            "How can I create shaded areas in my rooftop garden?"
         ],
        "🌱 Which Crops to Grow in Which Season": [
            "What vegetables can I grow in the spring on my rooftop?",
            "Which herbs thrive in summer rooftop gardens?",
            "What are the best fall crops for rooftop gardening?",
            "How can I grow winter vegetables in a rooftop garden?",
            "What are the best fruits to grow in a rooftop garden by season?",
            "How do I choose companion plants for my rooftop garden?",
            "What are the best crops for container gardening on rooftops?",
            "How can I extend the growing season in my rooftop garden?",
            "What are the best microgreens to grow indoors or on a rooftop?",
            "How do seasonal changes affect plant selection for rooftop gardens?"
         ],
        "🌿 Proper Manure and Preparation Methods": [
            "What types of manure are best for rooftop gardening?",
            "How do I prepare manure for use in my rooftop garden?",
            "What is the difference between compost and manure?",
            "How can I make my own organic manure at home?",
            "What are the benefits of using manure in rooftop gardening?",
            "How do I apply manure to my rooftop garden?",
            "What is the proper ratio of manure to soil for container gardening?",
            "How can I tell if my manure is ready for use?",
            "What precautions should I take when using manure in my garden?",
            "How can I store manure safely for future use?"
         ],
        "💧 Techniques for Manure and Water Management": [
            "What are the best techniques for composting on a rooftop?",
            "How can I integrate rainwater harvesting into my rooftop garden?",
            "What are the benefits of using drip irrigation in rooftop gardening?",
            "How do I set up a simple irrigation system for my rooftop garden?",
            "What are the best practices for watering plants in containers?",
            "How can I use greywater in my rooftop garden?",
            "What are the signs of overwatering in rooftop plants?",
            "How can I create a self-watering system for my rooftop garden?",
            "What are the best times of day to water rooftop plants?",
            "How can I prevent water runoff from my rooftop garden?"
         ],
        "🐛 Pest Management in Rooftop Gardens": [
            "What are common pests in rooftop gardens and how can I manage them?",
            "How can I use companion planting to deter pests?",
            "What natural pest control methods are effective for rooftop gardens?",
            "How do I identify signs of pest infestations in my plants?",
            "What are the best organic pesticides for rooftop gardening?",
            "How can I attract beneficial insects to my rooftop garden?",
            "What are the best practices for maintaining plant health to prevent pests?",
            "How can I create barriers to protect my rooftop garden from pests?",
            "What role do birds play in pest management on rooftops?",
            "How can I use traps to control pests in my rooftop garden?"
         ]
     }
    
    # Display prompts in expandable sections
    for category, prompts in categories.items():
        with st.expander(category):
            for i, prompt in enumerate(prompts, 1):
                st.markdown(f"{i}. {prompt}")
    
    # Additional categories (collapsed by default)
    with st.expander("View More Categories"):
        st.header("🌱 Soil Preparation and Maintenance")
        st.header("🌍 Sustainable Practices in Rooftop Gardening")
        st.header("🍂 Seasonal Care and Maintenance")
        st.header("👥 Community and Education")
        st.header("🚀 Innovations in Rooftop Gardening")
        st.info("Click on any category above to see specific prompts")

# Forum Page Content
def render_forum_page():
    st.title("💬 Community Forum")
    st.markdown("Engage with fellow gardening enthusiasts, ask questions, and share experiences.")
    
    # Form to submit a new discussion
    with st.form(key="forum_form"):
        user_name = st.text_input("Your Name", placeholder="Enter your name")
        post_content = st.text_area("Share your thoughts or ask a question...", height=100)
        submit_button = st.form_submit_button("Post")
        
        if submit_button and user_name and post_content:
            timestamp = datetime.now()
            new_post = {"user": user_name, "content": post_content, "replies": [], "timestamp": timestamp}
            st.session_state.forum_data.append(new_post)
            st.success("✅ Your post has been added!")
            st.rerun()
    
    st.write("### 🌿 Community Discussions")
    if st.session_state.forum_data:
        for idx, post in enumerate(st.session_state.forum_data):
            with st.container():
                st.markdown(f"**📝 {post['user']} says:**")
                st.info(post["content"])
                st.caption(f"Posted on: {format_datetime(post['timestamp'])}")
                
                # Reply button to toggle reply form
                reply_key = f"reply_button_{idx}"
                if st.button("Reply", key=reply_key):
                    st.session_state.replying[idx] = not st.session_state.replying.get(idx, False)
                    st.rerun()
                
                # Display reply form if the reply button is clicked
                if st.session_state.replying.get(idx, False):
                    with st.form(key=f"reply_form_{idx}"):
                        reply_name = st.text_input("Your Name", placeholder="Enter your name", key=f"reply_name_{idx}")
                        reply_content = st.text_area("Your Reply...", height=50, key=f"reply_content_{idx}")
                        reply_submit_button = st.form_submit_button("Submit Reply")
                        
                        if reply_submit_button and reply_name and reply_content:
                            reply_timestamp = datetime.now()
                            new_reply = {"user": reply_name, "content": reply_content, "timestamp": reply_timestamp}
                            st.session_state.forum_data[idx]["replies"].append(new_reply)
                            st.session_state.replying[idx] = False
                            st.success("✅ Your reply has been added!")
                            st.rerun()
                
                # Display replies
                if post["replies"]:
                    st.write("**Replies:**")
                    for reply in post["replies"]:
                        st.markdown(f"**🗨️ {reply['user']} replied:**")
                        st.info(reply["content"])
                        st.caption(f"Replied on: {format_datetime(reply['timestamp'])}")
    else:
        st.info("No discussions yet. Be the first to start a conversation!")

if __name__ == "__main__":
    main()
