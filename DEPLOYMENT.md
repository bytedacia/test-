# 🚀 Deployment Guide - Discord Music Bot with Hidden Defense System

## 📋 Prerequisiti

- Python 3.8 o superiore
- pip3 installato
- Account Discord con bot token
- Account Spotify (opzionale)
- Account Google per Gemini AI
- Account email per notifiche

## 🔧 Installazione Locale

### 1. Clona il Repository
```bash
git clone https://github.com/bytedacia/test-.git
cd test-
```

### 2. Installa Dipendenze
```bash
# Metodo 1: Usando pip
pip install -r requirements.txt

# Metodo 2: Usando setup.py
python setup.py install

# Metodo 3: Usando deploy script
chmod +x deploy.sh
./deploy.sh
```

### 3. Configurazione
```bash
# Copia il file di configurazione
cp config.env.example config.env

# Modifica config.env con le tue credenziali
nano config.env
```

### 4. Avvio
```bash
# Metodo 1: Script Python
python run_bot.py

# Metodo 2: Script batch (Windows)
start.bat

# Metodo 3: Modulo principale
python main.py
```

## 🐳 Deployment con Docker

### 1. Build dell'Immagine
```bash
docker build -t discord-music-defense-bot .
```

### 2. Avvio con Docker Compose
```bash
docker-compose up -d
```

### 3. Monitoraggio
```bash
# Logs
docker-compose logs -f

# Status
docker-compose ps

# Restart
docker-compose restart
```

## ☁️ Deployment Cloud

### Heroku
1. Crea app su Heroku
2. Connetti repository GitHub
3. Aggiungi variabili d'ambiente
4. Deploy automatico

### Railway
1. Connetti repository
2. Configura variabili d'ambiente
3. Deploy automatico

### DigitalOcean App Platform
1. Crea app
2. Connetti repository
3. Configura build e run commands
4. Deploy

## 🔧 Configurazione Avanzata

### Variabili d'Ambiente
```env
# Discord
DISCORD_TOKEN=your_bot_token
DISCORD_APPLICATION_ID=1428455175038963876
DISCORD_PUBLIC_KEY=85aa6f8f2af5ec24fdc6822f57fb734be5fad49008589073d763090cd9cd1ac4

# Spotify (opzionale)
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret

# Gemini AI
GEMINI_API_KEY=AIzaSyDAM3XfwTJpJX05xzSZzOR3rkXLWToYhgo

# Email
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
ADMIN_EMAIL=daciabyte@gmail.com

# Developer
DEV_USER_ID=880170915340644352
```

### Permessi Discord
- `applications.commands`
- `bot`
- `messages.read`
- `messages.send`
- `voice`
- `manage_channels`
- `manage_roles`
- `ban_members`
- `kick_members`

## 📊 Monitoraggio

### Script di Monitoraggio
```bash
python monitor.py
```

### Log Files
- `logs/bot.log` - Log generali
- `logs/error.log` - Errori
- `logs/defense.log` - Sistema di difesa
- `logs/music.log` - Sistema musicale

### Health Check
```bash
# Controlla status bot
curl http://localhost:8080/health

# Controlla logs
tail -f logs/bot.log
```

## 🛡️ Sicurezza

### Protezione File Sensibili
- `config.env` è nel `.gitignore`
- Usa `config.env.example` come template
- Non committare mai token o chiavi

### Utenti Protetti
- `by_bytes` - Protetto automaticamente
- Bot Owner - Sempre protetto
- Server Creators - Protezione speciale

### Backup Automatici
- Backup creati in `backups/`
- Formato: `guild_id_backup_timestamp.json`
- Ripristino con `!restore_server`

## 🔄 Aggiornamenti

### Aggiornamento Codice
```bash
git pull origin main
pip install -r requirements.txt
python run_bot.py
```

### Aggiornamento Docker
```bash
docker-compose pull
docker-compose up -d
```

## 🆘 Troubleshooting

### Problemi Comuni

1. **Bot non si avvia**
   - Controlla `config.env`
   - Verifica token Discord
   - Controlla logs

2. **Errori di permessi**
   - Verifica permessi bot su server
   - Controlla ruoli e canali

3. **Problemi musicali**
   - Installa FFmpeg
   - Verifica credenziali Spotify
   - Controlla connessione internet

4. **Sistema di difesa non funziona**
   - Verifica email configuration
   - Controlla logs defense
   - Testa comandi nascosti

### Supporto
- GitHub Issues: [https://github.com/bytedacia/test-/issues](https://github.com/bytedacia/test-/issues)
- Email: daciabyte@gmail.com

## 📈 Performance

### Ottimizzazioni
- Usa virtual environment
- Monitora uso memoria
- Configura rate limiting
- Ottimizza database queries

### Metriche
- Uptime bot
- Messaggi processati
- Raid rilevati
- Utenti protetti
- Errori sistema

## 🔐 Sicurezza Avanzata

### Firewall
- Blocca porte non necessarie
- Usa VPN se necessario
- Monitora connessioni

### Backup
- Backup automatici ogni ora
- Backup manuali con comandi
- Ripristino rapido

### Monitoring
- Alert email per errori
- Log rotation
- Performance monitoring

---

**⚠️ Importante**: Questo bot è progettato per scopi educativi e di sicurezza. Usa responsabilmente e in conformità con i Termini di Servizio di Discord.
