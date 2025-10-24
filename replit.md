# Telegram Auto Status Userbot

## Project Overview
A Telegram userbot with a web interface for easy setup that automatically updates your display name based on online/offline status and sends auto-replies when offline. Built with Python, Telethon, and Flask.

## Recent Changes
- **2025-10-24**: Made project Docker-compatible and Koyeb-ready
  - Created Dockerfile with optimized multi-process setup
  - Added docker-compose.yml for easy local deployment
  - Created start.sh entrypoint to run both Flask and bot
  - Added Gunicorn for production-ready Flask deployment
  - Created .dockerignore for optimized builds
  - Comprehensive Koyeb deployment documentation
  - Created detailed README.md with Docker instructions
  - Updated .env.example with better documentation
  
- **2025-10-24**: Complete project setup with web interface and settings page
  - Created Flask web app for easy authentication
  - Implemented web-based OTP entry system
  - Developed clean UI for phone number and verification code entry
  - Added automatic session string generation and saving
  - Added Settings page for easy customization of bot name and auto-reply message
  - Session automatically saved to environment when generated (no manual setup needed!)
  - Settings saved to .env file and apply immediately
  - Organized project structure (templates/, static/, docs/, scripts/)
  - Created comprehensive documentation
  - Fixed auto-reply reset logic

## Features
- 🌐 **Web Interface**: Easy setup through a browser (no command line needed!)
- ⚙️ **Settings Page**: Customize your bot name and auto-reply message from the web interface
- 💾 **Auto-Save**: Session automatically saved when generated - no manual configuration!
- 🐳 **Docker Ready**: One-command deployment with Docker Compose
- 📱 **Auto Name Updates**: "Hashir ( Online )" / "Hashir ( Offline )"
- 💬 **Auto-Reply**: Sends "I'll respond when I get online" when offline
- 🔄 **Smart Reset**: Auto-reply resets when you come back online or send a message
- ⚡ **Real-time Monitoring**: Status checked every 30 seconds
- 🚀 **Cloud Ready**: Deploy to Koyeb for 24/7 uptime with Docker

## Project Structure
```
/
├── app.py                    # Flask web application for setup
├── main.py                   # Core bot logic with Telethon
├── start.sh                  # Docker entrypoint script
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker container configuration
├── docker-compose.yml        # Docker Compose setup
├── .dockerignore             # Docker build exclusions
├── .env.example              # Environment variables template
├── README.md                 # Main documentation
├── templates/               # HTML templates for web interface
│   ├── index.html          # Landing page/dashboard
│   ├── setup.html          # Authentication setup
│   ├── settings.html       # Settings page for customization
│   ├── bot.html            # Bot status page
│   ├── error.html          # Error page
│   └── docs.html           # Documentation
├── static/
│   └── css/
│       └── style.css       # Web interface styling
├── docs/                    # Documentation
│   ├── QUICK_START.md
│   ├── README.md
│   ├── KOYEB_DEPLOYMENT.md  # Docker deployment guide
│   └── SETUP_INSTRUCTIONS.txt
└── scripts/                 # Helper scripts
    ├── setup.py            # CLI setup (alternative)
    └── auth.py             # Authentication helper
```

## How to Use

### Local/Replit Setup
1. **Access the Web Interface**: Open the webview in Replit or http://localhost:5000
2. **Enter Phone Number**: Follow the on-screen prompts
3. **Enter OTP**: Check Telegram for verification code
4. **Session Auto-Saved**: Session string is automatically saved - no manual setup needed!
5. **Customize Settings**: Click "Settings" button to change your name or auto-reply message
6. **Done!**: Bot starts automatically

### Docker Deployment
1. **Clone the repository**: `git clone <repo-url>`
2. **Create .env file**: `cp .env.example .env` and fill in your credentials
3. **Run with Docker**: `docker-compose up -d`
4. **Access web interface**: Open http://localhost:5000
5. **Done!**: Both Flask and bot run automatically in container

### Koyeb Cloud Deployment
1. **Push to GitHub**: Commit and push your code
2. **Connect to Koyeb**: Link your GitHub repository
3. **Set environment variables**: Add API_ID, API_HASH, SESSION_SECRET
4. **Deploy!**: Koyeb automatically builds and deploys Docker container
5. **Monitor**: View logs and access web interface at Koyeb URL
See [docs/KOYEB_DEPLOYMENT.md](docs/KOYEB_DEPLOYMENT.md) for detailed guide

## Environment Variables Required
- `API_ID`: Telegram API ID (from my.telegram.org) - Already set ✅
- `API_HASH`: Telegram API Hash - Already set ✅
- `SESSION_SECRET`: Session string generated through web interface - Needs setup
- `BASE_NAME`: Your base name without status (default: Hashir)
- `AUTO_REPLY_MESSAGE`: Message to send when offline (optional)

## User Preferences
- Base name: "Hashir"
- Platform: Koyeb deployment (24/7)
- Auto-reply message: "I'll respond when I get online"
- Setup method: Web interface (no command line needed)

## Technical Stack
- **Backend**: Python 3.11, Flask 3.1.0, Gunicorn 22.0.0
- **Telegram**: Telethon 1.41.2
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Environment**: python-dotenv
- **Containerization**: Docker, Docker Compose
- **Deployment**: Replit + Koyeb (Docker-based)

## Deployment Notes
- Web interface running on port 5000 (Gunicorn in production)
- Authentication done through browser
- Session stored as StringSession for cloud deployment
- Runs as userbot (on user's account, not a bot)
- Requires continuous uptime for status monitoring
- Docker container runs both Flask app and Telegram bot
- start.sh manages multi-process execution
- Optimized Dockerfile for minimal image size (~200MB)
- Docker Compose for easy local testing
