-- Discord Music Bot with Hidden Defense System
-- Database schema for persistent data storage

-- Users table for tracking user data
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    display_name VARCHAR(255),
    is_protected BOOLEAN DEFAULT FALSE,
    toxicity_level FLOAT DEFAULT 0.0,
    message_count INTEGER DEFAULT 0,
    toxic_messages INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Guilds table for server data
CREATE TABLE IF NOT EXISTS guilds (
    guild_id BIGINT PRIMARY KEY,
    guild_name VARCHAR(255) NOT NULL,
    owner_id BIGINT,
    is_protected BOOLEAN DEFAULT FALSE,
    defense_active BOOLEAN DEFAULT FALSE,
    last_backup TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Defense logs table
CREATE TABLE IF NOT EXISTS defense_logs (
    id SERIAL PRIMARY KEY,
    guild_id BIGINT NOT NULL,
    action VARCHAR(100) NOT NULL,
    user_id BIGINT,
    details TEXT,
    threat_level INTEGER DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (guild_id) REFERENCES guilds(guild_id)
);

-- Music queue table
CREATE TABLE IF NOT EXISTS music_queue (
    id SERIAL PRIMARY KEY,
    guild_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    track_url TEXT NOT NULL,
    track_title VARCHAR(255),
    track_duration INTEGER,
    position INTEGER NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (guild_id) REFERENCES guilds(guild_id)
);

-- Toxicity history table
CREATE TABLE IF NOT EXISTS toxicity_history (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    message_id BIGINT,
    toxicity_score FLOAT NOT NULL,
    message_preview TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Protected users table
CREATE TABLE IF NOT EXISTS protected_users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    protection_type VARCHAR(50) NOT NULL, -- 'manual', 'server_creator', 'bot_owner'
    added_by BIGINT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_toxicity ON users(toxicity_level);
CREATE INDEX IF NOT EXISTS idx_defense_logs_guild ON defense_logs(guild_id);
CREATE INDEX IF NOT EXISTS idx_defense_logs_timestamp ON defense_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_music_queue_guild ON music_queue(guild_id);
CREATE INDEX IF NOT EXISTS idx_toxicity_history_user ON toxicity_history(user_id);
CREATE INDEX IF NOT EXISTS idx_toxicity_history_timestamp ON toxicity_history(timestamp);

-- Insert default protected user
INSERT INTO protected_users (user_id, username, protection_type) 
VALUES (0, 'by_bytes', 'special') 
ON CONFLICT (user_id) DO NOTHING;
