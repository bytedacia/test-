#!/usr/bin/env python3
"""
Discord Music Bot with Hidden Defense System
Main entry point for running the bot
"""

import asyncio
import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import and run the bot
from main import main

if __name__ == "__main__":
    try:
        print("🚀 Starting Discord Music Bot with Hidden Defense System...")
        print("🛡️ Defense systems initialized")
        print("🎵 Music system ready")
        print("📧 Email alerts configured")
        print("🔒 Protected users: by_bytes (automatic)")
        print("-" * 50)
        
        # Run the bot
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        sys.exit(1)
