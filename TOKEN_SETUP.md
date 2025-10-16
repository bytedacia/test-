# Token Setup Instructions

## Discord Bot Token Configuration

Il token del bot Discord deve essere configurato localmente per sicurezza.

### Passi per configurare il token:

1. **Copia il file di configurazione:**
   ```bash
   copy config.env.github config.env
   ```

2. **Modifica il file config.env:**
   Apri `config.env` e sostituisci:
   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   ```
   
   Con il token fornito dallo sviluppatore

3. **Avvia il bot:**
   ```bash
   python main.py
   ```

### Informazioni del Bot:

- **Application ID**: 1428455175038963876
- **Public Key**: 85aa6f8f2af5ec24fdc6822f57fb734be5fad49008589073d763090cd9cd1ac4
- **Developer ID**: 880170915340644352
- **Protected User**: by_bytes

### Sicurezza:

- Il file `config.env` è escluso da Git per sicurezza
- Il token è presente solo localmente
- GitHub ha bloccato il push del token per protezione

### Comandi di Test:

Una volta avviato il bot, puoi testare:

**Comandi Musica (Visibili a tutti):**
- `!play <link/query>` - Riproduci musica
- `!pause` - Metti in pausa
- `!resume` - Riprendi
- `!skip` - Salta canzone
- `!queue` - Mostra coda
- `!volume <1-100>` - Cambia volume

**Comandi Difesa (Solo per by_bytes):**
- `!defense_status` - Stato sistema difesa
- `!encrypt_channels` - Cripta canali
- `!cybersecurity_status` - Stato cybersecurity
- `!protected_users` - Lista utenti protetti

Il bot è pronto per l'uso! 🎵🛡️
