<p>
  <img src="static/images/cerebromail-logo.png" alt="CerbroMail Logo" width="180" >
</p>

# CerbroMail - AI Email Intelligence

**Intelligent email management system powered by Google Gemini AI**

an adaptive, AI-driven email productivity system that transforms raw inboxes into actionable insights. Powered by Google Gemini, it intelligently categorizes messages, extracts tasks, generates drafts, and enables chat-based email understanding — all through a clean, user-friendly interface.

---

## ⚡ Quick Start

```bash
# 1. Clone and install
git clone https://github.com/lalitaditya04/CerebroMail
cd CerebroMail
python -m venv venv "or" conda create -n env_name python=3.12
venv\Scripts\activate "or" conda activate env_name # Windows
source venv/bin/activate  "or" conda activate env_name # macOS/Linux
pip install -r requirements.txt

# 2. Configure API key
# Create .env file:
echo "GEMINI_API_KEY=your_key_here" > .env

# 3. Run
python app.py
```

Then open: **http://localhost:5000**

---

## 🎯 Features

### AI-Powered Intelligence
- 🤖 **Smart Categorization** - Auto-sorts emails (Important, Newsletter, Spam, To-Do, Project)
- ✅ **Action Extraction** - Both automatic AND manual extraction via button
- ✏️ **Draft Generation** - Context-aware professional replies
- 💬 **AI Chat** - Ask questions about any email
- 🎯 **Custom Analyzers** - Create custom prompts for specific insights
- 📊 **Email Summaries** - Quick 2-3 sentence overviews

### Productivity Features
- 📋 **Task Manager** - Track and manage extracted action items
- 📅 **Calendar Integration** - Export tasks to Google Calendar
- 🎨 **Customizable AI** - Modify prompts to match your workflow
- 🔍 **Priority Filtering** - Focus on High/Medium/Low priority tasks
- 📧 **Mock & Gmail Support** - Test with mock data or connect real Gmail

### 🆕 Enhanced Features
- **Manual Action Extraction** - Extract actions anytime by clicking the button
- **Modular Architecture** - Clean, maintainable code structure
- **Multiple Drafts** - Save and manage multiple draft replies per email
- **Chat History** - Conversations persist across sessions
- **Batch Processing** - Process emails in batches (configurable)

---

## 🏗️ Architecture (SOLID Principles)

```
CerebroMail/
├── app.py                      # Main Flask app (routing only)
├── requirements.txt            # Dependencies
├── .env                        # Configuration (not in Git)
│
├── models/                     # Data models (Single Responsibility)
│   ├── email_models.py         # EmailData, ActionItem
│   └── user_model.py           # User authentication
│
├── services/                   # Business logic layer
│   ├── gemini_service.py       # AI operations
│   ├── gmail_service.py        # Gmail integration
│   ├── email_storage.py        # Email storage
│   └── user_service.py         # User management
│
├── routes/                     # API endpoints (Interface Segregation)
│   ├── email_routes.py         # Email CRUD
│   ├── ai_routes.py            # AI processing
│   ├── config_routes.py        # Configuration
│   ├── gmail_routes.py         # Gmail OAuth
│   ├── chat_routes.py          # Chat history
│   └── admin_routes.py         # Admin dashboard
│
├── middleware/                 # Security & rate limiting
│   └── security.py             # Rate limits, headers, protection
│
├── database/                   # Data persistence
│   └── db_manager.py           # SQLite database
│
├── utils/                      # Utilities
│   ├── error_handler.py        # Error handling
│   ├── error_logger.py         # Error logging
│   └── exceptions.py           # Custom exceptions
│
├── config/                     # Configuration
│   ├── settings.py             # App settings
│   └── constants.py            # Constants & defaults
│
├── static/                     # Frontend assets
│   ├── css/custom.css          # Custom styles
│   └── js/                     # Modular JavaScript
│       ├── state.js            # State management
│       ├── api.js              # API calls
│       ├── chat.js             # Chat functionality
│       ├── drafts.js           # Draft management
│       ├── tasks.js            # Task management
│       ├── handlers.js         # Event handlers
│       ├── renders.js          # Main rendering
│       ├── renders-details.js  # Detail rendering
│       └── app.js              # Initialization
│
└── templates/
    └── index.html              # Main UI (23 lines!)
```

---

## 💻 Technology Stack

### Backend
- **Python 3.8+** - Core language
- **Flask 3.0** - Web framework
- **Google Gemini AI** - AI engine (Flash/Pro models)
- **SQLite** - Data persistence
- **Gmail API** - Email integration

### Frontend
- **Vanilla JavaScript** - Modular architecture (9 files)
- **TailwindCSS** - Utility-first styling
- **HTML5** - Single-page application

### Security
- **Rate Limiting** - Protect API quota (5 req/min for AI)
- **Security Headers** - XSS, clickjacking, MIME protection
- **Environment Variables** - Secure API key management
- **Content Length Limits** - DoS protection
- **CORS** - Controlled cross-origin access

---

## 🚀 Usage Guide

### 1. Loading Emails
- **Mock Data**: Click "Reset with Mock Data"
- **Gmail**: Click "Connect to Gmail" (OAuth flow)

### 2. Processing Emails

#### Automatic Batch Processing
- Click **"Process Emails"** to process 4 emails at a time
- First run automatically processes 5 emails
- Subsequent clicks process next 4 unprocessed emails

#### Manual Action Extraction
1. Select any email
2. View the email content tab
3. Click **"Extract Actions"** button
4. AI analyzes and extracts action items

### 3. Customizing AI Agent
1. Click **"Agent Brain"** icon (lightbulb)
2. Select AI model (Gemini Flash/Pro)
3. Edit prompts:
   - Categorization rules
   - Action extraction logic
   - Auto-reply tone and style
4. Add custom analyzers (sentiment, urgency, etc.)
5. Click "Save Configuration"

### 4. Managing Tasks
- View all tasks in **"To-Do List"** tab
- Filter by priority (High/Medium/Low)
- Check off completed items
- Export to Google Calendar
- Click task to view original email

### 5. Chat with Emails
- Select email → **"Agent Chat"** tab
- Ask questions about the email
- Use quick actions (Summarize, Find Tasks, Check Urgency)
- Chat history persists automatically

### 6. Draft Management
- Multiple drafts per email
- AI-powered generation with custom instructions
- Auto-save functionality
- Version history

---

## 📋 API Endpoints

### Email Operations
```
GET    /api/emails              # Get all emails
POST   /api/emails/load-mock    # Load mock data
GET    /api/emails/<id>         # Get specific email
PUT    /api/emails/<id>         # Update email
POST   /api/emails/simulate     # Simulate new email
```

### AI Operations (Rate Limited)
```
POST   /api/process-inbox       # Process batch (5 req/min)
POST   /api/extract-actions     # Extract actions (5 req/min)
POST   /api/categorize          # Categorize (5 req/min)
POST   /api/summarize           # Summarize (5 req/min)
POST   /api/generate-draft      # Draft reply (5 req/min)
POST   /api/chat                # Chat (30 req/min)
POST   /api/custom-analyzer     # Custom analysis (5 req/min)
```

### Configuration
```
GET    /api/prompts             # Get prompts
PUT    /api/prompts             # Update prompts
GET    /api/model-config        # Get AI model config
POST   /api/model-config        # Update AI model
```

### Gmail Integration
```
GET    /api/gmail/auth          # Start OAuth flow
GET    /api/gmail/auth/callback # OAuth callback
GET    /api/gmail/emails        # Fetch Gmail emails
POST   /api/gmail/disconnect    # Disconnect Gmail
GET    /api/gmail/status        # Check connection
```

### Chat History
```
POST   /api/chat/save           # Save chat (30 req/min, 100KB max)
GET    /api/chat/load           # Load chat history
DELETE /api/chat/delete         # Delete chat
```

### Admin & Monitoring
```
GET    /api/admin/errors/recent # Recent errors
GET    /api/admin/errors/stats  # Error statistics
GET    /api/admin/dashboard     # Error dashboard
```

---

## 🔒 Security Features

### ✅ Layer 1: Rate Limiting
- **AI Endpoints**: 5 requests/minute (expensive operations)
- **Chat Endpoints**: 30 requests/minute
- **General Endpoints**: 60 requests/minute
- Automatic cleanup of old entries
- User-friendly error messages with retry times

### ✅ Layer 2: API Key Protection
- Environment variables only (never in frontend)
- Backend-only API access
- No secrets exposed in JavaScript
- Secure credential management

### ✅ Layer 3: Security Headers
```python
X-Frame-Options: SAMEORIGIN           # Prevents clickjacking
X-Content-Type-Options: nosniff        # Prevents MIME attacks
X-XSS-Protection: 1; mode=block        # XSS protection
Content-Security-Policy: ...           # CSP restrictions
Referrer-Policy: strict-origin         # Referrer control
Permissions-Policy: ...                # Feature restrictions
Strict-Transport-Security: ...         # HTTPS enforcement (production)
```

### Additional Security
- **Content Length Limits**: 100KB for chat, configurable for others
- **CORS Configuration**: Controlled origins
- **Session Management**: 45-minute timeout, HTTP-only cookies
- **Error Logging**: Comprehensive error tracking in SQLite
- **IP Whitelisting**: Optional admin endpoint protection

---

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
AI_MODEL=gemini-1.5-flash                    # or gemini-1.5-pro
SECRET_KEY=your_secret_key_here              # Auto-generated if not set
PORT=5000                                     # Server port
FLASK_ENV=development                         # or production
INTERNAL_API_KEY=your_internal_key           # For admin endpoints
```

---

## 🐛 Troubleshooting

### Common Issues

**"No module named 'routes'"**
```bash
cd CerebroMail
python app.py
```

**"API key not found"**
```bash
# Check .env file has:
GEMINI_API_KEY=your_actual_key
```

**"Rate limit exceeded"**
- Wait for the retry timer
- Or increase limits in `middleware/security.py`

**Port already in use**
```bash
# Change in .env:
PORT=5001
```

**Gmail OAuth not working**
- Check redirect URI in Google Cloud Console
- Ensure credentials.json is present
- Verify HTTPS in production

---

## 🚀 Deployment

### Deploy to Render (Recommended)

See **[RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)** for complete guide.

Quick steps:
1. Push code to GitHub
2. Create Render Web Service
3. Set environment variables
4. Deploy!

Your app will be live at: `https://your-app.onrender.com`

### Local Deployment

```bash
# Production mode
gunicorn app:app --bind 0.0.0.0:5000 --workers 4
```

---

## 📊 Project Stats

- **Backend Lines**: ~3,000 lines (Python)
- **Frontend Lines**: ~2,000 lines (JavaScript)
- **Main HTML**: 23 lines (modularized!)
- **JavaScript Modules**: 9 files
- **API Endpoints**: 30+
- **Security Layers**: 3 (rate limiting, headers, key protection)

---

## ✨ What Makes This Special

### Architecture
- ✅ **SOLID Principles** - Every file has one responsibility
- ✅ **Modular JavaScript** - 9 organized modules (was 1 monolith)
- ✅ **Clean Separation** - Backend/Frontend completely separated
- ✅ **Type Safety** - Pydantic models for data validation

### User Experience
- ✅ **Fast** - Optimized AI calls, batch processing
- ✅ **Intuitive** - Clean UI, minimal learning curve
- ✅ **Persistent** - SQLite storage, chat history
- ✅ **Customizable** - Edit prompts, models, analyzers

### Developer Experience
- ✅ **Easy to Understand** - Well-organized codebase
- ✅ **Easy to Extend** - Add features without breaking existing
- ✅ **Easy to Test** - Modular components
- ✅ **Easy to Deploy** - Simple requirements, no build step

### Production Ready
- ✅ **Secure** - Rate limiting, headers, key protection
- ✅ **Scalable** - Modular architecture supports growth
- ✅ **Monitored** - Error logging, admin dashboard
- ✅ **Documented** - Comprehensive docs and guides

---

## 📄 License

This project is provided as-is for educational and demonstration purposes.

---

## 🙏 Acknowledgments

- **Google Gemini AI** - Powerful AI engine
- **Flask** - Excellent web framework
- **TailwindCSS** - Beautiful styling
- **Render** - Easy deployment platform

---

**Built with ❤️ using Python, Flask, and Google Gemini AI**

🚀 **Production-ready, secure, and modular AI email assistant!**

---

**Star ⭐ this repo if you find it useful!**
