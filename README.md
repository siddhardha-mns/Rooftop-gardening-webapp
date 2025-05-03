# 🌿 Rooftop Gardening Assistant

![Rooftop Gardening](https://sl.bing.net/df80MIH7xYq)

## Overview

A comprehensive Streamlit web application designed to assist urban dwellers in creating and maintaining rooftop gardens. This application combines educational resources, community features, and AI-powered assistance to make rooftop gardening accessible to everyone.

## 🌱 Features

### User Authentication
- Simple login system for personalized experience
- Customized reminders based on user login

### Smart Reminders
- Water reminder (24-hour cycle)
- Fertilizer reminder (48-hour cycle)
- Visual progress bars for easy tracking

### AI-Powered Chatbot
- Powered by Google's Gemini 1.5 Flash model
- Text and voice input options for questions
- Instant responses to gardening queries

### Educational Resources
- Comprehensive prompts organized by categories:
  - Garden design guidance
  - Seasonal crop selection
  - Manure and soil preparation
  - Water management techniques
  - Pest control strategies
  - And much more!

### Community Forum
- Post questions and share experiences
- Reply to other community members
- Timestamped discussions

## 📋 Prerequisites

- Python 3.7+
- An API key for Google's Generative AI (Gemini)

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/siddhardha-mns/Rooftop-gardening-webapp.git
cd Rooftop-gardening-webapp
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install required dependencies:
```bash
pip install streamlit google-generativeai pydub SpeechRecognition
```

4. Update the API key:
   - Open the file in your code editor
   - Replace `"YOUR_API_KEY_HERE"` with your actual Gemini API key

## 💻 Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Access the application in your web browser (typically at http://localhost:8501)

3. Login credentials:
   - Username: Choose from "sanketh", "nikhil", "karthik", "shiva"
   - Password: "rooftop"

4. Navigation:
   - Use the sidebar to switch between Home, Chatbot, Prompts, and Forum pages
   - Track your watering and fertilizing schedules in the top section

## 🎤 Using Voice Input

1. Navigate to the Chatbot page
2. Select "Audio" as the input method
3. Upload an audio file containing your gardening question
4. Click "Transcribe Audio" to convert your speech to text
5. Review the transcription and click "Generate Response" to get your answer

## 🛠️ Customization

### Changing the Background
To change the background image, modify the URL in the CSS section at the beginning of the script.

### Adding More Users
Extend the `valid_users` list in the `login` function to add more authorized users.

### Adjusting Reminder Times
Modify the duration values in the `calculate_progress` function calls to change how often reminders appear.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the web application framework
- [Google Generative AI](https://ai.google.dev/) for the Gemini model
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) for audio transcription capabilities
- [Pydub](https://github.com/jiaaro/pydub) for audio processing

## 📞 Contact

MNS SIDDHARDHA- mnssiddhardha@gmail.com

Project Link: [https://github.com/siddhardha-mns/Rooftop-gardening-webapp](https://github.com/siddhardha-mns/Rooftop-gardening-webapp)

---

🌱 Happy Gardening! 🌱
