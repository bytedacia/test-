# Protezione Anti-Raid Umano

## 🎯 **Problema Identificato**

Hai ragione! I raid non vengono fatti solo con bot, ma spesso con **account umani coordinati**. Il sistema originale era troppo focalizzato sui bot automatizzati. Ecco come ho aggiornato il sistema per proteggere anche da raid umani.

## 🛡️ **Nuove Funzionalità Anti-Raid Umano**

### **1. Rilevamento di Pattern di Join Coordinati**

```python
# Rileva cluster di join sospetti
def detect_time_clusters(self, timestamps, window):
    # Identifica gruppi di persone che si uniscono insieme
    # Esempio: 10 persone che si uniscono in 2 minuti = sospetto
```

**Come Funziona:**
- **Analisi Temporale**: Rileva quando più persone si uniscono in brevi periodi
- **Clustering**: Identifica gruppi di join sospetti (es. 15 join in 10 minuti)
- **Soglie Intelligenti**: Più di 3 cluster = possibile raid coordinato

### **2. Analisi Pattern di Account**

```python
# Analizza caratteristiche sospette degli account
async def analyze_member_patterns(self, guild, recent_joins):
    # Controlla:
    # - Età dell'account (nuovi account)
    # - Nomi utente simili
    # - Mancanza di personalizzazione profilo
```

**Indicatori di Raid Umano:**
- **Account Nuovi**: Creati negli ultimi 7 giorni
- **Nomi Simili**: Pattern nei nomi utente (es. "RaidUser1", "RaidUser2")
- **Profili Vuoti**: Nessuna immagine profilo, username generico
- **Comportamento Coordinato**: Azioni simili in tempi ravvicinati

### **3. Rilevamento Coordinamento Messaggi**

```python
# Rileva spam coordinato
async def detect_message_coordination(self, guild):
    # Controlla:
    # - Messaggi ripetitivi
    # - Spam di @everyone/@here
    # - Contenuto identico da utenti diversi
```

**Pattern di Messaggio Sospetti:**
- **Spam Ripetitivo**: Stesso messaggio da più utenti
- **Mention Bombing**: Spam di @everyone/@here
- **Contenuto Coordinato**: Messaggi simili in sequenza
- **Timing Sospetto**: Messaggi ravvicinati da account diversi

### **4. Rilevamento Azioni Distruttive Coordinate**

```python
# Monitora azioni distruttive
async def detect_coordinated_actions(self, guild):
    # Rileva:
    # - Eliminazione canali coordinata
    # - Modifica ruoli simultanea
    # - Azioni distruttive multiple
```

**Azioni Monitorate:**
- **Eliminazione Canali**: Più di 3 canali eliminati in 5 minuti
- **Manipolazione Ruoli**: Più di 5 modifiche ruoli simultanee
- **Cambio Permessi**: Modifiche massive ai permessi

## 🚨 **Sistema di Allerta Avanzato**

### **Soglie di Allarme:**
- **15+ join in 10 minuti** = Allerta
- **Più di 3 cluster temporali** = Raid rilevato
- **10+ account sospetti** = Azione richiesta
- **50+ messaggi in 5 minuti** = Spam coordinato

### **Email di Emergenza:**
```
🚨 RAID UMANO RILEVATO
Server: Nome Server
Tipo: Raid Coordinato Umano
Motivo: Multiple join clusters detected
Tempo: 2024-01-15 14:30:00
Membri Sospetti: 23
AZIONE IMMEDIATA RICHIESTA!
```

## 🛠️ **Comandi di Emergenza Aggiornati**

### **`!raid_analysis`** - Analisi Dettagliata
```
🔍 Raid Analysis Report
📊 Recent Activity: Joins (10min): 25, Messages (5min): 150
⚠️ Suspicious Members: New accounts: 18, Total recent: 25
🚨 Risk Level: CRITICAL
```

### **`!emergency_lockdown`** - Lockdown Automatico
- **Ban Automatico**: Banna tutti gli account sospetti (nuovi account)
- **Protezione Canali**: Nasconde immediatamente tutti i canali
- **Email di Emergenza**: Notifica immediata al proprietario
- **Backup Automatico**: Crea backup prima del lockdown

### **`!clear_suspicious_data`** - Reset Dati
- Pulisce tutti i dati di tracking
- Reset delle soglie di allarme
- Permette di ripartire da zero

## 🎭 **Vantaggi del Sistema Nascosto**

### **Per i Raider:**
- **Sembra innocuo**: Il bot appare come semplice bot musicale
- **Non sospettano**: Non si aspettano protezione da un bot musicale
- **Sorpresa**: Quando si attiva la protezione è troppo tardi

### **Per il Proprietario:**
- **Protezione Totale**: Contro bot E raid umani
- **Allerta Immediata**: Email istantanee per ogni minaccia
- **Azioni Automatiche**: Il bot agisce prima che sia troppo tardi
- **Analisi Dettagliata**: Report completi su ogni situazione

## 📊 **Esempi di Rilevamento**

### **Scenario 1: Raid Coordinato**
```
14:25 - 5 persone si uniscono
14:26 - 8 persone si uniscono  
14:27 - 12 persone si uniscono
14:28 - BOT: "Raid coordinato rilevato!"
14:28 - Protezione automatica attivata
14:28 - Email di emergenza inviata
```

### **Scenario 2: Spam Coordinato**
```
14:30 - 50 messaggi identici in 2 minuti
14:31 - BOT: "Spam coordinato rilevato!"
14:31 - Protezione canali attivata
14:31 - Account sospetti bannati automaticamente
```

### **Scenario 3: Distruzione Coordinata**
```
14:35 - Canale #general eliminato
14:36 - Canale #chat eliminato
14:37 - Canale #rules eliminato
14:37 - BOT: "Distruzione coordinata rilevata!"
14:37 - Lockdown di emergenza
14:37 - Backup ripristinato automaticamente
```

## ⚡ **Risposta Automatica**

Il sistema ora risponde **automaticamente** a:

1. **Raid Bot**: Rilevamento rapido join automatizzati
2. **Raid Umano**: Analisi pattern comportamentali
3. **Spam Coordinato**: Rilevamento messaggi ripetitivi
4. **Azioni Distruttive**: Monitoraggio eliminazioni canali/ruoli
5. **Account Sospetti**: Analisi età account e pattern nomi

## 🎯 **Risultato Finale**

Il bot ora è un **sistema di difesa completo** che:

- ✅ **Protegge da bot raid** (sistema originale)
- ✅ **Protegge da raid umani** (nuovo sistema)
- ✅ **Rileva coordinamento** (analisi pattern)
- ✅ **Agisce automaticamente** (protezione istantanea)
- ✅ **Mantiene l'aspetto innocuo** (camuffamento perfetto)

Gli attaccanti non si aspettano mai che un "semplice bot musicale" possa fermare il loro raid coordinato! 🎵🛡️
