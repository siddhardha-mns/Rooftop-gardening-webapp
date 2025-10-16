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

# Add animations function
def add_animations():
    st.markdown(
    """
    <style>
    /* Import Google Fonts for modern look */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    body {
        background-image: linear-gradient(rgba(34,197,94,0.10), rgba(34,197,94,0.10)), url("https://images.unsplash.com/photo-1501004318641-b39e6451bec6?q=80&w=1600&auto=format&fit=crop");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        overflow-x: hidden;
    }
    
    .stApp {
        padding: 20px;
        border-radius: 10px;
        backdrop-filter: blur(8px);
    }
    
    /* Modern card-like sections */
    .element-container {
        animation: fadeInUp 0.6s ease-out forwards;
        opacity: 0;
    }
    
    /* Heading Animations */
    h1, h2, h3 { 
        color: #16a34a !important;
        animation: popIn 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
        opacity: 0;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    
    h1 {
        animation-delay: 0.2s;
        font-size: 2.5rem !important;
    }
    
    h2 {
        animation-delay: 0.4s;
        font-size: 2rem !important;
    }
    
    h3 {
        animation-delay: 0.6s;
        font-size: 1.5rem !important;
    }
    
    /* Paragraph text animations */
    p, .stMarkdown, .stInfo, .stSuccess, .stWarning {
        animation: fadeInUp 0.8s ease-out forwards;
        animation-delay: 0.8s;
        opacity: 0;
    }
    
    /* Button hover effects */
    .stButton>button {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: #ffffff;
        border: 0;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px -1px rgba(34, 197, 94, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -5px rgba(34, 197, 94, 0.5);
    }
    
    .stButton>button:hover:before {
        left: 100%;
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Input fields modern styling */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        border: 2px solid rgba(34, 197, 94, 0.2) !important;
        border-radius: 12px !important;
        padding: 12px !important;
        transition: all 0.3s ease !important;
        background: rgba(255, 255, 255, 0.9) !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #22c55e !important;
        box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1) !important;
        transform: scale(1.01);
    }
    
    /* Sidebar modern styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(240,253,244,0.95) 100%);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(34, 197, 94, 0.2);
    }
    
    section[data-testid="stSidebar"] .stRadio > label {
        font-weight: 600;
        color: #16a34a;
    }
    
    /* Links */
    a { 
        color: #16a34a !important;
        text-decoration: none;
        position: relative;
        transition: color 0.3s ease;
    }
    
    a:hover {
        color: #15803d !important;
    }
    
    a:after {
        content: '';
        position: absolute;
        width: 0;
        height: 2px;
        bottom: -2px;
        left: 0;
        background-color: #16a34a;
        transition: width 0.3s ease;
    }
    
    a:hover:after {
        width: 100%;
    }
    
    /* Falling Leaves Container */
    .leaves-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: 1;
        overflow: hidden;
    }
    
    /* Individual Leaf Styling */
    .leaf {
        position: absolute;
        top: -50px;
        font-size: 24px;
        opacity: 0.7;
        animation: fall linear infinite;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }
    
    /* Different leaf animations for variety */
    .leaf:nth-child(1) {
        left: 10%;
        animation-duration: 12s;
        animation-delay: 0s;
        font-size: 28px;
    }
    
    .leaf:nth-child(2) {
        left: 25%;
        animation-duration: 15s;
        animation-delay: 2s;
        font-size: 22px;
    }
    
    .leaf:nth-child(3) {
        left: 40%;
        animation-duration: 18s;
        animation-delay: 4s;
        font-size: 26px;
    }
    
    .leaf:nth-child(4) {
        left: 55%;
        animation-duration: 14s;
        animation-delay: 1s;
        font-size: 24px;
    }
    
    .leaf:nth-child(5) {
        left: 70%;
        animation-duration: 16s;
        animation-delay: 3s;
        font-size: 20px;
    }
    
    .leaf:nth-child(6) {
        left: 85%;
        animation-duration: 13s;
        animation-delay: 5s;
        font-size: 25px;
    }
    
    .leaf:nth-child(7) {
        left: 15%;
        animation-duration: 17s;
        animation-delay: 6s;
        font-size: 23px;
    }
    
    .leaf:nth-child(8) {
        left: 60%;
        animation-duration: 19s;
        animation-delay: 7s;
        font-size: 21px;
    }
    
    /* Keyframe Animations */
    @keyframes fall {
        0% {
            top: -50px;
            transform: translateX(0) rotate(0deg);
            opacity: 0.7;
        }
        25% {
            transform: translateX(20px) rotate(90deg);
            opacity: 0.8;
        }
        50% {
            transform: translateX(-20px) rotate(180deg);
            opacity: 0.6;
        }
        75% {
            transform: translateX(15px) rotate(270deg);
            opacity: 0.7;
        }
        100% {
            top: 110vh;
            transform: translateX(-10px) rotate(360deg);
            opacity: 0.3;
        }
    }
    
    @keyframes popIn {
        0% {
            opacity: 0;
            transform: scale(0.8) translateY(20px);
        }
        50% {
            transform: scale(1.05) translateY(-5px);
        }
        100% {
            opacity: 1;
            transform: scale(1) translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        0% {
            opacity: 0;
            transform: translateY(30px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Card-like containers */
    .stContainer {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .stContainer:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    
    /* Expander modern styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(22, 163, 74, 0.1) 100%);
        border-radius: 12px;
        border: 2px solid rgba(34, 197, 94, 0.2);
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(22, 163, 74, 0.2) 100%);
        border-color: #22c55e;
    }
    
    /* Info, Success, Warning boxes */
    .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 12px;
        padding: 1rem 1.5rem;
        border-left: 4px solid;
    }
    
    /* Smooth page transitions */
    .main .block-container {
        animation: pageLoad 0.5s ease-out;
    }
    
    @keyframes pageLoad {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Form styling */
    .stForm {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.1);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #22c55e 0%, #16a34a 100%);
        border-radius: 10px;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        h1 {
            font-size: 1.8rem !important;
        }
        
        h2 {
            font-size: 1.5rem !important;
        }
        
        .leaf {
            font-size: 18px;
        }
    }
    </style>
    
    <!-- Falling Leaves HTML -->
    <div class="leaves-container">
        <div class="leaf">🍃</div>
        <div class="leaf">🍂</div>
        <div class="leaf">🍃</div>
        <div class="leaf">🌿</div>
        <div class="leaf">🍂</div>
        <div class="leaf">🍃</div>
        <div class="leaf">🌿</div>
        <div class="leaf">🍂</div>
    </div>
    
    <script>
    // Add staggered animation delays to elements
    document.addEventListener('DOMContentLoaded', function() {
        const elements = document.querySelectorAll('.element-container');
        elements.forEach((el, index) => {
            el.style.animationDelay = (index * 0.1) + 's';
        });
    });
    </script>
    """,
    unsafe_allow_html=True
    )

# Call animations at the start
add_animations()

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
    if "cart" not in st.session_state:
        st.session_state.cart = []
    if "supabase_user" not in st.session_state:
        st.session_state.supabase_user = None
    if "supabase_session" not in st.session_state:
        st.session_state.supabase_session = None

init_session_state()

# Supabase client setup (cached)
try:
    from supabase import create_client, Client
except Exception:
    create_client = None
    Client = None

def _get_secret(name):
    try:
        if hasattr(st, "secrets") and name in st.secrets:
            return st.secrets.get(name)
    except Exception:
        return None
    return None

def get_supabase():
    url = os.getenv("SUPABASE_URL") or _get_secret("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY") or _get_secret("SUPABASE_ANON_KEY")
    if not url or not key or not create_client:
        return None
    if "_supabase_client" not in st.session_state:
        st.session_state._supabase_client = create_client(url, key)
    return st.session_state._supabase_client

# Supabase Auth helpers
def is_authenticated():
    return st.session_state.supabase_user is not None and st.session_state.supabase_session is not None

def supabase_login_ui():
    st.title("🔐 Sign in to RoofTop Gardening")
    st.caption("Please sign in or create an account to continue.")
    mode = st.radio("", ["Sign In", "Sign Up"], horizontal=True)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    sb = get_supabase()
    if not sb:
        st.error("Supabase is not configured. Set SUPABASE_URL and SUPABASE_ANON_KEY in .env or secrets.")
        return
    col_a, col_b = st.columns([1,1])
    with col_a:
        if st.button(mode):
            if not email or not password:
                st.warning("Enter email and password.")
                return
            try:
                if mode == "Sign In":
                    res = sb.auth.sign_in_with_password({"email": email, "password": password})
                else:
                    res = sb.auth.sign_up({"email": email, "password": password})
                user = getattr(res, "user", None) or getattr(res, "session", {}).get("user")
                session = getattr(res, "session", None)
                if not session:
                    st.info("Check your email to confirm your account, then sign in.")
                    return
                st.session_state.supabase_user = user
                st.session_state.supabase_session = session
                st.success("Signed in successfully.")
                st.rerun()
            except Exception as e:
                st.error(f"Auth error: {e}")
    with col_b:
        if st.button("Forgot password?"):
            st.info("Password recovery must be handled via Supabase auth flows (magic links).")

    st.divider()
    st.caption("By continuing, you agree to our Terms and Privacy Policy.")

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
    api_key = os.getenv("GEMINI_API_KEY") or _get_secret("GEMINI_API_KEY")
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
        audio_bytes = audio_file.getvalue()
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        wav_audio = io.BytesIO()
        audio.export(wav_audio, format="wav")
        wav_audio.seek(0)
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
    if not is_authenticated():
        supabase_login_ui()
        return

    with st.sidebar:
        st.write(f"Signed in as: {st.session_state.supabase_user.email if st.session_state.supabase_user else 'User'}")
        if st.button("Log out"):
            sb = get_supabase()
            try:
                if sb:
                    sb.auth.sign_out()
            except Exception:
                pass
            st.session_state.supabase_user = None
            st.session_state.supabase_session = None
            st.rerun()

    st.sidebar.title("🌿 Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Chatbot", "Prompts", "Forum", "Contact", "Order", "Checkout"])
    
    if page == "Home":
        render_home_page()
    elif page == "Chatbot":
        render_chatbot_page()
    elif page == "Prompts":
        render_prompts_page()
    elif page == "Forum":
        render_forum_page()
    elif page == "Contact":
        render_contact_page()
    elif page == "Order":
        render_order_page()
    elif page == "Checkout":
        render_checkout_page()

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
    
    for category, prompts in categories.items():
        with st.expander(category):
            for i, prompt in enumerate(prompts, 1):
                st.markdown(f"{i}. {prompt}")
    
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
                
                reply_key = f"reply_button_{idx}"
                if st.button("Reply", key=reply_key):
                    st.session_state.replying[idx] = not st.session_state.replying.get(idx, False)
                    st.rerun()
                
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
                
                if post["replies"]:
                    st.write("**Replies:**")
                    for reply in post["replies"]:
                        st.markdown(f"**🗨️ {reply['user']} replied:**")
                        st.info(reply["content"])
                        st.caption(f"Replied on: {format_datetime(reply['timestamp'])}")
    else:
        st.info("No discussions yet. Be the first to start a conversation!")

# Contact Page Content
def render_contact_page():
    st.title("📬 Contact Us")
    st.markdown("We'd love to hear from you. Send us your questions or feedback.")
    name = st.text_input("Your Name")
    email = st.text_input("Email")
    message = st.text_area("Message", height=150)
    submitted = st.button("Send Message")
    if submitted:
        if not name or not email or not message:
            st.warning("Please fill in all fields.")
            return
        sb = get_supabase()
        if not sb:
            st.error("Supabase is not configured. Set SUPABASE_URL and SUPABASE_ANON_KEY.")
            return
        try:
            payload = {"name": name, "email": email, "message": message, "created_at": datetime.utcnow().isoformat()}
            res = sb.table("contacts").insert(payload).execute()
            if getattr(res, "data", None) is not None:
                st.success("Thanks! Your message has been sent.")
            else:
                st.info("Submitted, but no data returned. Check your Supabase table.")
        except Exception as e:
            st.error(f"Could not save your message: {e}")

# Simple in-app catalog
def get_catalog():
    return [
        {"id": 1, "name": "Organic Potting Soil (10L)", "price": 9.99},
        {"id": 2, "name": "Coco Peat Brick", "price": 4.50},
        {"id": 3, "name": "Terrace Planter (Medium)", "price": 14.99},
        {"id": 4, "name": "Drip Irrigation Kit", "price": 29.99},
        {"id": 5, "name": "Neem Oil (250ml)", "price": 6.75}
    ]

def add_to_cart(item, quantity):
    qty = max(1, int(quantity))
    for cart_item in st.session_state.cart:
        if cart_item["id"] == item["id"]:
            cart_item["quantity"] += qty
            return
    st.session_state.cart.append({"id": item["id"], "name": item["name"], "price": item["price"], "quantity": qty})

def remove_from_cart(item_id):
    st.session_state.cart = [ci for ci in st.session_state.cart if ci["id"] != item_id]

def cart_total():
    return sum(ci["price"] * ci["quantity"] for ci in st.session_state.cart)

# Order Page Content
def render_order_page():
    st.title("🛒 Order Supplies")
    st.markdown("Select items for your rooftop garden and add them to your cart.")

    catalog = get_catalog()
    for product in catalog:
        cols = st.columns([5, 2, 2])
        with cols[0]:
            st.write(f"**{product['name']}** — ${product['price']:.2f}")
        with cols[1]:
            qty = st.number_input(f"Qty {product['id']}", min_value=1, max_value=50, value=1, step=1, key=f"qty_{product['id']}")
        with cols[2]:
            if st.button("Add", key=f"add_{product['id']}"):
                add_to_cart(product, qty)
                st.success(f"Added {qty} × {product['name']} to cart")
                st.rerun()

    st.subheader("Your Cart")
    if st.session_state.cart:
        for ci in st.session_state.cart:
            ccols = st.columns([5, 2, 2])
            with ccols[0]:
                st.write(f"{ci['name']} — ${ci['price']:.2f} × {ci['quantity']}")
            with ccols[1]:
                st.write(f"${ci['price']*ci['quantity']:.2f}")
            with ccols[2]:
                if st.button("Remove", key=f"rm_{ci['id']}"):
                    remove_from_cart(ci["id"])
                    st.rerun()
        st.write(f"**Total: ${cart_total():.2f}**")
        if st.button("Proceed to Checkout"):
            st.success("Going to checkout…")
            st.session_state._navigate_to = "Checkout"
            st.rerun()
    else:
        st.info("Your cart is empty. Add some items above.")

# Checkout Page Content
def render_checkout_page():
    st.title("✅ Checkout")
    if not st.session_state.cart:
        st.info("Your cart is empty. Add items from the Order page.")
        return

    st.subheader("Order Summary")
    for ci in st.session_state.cart:
        st.write(f"- {ci['name']} × {ci['quantity']} — ${ci['price']*ci['quantity']:.2f}")
    total = cart_total()
    st.write(f"**Total: ${total:.2f}**")

    st.subheader("Shipping Details")
    customer_name = st.text_input("Full Name")
    email = st.text_input("Email")
    address = st.text_area("Address", height=100)
    place_order = st.button("Place Order")

    if place_order:
        if not customer_name or not email or not address:
            st.warning("Please fill in all details.")
            return
        sb = get_supabase()
        if not sb:
            st.error("Supabase is not configured. Set SUPABASE_URL and SUPABASE_ANON_KEY.")
            return
        try:
            order_payload = {
                "customer_name": customer_name,
                "email": email,
                "address": address,
                "total": float(f"{total:.2f}"),
                "created_at": datetime.utcnow().isoformat()
            }
            order_res = sb.table("orders").insert(order_payload).execute()
            data = getattr(order_res, "data", None)
            if not data:
                st.error("Order creation did not return data. Check Supabase schema.")
                return
            order_id = data[0].get("id") if isinstance(data, list) else data.get("id")
            if not order_id:
                st.error("Could not determine order ID from response.")
                return
            items_payload = [
                {"order_id": order_id, "product_id": ci["id"], "product_name": ci["name"], "unit_price": ci["price"], "quantity": ci["quantity"]}
                for ci in st.session_state.cart
            ]
            sb.table("order_items").insert(items_payload).execute()
            st.success(f"Order placed successfully! Order ID: {order_id}")
            st.session_state.cart = []
        except Exception as e:
            st.error(f"Could not place order: {e}")

if __name__ == "__main__":
    if getattr(st.session_state, "_navigate_to", None) == "Checkout":
        st.session_state._navigate_to = None
        render_checkout_page()
    else:
        main()
