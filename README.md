# Discord Music Bot with Hidden Defense System

A sophisticated Discord bot that appears to be a normal music bot but includes advanced server protection capabilities.

## Features

### 🎵 Professional Music Features (Visible)
- **Multi-Platform Support**: YouTube, Spotify, SoundCloud, Amazon Music, Apple Music, Deezer, Tidal
- **Advanced Queue Management**: Add, remove, shuffle, clear tracks
- **Professional Controls**: Play, pause, resume, skip, loop, volume
- **Link Security**: Validates all URLs for malicious content
- **High-Quality Audio**: Professional audio streaming with error handling
- **Rate Limiting**: Prevents spam and abuse
- **Smart Search**: Intelligent music discovery across platforms

### 🛡️ Hidden Defense Features
- **Server Backup System**: Automatically creates backups of server structure
- **Raid Protection**: Detects and prevents raid attempts
- **Channel Protection**: Can hide all channels during attacks
- **Toxicity Detection**: Uses AI to detect toxic behavior and assign warning roles
- **Email Alerts**: Sends notifications to developer during security incidents
- **Self-Protection**: Protects bot code from tampering
- **Protected Users System**: Specific users (like "by_bytes") are immune to all restrictions
- **Cybersecurity Combat Mode**: Advanced protection with channel lockdown and permission disabling

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
1. Copy `config.env.github` to `config.env`
2. Add your Discord bot token to `config.env`:
   ```
   DISCORD_TOKEN=your_actual_discord_bot_token_here
   ```
3. Fill in other credentials as needed:
   - Spotify API credentials
   - Gemini AI API key
   - Email settings for alerts
   - Developer User ID (for protection)
   - Discord Application ID and Public Key

**Note:** The `config.env` file is gitignored for security. Use `config.env.github` as a template.

### 3. Discord Bot Setup
1. Go to Discord Developer Portal
2. Create a new application
3. Go to Bot section and create a bot
4. Copy the token to `config.env`
5. Enable all necessary intents

### 4. Spotify Setup
1. Go to Spotify Developer Dashboard
2. Create a new app
3. Get Client ID and Secret
4. Add credentials to `config.env`

### 5. Gemini AI Setup
1. Go to Google AI Studio
2. Create API key
3. Add to `config.env`

### 6. Run the Bot
```bash
python main.py
```

## Commands

### Music Commands (Visible to all users)
- `!play <song/link>` - Play music from any platform
- `!stop` - Stop music and disconnect
- `!skip` - Skip current song
- `!pause` - Pause music
- `!resume` - Resume music
- `!queue` - Show music queue
- `!shuffle` - Shuffle queue
- `!loop` - Toggle loop mode
- `!clear` - Clear queue
- `!remove <position>` - Remove track from queue
- `!volume <0-100>` - Set volume
- `!platforms` - Show supported platforms
- `!help` - Show comprehensive help

### Defense Commands (Hidden - Owner only)
- `!defense_status` - Check defense system status
- `!protect_channels` - Activate channel protection
- `!unprotect_channels` - Deactivate channel protection
- `!restore_server [backup_file]` - Restore server from backup
- `!analyze_toxicity <user>` - Analyze user toxicity level
- `!reset_toxicity <user>` - Reset user toxicity level
- `!raid_analysis` - Analyze current raid situation
- `!emergency_lockdown` - Emergency lockdown (ban suspicious members)
- `!clear_suspicious_data` - Clear tracking data

### Channel Encryption Commands (Hidden - Owner only)
- `!encrypt_channels` - Emergency channel encryption (hide & encrypt all)
- `!confirm_encrypt` - Confirm encryption process
- `!cancel_encrypt` - Cancel pending encryption
- `!decrypt_channels` - Decrypt and restore all channels
- `!encryption_status` - Check encryption status

### Cybersecurity Combat Commands (Hidden - Programmer Only)
- `!cybersecurity_status` - Check cybersecurity combat status
- `!deactivate_cybersecurity` - Deactivate cybersecurity combat mode
- `!combat_logs [limit]` - Show cybersecurity combat logs

### Protected Users Management (Hidden - Programmer Only)
- `!add_protected_user <user>` - Add user to protected list
- `!add_server_creator <user>` - Add server creator to protected list
- `!remove_protected_user <user>` - Remove user from protected list
- `!protected_users` - Show list of all protected users

**Note**: User "by_bytes" is automatically protected and immune to all restrictions.

### Additional Music Commands
- `!shuffle` - Shuffle the music queue
- `!clear` - Clear the music queue (keeps currently playing)

## Security Features

### Automatic Protection
- Monitors server activity 24/7
- Creates automatic backups
- Detects suspicious patterns
- Sends email alerts for threats

### Advanced Raid Detection
- **Bot Raid Detection**: Identifies rapid automated joins
- **Human Raid Detection**: Detects coordinated human attacks
- **Pattern Analysis**: Analyzes join times, usernames, and behavior
- **Account Age Monitoring**: Flags suspicious new accounts
- **Message Coordination**: Detects spam and coordinated messaging

### Toxicity Management
- AI-powered message analysis using Gemini AI
- Automatic role assignment for toxic users
- Gradual warning system
- Risk level categorization

### Raid Prevention & Response
- Real-time member monitoring
- Channel protection system
- Emergency lockdown capabilities
- Automatic suspicious member banning
- Quick restoration options
- Coordinated action detection

### Advanced Channel Encryption
- **Emergency Channel Encryption**: Hide and encrypt all channels during raids
- **Automatic Activation**: Triggers on raid detection
- **Manual Control**: Owner can activate/deactivate anytime
- **Email Control**: Manage encryption via email responses
- **Secure Decryption**: Fernet encryption with unique keys
- **Data Backup**: Automatic backup before encryption

### Cybersecurity Combat System (Programmer Exclusive)
- **Automatic Raid Combat**: Activates when raids are detected
- **Channel Lockdown**: Immediately hides all channels except from programmer
- **Permission Disabling**: Disables all permissions for 60 seconds
- **Countermeasures**: Rate limiting, behavior analysis, pattern detection
- **Auto-Ban System**: Automatically bans suspicious accounts
- **Combat Logging**: Detailed logs of all cybersecurity actions
- **Threat Level Assessment**: Dynamic threat level (1-10) based on attack type

### Protected Users System (Programmer Exclusive)
- **Protected Users**: Specific users protected from all restrictions
- **Server Creators**: Automatic protection for server creators
- **Bot Owner**: Always protected from all restrictions
- **Special User "by_bytes"**: Automatically protected by username , this is creator of bot discord
- 
- **Toxicity Immunity**: Protected users never get toxicity roles
- **Raid Immunity**: Protected users never get banned during raids
- **Permission Immunity**: Protected users keep permissions during lockdown
- **Complete Protection**: Protected from all system restrictions

## Important Notes

⚠️ **This bot is designed for educational and security purposes only.**
- Use responsibly and in accordance with Discord's Terms of Service
- Ensure you have proper permissions before deploying
- Keep your API keys secure and never share them
- The defense features are hidden by design

## Support

For issues or questions, contact the developer through the configured email system.
