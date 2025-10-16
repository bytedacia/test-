# 🔒 Sistema di Crittografia Canali - Anti-Raid

## 🎯 **Funzionalità Principale**

Il sistema di crittografia dei canali è progettato per **prevenire raid** nascondendo e crittografando tutti i contenuti del server in caso di emergenza.

## 🚨 **Come Funziona**

### **1. Attivazione Manuale:**
```
Comando: !encrypt_channels
→ Conferma richiesta: !confirm_encrypt
→ Tutti i canali vengono nascosti e crittografati
→ Email di conferma inviata a daciabyte@gmail.com
```

### **2. Attivazione Automatica:**
- **Raid Rilevato** → Crittografia automatica
- **Spam Coordinato** → Crittografia automatica
- **Azioni Distruttive** → Crittografia automatica

## 🔒 **Processo di Crittografia**

### **Step 1: Backup e Preparazione**
- ✅ **Backup Completo** del server creato
- ✅ **Chiave di Crittografia** generata (Fernet)
- ✅ **Dati Canali** salvati (ultimi 100 messaggi per canale)

### **Step 2: Nascondere Canali**
- 🔒 **@everyone** → Accesso negato a tutti i canali
- 🔒 **Tutti i Ruoli** → Permessi revocati
- 🔒 **Solo Bot Owner** → Mantiene accesso (se possibile)

### **Step 3: Crittografia Dati**
- 🔐 **Messaggi** crittografati con Fernet
- 🔐 **Metadati** canali crittografati
- 🔐 **Chiave Sicura** memorizzata in memoria

## 📧 **Controllo via Email**

### **Email di Attivazione:**
```
Oggetto: 🚨 EMERGENCY CHANNEL ENCRYPTION ACTIVATED

EMERGENCY CHANNEL ENCRYPTION ACTIVATED

Server: Nome Server
Guild ID: 123456789
Channels Encrypted: 15
Time: 2024-01-15 14:30:00
Backup Created: backups/123456789_backup_20240115_143000.json
Encryption Key Generated: YES

ALL CHANNELS ARE NOW HIDDEN AND ENCRYPTED!
Use !decrypt_channels command to restore access.

🔓 PER DISATTIVARE:
Rispondi a questa email con "DECRYPT" o usa !decrypt_channels
```

### **Email di Disattivazione:**
```
Oggetto: ✅ CHANNEL DECRYPTION COMPLETED

CHANNEL DECRYPTION COMPLETED

Server: Nome Server
Guild ID: 123456789
Channels Restored: 15
Time: 2024-01-15 14:45:00

ALL CHANNELS HAVE BEEN RESTORED AND DECRYPTED!
```

## 🎛️ **Comandi Disponibili**

### **Comandi di Controllo (Nascosti - Solo Owner):**
- **`!encrypt_channels`** - Avvia processo di crittografia
- **`!confirm_encrypt`** - Conferma crittografia (5 min timeout)
- **`!cancel_encrypt`** - Annulla crittografia in sospeso
- **`!decrypt_channels`** - Decrittografia e ripristino
- **`!encryption_status`** - Stato attuale della crittografia

### **Processo di Conferma:**
```
1. !encrypt_channels → Mostra avviso di sicurezza
2. !confirm_encrypt → Conferma e avvia crittografia
3. !decrypt_channels → Ripristina tutto
```

## 🛡️ **Protezione Anti-Raid**

### **Scenario 1: Raid Bot**
```
14:25 - 20 bot si uniscono
14:25 - Raid rilevato automaticamente
14:25 - Crittografia automatica attivata
14:26 - Tutti i canali nascosti e crittografati
14:26 - Email inviata a daciabyte@gmail.com
```

### **Scenario 2: Raid Umano**
```
14:30 - 15 persone si uniscono in 5 minuti
14:30 - Pattern sospetto rilevato
14:30 - Crittografia automatica attivata
14:31 - Canali protetti, dati al sicuro
```

### **Scenario 3: Attivazione Manuale**
```
14:35 - Proprietario usa !encrypt_channels
14:35 - Conferma con !confirm_encrypt
14:36 - Crittografia completata
14:36 - Email di conferma inviata
```

## 🔓 **Decrittografia e Ripristino**

### **Metodo 1: Comando Discord**
```
!decrypt_channels
→ Ripristina tutti i canali
→ Decrittografia automatica
→ Email di conferma
```

### **Metodo 2: Risposta Email**
```
Rispondi all'email con: "DECRYPT"
→ Il bot leggerà l'email
→ Decrittografia automatica
→ Conferma via Discord
```

### **Processo di Ripristino:**
1. ✅ **Validazione Chiave** - Verifica chiave di crittografia
2. ✅ **Ripristino Visibilità** - Canali tornano visibili
3. ✅ **Decrittografia Dati** - Messaggi ripristinati
4. ✅ **Cleanup Sicuro** - Chiavi e dati temporanei rimossi

## 🔐 **Sicurezza della Crittografia**

### **Algoritmo Utilizzato:**
- **Fernet** - Crittografia simmetrica AES 128
- **Chiave Unica** per ogni attivazione
- **Base64 Encoding** per compatibilità
- **Chiavi in Memoria** - Non salvate su disco

### **Protezioni:**
- ✅ **Chiavi Temporanee** - Eliminate dopo ripristino
- ✅ **Backup Sicuri** - Dati crittografati
- ✅ **Accesso Limitato** - Solo bot owner
- ✅ **Timeout Sicurezza** - Conferme scadono in 5 minuti

## 📊 **Stato del Sistema**

### **Comando: `!encryption_status`**
```
🔒 Stato Crittografia Canali

🚨 Modalità Emergenza: ✅ ATTIVA
🔒 Canali Crittografati: 15
🔑 Chiave Crittografia: ✅ Presente

📋 Canali Crittografati:
• #general (2024-01-15T14:30:00)
• #chat (2024-01-15T14:30:00)
• #rules (2024-01-15T14:30:00)
... e 12 altri
```

## ⚠️ **Importante**

### **Prima dell'Uso:**
- 🚨 **Backup Automatico** - Sempre creato prima della crittografia
- 🔒 **Test in Ambiente Sicuro** - Prova prima su server di test
- 📧 **Email Configurata** - Verifica che daciabyte@gmail.com funzioni

### **Durante l'Uso:**
- ⏱️ **Timeout 5 Minuti** - Conferme scadono automaticamente
- 🔑 **Chiavi in Memoria** - Non perdere l'accesso al bot
- 📧 **Monitor Email** - Controlla le notifiche

### **Dopo l'Uso:**
- ✅ **Verifica Ripristino** - Controlla che tutto funzioni
- 🗑️ **Cleanup Automatico** - Dati temporanei rimossi
- 📧 **Email di Conferma** - Ricevuta per ogni operazione

## 🎯 **Vantaggi del Sistema**

### **Protezione Totale:**
- 🛡️ **Raid Impossibili** - Canali invisibili agli attaccanti
- 🔒 **Dati Sicuri** - Contenuti crittografati
- 📧 **Controllo Remoto** - Gestione via email
- 🔄 **Ripristino Rapido** - Decrittografia in secondi

### **Facilità d'Uso:**
- ⚡ **Un Comando** - `!encrypt_channels` per attivare
- 📱 **Controllo Email** - Gestisci da qualsiasi dispositivo
- 🔄 **Processo Automatico** - Backup e ripristino automatici
- 🎭 **Nascosto** - Invisibile agli utenti normali

**Il sistema di crittografia dei canali offre protezione totale contro raid e attacchi, mantenendo i tuoi dati al sicuro!** 🔒🛡️
