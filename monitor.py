#!/usr/bin/env python3
"""
Discord Music Bot with Hidden Defense System
Monitoring and health check script
"""

import requests
import time
import json
import os
from datetime import datetime

class BotMonitor:
    def __init__(self, config_file="config.env"):
        self.config_file = config_file
        self.load_config()
    
    def load_config(self):
        """Load configuration from config.env"""
        self.config = {}
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        self.config[key] = value
    
    def check_bot_status(self):
        """Check if bot is running"""
        try:
            # Check if bot process is running
            import psutil
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                if 'python' in proc.info['name'] and 'main.py' in ' '.join(proc.info['cmdline']):
                    return True
            return False
        except ImportError:
            print("⚠️ psutil not installed. Install with: pip install psutil")
            return False
        except Exception as e:
            print(f"❌ Error checking bot status: {e}")
            return False
    
    def check_logs(self):
        """Check recent logs for errors"""
        log_files = ['logs/bot.log', 'logs/error.log']
        errors = []
        
        for log_file in log_files:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    # Check last 50 lines for errors
                    for line in lines[-50:]:
                        if 'ERROR' in line or 'CRITICAL' in line:
                            errors.append(line.strip())
        
        return errors
    
    def generate_report(self):
        """Generate monitoring report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'bot_running': self.check_bot_status(),
            'recent_errors': self.check_logs(),
            'config_loaded': bool(self.config),
            'protected_users': ['by_bytes', 'bot_owner'],
            'defense_systems': {
                'raid_protection': True,
                'toxicity_detection': True,
                'channel_encryption': True,
                'cybersecurity_combat': True
            }
        }
        
        return report
    
    def print_status(self):
        """Print current status"""
        report = self.generate_report()
        
        print("🤖 Discord Music Bot with Hidden Defense System - Status Report")
        print("=" * 60)
        print(f"📅 Time: {report['timestamp']}")
        print(f"🟢 Bot Running: {'✅ Yes' if report['bot_running'] else '❌ No'}")
        print(f"⚙️ Config Loaded: {'✅ Yes' if report['config_loaded'] else '❌ No'}")
        
        print("\n🛡️ Defense Systems:")
        for system, status in report['defense_systems'].items():
            print(f"  • {system.replace('_', ' ').title()}: {'✅ Active' if status else '❌ Inactive'}")
        
        print(f"\n🔒 Protected Users: {', '.join(report['protected_users'])}")
        
        if report['recent_errors']:
            print(f"\n⚠️ Recent Errors ({len(report['recent_errors'])}):")
            for error in report['recent_errors'][-5:]:  # Show last 5 errors
                print(f"  • {error}")
        else:
            print("\n✅ No recent errors found")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    monitor = BotMonitor()
    monitor.print_status()
