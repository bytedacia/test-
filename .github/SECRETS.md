# GitHub Secrets Configuration

Per configurare il deployment automatico, aggiungi questi secrets nel repository GitHub:

## 🔐 Secrets Richiesti

### Discord Configuration
- `DISCORD_TOKEN` - Token del bot Discord
- `DISCORD_APPLICATION_ID` - 1428455175038963876
- `DISCORD_PUBLIC_KEY` - 85aa6f8f2af5ec24fdc6822f57fb734be5fad49008589073d763090cd9cd1ac4

### Spotify Configuration (Opzionale)
- `SPOTIFY_CLIENT_ID` - Client ID Spotify
- `SPOTIFY_CLIENT_SECRET` - Client Secret Spotify

### Gemini AI Configuration
- `GEMINI_API_KEY` - AIzaSyDAM3XfwTJpJX05xzSZzOR3rkXLWToYhgo

### Email Configuration
- `EMAIL_SMTP_SERVER` - smtp.gmail.com
- `EMAIL_SMTP_PORT` - 587
- `EMAIL_USERNAME` - your_email@gmail.com
- `EMAIL_PASSWORD` - your_app_password
- `ADMIN_EMAIL` - daciabyte@gmail.com

### Developer Configuration
- `DEV_USER_ID` - 880170915340644352

## 📋 Come Aggiungere Secrets

1. Vai su GitHub Repository
2. Clicca su "Settings"
3. Clicca su "Secrets and variables" → "Actions"
4. Clicca su "New repository secret"
5. Aggiungi ogni secret con il nome e valore corrispondente

## ⚠️ Sicurezza

- **NON** committare mai i secrets nel codice
- Usa sempre GitHub Secrets per dati sensibili
- I secrets sono crittografati e accessibili solo durante le Actions
- Ogni secret ha un nome specifico che deve corrispondere esattamente

## 🔄 Deployment Automatico

Una volta configurati i secrets, il deployment avverrà automaticamente ad ogni push sul branch main.

Il bot sarà configurato con:
- ✅ Protezione completa per "by_bytes"
- ✅ Sistema di difesa avanzato
- ✅ Analisi tossicità con Gemini AI
- ✅ Email alert a daciabyte@gmail.com
- ✅ Tutte le funzionalità musicali
