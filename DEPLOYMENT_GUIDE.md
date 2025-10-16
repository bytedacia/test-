# Discord Bot Deployment Guide

## Quick Start

### 1. Prerequisites
- Python 3.8 or higher
- Discord Bot Token
- Spotify API credentials (optional)
- Gemini AI API key
- Email account for alerts

### 2. Installation

1. **Clone or download the bot files**
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot:**
   ```bash
   cp config.env.example config.env
   # Edit config.env with your credentials
   ```

4. **Run the bot:**
   ```bash
   python main.py
   ```
   Or on Windows:
   ```bash
   start.bat
   ```

## Detailed Setup

### Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and create a bot
4. Copy the token and add it to `config.env`
5. Enable these intents:
   - Message Content Intent
   - Server Members Intent
   - Presence Intent

### Spotify Setup (Optional)

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Get Client ID and Client Secret
4. Add credentials to `config.env`

### Gemini AI Setup

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Add to `config.env`

### Email Setup

1. Use Gmail with App Password:
   - Enable 2FA on Gmail
   - Generate App Password
   - Use App Password in `config.env`

2. Or use other SMTP providers:
   - Update SMTP server and port in `config.env`

## File Structure

```
discord-bot/
├── main.py                 # Main bot file
├── defense_system.py       # Defense system module
├── toxicity_analyzer.py    # Toxicity analysis module
├── music_system.py         # Music system module
├── requirements.txt        # Python dependencies
├── config.env             # Configuration file
├── config.env.example     # Configuration template
├── start.bat              # Windows startup script
├── README.md              # Documentation
├── DEPLOYMENT_GUIDE.md    # This file
└── backups/               # Server backups (auto-created)
```

## Security Features

### Automatic Protection
- **24/7 Monitoring**: Continuously monitors server for threats
- **Auto Backups**: Creates backups when suspicious activity detected
- **Raid Detection**: Detects rapid member joins/channel deletions
- **Email Alerts**: Sends immediate notifications for threats

### Toxicity Management
- **AI Analysis**: Uses Gemini AI to analyze message toxicity
- **Role Assignment**: Automatically assigns warning roles
- **Risk Levels**: Categorizes users by risk level
- **Detailed Reports**: Provides comprehensive user analysis

### Self-Protection
- **Code Monitoring**: Detects file modifications
- **Command Filtering**: Blocks suspicious commands
- **Alert System**: Notifies developer of tampering attempts

## Usage

### Music Commands (Visible to all users)
- `!play <song>` - Play music from YouTube/Spotify
- `!stop` - Stop music and disconnect
- `!skip` - Skip current song
- `!queue` - Show music queue
- `!shuffle` - Shuffle queue
- `!clear` - Clear queue
- `!help` - Show help

### Defense Commands (Hidden - Owner only)
- `!defense_status` - Check system status
- `!protect_channels` - Activate channel protection
- `!unprotect_channels` - Deactivate channel protection
- `!restore_server` - Restore from backup
- `!analyze_toxicity <user>` - Analyze user
- `!reset_toxicity <user>` - Reset user toxicity

## Troubleshooting

### Common Issues

1. **Bot won't start:**
   - Check Discord token is correct
   - Verify all required intents are enabled
   - Check Python version (3.8+)

2. **Music not playing:**
   - Install FFmpeg: https://ffmpeg.org/download.html
   - Check voice channel permissions
   - Verify internet connection

3. **Toxicity analysis not working:**
   - Check Gemini API key is valid
   - Verify API quotas not exceeded
   - Check internet connection

4. **Email alerts not working:**
   - Verify email credentials
   - Check SMTP settings
   - Use App Password for Gmail

### Logs
- Check console output for error messages
- Logs are written to console
- Check `backups/` folder for server backups

## Advanced Configuration

### Customizing Protection
Edit `defense_system.py` to modify:
- Raid detection thresholds
- Backup frequency
- Protection triggers

### Customizing Toxicity Analysis
Edit `toxicity_analyzer.py` to modify:
- Toxicity thresholds
- Role names and colors
- Analysis prompts

### Customizing Music Features
Edit `music_system.py` to modify:
- Audio quality settings
- Queue limits
- Search behavior

## Security Notes

⚠️ **Important Security Considerations:**

1. **Keep credentials secure**: Never share your config.env file
2. **Use App Passwords**: For Gmail, use App Passwords instead of regular passwords
3. **Monitor logs**: Regularly check for suspicious activity
4. **Update regularly**: Keep dependencies updated
5. **Backup data**: Regular backups of the bot files and server data

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review console logs for errors
3. Verify all credentials are correct
4. Check Discord API status

## Legal Notice

This bot is designed for educational and security purposes. Users are responsible for:
- Complying with Discord's Terms of Service
- Respecting server rules and member privacy
- Using the bot responsibly and ethically
- Ensuring proper permissions before deployment
