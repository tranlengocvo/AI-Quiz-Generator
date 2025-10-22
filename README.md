# 🎯 AI Quiz Generator

> An intelligent quiz application powered by Claude AI that generates custom multiple-choice questions on any topic and provides detailed explanations.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.30+-red.svg)

## ✨ Features

- 🤖 **AI-Powered Question Generation** - Claude generates 5 relevant multiple-choice questions on any topic
- 🎨 **Beautiful Web Interface** - Modern, responsive UI built with Streamlit
- 📝 **Interactive Quiz Experience** - Smooth answering flow with instant visual feedback
- 🧠 **Intelligent Grading** - AI analyzes your answers and provides detailed explanations
- 💾 **Smart Caching** - Minimizes API calls to save costs (same topic = no re-generation!)
- 📊 **Detailed Results** - Color-coded feedback with comprehensive explanations

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/tranlengocvo/AI-Quiz-Generator.git
   cd AI-Quiz-Generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your Anthropic API key**

   - Visit [Anthropic Console](https://console.anthropic.com/)
   - Sign up or log in
   - Create a new API key

   **Note**: You'll enter the API key in the app's sidebar when you run it.

### Running the App

#### 🌐 Web App (Recommended)

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

**First-time setup:**
1. Enter your Anthropic API key in the sidebar
2. The key is only used during your session and never stored
3. Start creating quizzes!

#### 💻 CLI App

For the CLI version, create a `.env` file first:
```env
ANTHROPIC_API_KEY=your-api-key-here
```

Then run:
```bash
python quiz_app.py
```

## 📖 Usage Guide

### Web App Features

1. **Enter API Key** - Input your Anthropic API key in the sidebar (one-time per session)
2. **Enter a Topic** - Type any subject (e.g., "Python Programming", "World History", "Physics")
3. **Generate Questions** - AI creates 5 unique multiple-choice questions
4. **Take the Quiz** - Select answers using intuitive radio buttons
5. **View Results** - Get instant feedback with:
   - ✅ Green highlighting for correct answers
   - ❌ Red highlighting for incorrect answers
   - 📝 Detailed explanations for each question
   - 📊 Overall score percentage

### Example Topics

- Programming: "Python decorators", "React hooks", "SQL joins"
- Science: "Quantum physics", "Cellular biology", "Chemistry basics"
- History: "Ancient Rome", "World War 2", "Renaissance art"
- General: "Marine biology", "Space exploration", "Climate change"

## 💰 Cost Optimization

### API Usage per Quiz

| Action | Web App | CLI App |
|--------|---------|---------|
| First time with topic | 2 calls | 2 calls |
| Same topic again | 0 calls* | 2 calls |
| Retake same quiz | 1 call** | 2 calls |

**\*** Questions are cached
**\*\*** Only grading call needed

### Why Web App Saves Money

- **Caching**: Questions for the same topic are cached - no re-generation needed
- **Session Persistence**: Retake quizzes without regenerating questions
- **Better Control**: Clear visibility of when API calls are made

**💡 Tip**: The web app can save you up to 50% on API costs compared to the CLI version!

## 🏗️ Project Structure

```
AI-Quiz-Generator/
├── app.py                  # Streamlit web application
├── quiz_app.py            # CLI version
├── requirements.txt       # Python dependencies
├── .env                   # API key (create this)
├── .env.example          # Example environment file
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🛠️ Tech Stack

- **AI Model**: Claude Sonnet 4.5 (Anthropic)
- **Web Framework**: Streamlit
- **Language**: Python 3.7+
- **Key Libraries**:
  - `anthropic` - Claude API client
  - `streamlit` - Web interface
  - `python-dotenv` - Environment management

## 🎨 Screenshots

### Web Interface
- Clean, modern design with gradient headers
- Intuitive radio button selection
- Color-coded results with emoji indicators
- Responsive layout for all screen sizes

## 📚 How It Works

1. **Question Generation**
   - User enters a topic
   - App sends prompt to Claude API
   - AI generates 5 multiple-choice questions in JSON format
   - Questions are cached (web app only)

2. **Quiz Taking**
   - Questions displayed one by one
   - User selects answers (A, B, C, or D)
   - Answers stored in session state

3. **Grading & Feedback**
   - Answers sent to Claude for analysis
   - AI evaluates correctness
   - Detailed explanations generated for each question
   - Results displayed with visual feedback

## 🔒 Security Notes

- 🔑 **Web App**: Enter your API key in the sidebar - it's only used during your session and never stored or shared
- ⚠️ **CLI App**: Never commit your `.env` file - it contains your API key
- 🛡️ **Use `.gitignore`** - the provided `.gitignore` protects sensitive files
- 💳 **Monitor your usage** - check your Anthropic dashboard regularly
- 🎯 **Deployment**: When deploying, users will need to provide their own API keys (you won't pay for their usage!)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest new features
- 🔧 Submit pull requests

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🙋‍♂️ Support

If you encounter any issues:
1. Check that your API key is correctly set in `.env`
2. Ensure all dependencies are installed: `pip install -r requirements.txt`
3. Verify you're using Python 3.7 or higher: `python --version`

## 🌟 Acknowledgments

- Powered by [Anthropic's Claude AI](https://www.anthropic.com/)
- Built with [Streamlit](https://streamlit.io/)

---

<div align="center">
  Made with ❤️ using Claude AI
  <br>
  <sub>Star ⭐ this repo if you find it helpful!</sub>
</div>
