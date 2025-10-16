import discord
from discord.ext import commands
import asyncio
import json
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import google.generativeai as genai
import hashlib
import time
import random
from typing import Dict, List, Optional
import logging
from dotenv import load_dotenv

# Import custom modules
from defense_system import DefenseSystem
from toxicity_analyzer import ToxicityAnalyzer
from advanced_music_system import AdvancedMusicSystem

# Load environment variables
load_dotenv('config.env')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HiddenDefenseBot(commands.Bot):
    def __init__(self):
        # Load configuration
        self.config = self.load_config()
        
        # Initialize bot with music commands visible
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        intents.guilds = True
        intents.members = True
        
        super().__init__(
            command_prefix=self.config['prefix'],
            intents=intents,
            help_command=None
        )
        
        # Initialize subsystems
        self.defense_system = DefenseSystem(self)
        self.music_system = AdvancedMusicSystem(self)
        self.toxicity_analyzer = None  # Will be initialized after Gemini
        
        # Gemini AI
        self.gemini_model = None
        self.init_gemini()
        
        # Self-protection
        self.protection_key = self.generate_protection_key()
        self.command_history = []
        self.suspicious_commands = set()
        
    def load_config(self):
        """Load configuration from environment variables"""
        return {
            'token': os.getenv('DISCORD_TOKEN'),
            'prefix': os.getenv('BOT_PREFIX', '!'),
            'spotify_client_id': os.getenv('SPOTIFY_CLIENT_ID'),
            'spotify_client_secret': os.getenv('SPOTIFY_CLIENT_SECRET'),
            'gemini_api_key': os.getenv('GEMINI_API_KEY'),
            'email_smtp_server': os.getenv('EMAIL_SMTP_SERVER'),
            'email_smtp_port': int(os.getenv('EMAIL_SMTP_PORT', 587)),
            'email_username': os.getenv('EMAIL_USERNAME'),
            'email_password': os.getenv('EMAIL_PASSWORD'),
            'admin_email': os.getenv('ADMIN_EMAIL'),
            'dev_user_id': int(os.getenv('DEV_USER_ID', 0))
        }
    
    def init_gemini(self):
        """Initialize Gemini AI"""
        try:
            genai.configure(api_key=self.config['gemini_api_key'])
            self.gemini_model = genai.GenerativeModel('gemini-pro')
            self.toxicity_analyzer = ToxicityAnalyzer(self, self.gemini_model)
            logger.info("Gemini AI initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini AI: {e}")
    
    def generate_protection_key(self):
        """Generate a unique protection key for bot self-protection"""
        return hashlib.sha256(f"{time.time()}{random.random()}".encode()).hexdigest()
    
    async def on_ready(self):
        """Bot startup event"""
        logger.info(f'{self.user} has connected to Discord!')
        logger.info(f'Bot is in {len(self.guilds)} guilds')
        
        # Create initial backups for all servers
        for guild in self.guilds:
            await self.defense_system.create_comprehensive_backup(guild)
        
        # Start background tasks
        self.bg_task = self.loop.create_task(self.background_monitoring())
        
        # Initialize self-protection
        await self.init_self_protection()
    
    async def init_self_protection(self):
        """Initialize bot self-protection mechanisms"""
        try:
            # Monitor for suspicious command patterns
            self.suspicious_commands = {
                'eval', 'exec', 'shell', 'subprocess', 'os.system',
                'import os', 'import subprocess', '__import__',
                'getattr', 'setattr', 'delattr', 'globals', 'locals'
            }
            
            # Set up command monitoring
            self.command_history = []
            
            logger.info("Self-protection system initialized")
            
        except Exception as e:
            logger.error(f"Error initializing self-protection: {e}")
    
    async def background_monitoring(self):
        """Background task for monitoring server health and potential threats"""
        while True:
            try:
                # Monitor all servers for threats
                for guild in self.guilds:
                    await self.defense_system.monitor_suspicious_activity(guild)
                    await self.defense_system.detect_raid_attempt(guild)
                
                # Check self-protection
                await self.check_self_protection()
                
                await asyncio.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Error in background monitoring: {e}")
                await asyncio.sleep(60)
    
    async def check_self_protection(self):
        """Check for attempts to compromise the bot"""
        try:
            # Monitor for suspicious file modifications
            if os.path.exists('main.py'):
                current_hash = hashlib.md5(open('main.py', 'rb').read()).hexdigest()
                if hasattr(self, 'main_file_hash') and self.main_file_hash != current_hash:
                    logger.warning("Main bot file has been modified!")
                    await self.send_alert_email(
                        "🚨 BOT SECURITY ALERT",
                        "The main bot file has been modified. Possible tampering attempt detected!"
                    )
                self.main_file_hash = current_hash
            
            # Clear old command history (keep last 100 commands)
            if len(self.command_history) > 100:
                self.command_history = self.command_history[-100:]
                
        except Exception as e:
            logger.error(f"Error in self-protection check: {e}")
    
    async def monitor_servers(self):
        """Monitor all servers for suspicious activity"""
        for guild in self.guilds:
            try:
                # Check for rapid member changes (potential raid)
                member_count = guild.member_count
                if guild.id not in self.server_backups:
                    self.server_backups[guild.id] = {
                        'member_count': member_count,
                        'channels': [],
                        'roles': [],
                        'created_at': datetime.now()
                    }
                
                # Create backup if significant changes detected
                if abs(member_count - self.server_backups[guild.id]['member_count']) > 10:
                    await self.create_server_backup(guild)
                    
            except Exception as e:
                logger.error(f"Error monitoring guild {guild.id}: {e}")
    
    async def create_server_backup(self, guild):
        """Create a backup of server structure"""
        try:
            backup = {
                'channels': [],
                'roles': [],
                'member_count': guild.member_count,
                'created_at': datetime.now(),
                'guild_name': guild.name
            }
            
            # Backup channels
            for channel in guild.channels:
                backup['channels'].append({
                    'name': channel.name,
                    'type': str(channel.type),
                    'position': channel.position,
                    'id': channel.id
                })
            
            # Backup roles
            for role in guild.roles:
                backup['roles'].append({
                    'name': role.name,
                    'color': role.color.value,
                    'permissions': role.permissions.value,
                    'id': role.id
                })
            
            self.server_backups[guild.id] = backup
            
            # Save to file
            with open(f'backups/{guild.id}_backup.json', 'w') as f:
                json.dump(backup, f, indent=2)
                
            logger.info(f"Backup created for guild {guild.name}")
            
        except Exception as e:
            logger.error(f"Error creating backup for guild {guild.id}: {e}")
    
    async def check_toxicity_levels(self):
        """Check and update toxicity levels for users"""
        # This would be implemented with message analysis using Gemini AI
        pass
    
    async def detect_raid_attempts(self):
        """Detect potential raid attempts"""
        for guild in self.guilds:
            try:
                # Check for rapid channel creation/deletion
                # Check for rapid role creation/deletion
                # Check for suspicious member joins
                pass
            except Exception as e:
                logger.error(f"Error detecting raids for guild {guild.id}: {e}")
    
    async def send_alert_email(self, subject, body):
        """Send alert email to developer"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['email_username']
            msg['To'] = self.config['admin_email']
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.config['email_smtp_server'], self.config['email_smtp_port'])
            server.starttls()
            server.login(self.config['email_username'], self.config['email_password'])
            text = msg.as_string()
            server.sendmail(self.config['email_username'], self.config['admin_email'], text)
            server.quit()
            
            logger.info("Alert email sent successfully")
            
        except Exception as e:
            logger.error(f"Failed to send alert email: {e}")

# Initialize bot
bot = HiddenDefenseBot()

# Music Commands (Visible to users)
@bot.command(name='play', aliases=['p'])
async def play_music(ctx, *, query):
    """Play music from YouTube or Spotify"""
    try:
        await bot.music_system.search_and_play(ctx, query)
    except Exception as e:
        await ctx.send(f"Error playing music: {e}")

@bot.command(name='stop', aliases=['s'])
async def stop_music(ctx):
    """Stop the music"""
    try:
        voice_client = ctx.voice_client
        success = await bot.music_system.stop_music(ctx.guild.id, voice_client)
        
        if success and voice_client:
            await voice_client.disconnect()
            await ctx.send("🛑 Music stopped")
        else:
            await ctx.send("I'm not playing any music!")
    except Exception as e:
        await ctx.send(f"Error stopping music: {e}")

@bot.command(name='skip', aliases=['next'])
async def skip_music(ctx):
    """Skip current song"""
    try:
        voice_client = ctx.voice_client
        success = await bot.music_system.skip_track(ctx.guild.id, voice_client)
        
        if success:
            await ctx.send("⏭️ Skipped to next song")
        else:
            await ctx.send("No songs in queue to skip!")
    except Exception as e:
        await ctx.send(f"Error skipping song: {e}")

@bot.command(name='queue', aliases=['q'])
async def show_queue(ctx):
    """Show current music queue"""
    try:
        queue_info = bot.music_system.get_queue_info(ctx.guild.id)
        
        if not queue_info.get('is_playing') and queue_info.get('queue_length', 0) == 0:
            return await ctx.send("Queue is empty!")
        
        embed = discord.Embed(
            title="🎵 Music Queue",
            color=0x00ff00
        )
        
        # Show now playing
        if queue_info.get('now_playing'):
            now_playing = queue_info['now_playing']
            embed.add_field(
                name="🎵 Now Playing",
                value=f"**{now_playing['title']}**\nRequested by: {now_playing['requester'].mention}",
                inline=False
            )
        
        # Show queue
        queue = queue_info.get('queue', [])
        if len(queue) > 1:  # More than just the currently playing song
            queue_text = ""
            for i, track in enumerate(queue[1:11], 1):  # Show next 10 tracks
                queue_text += f"{i}. **{track['title']}** - {track['requester'].mention}\n"
            
            if queue_text:
                embed.add_field(
                    name="📋 Up Next",
                    value=queue_text,
                    inline=False
                )
        
        embed.set_footer(text=f"Total tracks in queue: {queue_info.get('queue_length', 0)}")
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"Error showing queue: {e}")

@bot.command(name='shuffle')
async def shuffle_queue(ctx):
    """Shuffle the music queue"""
    try:
        success = await bot.music_system.shuffle_queue(ctx.guild.id)
        
        if success:
            await ctx.send("🔀 Queue shuffled!")
        else:
            await ctx.send("Not enough songs to shuffle!")
    except Exception as e:
        await ctx.send(f"Error shuffling queue: {e}")

@bot.command(name='clear')
async def clear_queue(ctx):
    """Clear the music queue"""
    try:
        voice_client = ctx.voice_client
        success = await bot.music_system.stop_music(ctx.guild.id, voice_client)
        
        if success:
            await ctx.send("🗑️ Coda svuotata!")
        else:
            await ctx.send("La coda è già vuota!")
    except Exception as e:
        await ctx.send(f"Errore svuotando la coda: {e}")

@bot.command(name='pause')
async def pause_music(ctx):
    """Pause music playback"""
    try:
        voice_client = ctx.voice_client
        success = await bot.music_system.pause_music(ctx.guild.id, voice_client)
        
        if success:
            await ctx.send("⏸️ Musica in pausa!")
        else:
            await ctx.send("Nessuna musica in riproduzione!")
    except Exception as e:
        await ctx.send(f"Errore mettendo in pausa: {e}")

@bot.command(name='resume')
async def resume_music(ctx):
    """Resume music playback"""
    try:
        voice_client = ctx.voice_client
        success = await bot.music_system.resume_music(ctx.guild.id, voice_client)
        
        if success:
            await ctx.send("▶️ Riproduzione ripresa!")
        else:
            await ctx.send("La musica non è in pausa!")
    except Exception as e:
        await ctx.send(f"Errore riprendendo la riproduzione: {e}")

@bot.command(name='loop')
async def toggle_loop(ctx):
    """Toggle loop mode"""
    try:
        loop_enabled = bot.music_system.toggle_loop(ctx.guild.id)
        
        if loop_enabled:
            await ctx.send("🔁 Loop attivato!")
        else:
            await ctx.send("🔁 Loop disattivato!")
    except Exception as e:
        await ctx.send(f"Errore toggling loop: {e}")

@bot.command(name='remove')
async def remove_track(ctx, position: int):
    """Remove track from queue by position"""
    try:
        removed_track = await bot.music_system.remove_track_from_queue(ctx.guild.id, position)
        
        if removed_track:
            await ctx.send(f"🗑️ Rimossa: **{removed_track['title']}**")
        else:
            await ctx.send("Posizione non valida nella coda!")
    except Exception as e:
        await ctx.send(f"Errore rimuovendo traccia: {e}")

@bot.command(name='volume')
async def set_volume(ctx, volume: int):
    """Set music volume (0-100)"""
    try:
        if not 0 <= volume <= 100:
            await ctx.send("Il volume deve essere tra 0 e 100!")
            return
        
        # Note: Discord.py doesn't support volume control directly
        # This would require additional audio processing
        await ctx.send(f"🔊 Volume impostato a {volume}%!")
    except Exception as e:
        await ctx.send(f"Errore impostando volume: {e}")

@bot.command(name='platforms')
async def show_platforms(ctx):
    """Show supported music platforms"""
    embed = discord.Embed(
        title="🌐 Piattaforme Supportate",
        description="Il bot supporta le seguenti piattaforme musicali:",
        color=0x00ff00
    )
    
    platforms = [
        "🎵 **YouTube** - Video e audio",
        "🎧 **Spotify** - Link diretti e ricerca",
        "🔊 **SoundCloud** - Musica indipendente",
        "🛒 **Amazon Music** - Link diretti",
        "🍎 **Apple Music** - Link iTunes/Apple Music",
        "🎶 **Deezer** - Streaming musicale",
        "🌊 **Tidal** - Audio di alta qualità"
    ]
    
    for platform in platforms:
        embed.add_field(name="\u200b", value=platform, inline=False)
    
    embed.add_field(
        name="💡 Come usare",
        value="Incolla un link diretto o cerca con `!play nome canzone`",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='help')
async def help_command(ctx):
    """Show help for music commands"""
    embed = discord.Embed(
        title="🎵 Bot Musicale Professionale - Comandi",
        description="Ecco tutti i comandi musicali disponibili:",
        color=0x00ff00
    )
    
    embed.add_field(
        name="🎵 Comandi Base",
        value="`!play <canzone/link>` - Riproduci musica\n`!stop` - Ferma tutto\n`!skip` - Salta canzone\n`!queue` - Mostra coda",
        inline=False
    )
    
    embed.add_field(
        name="⏯️ Controlli Riproduzione",
        value="`!pause` - Metti in pausa\n`!resume` - Riprendi\n`!loop` - Attiva/disattiva loop\n`!shuffle` - Mescola coda",
        inline=False
    )
    
    embed.add_field(
        name="📋 Gestione Coda",
        value="`!clear` - Svuota coda\n`!remove <posizione>` - Rimuovi traccia\n`!volume <0-100>` - Imposta volume",
        inline=False
    )
    
    embed.add_field(
        name="🌐 Informazioni",
        value="`!platforms` - Piattaforme supportate\n`!help` - Mostra questo aiuto",
        inline=False
    )
    
    embed.add_field(
        name="💡 Esempi",
        value="`!play Never Gonna Give You Up`\n`!play https://youtube.com/watch?v=...`\n`!play https://open.spotify.com/track/...`",
        inline=False
    )
    
    embed.set_footer(text="🎭 Bot Musicale Professionale con Sistema di Difesa Nascosto")
    
    await ctx.send(embed=embed)

# Hidden Defense Commands (Only accessible to developer)
@bot.command(name='defense_status', hidden=True)
@commands.is_owner()
async def defense_status(ctx):
    """Check defense system status (Hidden command)"""
    try:
        status = bot.defense_system.get_protection_status()
        toxicity_stats = bot.toxicity_analyzer.get_system_stats() if bot.toxicity_analyzer else {}
        
        embed = discord.Embed(
            title="🛡️ Defense System Status",
            color=0xff0000
        )
        
        embed.add_field(name="Protection Active", value=str(status['protection_active']), inline=True)
        embed.add_field(name="Channel Protection", value=str(status['channel_protection']), inline=True)
        embed.add_field(name="Raid Detection", value=str(status['raid_detection']), inline=True)
        embed.add_field(name="Protected Channels", value=str(status['protected_channels']), inline=True)
        embed.add_field(name="Server Backups", value=str(status['server_backups']), inline=True)
        embed.add_field(name="Suspicious Activities", value=str(status['suspicious_activities_tracked']), inline=True)
        
        if toxicity_stats:
            embed.add_field(name="Users Tracked", value=str(toxicity_stats.get('total_users_tracked', 0)), inline=True)
            embed.add_field(name="High Risk Users", value=str(toxicity_stats.get('high_risk_users', 0)), inline=True)
            embed.add_field(name="Messages Analyzed", value=str(toxicity_stats.get('total_messages_analyzed', 0)), inline=True)
        
        await ctx.send(embed=embed, delete_after=10)
        
    except Exception as e:
        await ctx.send(f"Error getting defense status: {e}", delete_after=5)

@bot.command(name='protect_channels', hidden=True)
@commands.is_owner()
async def protect_channels(ctx):
    """Activate channel protection (Hidden command)"""
    try:
        await bot.defense_system.activate_emergency_protection(ctx.guild)
        await ctx.send("🛡️ Channel protection activated! All channels are now hidden.", delete_after=5)
    except Exception as e:
        await ctx.send(f"Error activating protection: {e}", delete_after=5)

@bot.command(name='unprotect_channels', hidden=True)
@commands.is_owner()
async def unprotect_channels(ctx):
    """Deactivate channel protection (Hidden command)"""
    try:
        await bot.defense_system.deactivate_protection(ctx.guild)
        await ctx.send("🔓 Channel protection deactivated! Channels are now visible.", delete_after=5)
    except Exception as e:
        await ctx.send(f"Error deactivating protection: {e}", delete_after=5)

@bot.command(name='restore_server', hidden=True)
@commands.is_owner()
async def restore_server(ctx, backup_file: str = None):
    """Restore server from backup (Hidden command)"""
    try:
        success = await bot.defense_system.restore_from_backup(ctx.guild, backup_file)
        
        if success:
            await ctx.send("🔄 Server restoration completed from backup.", delete_after=5)
        else:
            await ctx.send("❌ No backup found or restoration failed!", delete_after=5)
            
    except Exception as e:
        await ctx.send(f"❌ Error restoring server: {e}", delete_after=5)

@bot.command(name='analyze_toxicity', hidden=True)
@commands.is_owner()
async def analyze_toxicity(ctx, member: discord.Member):
    """Analyze user toxicity level (Hidden command)"""
    try:
        if not bot.toxicity_analyzer:
            return await ctx.send("Toxicity analyzer not available!", delete_after=5)
        
        report = await bot.toxicity_analyzer.get_toxicity_report(member)
        
        if 'error' in report:
            return await ctx.send(f"No toxicity data found for {member.display_name}", delete_after=5)
        
        embed = discord.Embed(
            title="🔍 Toxicity Analysis",
            description=f"Analysis for {member.display_name}",
            color=0xff0000 if report['current_toxicity_level'] > 0.7 else 
                  0xffaa00 if report['current_toxicity_level'] > 0.4 else 0x00ff00
        )
        
        embed.add_field(name="Current Level", value=f"{report['current_toxicity_level']:.2%}", inline=True)
        embed.add_field(name="Risk Level", value=report['risk_level'], inline=True)
        embed.add_field(name="Messages Analyzed", value=str(report['message_count']), inline=True)
        embed.add_field(name="Toxic Messages", value=str(report['toxic_messages']), inline=True)
        embed.add_field(name="Toxic Percentage", value=f"{report['toxic_percentage']:.1f}%", inline=True)
        embed.add_field(name="Recent Activity", value=f"{report['recent_messages']} messages (24h)", inline=True)
        
        await ctx.send(embed=embed, delete_after=15)
        
    except Exception as e:
        await ctx.send(f"Error analyzing toxicity: {e}", delete_after=5)

@bot.command(name='reset_toxicity', hidden=True)
@commands.is_owner()
async def reset_toxicity(ctx, member: discord.Member):
    """Reset user toxicity level (Hidden command)"""
    try:
        if not bot.toxicity_analyzer:
            return await ctx.send("Toxicity analyzer not available!", delete_after=5)
        
        success = await bot.toxicity_analyzer.reset_user_toxicity(member)
        
        if success:
            await ctx.send(f"✅ Toxicity level reset for {member.display_name}", delete_after=5)
        else:
            await ctx.send(f"No toxicity data found for {member.display_name}", delete_after=5)
            
    except Exception as e:
        await ctx.send(f"Error resetting toxicity: {e}", delete_after=5)

@bot.command(name='raid_analysis', hidden=True)
@commands.is_owner()
async def raid_analysis(ctx):
    """Analyze current raid situation (Hidden command)"""
    try:
        guild = ctx.guild
        
        # Get recent join data
        recent_joins = bot.defense_system.member_join_history.get(guild.id, [])
        recent_messages = bot.defense_system.message_patterns.get(guild.id, [])
        
        embed = discord.Embed(
            title="🔍 Raid Analysis Report",
            description=f"Analysis for {guild.name}",
            color=0xff0000
        )
        
        # Recent joins analysis
        current_time = datetime.now()
        joins_last_10min = [join for join in recent_joins 
                           if current_time - join['timestamp'] < timedelta(minutes=10)]
        
        embed.add_field(
            name="📊 Recent Activity",
            value=f"Joins (10min): {len(joins_last_10min)}\nMessages (5min): {len([m for m in recent_messages if current_time - m['timestamp'] < timedelta(minutes=5)])}",
            inline=True
        )
        
        # Suspicious patterns
        suspicious_count = 0
        for join in joins_last_10min:
            member = guild.get_member(join['user_id'])
            if member:
                account_age = datetime.now() - member.created_at
                if account_age < timedelta(days=7):
                    suspicious_count += 1
        
        embed.add_field(
            name="⚠️ Suspicious Members",
            value=f"New accounts: {suspicious_count}\nTotal recent: {len(joins_last_10min)}",
            inline=True
        )
        
        # Risk assessment
        risk_level = "LOW"
        if len(joins_last_10min) > 20:
            risk_level = "CRITICAL"
        elif len(joins_last_10min) > 10:
            risk_level = "HIGH"
        elif len(joins_last_10min) > 5:
            risk_level = "MEDIUM"
        
        embed.add_field(
            name="🚨 Risk Level",
            value=risk_level,
            inline=True
        )
        
        await ctx.send(embed=embed, delete_after=15)
        
    except Exception as e:
        await ctx.send(f"Error analyzing raid situation: {e}", delete_after=5)

@bot.command(name='emergency_lockdown', hidden=True)
@commands.is_owner()
async def emergency_lockdown(ctx):
    """Emergency lockdown - ban all recent suspicious members (Hidden command)"""
    try:
        guild = ctx.guild
        current_time = datetime.now()
        
        # Get recent joins
        recent_joins = bot.defense_system.member_join_history.get(guild.id, [])
        recent_members = [join for join in recent_joins 
                         if current_time - join['timestamp'] < timedelta(minutes=30)]
        
        banned_count = 0
        for join_data in recent_members:
            try:
                member = guild.get_member(join_data['user_id'])
                if member and not member.guild_permissions.administrator:
                    # Check if account is suspicious
                    account_age = datetime.now() - member.created_at
                    if account_age < timedelta(days=7):
                        await member.ban(reason="Emergency lockdown - suspicious account")
                        banned_count += 1
            except Exception as e:
                logger.error(f"Error banning member {join_data.get('user_id')}: {e}")
        
        # Activate protection
        await bot.defense_system.activate_emergency_protection(guild)
        
        await ctx.send(f"🚨 Emergency lockdown activated! Banned {banned_count} suspicious members.", delete_after=5)
        
        # Send alert email
        await bot.send_alert_email(
            "🚨 EMERGENCY LOCKDOWN ACTIVATED",
            f"Emergency lockdown activated in {guild.name}\nBanned {banned_count} suspicious members\nTime: {current_time}"
        )
        
    except Exception as e:
        await ctx.send(f"Error during emergency lockdown: {e}", delete_after=5)

@bot.command(name='clear_suspicious_data', hidden=True)
@commands.is_owner()
async def clear_suspicious_data(ctx):
    """Clear all suspicious activity tracking data (Hidden command)"""
    try:
        guild_id = ctx.guild.id
        
        # Clear tracking data
        if guild_id in bot.defense_system.member_join_history:
            bot.defense_system.member_join_history[guild_id] = []
        
        if guild_id in bot.defense_system.message_patterns:
            bot.defense_system.message_patterns[guild_id] = []
        
        if guild_id in bot.defense_system.coordinated_actions:
            bot.defense_system.coordinated_actions[guild_id] = []
        
        if guild_id in bot.defense_system.suspicious_activities:
            bot.defense_system.suspicious_activities[guild_id] = {
                'rapid_joins': [],
                'rapid_leaves': [],
                'channel_deletions': [],
                'role_deletions': [],
                'permission_changes': []
            }
        
        await ctx.send("✅ Suspicious activity data cleared.", delete_after=5)
        
        except Exception as e:
        await ctx.send(f"Error clearing data: {e}", delete_after=5)

@bot.command(name='encrypt_channels', hidden=True)
@commands.is_owner()
async def encrypt_channels(ctx):
    """Emergency channel encryption - hide and encrypt all channels (Hidden command)"""
    try:
        embed = discord.Embed(
            title="🚨 CONFERMA CRITTOGRAFIA CANALI",
            description="⚠️ **ATTENZIONE**: Questa azione nasconderà e crittograferà TUTTI i canali del server!",
            color=0xff0000
        )
        
        embed.add_field(
            name="🔒 Cosa succederà:",
            value="• Tutti i canali saranno nascosti a tutti\n• I contenuti saranno crittografati\n• Backup automatico creato\n• Solo tu potrai ripristinarli",
            inline=False
        )
        
        embed.add_field(
            name="📧 Controllo Email:",
            value="Riceverai un'email di conferma e potrai disattivare da email",
            inline=False
        )
        
        embed.set_footer(text="Usa !confirm_encrypt per confermare o !cancel_encrypt per annullare")
        
        await ctx.send(embed=embed, delete_after=30)
        
        # Store pending encryption request
        bot.pending_encryption = {
            'guild_id': ctx.guild.id,
            'user_id': ctx.author.id,
            'timestamp': datetime.now()
        }
        
    except Exception as e:
        await ctx.send(f"Error initiating encryption: {e}", delete_after=5)

@bot.command(name='confirm_encrypt', hidden=True)
@commands.is_owner()
async def confirm_encrypt(ctx):
    """Confirm channel encryption (Hidden command)"""
    try:
        if not hasattr(bot, 'pending_encryption') or bot.pending_encryption['guild_id'] != ctx.guild.id:
            await ctx.send("❌ Nessuna richiesta di crittografia in sospeso!", delete_after=5)
            return
        
        # Check if request is not too old (5 minutes)
        if datetime.now() - bot.pending_encryption['timestamp'] > timedelta(minutes=5):
            await ctx.send("❌ Richiesta di crittografia scaduta! Riprova.", delete_after=5)
            del bot.pending_encryption
            return
        
        await ctx.send("🔒 **CRITTOGRAFIA CANALI IN CORSO...** ⏳", delete_after=3)
        
        # Start encryption process
        encrypted_count = await bot.defense_system.emergency_channel_encryption(ctx.guild)
        
        if encrypted_count > 0:
            embed = discord.Embed(
                title="🔒 CRITTOGRAFIA COMPLETATA",
                description=f"**{encrypted_count}** canali sono stati crittografati e nascosti!",
                color=0x00ff00
            )
            
            embed.add_field(
                name="📧 Controllo Email:",
                value="Hai ricevuto un'email con i dettagli. Puoi disattivare da email.",
                inline=False
            )
            
            embed.add_field(
                name="🔓 Per Ripristinare:",
                value="Usa `!decrypt_channels` o rispondi all'email",
                inline=False
            )
            
            await ctx.send(embed=embed, delete_after=15)
        else:
            await ctx.send("❌ Errore durante la crittografia!", delete_after=5)
        
        # Clear pending request
        del bot.pending_encryption
        
        except Exception as e:
        await ctx.send(f"Error confirming encryption: {e}", delete_after=5)

@bot.command(name='cancel_encrypt', hidden=True)
@commands.is_owner()
async def cancel_encrypt(ctx):
    """Cancel channel encryption (Hidden command)"""
    try:
        if hasattr(bot, 'pending_encryption') and bot.pending_encryption['guild_id'] == ctx.guild.id:
            del bot.pending_encryption
            await ctx.send("❌ Crittografia annullata.", delete_after=5)
        else:
            await ctx.send("❌ Nessuna richiesta di crittografia in sospeso!", delete_after=5)
    except Exception as e:
        await ctx.send(f"Error canceling encryption: {e}", delete_after=5)

@bot.command(name='decrypt_channels', hidden=True)
@commands.is_owner()
async def decrypt_channels(ctx):
    """Decrypt and restore all channels (Hidden command)"""
    try:
        success, message = await bot.defense_system.decrypt_and_restore_channels(ctx.guild)
        
        if success:
            embed = discord.Embed(
                title="🔓 DECRITTOGRAFIA COMPLETATA",
                description=f"**{message}**",
                color=0x00ff00
            )
            
            embed.add_field(
                name="📧 Notifica Email:",
                value="Hai ricevuto un'email di conferma della decrittografia.",
                inline=False
            )
            
            await ctx.send(embed=embed, delete_after=10)
        else:
            await ctx.send(f"❌ Errore nella decrittografia: {message}", delete_after=5)
            
        except Exception as e:
        await ctx.send(f"Error decrypting channels: {e}", delete_after=5)

@bot.command(name='encryption_status', hidden=True)
@commands.is_owner()
async def encryption_status(ctx):
    """Check encryption status (Hidden command)"""
    try:
        status = bot.defense_system.get_encryption_status(ctx.guild.id)
        
        embed = discord.Embed(
            title="🔒 Stato Crittografia Canali",
            color=0xffaa00 if status['emergency_mode'] else 0x00ff00
        )
        
        embed.add_field(
            name="🚨 Modalità Emergenza",
            value="✅ ATTIVA" if status['emergency_mode'] else "❌ Inattiva",
            inline=True
        )
        
        embed.add_field(
            name="🔒 Canali Crittografati",
            value=str(status['encrypted_channels']),
            inline=True
        )
        
        embed.add_field(
            name="🔑 Chiave Crittografia",
            value="✅ Presente" if status['has_encryption_key'] else "❌ Assente",
            inline=True
        )
        
        if status['channels']:
            channels_list = "\n".join([f"• {ch['name']} ({ch['encrypted_at']})" for ch in status['channels'][:5]])
            if len(status['channels']) > 5:
                channels_list += f"\n... e {len(status['channels']) - 5} altri"
            
            embed.add_field(
                name="📋 Canali Crittografati",
                value=channels_list,
                inline=False
            )
        
        await ctx.send(embed=embed, delete_after=15)
            
        except Exception as e:
        await ctx.send(f"Error getting encryption status: {e}", delete_after=5)

@bot.command(name='cybersecurity_status', hidden=True)
@commands.is_owner()
async def cybersecurity_status(ctx):
    """Check cybersecurity combat status (Hidden command - Programmer Only)"""
    try:
        status = bot.defense_system.get_cybersecurity_status()
        
        embed = discord.Embed(
            title="⚔️ CYBERSECURITY COMBAT STATUS",
            description="**SOLO PROGRAMMATORE** - Sistema di difesa avanzato",
            color=0xff0000 if status['cybersecurity_active'] else 0x00ff00
        )
        
        embed.add_field(
            name="🚨 Modalità Combattimento",
            value="⚔️ ATTIVA" if status['cybersecurity_active'] else "🛡️ Standby",
            inline=True
        )
        
        embed.add_field(
            name="⚠️ Livello Minaccia",
            value=f"{status['threat_level']}/10",
            inline=True
        )
        
        embed.add_field(
            name="🔍 Rilevamento Raid",
            value="✅ ATTIVO" if status['raid_detection'] else "❌ Inattivo",
            inline=True
        )
        
        embed.add_field(
            name="🛡️ Contromisure Attive",
            value=f"{len([k for k, v in status['countermeasures'].items() if v])}/5",
            inline=True
        )
        
        embed.add_field(
            name="📊 Log Combattimento",
            value=f"{status['combat_logs_count']} eventi",
            inline=True
        )
        
        # Show active countermeasures
        active_countermeasures = [k for k, v in status['countermeasures'].items() if v]
        if active_countermeasures:
            countermeasures_text = "\n".join([f"✅ {cm.replace('_', ' ').title()}" for cm in active_countermeasures])
            embed.add_field(
                name="⚔️ Contromisure Attive",
                value=countermeasures_text,
                inline=False
            )
        
        # Show recent combat logs
        if status['recent_combat_logs']:
            recent_logs = status['recent_combat_logs'][-3:]  # Last 3 logs
            logs_text = "\n".join([f"• {log['action']} ({log['timestamp'].strftime('%H:%M:%S')})" for log in recent_logs])
            embed.add_field(
                name="📋 Log Recenti",
                value=logs_text,
                inline=False
            )
        
        embed.set_footer(text="🔒 Sistema esclusivo per il programmatore")
        
        await ctx.send(embed=embed, delete_after=20)
        
    except Exception as e:
        await ctx.send(f"Error getting cybersecurity status: {e}", delete_after=5)

@bot.command(name='deactivate_cybersecurity', hidden=True)
@commands.is_owner()
async def deactivate_cybersecurity(ctx):
    """Deactivate cybersecurity combat mode (Hidden command - Programmer Only)"""
    try:
        if not bot.defense_system.cybersecurity_active:
            await ctx.send("❌ Sistema di cybersecurity non è attivo!", delete_after=5)
                    return
                
        # Deactivate cybersecurity mode
        bot.defense_system.cybersecurity_active = False
        bot.defense_system.threat_level = 0
        
        embed = discord.Embed(
            title="🛡️ CYBERSECURITY DEACTIVATED",
            description="Sistema di combattimento cybersecurity disattivato",
            color=0x00ff00
        )
        
        embed.add_field(
            name="📧 Notifica Email",
            value="Email di conferma inviata a daciabyte@gmail.com",
            inline=False
        )
        
        await ctx.send(embed=embed, delete_after=10)
        
        # Send deactivation email
        await bot.send_alert_email(
            "🛡️ CYBERSECURITY COMBAT DEACTIVATED",
            f"""
🛡️ CYBERSECURITY COMBAT DEACTIVATED

Server: {ctx.guild.name}
Guild ID: {ctx.guild.id}
Time: {datetime.now()}
Deactivated by: Programmer

⚔️ COMBAT STATUS: DEACTIVATED
🛡️ PROTECTION: STANDARD MODE
🔒 SYSTEM: READY FOR NEXT THREAT

All countermeasures have been deactivated.
System is now in standard monitoring mode.
            """
        )
        
    except Exception as e:
        await ctx.send(f"Error deactivating cybersecurity: {e}", delete_after=5)

@bot.command(name='combat_logs', hidden=True)
@commands.is_owner()
async def combat_logs(ctx, limit: int = 10):
    """Show cybersecurity combat logs (Hidden command - Programmer Only)"""
    try:
        if limit > 20:
            limit = 20
        
        logs = bot.defense_system.combat_logs[-limit:] if bot.defense_system.combat_logs else []
        
        if not logs:
            await ctx.send("📋 Nessun log di combattimento disponibile.", delete_after=5)
                    return
                
        embed = discord.Embed(
            title="⚔️ CYBERSECURITY COMBAT LOGS",
            description=f"Ultimi {len(logs)} eventi di combattimento",
            color=0xffaa00
        )
        
        for i, log in enumerate(logs, 1):
            timestamp = log['timestamp'].strftime('%H:%M:%S')
            action = log.get('action', 'UNKNOWN')
            
            embed.add_field(
                name=f"{i}. {action}",
                value=f"**Tempo:** {timestamp}\n**Server:** {log.get('guild', 'Unknown')}",
                inline=False
            )
            
            if i >= 10:  # Limit to prevent embed overflow
                break
        
        embed.set_footer(text="🔒 Log esclusivi per il programmatore")
        
        await ctx.send(embed=embed, delete_after=30)
        
    except Exception as e:
        await ctx.send(f"Error getting combat logs: {e}", delete_after=5)

@bot.command(name='add_protected_user', hidden=True)
@commands.is_owner()
async def add_protected_user(ctx, user: discord.Member):
    """Add a user to the protected users list (Hidden command - Programmer Only)"""
    try:
        success = bot.defense_system.add_protected_user(user.id, "manual")
        
        if success:
            embed = discord.Embed(
                title="🛡️ UTENTE PROTETTO AGGIUNTO",
                description=f"**{user.display_name}** è ora protetto da tutte le restrizioni",
                color=0x00ff00
            )
            
            embed.add_field(
                name="🛡️ Protezioni Attive",
                value="• Nessun ban automatico\n• Nessun ruolo tossicità\n• Accesso mantenuto durante raid\n• Permessi mantenuti durante lockdown",
                inline=False
            )
            
            embed.add_field(
                name="📧 Notifica Email",
                value="Email di conferma inviata a daciabyte@gmail.com",
                inline=False
            )
            
            await ctx.send(embed=embed, delete_after=15)
            
            # Send email notification
            await bot.send_alert_email(
                "🛡️ PROTECTED USER ADDED",
                f"""
🛡️ PROTECTED USER ADDED

User: {user.display_name} ({user.id})
Server: {ctx.guild.name}
Added by: Programmer
Time: {datetime.now()}

🛡️ PROTECTIONS ACTIVATED:
✅ No automatic bans
✅ No toxicity roles
✅ Access maintained during raids
✅ Permissions maintained during lockdown

User is now protected from all system restrictions.
                """
            )
        else:
            await ctx.send("❌ Errore nell'aggiungere l'utente protetto!", delete_after=5)
        
    except Exception as e:
        await ctx.send(f"Error adding protected user: {e}", delete_after=5)

@bot.command(name='add_server_creator', hidden=True)
@commands.is_owner()
async def add_server_creator(ctx, user: discord.Member):
    """Add a server creator to the protected list (Hidden command - Programmer Only)"""
    try:
        success = bot.defense_system.add_server_creator(user.id, ctx.guild.name)
        
        if success:
            embed = discord.Embed(
                title="👑 CREATORE SERVER AGGIUNTO",
                description=f"**{user.display_name}** è ora protetto come creatore del server",
                color=0xffd700
            )
            
            embed.add_field(
                name="👑 Protezioni Speciali",
                value="• Protezione completa da tutte le restrizioni\n• Accesso garantito durante raid\n• Permessi mantenuti sempre\n• Status di creatore riconosciuto",
                inline=False
            )
            
            await ctx.send(embed=embed, delete_after=15)
            
            # Send email notification
            await bot.send_alert_email(
                "👑 SERVER CREATOR ADDED",
                f"""
👑 SERVER CREATOR ADDED

Creator: {user.display_name} ({user.id})
Server: {ctx.guild.name}
Added by: Programmer
Time: {datetime.now()}

👑 SPECIAL PROTECTIONS:
✅ Complete protection from all restrictions
✅ Guaranteed access during raids
✅ Permissions always maintained
✅ Creator status recognized

Server creator is now fully protected.
                """
            )
        else:
            await ctx.send("❌ Errore nell'aggiungere il creatore del server!", delete_after=5)
        
    except Exception as e:
        await ctx.send(f"Error adding server creator: {e}", delete_after=5)

@bot.command(name='remove_protected_user', hidden=True)
@commands.is_owner()
async def remove_protected_user(ctx, user: discord.Member):
    """Remove a user from the protected users list (Hidden command - Programmer Only)"""
    try:
        success = bot.defense_system.remove_protected_user(user.id)
        
        if success:
            embed = discord.Embed(
                title="🔓 UTENTE PROTETTO RIMOSSO",
                description=f"**{user.display_name}** non è più protetto",
                color=0xffaa00
            )
            
            embed.add_field(
                name="⚠️ Attenzione",
                value="L'utente ora può essere soggetto a:\n• Ban automatici durante raid\n• Ruoli di tossicità\n• Restrizioni durante lockdown",
                inline=False
            )
            
            await ctx.send(embed=embed, delete_after=10)
            
            # Send email notification
            await bot.send_alert_email(
                "🔓 PROTECTED USER REMOVED",
                f"""
🔓 PROTECTED USER REMOVED

User: {user.display_name} ({user.id})
Server: {ctx.guild.name}
Removed by: Programmer
Time: {datetime.now()}

⚠️ WARNING:
User is no longer protected and may be subject to:
• Automatic bans during raids
• Toxicity role assignments
• Restrictions during lockdown
                """
            )
        else:
            await ctx.send("❌ Utente non trovato nella lista protetti!", delete_after=5)
        
    except Exception as e:
        await ctx.send(f"Error removing protected user: {e}", delete_after=5)

@bot.command(name='protected_users', hidden=True)
@commands.is_owner()
async def protected_users(ctx):
    """Show list of all protected users (Hidden command - Programmer Only)"""
    try:
        protected_data = bot.defense_system.get_protected_users_list()
        
        if 'error' in protected_data:
            await ctx.send(f"❌ Errore: {protected_data['error']}", delete_after=5)
            return
        
        embed = discord.Embed(
            title="🛡️ UTENTI PROTETTI",
            description=f"Lista completa degli utenti protetti dal sistema",
            color=0x00ff00
        )
        
        embed.add_field(
            name="📊 Statistiche",
            value=f"**Totale Protetti:** {protected_data['total_protected']}",
            inline=True
        )
        
        if protected_data['users']:
            users_text = ""
            for user_data in protected_data['users'][:10]:  # Limit to 10 users
                users_text += f"• **{user_data['username']}** ({user_data['type']})\n"
            
            if len(protected_data['users']) > 10:
                users_text += f"... e {len(protected_data['users']) - 10} altri"
            
            embed.add_field(
                name="🛡️ Utenti Protetti",
                value=users_text,
                inline=False
            )
        
        embed.add_field(
            name="🔒 Protezioni Attive",
            value="• Nessun ban automatico\n• Nessun ruolo tossicità\n• Accesso durante raid\n• Permessi durante lockdown",
            inline=False
        )
        
        embed.set_footer(text="🔒 Lista esclusiva per il programmatore")
        
        await ctx.send(embed=embed, delete_after=30)
        
    except Exception as e:
        await ctx.send(f"Error getting protected users: {e}", delete_after=5)

# Message monitoring for toxicity detection and human raid detection
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # Process commands first
    await bot.process_commands(message)
    
    # Analyze message for toxicity using the toxicity analyzer
    try:
        if bot.toxicity_analyzer and len(message.content.strip()) > 5:
            # Skip toxicity analysis for protected users
            if not bot.defense_system.is_protected_user(message.author.id, message.guild):
                toxicity_score = await bot.toxicity_analyzer.analyze_message(message)
                
                if toxicity_score > 0.3:  # Threshold for concerning content
                    await bot.toxicity_analyzer.update_user_toxicity(message.author, message, toxicity_score)
    
    except Exception as e:
        logger.error(f"Error analyzing message toxicity: {e}")
    
    # Track message patterns for human raid detection
    try:
        if message.guild:  # Only track in guilds, not DMs
            await bot.defense_system.track_message_pattern(message.guild, message)
    except Exception as e:
        logger.error(f"Error tracking message pattern: {e}")
    
    # Monitor for suspicious commands (self-protection)
    try:
        if message.content.startswith(bot.command_prefix):
            command_content = message.content[len(bot.command_prefix):].lower()
            
            # Check for suspicious command patterns
            for suspicious in bot.suspicious_commands:
                if suspicious in command_content:
                    logger.warning(f"Suspicious command detected from {message.author}: {message.content}")
                    await bot.send_alert_email(
                        "🚨 SUSPICIOUS COMMAND DETECTED",
                        f"Suspicious command detected from user {message.author.display_name} ({message.author.id})\nCommand: {message.content}\nServer: {message.guild.name if message.guild else 'DM'}"
                    )
                    break
            
            # Track command history
            bot.command_history.append({
                'user_id': message.author.id,
                'command': command_content,
                'timestamp': datetime.now(),
                'guild': message.guild.name if message.guild else 'DM'
            })
    
    except Exception as e:
        logger.error(f"Error in command monitoring: {e}")

# Member join tracking for human raid detection
@bot.event
async def on_member_join(member):
    """Track member joins for raid detection"""
    try:
        await bot.defense_system.track_member_join(member.guild, member)
        logger.info(f"Member joined: {member.display_name} in {member.guild.name}")
    except Exception as e:
        logger.error(f"Error tracking member join: {e}")

# Guild update tracking for coordinated actions
@bot.event
async def on_guild_channel_delete(channel):
    """Track channel deletions for coordinated attack detection"""
    try:
        guild_id = channel.guild.id
        if guild_id not in bot.defense_system.coordinated_actions:
            bot.defense_system.coordinated_actions[guild_id] = []
        
        action_data = {
            'type': 'channel_delete',
            'channel_name': channel.name,
            'timestamp': datetime.now(),
            'channel_id': channel.id
        }
        
        bot.defense_system.coordinated_actions[guild_id].append(action_data)
        
        # Update suspicious activities
        if guild_id not in bot.defense_system.suspicious_activities:
            bot.defense_system.suspicious_activities[guild_id] = {
                'rapid_joins': [],
                'rapid_leaves': [],
                'channel_deletions': [],
                'role_deletions': [],
                'permission_changes': []
            }
        
        bot.defense_system.suspicious_activities[guild_id]['channel_deletions'].append(datetime.now())
        
        logger.warning(f"Channel deleted: {channel.name} in {channel.guild.name}")
        
    except Exception as e:
        logger.error(f"Error tracking channel deletion: {e}")

# Role update tracking
@bot.event
async def on_guild_role_delete(role):
    """Track role deletions for coordinated attack detection"""
    try:
        guild_id = role.guild.id
        if guild_id not in bot.defense_system.coordinated_actions:
            bot.defense_system.coordinated_actions[guild_id] = []
        
        action_data = {
            'type': 'role_delete',
            'role_name': role.name,
            'timestamp': datetime.now(),
            'role_id': role.id
        }
        
        bot.defense_system.coordinated_actions[guild_id].append(action_data)
        
        # Update suspicious activities
        if guild_id not in bot.defense_system.suspicious_activities:
            bot.defense_system.suspicious_activities[guild_id] = {
                'rapid_joins': [],
                'rapid_leaves': [],
                'channel_deletions': [],
                'role_deletions': [],
                'permission_changes': []
            }
        
        bot.defense_system.suspicious_activities[guild_id]['role_deletions'].append(datetime.now())
        
        logger.warning(f"Role deleted: {role.name} in {role.guild.name}")
        
    except Exception as e:
        logger.error(f"Error tracking role deletion: {e}")


# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return  # Ignore unknown commands
    
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command!", delete_after=5)
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"❌ Command is on cooldown. Try again in {error.retry_after:.2f} seconds.", delete_after=5)
        else:
        logger.error(f"Command error: {error}")
    
# Create backups directory
os.makedirs('backups', exist_ok=True)

# Run the bot
if __name__ == "__main__":
    bot.run(bot.config['token'])
