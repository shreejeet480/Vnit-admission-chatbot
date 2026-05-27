# 🎓 VNIT Nagpur Admission Chatbot

An intelligent AI-driven conversational assistant designed to help prospective students with all their queries about admissions at **Visvesvaraya National Institute of Technology (VNIT), Nagpur**.

## 📋 Table of Contents

- [Features](#features)
- [Project Architecture](#project-architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure & File Descriptions](#project-structure--file-descriptions)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [Future Enhancements](#future-enhancements)

---

## ✨ Features

- **24/7 Admission Support**: Instant answers to frequently asked questions
- **Multi-Program Information**: Details about B.Tech, B.Arch, M.Tech, M.Sc, MBA, and Ph.D programs
- **Smart Intent Recognition**: NLP-based understanding of user queries
- **Multiple Interfaces**: CLI (command-line), Web, and REST API support
- **Conversation History**: Tracks user interactions for personalized experience
- **FAQ Database**: 16+ comprehensive frequently asked questions
- **Eligibility Checker**: Provides program-specific eligibility criteria
- **Placement Information**: Statistics about job placements and average packages
- **Real-time Counseling Guidance**: Information about JoSAA, CCMT, and CCMN counseling processes

---

## 🏗️ Project Architecture

```
VNIT Chatbot Architecture:

┌─────────────────────────────────────────────────────┐
│              User Interfaces                         │
│    (CLI | Web | API)                                │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│         Main Chatbot Class (VNITChatbot)            │
│  - Orchestrates all operations                       │
│  - Manages conversation flow                         │
└──────┬────────────────────────────────────┬──────────┘
       │                                    │
   ┌───▼────────────────────┐   ┌──────────▼──────────┐
   │ Intent Recognition     │   │ Response Generator  │
   │ - Analyzes user input  │   │ - Generates replies │
   │ - Identifies intent    │   │ - Provides          │
   └───┬────────────────────┘   │   suggestions       │
       │                        └──────────┬──────────┘
       │                                   │
       └────────────────────┬──────────────┘
                            │
              ┌─────────────▼───────────────┐
              │    Data Files (JSON)        │
              │ - admission_data.json       │
              │ - faqs.json                 │
              │ - programs.json             │
              └─────────────────────────────┘
                            │
              ┌─────────────▼───────────────┐
              │    SQLite Database          │
              │ - Stores conversations      │
              │ - Analytics & Logging       │
              └─────────────────────────────┘
```

---

## 🛠️ Technology Stack

- **Backend**: Python 3.8+
- **NLP**: NLTK, spaCy (for future advanced NLP)
- **Web Framework**: Flask
- **Database**: SQLite
- **Testing**: Pytest
- **Data Format**: JSON
- **CLI Styling**: Colorama

---

## 📦 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/shreejeet480/Vnit-admission-chatbot.git
cd Vnit-admission-chatbot
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python main.py --help
```

---

## 🚀 Usage

### CLI Mode (Interactive Chatbot)

```bash
python main.py --mode cli
```

Example interaction:
```
======================================================
  🎓 VNIT NAGPUR ADMISSION CHATBOT
======================================================

You: What is VNIT?
Bot: VNIT (Visvesvaraya National Institute of Technology)...

You: Tell me about B.Tech
Bot: 📚 **Here are the programs offered at VNIT Nagpur:**...
```

### Web Mode

```bash
python main.py --mode web
```

Then open your browser: `http://localhost:5000`

### Quick Commands

```bash
# Get help
You: help

# Exit chatbot
You: exit

# Ask about programs
You: What programs does VNIT offer?

# Check eligibility
You: Am I eligible for B.Tech?

# Know about admissions
You: How is the admission process?
```

---

## 🔌 API Endpoints

If running in API/Web mode:

### Chat Endpoint

**POST** `/api/chat`

Request:
```json
{
  "message": "Tell me about B.Tech",
  "session_id": "user_123"
}
```

Response:
```json
{
  "session_id": "user_123",
  "response": "📚 **Here are the programs offered at VNIT Nagpur:**...",
  "intent": "program_info",
  "confidence": 0.95,
  "suggestions": ["Tell me about B.Tech", "What is M.Tech?", "How about MBA?"]
}
```

### Get Programs Endpoint

**GET** `/api/programs?session_id=user_123`

Returns: All available programs and details

### Get FAQs Endpoint

**GET** `/api/faq?session_id=user_123&limit=10`

Returns: List of frequently asked questions

---

## 📁 Project Structure & File Descriptions

### 1. **config/config.py**
- **Purpose**: Centralized configuration management
- **Contains**: 
  - NLP settings (intent threshold, stemming options)
  - Database paths
  - VNIT institute information
  - Program list
  - Chatbot behavior settings
- **Why**: Keeps all settings in one place for easy modification

### 2. **data/admission_data.json**
- **Purpose**: Comprehensive admission information database
- **Contains**:
  - Eligibility criteria for each program
  - Entrance exams required
  - Specializations available
  - Cutoff ranks by category
  - Required documents
  - Fee structure
  - Placement statistics
- **Why**: Centralized data source for all admission information

### 3. **data/faqs.json**
- **Purpose**: Frequently asked questions database
- **Contains**: 16+ Q&A pairs organized by category
- **Why**: Provides quick answers to common questions

### 4. **data/programs.json**
- **Purpose**: Detailed program information
- **Contains**: 
  - Program levels (UG, PG, Doctorate)
  - Duration
  - Specializations
  - Seat information
- **Why**: Structured data for easy program lookup

### 5. **src/intent_recognition.py**
- **Purpose**: Identifies what the user is asking about
- **How it works**:
  1. Analyzes user message
  2. Matches against predefined patterns and keywords
  3. Returns intent (e.g., 'program_info', 'eligibility')
  4. Provides confidence score
- **Intents Recognized**:
  - `program_info`: Questions about programs
  - `eligibility`: Eligibility requirements
  - `admission_process`: How to apply
  - `entrance_exam`: Required exams
  - `documents`: Required documents
  - `fees`: Fee information
  - `placement`: Job placement data
  - `counseling`: Counseling processes
  - `general`: General queries
- **Why**: Enables the chatbot to understand user intent

### 6. **src/response_generator.py**
- **Purpose**: Generates appropriate responses
- **How it works**:
  1. Receives intent from IntentRecognizer
  2. Calls appropriate handler function
  3. Retrieves data from JSON files
  4. Formats response with emojis and markdown
  5. Provides follow-up suggestions
- **Handler Functions**:
  - `_handle_program_info()`: Program information
  - `_handle_eligibility()`: Eligibility criteria
  - `_handle_admission_process()`: Step-by-step process
  - `_handle_entrance_exam()`: Entrance exam details
  - `_handle_documents()`: Required documents
  - `_handle_fees()`: Fee structure
  - `_handle_placement()`: Placement statistics
  - `_handle_counseling()`: Counseling information
- **Why**: Generates context-aware, helpful responses

### 7. **src/chatbot.py**
- **Purpose**: Main orchestrator class
- **Key Methods**:
  - `process_message()`: Main method to process user queries
  - `set_user_id()`: Track user sessions
  - `get_conversation_history()`: Retrieve past messages
  - `clear_history()`: Clear conversation
  - `get_program_info()`: Get program details
  - `get_faq()`: Get FAQ list
- **Why**: Coordinates all chatbot components

### 8. **src/database.py**
- **Purpose**: Database operations
- **Tables**:
  - `conversations`: Logs all user-bot interactions
  - `users`: Tracks unique users
- **Functions**:
  - `log_conversation()`: Store interaction
  - `get_user_conversations()`: Retrieve history
  - `get_conversation_stats()`: Analytics
- **Why**: Enables learning and analytics

### 9. **src/utils.py**
- **Purpose**: Utility functions
- **Functions**:
  - `clean_text()`: Text preprocessing
  - `extract_program_name()`: Program extraction
  - `tokenize()`: Text tokenization
- **Why**: Reusable helper functions

### 10. **interfaces/cli.py**
- **Purpose**: Command-line chatbot interface
- **Features**:
  - Colored terminal output
  - Interactive conversation loop
  - Help command
  - User-friendly prompts
- **Why**: Easy testing and quick access

### 11. **interfaces/web_app.py**
- **Purpose**: Flask web application
- **Endpoints**: `/`, `/api/chat`, `/api/programs`, `/api/faq`
- **Session Management**: Tracks user sessions
- **Why**: Web-based chatbot interface

### 12. **main.py**
- **Purpose**: Application entry point
- **Usage**:
  ```bash
  python main.py --mode cli        # CLI mode
  python main.py --mode web        # Web mode
  python main.py --help            # Show options
  ```
- **Why**: Easy-to-use entry point

### 13. **requirements.txt**
- **Purpose**: Python dependencies
- **Contains**: All required packages with versions
- **Why**: Easy environment setup

### 14. **tests/test_chatbot.py** & **tests/test_intent.py**
- **Purpose**: Unit tests for verification
- **Why**: Ensures code quality and functionality

---

## ⚙️ Configuration

Edit `config/config.py` to customize:

```python
# Change intent confidence threshold
NLP_CONFIG = {
    'intent_threshold': 0.6,  # Lower = more lenient
}

# Enable/disable features
CHATBOT_CONFIG = {
    'log_conversations': True,  # Save to database
    'enable_learning': True,    # Improve over time
}

# Update VNIT contact info
VNIT_INFO = {
    'email': 'admissions@vnit.ac.in',
    'phone': '+91-712-2801000',
}
```

---

## 🧠 How It Works

### Chatbot Flow

```
1. User Input
   ↓
2. Intent Recognition
   - Analyzes message
   - Matches patterns/keywords
   - Assigns confidence score
   ↓
3. Response Generation
   - Loads relevant data
   - Formats response
   - Adds suggestions
   ↓
4. Display Response
   - Shows to user
   - Logs to database
   ↓
5. Conversation History
   - Maintained for context
   - Used for personalization
```

### Example Flow

**User**: "What is the eligibility for B.Tech?"

**Step 1 - Intent Recognition**:
- Finds keywords: "eligibility", "B.Tech"
- Matches pattern: "eligibility.*for"
- Intent identified: `eligibility`
- Confidence: 0.95

**Step 2 - Response Generation**:
- Recognizes `eligibility` intent
- Calls `_handle_eligibility()`
- Extracts B.Tech eligibility from `admission_data.json`
- Formats response with bullet points

**Step 3 - Display**:
- Shows eligibility criteria
- Provides suggestions: "B.Tech admission", "M.Tech requirements", etc.

---

## 🐛 Testing

Run tests:

```bash
pytest tests/

# With coverage
pytest tests/ --cov=src
```

---

## 🔮 Future Enhancements

- [ ] Machine learning-based NLP using transformers
- [ ] Integration with official VNIT admission portal
- [ ] Real-time cutoff tracking
- [ ] Multi-language support (Hindi, Marathi)
- [ ] Voice interface (speech-to-text)
- [ ] Telegram/WhatsApp integration
- [ ] Email notifications
- [ ] Counseling appointment booking
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard

---

## 📞 Support

For issues or suggestions:
1. Check existing [GitHub Issues](https://github.com/shreejeet480/Vnit-admission-chatbot/issues)
2. Create a new issue with details
3. Contact: admissions@vnit.ac.in

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

**Shreejeet480**
- GitHub: [@shreejeet480](https://github.com/shreejeet480)

---

## ⭐ Acknowledgments

- VNIT Nagpur for admission information
- Python community for amazing libraries
- Contributors and testers

---

## 📢 Disclaimer

This chatbot is an educational project. For official admission information, always refer to [VNIT Nagpur official website](https://vnit.ac.in/section/academics/admission/).
