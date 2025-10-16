#!/usr/bin/env python3
"""
Discord Music Bot with Hidden Defense System
Automatic backup script
"""

import os
import json
import shutil
import gzip
from datetime import datetime
from pathlib import Path

class BackupManager:
    def __init__(self, backup_dir="backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_backup(self, data, backup_type="manual"):
        """Create a backup of the given data"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{backup_type}_backup_{timestamp}.json.gz"
            filepath = self.backup_dir / filename
            
            # Compress and save data
            with gzip.open(filepath, 'wt', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            
            print(f"✅ Backup created: {filename}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return None
    
    def restore_backup(self, backup_file):
        """Restore data from backup file"""
        try:
            with gzip.open(backup_file, 'rt', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"✅ Backup restored: {backup_file}")
            return data
            
        except Exception as e:
            print(f"❌ Error restoring backup: {e}")
            return None
    
    def list_backups(self):
        """List all available backups"""
        backups = []
        for file in self.backup_dir.glob("*.json.gz"):
            stat = file.stat()
            backups.append({
                'filename': file.name,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime),
                'path': str(file)
            })
        
        return sorted(backups, key=lambda x: x['created'], reverse=True)
    
    def cleanup_old_backups(self, keep_days=30):
        """Remove backups older than specified days"""
        try:
            cutoff_date = datetime.now().timestamp() - (keep_days * 24 * 60 * 60)
            removed_count = 0
            
            for file in self.backup_dir.glob("*.json.gz"):
                if file.stat().st_ctime < cutoff_date:
                    file.unlink()
                    removed_count += 1
            
            print(f"✅ Cleaned up {removed_count} old backups")
            return removed_count
            
        except Exception as e:
            print(f"❌ Error cleaning up backups: {e}")
            return 0
    
    def backup_bot_data(self):
        """Backup all bot data"""
        try:
            # Collect all data to backup
            data = {
                'timestamp': datetime.now().isoformat(),
                'backup_type': 'full',
                'bot_version': '1.0.0',
                'data': {
                    'config': self._backup_config(),
                    'logs': self._backup_logs(),
                    'database': self._backup_database(),
                    'files': self._backup_files()
                }
            }
            
            return self.create_backup(data, "full")
            
        except Exception as e:
            print(f"❌ Error backing up bot data: {e}")
            return None
    
    def _backup_config(self):
        """Backup configuration files"""
        config_data = {}
        
        # Backup config.env (without sensitive data)
        if os.path.exists("config.env"):
            with open("config.env", 'r') as f:
                lines = f.readlines()
                # Remove sensitive lines
                safe_lines = []
                for line in lines:
                    if any(key in line.lower() for key in ['token', 'password', 'secret', 'key']):
                        safe_lines.append(line.split('=')[0] + '=***HIDDEN***\n')
                    else:
                        safe_lines.append(line)
                config_data['config_env'] = ''.join(safe_lines)
        
        return config_data
    
    def _backup_logs(self):
        """Backup log files"""
        log_data = {}
        log_files = ['logs/bot.log', 'logs/error.log', 'logs/defense.log']
        
        for log_file in log_files:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    # Get last 1000 lines
                    lines = f.readlines()
                    log_data[log_file] = lines[-1000:] if len(lines) > 1000 else lines
        
        return log_data
    
    def _backup_database(self):
        """Backup database if exists"""
        # This would backup database data if using a database
        return {"message": "Database backup not implemented"}
    
    def _backup_files(self):
        """Backup important files"""
        files_data = {}
        important_files = ['main.py', 'defense_system.py', 'toxicity_analyzer.py', 'advanced_music_system.py']
        
        for file in important_files:
            if os.path.exists(file):
                with open(file, 'r') as f:
                    files_data[file] = f.read()
        
        return files_data

if __name__ == "__main__":
    backup_manager = BackupManager()
    
    print("🔄 Starting backup process...")
    
    # Create full backup
    backup_file = backup_manager.backup_bot_data()
    
    if backup_file:
        print(f"✅ Backup completed: {backup_file}")
        
        # List recent backups
        print("\n📋 Recent backups:")
        backups = backup_manager.list_backups()
        for backup in backups[:5]:
            print(f"  • {backup['filename']} ({backup['size']} bytes)")
        
        # Cleanup old backups
        print("\n🧹 Cleaning up old backups...")
        removed = backup_manager.cleanup_old_backups(keep_days=30)
        print(f"✅ Removed {removed} old backups")
        
    else:
        print("❌ Backup failed")
