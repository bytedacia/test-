# 📧 Sistema di Allerta Email - daciabyte@gmail.com

## 🎯 **Email di Destinazione Configurata**

Tutte le email di allerta del sistema di difesa vengono inviate a: **`daciabyte@gmail.com`**

## 🚨 **Tipi di Allerta Inviate**

### **1. 🛡️ Allerte di Raid**

#### **Raid Rilevato:**
```
Oggetto: 🚨 RAID DETECTED - EMERGENCY ALERT

RAID DETECTED IN SERVER: Nome Server
REASON: Rapid member joins detected (Bot raid)
TIME: 2024-01-15 14:30:00
GUILD ID: 123456789
BACKUP CREATED: backups/123456789_backup_20240115_143000.json

IMMEDIATE ACTION REQUIRED!
```

#### **Raid Umano Coordinato:**
```
Oggetto: 🚨 RAID DETECTED - EMERGENCY ALERT

RAID DETECTED IN SERVER: Nome Server
REASON: Coordinated human raid detected (Multiple join clusters)
TIME: 2024-01-15 14:30:00
GUILD ID: 123456789
BACKUP CREATED: backups/123456789_backup_20240115_143000.json

IMMEDIATE ACTION REQUIRED!
```

#### **Spam Coordinato:**
```
Oggetto: 🚨 RAID DETECTED - EMERGENCY ALERT

RAID DETECTED IN SERVER: Nome Server
REASON: Coordinated message spam detected
TIME: 2024-01-15 14:30:00
GUILD ID: 123456789
BACKUP CREATED: backups/123456789_backup_20240115_143000.json

IMMEDIATE ACTION REQUIRED!
```

### **2. 🔍 Allerte di Sicurezza**

#### **Link Sospetto Rilevato:**
```
Oggetto: 🚨 SUSPICIOUS LINK DETECTED

Suspicious link detected from UserName (123456789)
Link: https://bit.ly/suspicious-link
Server: Nome Server
Time: 2024-01-15 14:30:00
```

#### **Comando Sospetto:**
```
Oggetto: 🚨 SUSPICIOUS COMMAND DETECTED

Suspicious command detected from user UserName (123456789)
Command: !eval os.system("rm -rf /")
Server: Nome Server
Time: 2024-01-15 14:30:00
```

#### **Modifica File Bot:**
```
Oggetto: 🚨 BOT SECURITY ALERT

The main bot file has been modified. Possible tampering attempt detected!
File: main.py
Time: 2024-01-15 14:30:00
Action: Immediate investigation required
```

### **3. 🛡️ Allerte di Protezione**

#### **Protezione Attivata:**
```
Oggetto: 🚨 PROTECTION ACTIVATED

Channel protection has been activated in server: Nome Server
Time: 2024-01-15 14:30:00
Reason: Manual activation or automatic raid response
```

#### **Protezione Disattivata:**
```
Oggetto: ✅ Protection Deactivated

All protection measures have been deactivated for server: Nome Server
Time: 2024-01-15 14:30:00
```

#### **Lockdown di Emergenza:**
```
Oggetto: 🚨 EMERGENCY LOCKDOWN ACTIVATED

Emergency lockdown activated in Nome Server
Banned 15 suspicious members
Time: 2024-01-15 14:30:00
Action: Server secured, investigation recommended
```

### **4. 🔍 Allerte di Tossicità**

#### **Tossicità Estrema:**
```
Oggetto: 🚨 EXTREME TOXICITY DETECTED

EXTREME TOXICITY ALERT

User: UserName (123456789)
Server: Nome Server
Toxicity Score: 95%
Message: [contenuto del messaggio]
Time: 2024-01-15 14:30:00

IMMEDIATE ACTION REQUIRED!
```

## 📊 **Frequenza delle Allerte**

### **Allerte Immediate (Critiche):**
- ✅ **Raid Rilevati** - Invio istantaneo
- ✅ **Link Sospetti** - Invio istantaneo
- ✅ **Comandi Sospetti** - Invio istantaneo
- ✅ **Modifiche File Bot** - Invio istantaneo
- ✅ **Tossicità Estrema** - Invio istantaneo

### **Allerte Informative:**
- ✅ **Protezione Attivata/Disattivata** - Invio immediato
- ✅ **Lockdown di Emergenza** - Invio immediato
- ✅ **Backup Creati** - Inclusi nelle allerte di raid

## 🔧 **Configurazione Email**

### **Impostazioni SMTP:**
```env
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
ADMIN_EMAIL=daciabyte@gmail.com
```

### **Setup Gmail:**
1. **Abilita 2FA** su Gmail
2. **Genera App Password** per il bot
3. **Usa App Password** invece della password normale
4. **Testa connessione** prima del deployment

## 📱 **Come Ricevere le Allerte**

### **Gmail:**
- ✅ **Notifiche Push** su smartphone
- ✅ **Email immediata** nella inbox
- ✅ **Filtri automatici** per categoria
- ✅ **Etichette personalizzate**

### **Filtri Consigliati:**
```
Filtro 1: "RAID DETECTED" → Etichetta: 🚨 CRITICO
Filtro 2: "SUSPICIOUS" → Etichetta: ⚠️ SICUREZZA  
Filtro 3: "PROTECTION" → Etichetta: 🛡️ PROTEZIONE
Filtro 4: "TOXICITY" → Etichetta: 🔍 TOSSICITÀ
```

## 🚀 **Esempi di Utilizzo**

### **Scenario 1: Raid Bot**
```
14:25 - 20 bot si uniscono al server
14:25 - EMAIL INVIATA a daciabyte@gmail.com
14:25 - Protezione automatica attivata
14:26 - Backup creato automaticamente
```

### **Scenario 2: Raid Umano**
```
14:30 - 15 persone si uniscono in 5 minuti
14:30 - Pattern sospetto rilevato
14:30 - EMAIL INVIATA a daciabyte@gmail.com
14:31 - Lockdown automatico attivato
```

### **Scenario 3: Link Sospetto**
```
14:35 - Utente invia link sospetto
14:35 - Link validato come malevolo
14:35 - EMAIL INVIATA a daciabyte@gmail.com
14:35 - Utente avvisato, link bloccato
```

## ⚠️ **Importante**

### **Email Critiche:**
- 🚨 **Raid** - Azione immediata richiesta
- 🚨 **Sicurezza** - Investigazione necessaria
- 🚨 **Tossicità Estrema** - Moderazione richiesta

### **Email Informative:**
- ✅ **Protezione** - Solo per conferma
- ✅ **Backup** - Solo per tracciamento
- ✅ **Status** - Solo per monitoraggio

## 🎯 **Risultato**

Con `daciabyte@gmail.com` configurato come email di destinazione, riceverai:

- ✅ **Allerte Immediate** per tutte le minacce
- ✅ **Notifiche Push** su smartphone Gmail
- ✅ **Email Strutturate** con tutti i dettagli
- ✅ **Categorizzazione Automatica** per priorità
- ✅ **Tracciamento Completo** di tutte le attività

**Il sistema di difesa ti terrà sempre informato su ogni minaccia al tuo server Discord!** 📧🛡️
