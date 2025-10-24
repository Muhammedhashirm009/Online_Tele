# Telegram Auto Status Bot 🤖

Automatically update your Telegram display name based on online/offline status and send auto-replies when you're away.

**"Hashir ( Online )"** ↔️ **"Hashir ( Offline )"**

## ✨ Features

- 🌐 **Web Interface** - Easy setup through browser (no command line!)
- ⚙️ **Settings Page** - Customize name and auto-reply message
- 💾 **Auto-Save** - Session automatically saved during setup
- 📱 **Smart Status** - Name updates based on your online/offline status
- 💬 **Auto-Reply** - Automatic responses when you're offline
- 🔄 **Smart Reset** - Auto-reply list clears when you're back online
- 🐳 **Docker Ready** - One-command deployment
- 🚀 **Cloud Deploy** - Easy deployment to Koyeb for 24/7 uptime

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/telegram-auto-status.git
cd telegram-auto-status

# 2. Create .env file with your credentials
cp .env.example .env
# Edit .env and add your API_ID, API_HASH, SESSION_SECRET

# 3. Run with Docker Compose
docker-compose up -d

# 4. Access web interface
open http://localhost:5000
```

### Option 2: Python (Local Development)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/telegram-auto-status.git
cd telegram-auto-status

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# 4. Run the web app (for setup)
python app.py

# 5. Generate session through web interface (http://localhost:5000)

# 6. Run the bot
python main.py
```

### Option 3: Deploy to Koyeb (24/7 Cloud)

See [Koyeb Deployment Guide](docs/KOYEB_DEPLOYMENT.md) for detailed instructions.

**Quick steps:**
1. Push code to GitHub
2. Connect GitHub to Koyeb
3. Add environment variables
4. Deploy! ✅

## 📋 Prerequisites

1. **Telegram API Credentials**
   - Visit [my.telegram.org](https://my.telegram.org)
   - Go to "API development tools"
   - Create an application
   - Note your `API_ID` and `API_HASH`

2. **Python 3.11+** (if running locally)
   OR
   **Docker** (recommended)

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
# Required
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
SESSION_SECRET=your_session_string_here

# Optional (customize)
BASE_NAME=Hashir
AUTO_REPLY_MESSAGE=I'll respond when I get online
```

### Getting Your Session String

**Method 1: Web Interface (Easiest)**
1. Run `python app.py` or `docker-compose up`
2. Open `http://localhost:5000`
3. Follow the setup wizard
4. Session is auto-saved!

**Method 2: Command Line**
```bash
python scripts/auth.py
```

## 🐳 Docker Commands

```bash
# Build the image
docker build -t telegram-auto-status .

# Run with Docker Compose (recommended)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down

# Restart the bot
docker-compose restart
```

## 📁 Project Structure

```
.
├── app.py                  # Flask web interface
├── main.py                 # Core Telegram bot logic
├── start.sh                # Docker entrypoint script
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── .dockerignore           # Docker ignore rules
├── templates/              # HTML templates
│   ├── index.html         # Dashboard
│   ├── setup.html         # Authentication setup
│   ├── settings.html      # Settings page
│   ├── bot.html           # Bot status
│   └── docs.html          # Documentation
├── static/
│   └── css/
│       └── style.css      # Styles
├── docs/                   # Documentation
│   ├── KOYEB_DEPLOYMENT.md
│   ├── QUICK_START.md
│   └── README.md
└── scripts/                # Helper scripts
    ├── setup.py
    └── auth.py
```

## 🌐 Web Interface

The web interface provides:

- **Dashboard** - View setup status and access settings
- **Setup Wizard** - Easy authentication flow
- **Settings Page** - Customize your bot name and auto-reply message
- **Bot Status** - Monitor bot activity
- **Documentation** - Built-in help

Access at: `http://localhost:5000`

## ⚙️ How It Works

1. **Status Monitoring**
   - Checks your Telegram status every 30 seconds
   - Detects when you go online/offline

2. **Name Updates**
   - Online: "Hashir ( Online )"
   - Offline: "Hashir ( Offline )"

3. **Auto-Reply**
   - Sends reply to first message from each user while offline
   - Won't spam - one reply per person
   - Resets when you come back online

4. **Smart Reset**
   - Auto-reply list clears when you:
     - Come back online
     - Send a message yourself

## 🔒 Security

- ✅ Session strings stored securely as environment variables
- ✅ `.env` file excluded from git
- ✅ No hardcoded credentials
- ✅ Docker secrets support
- ✅ Web interface uses secure session management

**Never share your:**
- API_ID and API_HASH
- SESSION_SECRET
- .env file

## 🚀 Deployment Options

### Local (Development)
```bash
python app.py  # Web interface (port 5000)
python main.py # Telegram bot
```

### Docker (Recommended)
```bash
docker-compose up -d
```

### Koyeb (24/7 Cloud)
See [docs/KOYEB_DEPLOYMENT.md](docs/KOYEB_DEPLOYMENT.md)

### Other Platforms
Works on any platform supporting Docker:
- Railway
- Render
- Heroku
- DigitalOcean
- AWS ECS
- Google Cloud Run

## 📊 Resource Requirements

Very lightweight:
- **CPU**: < 0.1 vCPU
- **RAM**: 50-100 MB
- **Storage**: < 100 MB
- **Network**: < 100 MB/month

**Perfect for free tiers!**

## 🛠️ Troubleshooting

### Bot won't start

**Check your environment variables:**
```bash
# Make sure these are set
echo $API_ID
echo $API_HASH
echo $SESSION_SECRET
```

**Verify session string:**
- Should be very long (~300+ characters)
- No line breaks or extra spaces
- Regenerate if needed

### Name doesn't update

**Common causes:**
- Invalid session (regenerate)
- API rate limits (wait a few minutes)
- Telegram server issues (temporary)

**Check the logs:**
```bash
# Docker
docker-compose logs -f

# Python
# Check terminal output
```

### Auto-reply not working

**Verify:**
- You're actually offline (close Telegram on all devices)
- AUTO_REPLY_MESSAGE is set
- Someone messages you first
- Check logs for "Sent auto-reply" messages

## 📝 Customization

### Change Your Name Format

Edit in settings page or `.env`:
```env
BASE_NAME=YourName
```

Bot will use: `YourName ( Online )` / `YourName ( Offline )`

### Change Auto-Reply Message

Edit in settings page or `.env`:
```env
AUTO_REPLY_MESSAGE=Custom message here
```

### Adjust Status Check Interval

Edit `main.py`:
```python
# Check every 30 seconds (default)
await asyncio.sleep(30)

# Change to 60 seconds
await asyncio.sleep(60)
```

## 📚 Documentation

- [Quick Start Guide](docs/QUICK_START.md)
- [Koyeb Deployment](docs/KOYEB_DEPLOYMENT.md)
- [Setup Instructions](docs/SETUP_INSTRUCTIONS.txt)

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use and modify!

## ⚠️ Disclaimer

This is a userbot that runs on your personal Telegram account. Use responsibly:
- Don't spam or abuse Telegram's API
- Respect rate limits
- Follow Telegram's Terms of Service
- Use at your own risk

## 🎯 Roadmap

- [ ] Multiple name templates
- [ ] Scheduled status changes
- [ ] Custom status messages
- [ ] Analytics dashboard
- [ ] Mobile app
- [ ] Multi-account support

## 💡 Tips

1. **Test locally first** before deploying to cloud
2. **Keep your session secure** - treat it like a password
3. **Monitor logs** regularly for any issues
4. **Update dependencies** periodically
5. **Use Docker** for consistent deployments

## 🙋 Support

Having issues? Check these first:
1. Read the [Troubleshooting](#-troubleshooting) section
2. Check [Documentation](docs/)
3. Review your `.env` configuration
4. Verify Telegram API credentials

## ⭐ Show Your Support

If you find this useful, please:
- Give it a star on GitHub ⭐
- Share with friends
- Report bugs
- Suggest features

---

**Made with ❤️ for Telegram users who want smart status updates**

**Current Status**: ✅ Production Ready | 🐳 Docker Compatible | ☁️ Cloud Deployable
