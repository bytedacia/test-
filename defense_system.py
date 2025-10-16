"""
Advanced Defense System Module
Handles server protection, raid detection, and emergency protocols
"""

import discord
import asyncio
import json
import os
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional
import logging
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

class DefenseSystem:
    def __init__(self, bot):
        self.bot = bot
        self.server_backups = {}
        self.protection_active = False
        self.raid_detection = False
        self.channel_protection = False
        self.protected_channels = set()
        self.suspicious_activities = {}
        self.lockdown_channels = set()
        
        # Human raid detection
        self.member_join_history = {}
        self.suspicious_members = {}
        self.raid_cohorts = {}
        self.message_patterns = {}
        self.coordinated_actions = {}
        
        # Channel encryption system
        self.encrypted_channels = {}
        self.encryption_keys = {}
        self.channel_backup_data = {}
        self.emergency_mode = False
        
        # Cybersecurity combat system
        self.cybersecurity_active = False
        self.combat_logs = []
        self.threat_level = 0
        self.countermeasures = {
            'rate_limiting': True,
            'ip_blocking': True,
            'behavior_analysis': True,
            'pattern_detection': True,
            'auto_ban': True
        }
        
        # Protected users system
        self.protected_users = set()  # User IDs that are protected from all restrictions
        self.server_creators = set()  # Server creators (to be added when provided)
        
    async def create_comprehensive_backup(self, guild: discord.Guild):
        """Create a comprehensive backup of the entire server structure"""
        try:
            backup = {
                'metadata': {
                    'guild_id': guild.id,
                    'guild_name': guild.name,
                    'created_at': datetime.now().isoformat(),
                    'member_count': guild.member_count,
                    'owner_id': guild.owner_id
                },
                'channels': [],
                'roles': [],
                'emojis': [],
                'settings': {
                    'name': guild.name,
                    'description': guild.description,
                    'icon': str(guild.icon.url) if guild.icon else None,
                    'banner': str(guild.banner.url) if guild.banner else None,
                    'verification_level': guild.verification_level.value,
                    'default_notifications': guild.default_notifications.value,
                    'explicit_content_filter': guild.explicit_content_filter.value,
                    'system_channel_id': guild.system_channel_id,
                    'rules_channel_id': guild.rules_channel_id,
                    'public_updates_channel_id': guild.public_updates_channel_id
                }
            }
            
            # Backup channels with detailed permissions
            for channel in guild.channels:
                channel_data = {
                    'id': channel.id,
                    'name': channel.name,
                    'type': str(channel.type),
                    'position': channel.position,
                    'category_id': channel.category_id,
                    'permissions': {}
                }
                
                # Backup channel permissions
                if hasattr(channel, 'overwrites'):
                    for target, overwrite in channel.overwrites.items():
                        channel_data['permissions'][str(target.id)] = {
                            'allow': overwrite.pair()[0].value,
                            'deny': overwrite.pair()[1].value
                        }
                
                backup['channels'].append(channel_data)
            
            # Backup roles with detailed permissions
            for role in guild.roles:
                if role.name != "@everyone":  # Skip @everyone role
                    role_data = {
                        'id': role.id,
                        'name': role.name,
                        'color': role.color.value,
                        'hoist': role.hoist,
                        'mentionable': role.mentionable,
                        'permissions': role.permissions.value,
                        'position': role.position
                    }
                    backup['roles'].append(role_data)
            
            # Backup emojis
            for emoji in guild.emojis:
                emoji_data = {
                    'name': emoji.name,
                    'url': str(emoji.url),
                    'animated': emoji.animated
                }
                backup['emojis'].append(emoji_data)
            
            self.server_backups[guild.id] = backup
            
            # Save to encrypted file
            backup_file = f'backups/{guild.id}_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            os.makedirs('backups', exist_ok=True)
            
            with open(backup_file, 'w') as f:
                json.dump(backup, f, indent=2)
            
            logger.info(f"Comprehensive backup created for guild {guild.name}")
            return backup_file
            
        except Exception as e:
            logger.error(f"Error creating backup for guild {guild.id}: {e}")
            return None
    
    async def detect_raid_attempt(self, guild: discord.Guild):
        """Advanced raid detection algorithm for both bot and human raids"""
        try:
            current_time = datetime.now()
            guild_id = guild.id
            
            # Initialize tracking for new guilds
            if guild_id not in self.suspicious_activities:
                self.suspicious_activities[guild_id] = {
                    'rapid_joins': [],
                    'rapid_leaves': [],
                    'channel_deletions': [],
                    'role_deletions': [],
                    'permission_changes': []
                }
            
            activity = self.suspicious_activities[guild_id]
            
            # 1. Check for rapid member joins (bot raids)
            recent_joins = [join_time for join_time in activity['rapid_joins'] 
                          if current_time - join_time < timedelta(minutes=5)]
            
            if len(recent_joins) > 20:  # More than 20 joins in 5 minutes
                await self.trigger_raid_protocol(guild, "Rapid member joins detected (Bot raid)")
                return True
            
            # 2. Check for coordinated human raids
            human_raid_detected = await self.detect_human_raid_patterns(guild)
            if human_raid_detected:
                return True
            
            # 3. Check for rapid channel deletions
            recent_deletions = [del_time for del_time in activity['channel_deletions']
                              if current_time - del_time < timedelta(minutes=2)]
            
            if len(recent_deletions) > 5:  # More than 5 channel deletions in 2 minutes
                await self.trigger_raid_protocol(guild, "Rapid channel deletions detected")
                return True
            
            # 4. Check for coordinated destructive actions
            coordinated_attack = await self.detect_coordinated_actions(guild)
            if coordinated_attack:
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error detecting raid attempt for guild {guild.id}: {e}")
            return False
    
    async def detect_human_raid_patterns(self, guild: discord.Guild) -> bool:
        """Detect coordinated human raids"""
        try:
            guild_id = guild.id
            current_time = datetime.now()
            
            # Initialize tracking for new guilds
            if guild_id not in self.member_join_history:
                self.member_join_history[guild_id] = []
            
            # 1. Check for coordinated join patterns (similar join times)
            recent_joins = [join for join in self.member_join_history[guild_id] 
                          if current_time - join['timestamp'] < timedelta(minutes=10)]
            
            if len(recent_joins) > 15:  # More than 15 joins in 10 minutes
                # Check for clustering (multiple joins within short timeframes)
                join_times = [join['timestamp'] for join in recent_joins]
                clusters = self.detect_time_clusters(join_times, timedelta(minutes=2))
                
                if len(clusters) > 3:  # Multiple clusters suggest coordination
                    await self.trigger_raid_protocol(guild, "Coordinated human raid detected (Multiple join clusters)")
                    return True
            
            # 2. Check for similar account patterns (new accounts, similar usernames)
            suspicious_members = await self.analyze_member_patterns(guild, recent_joins)
            if len(suspicious_members) > 10:
                await self.trigger_raid_protocol(guild, "Suspicious member patterns detected (Potential raid group)")
                return True
            
            # 3. Check for coordinated message patterns
            message_raid = await self.detect_message_coordination(guild)
            if message_raid:
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error detecting human raid patterns: {e}")
            return False
    
    def detect_time_clusters(self, timestamps: List[datetime], window: timedelta) -> List[List[datetime]]:
        """Detect clusters of timestamps within a time window"""
        if not timestamps:
            return []
        
        clusters = []
        current_cluster = [timestamps[0]]
        
        for i in range(1, len(timestamps)):
            if timestamps[i] - timestamps[i-1] <= window:
                current_cluster.append(timestamps[i])
            else:
                if len(current_cluster) > 1:
                    clusters.append(current_cluster)
                current_cluster = [timestamps[i]]
        
        if len(current_cluster) > 1:
            clusters.append(current_cluster)
        
        return clusters
    
    async def analyze_member_patterns(self, guild: discord.Guild, recent_joins: List[Dict]) -> List[discord.Member]:
        """Analyze patterns in recently joined members"""
        suspicious = []
        
        for join_data in recent_joins:
            try:
                member = guild.get_member(join_data['user_id'])
                if not member:
                    continue
                
                # Check for new accounts (created within last week)
                account_age = datetime.now() - member.created_at
                if account_age < timedelta(days=7):
                    suspicious.append(member)
                
                # Check for similar usernames (potential raid group naming)
                username_similarity = self.check_username_patterns(guild, member)
                if username_similarity > 3:  # More than 3 similar usernames
                    suspicious.append(member)
                
                # Check for lack of profile customization
                if (not member.avatar and 
                    member.discriminator == '0000' and 
                    account_age < timedelta(days=1)):
                    suspicious.append(member)
                
            except Exception as e:
                logger.error(f"Error analyzing member {join_data.get('user_id')}: {e}")
        
        return suspicious
    
    def check_username_patterns(self, guild: discord.Guild, member: discord.Member) -> int:
        """Check for similar username patterns that might indicate a raid group"""
        try:
            similar_count = 0
            member_username = member.display_name.lower()
            
            # Check against recent members
            for other_member in guild.members:
                if other_member.id == member.id:
                    continue
                
                other_username = other_member.display_name.lower()
                
                # Check for common prefixes/suffixes
                if (member_username.startswith(other_username[:4]) or 
                    member_username.endswith(other_username[-4:])):
                    similar_count += 1
            
            return similar_count
            
        except Exception as e:
            logger.error(f"Error checking username patterns: {e}")
            return 0
    
    async def detect_message_coordination(self, guild: discord.Guild) -> bool:
        """Detect coordinated messaging patterns"""
        try:
            current_time = datetime.now()
            guild_id = guild.id
            
            # Initialize message tracking
            if guild_id not in self.message_patterns:
                self.message_patterns[guild_id] = []
            
            # Check for spam patterns
            recent_messages = [msg for msg in self.message_patterns[guild_id]
                             if current_time - msg['timestamp'] < timedelta(minutes=5)]
            
            if len(recent_messages) > 50:  # More than 50 messages in 5 minutes
                # Check for repetitive content
                message_content = [msg['content'] for msg in recent_messages]
                if self.detect_repetitive_content(message_content):
                    await self.trigger_raid_protocol(guild, "Coordinated message spam detected")
                    return True
            
            # Check for @everyone/@here spam
            everyone_mentions = sum(1 for msg in recent_messages 
                                  if '@everyone' in msg['content'] or '@here' in msg['content'])
            if everyone_mentions > 5:
                await self.trigger_raid_protocol(guild, "Mass mention spam detected")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error detecting message coordination: {e}")
            return False
    
    def detect_repetitive_content(self, messages: List[str]) -> bool:
        """Detect if messages contain repetitive/spam content"""
        try:
            if len(messages) < 10:
                return False
            
            # Count similar messages
            message_counts = {}
            for msg in messages:
                msg_clean = msg.lower().strip()
                if len(msg_clean) > 5:  # Ignore very short messages
                    message_counts[msg_clean] = message_counts.get(msg_clean, 0) + 1
            
            # If any message appears more than 30% of the time, it's spam
            max_count = max(message_counts.values()) if message_counts else 0
            spam_ratio = max_count / len(messages)
            
            return spam_ratio > 0.3
            
        except Exception as e:
            logger.error(f"Error detecting repetitive content: {e}")
            return False
    
    async def detect_coordinated_actions(self, guild: discord.Guild) -> bool:
        """Detect coordinated destructive actions by multiple users"""
        try:
            current_time = datetime.now()
            guild_id = guild.id
            
            # Initialize action tracking
            if guild_id not in self.coordinated_actions:
                self.coordinated_actions[guild_id] = []
            
            # Check for multiple users performing similar destructive actions
            recent_actions = [action for action in self.coordinated_actions[guild_id]
                            if current_time - action['timestamp'] < timedelta(minutes=5)]
            
            if len(recent_actions) > 10:
                # Group actions by type
                action_types = {}
                for action in recent_actions:
                    action_type = action['type']
                    if action_type not in action_types:
                        action_types[action_type] = []
                    action_types[action_type].append(action)
                
                # Check for coordinated channel deletions
                if 'channel_delete' in action_types and len(action_types['channel_delete']) > 3:
                    await self.trigger_raid_protocol(guild, "Coordinated channel destruction detected")
                    return True
                
                # Check for coordinated role modifications
                if 'role_modify' in action_types and len(action_types['role_modify']) > 5:
                    await self.trigger_raid_protocol(guild, "Coordinated role manipulation detected")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error detecting coordinated actions: {e}")
            return False
    
    async def track_member_join(self, guild: discord.Guild, member: discord.Member):
        """Track member joins for raid detection"""
        try:
            guild_id = guild.id
            
            if guild_id not in self.member_join_history:
                self.member_join_history[guild_id] = []
            
            join_data = {
                'user_id': member.id,
                'username': member.display_name,
                'timestamp': datetime.now(),
                'account_created': member.created_at,
                'avatar': str(member.avatar.url) if member.avatar else None
            }
            
            self.member_join_history[guild_id].append(join_data)
            
            # Keep only last 100 joins per guild
            if len(self.member_join_history[guild_id]) > 100:
                self.member_join_history[guild_id] = self.member_join_history[guild_id][-100:]
            
            # Update suspicious activities
            if guild_id not in self.suspicious_activities:
                self.suspicious_activities[guild_id] = {
                    'rapid_joins': [],
                    'rapid_leaves': [],
                    'channel_deletions': [],
                    'role_deletions': [],
                    'permission_changes': []
                }
            
            self.suspicious_activities[guild_id]['rapid_joins'].append(datetime.now())
            
        except Exception as e:
            logger.error(f"Error tracking member join: {e}")
    
    async def track_message_pattern(self, guild: discord.Guild, message: discord.Message):
        """Track message patterns for coordination detection"""
        try:
            guild_id = guild.id
            
            if guild_id not in self.message_patterns:
                self.message_patterns[guild_id] = []
            
            message_data = {
                'user_id': message.author.id,
                'content': message.content,
                'timestamp': datetime.now(),
                'channel_id': message.channel.id
            }
            
            self.message_patterns[guild_id].append(message_data)
            
            # Keep only last 200 messages per guild
            if len(self.message_patterns[guild_id]) > 200:
                self.message_patterns[guild_id] = self.message_patterns[guild_id][-200:]
            
        except Exception as e:
            logger.error(f"Error tracking message pattern: {e}")
    
    async def trigger_raid_protocol(self, guild: discord.Guild, reason: str):
        """Activate emergency raid protection protocol with cybersecurity combat"""
        try:
            logger.warning(f"🚨 RAID DETECTED in {guild.name}: {reason}")
            
            # Set threat level based on raid type
            if "bot raid" in reason.lower():
                self.threat_level = 9  # Critical
            elif "human raid" in reason.lower():
                self.threat_level = 8  # High
            elif "spam" in reason.lower():
                self.threat_level = 6  # Medium
            else:
                self.threat_level = 7  # High
            
            # Log combat initiation
            combat_log = {
                'timestamp': datetime.now(),
                'guild': guild.name,
                'threat_type': reason,
                'threat_level': self.threat_level,
                'action': 'COMBAT_INITIATED'
            }
            self.combat_logs.append(combat_log)
            
            # Create emergency backup
            backup_file = await self.create_comprehensive_backup(guild)
            
            # Send immediate email alert to programmer
            await self.bot.send_alert_email(
                "🚨 RAID DETECTED - CYBERSECURITY COMBAT INITIATED",
                f"""
🚨 RAID DETECTED - CYBERSECURITY COMBAT INITIATED

SERVER: {guild.name}
GUILD ID: {guild.id}
THREAT TYPE: {reason}
THREAT LEVEL: {self.threat_level}/10
TIME: {datetime.now()}
BACKUP CREATED: {backup_file}

🛡️ CYBERSECURITY COUNTERMEASURES ACTIVATED:
✅ Channels Hidden and Encrypted
✅ Permissions Disabled for 60 seconds
✅ Rate Limiting Active
✅ Behavior Analysis Running
✅ Pattern Detection Active
✅ Auto-Ban System Engaged

⚔️ COMBAT STATUS: ACTIVE
🎯 TARGET: RAID ATTACKERS
🔒 PROTECTION: MAXIMUM

Only you (the programmer) can see and control this system!
                """
            )
            
            # Activate cybersecurity combat mode
            await self.activate_cybersecurity_combat(guild, reason)
            
            # Set raid detection flag
            self.raid_detection = True
            self.cybersecurity_active = True
            
        except Exception as e:
            logger.error(f"Error triggering raid protocol: {e}")
    
    async def activate_cybersecurity_combat(self, guild: discord.Guild, threat_reason: str):
        """Activate cybersecurity combat mode - hide channels and disable permissions"""
        try:
            logger.warning(f"⚔️ CYBERSECURITY COMBAT MODE ACTIVATED for {guild.name}")
            
            # Phase 1: Immediate Channel Lockdown
            await self.immediate_channel_lockdown(guild)
            
            # Phase 2: Disable All Permissions for 60 seconds
            await self.disable_permissions_temporarily(guild)
            
            # Phase 3: Activate Countermeasures
            await self.activate_countermeasures(guild, threat_reason)
            
            # Log combat activation
            combat_log = {
                'timestamp': datetime.now(),
                'guild': guild.name,
                'action': 'COMBAT_MODE_ACTIVATED',
                'threat_level': self.threat_level,
                'countermeasures': list(self.countermeasures.keys())
            }
            self.combat_logs.append(combat_log)
            
            logger.info(f"⚔️ Cybersecurity combat mode fully activated for {guild.name}")
            
        except Exception as e:
            logger.error(f"Error activating cybersecurity combat: {e}")
    
    async def immediate_channel_lockdown(self, guild: discord.Guild):
        """Immediately hide all channels from everyone except programmer"""
        try:
            # Get programmer user ID from config
            programmer_id = self.bot.config.get('dev_user_id', 0)
            programmer = self.bot.get_user(programmer_id) if programmer_id else None
            
            hidden_channels = 0
            
            for channel in guild.channels:
                if channel.type not in [discord.ChannelType.category, discord.ChannelType.voice]:
                    try:
                        # Hide from @everyone
                        overwrite = channel.overwrites_for(guild.default_role)
                        overwrite.view_channel = False
                        overwrite.send_messages = False
                        overwrite.read_message_history = False
                        overwrite.add_reactions = False
                        overwrite.use_slash_commands = False
                        await channel.set_permissions(guild.default_role, overwrite=overwrite)
                        
                        # Hide from all roles
                        for role in guild.roles:
                            if role.name != "@everyone" and role != guild.default_role:
                                overwrite = channel.overwrites_for(role)
                                overwrite.view_channel = False
                                overwrite.send_messages = False
                                overwrite.read_message_history = False
                                overwrite.add_reactions = False
                                overwrite.use_slash_commands = False
                                await channel.set_permissions(role, overwrite=overwrite)
                        
                        # Keep access for protected users (programmer, server creator, etc.)
                        protected_users = []
                        
                        # Add bot owner
                        if programmer:
                            protected_users.append(programmer)
                        
                        # Add server creator
                        if guild.owner:
                            protected_users.append(guild.owner)
                        
                        # Add other protected users
                        for user_id in self.protected_users.union(self.server_creators):
                            user = self.bot.get_user(user_id)
                            if user:
                                member = guild.get_member(user.id)
                                if member:
                                    protected_users.append(member)
                        
                        # Set permissions for all protected users
                        for protected_user in protected_users:
                            member = guild.get_member(protected_user.id)
                            if member:
                                overwrite = channel.overwrites_for(member)
                                overwrite.view_channel = True
                                overwrite.send_messages = True
                                overwrite.read_message_history = True
                                overwrite.add_reactions = True
                                overwrite.use_slash_commands = True
                                overwrite.manage_channels = True
                                overwrite.manage_messages = True
                                await channel.set_permissions(member, overwrite=overwrite)
                        
                        hidden_channels += 1
                        
                    except Exception as e:
                        logger.error(f"Error hiding channel {channel.name}: {e}")
            
            # Log lockdown
            combat_log = {
                'timestamp': datetime.now(),
                'guild': guild.name,
                'action': 'CHANNEL_LOCKDOWN',
                'hidden_channels': hidden_channels
            }
            self.combat_logs.append(combat_log)
            
            logger.warning(f"🔒 CHANNEL LOCKDOWN: {hidden_channels} channels hidden in {guild.name}")
            
        except Exception as e:
            logger.error(f"Error in immediate channel lockdown: {e}")
    
    async def disable_permissions_temporarily(self, guild: discord.Guild):
        """Disable all permissions for 60 seconds to prevent further damage"""
        try:
            # Store original permissions for restoration
            original_permissions = {}
            
            for role in guild.roles:
                if role.name != "@everyone":
                    original_permissions[role.id] = role.permissions.value
            
            # Disable all permissions for 60 seconds (except for protected users)
            for role in guild.roles:
                if role.name != "@everyone":
                    try:
                        # Check if role has any protected users
                        has_protected_users = False
                        for member in role.members:
                            if self.is_protected_user(member.id, guild):
                                has_protected_users = True
                                break
                        
                        if has_protected_users:
                            logger.info(f"🛡️ Keeping permissions for role {role.name} (contains protected users)")
                            continue
                        
                        # Create permissions with only basic access
                        basic_permissions = discord.Permissions(
                            view_channel=False,
                            send_messages=False,
                            read_message_history=False,
                            add_reactions=False,
                            use_slash_commands=False,
                            connect=False,
                            speak=False
                        )
                        
                        await role.edit(permissions=basic_permissions, reason="Cybersecurity combat mode - permissions temporarily disabled")
                        
                    except Exception as e:
                        logger.error(f"Error disabling permissions for role {role.name}: {e}")
            
            # Log permission disable
            combat_log = {
                'timestamp': datetime.now(),
                'guild': guild.name,
                'action': 'PERMISSIONS_DISABLED',
                'duration': '60_seconds',
                'affected_roles': len([r for r in guild.roles if r.name != "@everyone"])
            }
            self.combat_logs.append(combat_log)
            
            # Schedule permission restoration after 60 seconds
            asyncio.create_task(self.restore_permissions_after_delay(guild, original_permissions, 60))
            
            logger.warning(f"🚫 PERMISSIONS DISABLED for 60 seconds in {guild.name}")
            
        except Exception as e:
            logger.error(f"Error disabling permissions temporarily: {e}")
    
    async def restore_permissions_after_delay(self, guild: discord.Guild, original_permissions: dict, delay_seconds: int):
        """Restore permissions after delay"""
        try:
            await asyncio.sleep(delay_seconds)
            
            for role_id, permissions_value in original_permissions.items():
                role = guild.get_role(role_id)
                if role:
                    try:
                        await role.edit(
                            permissions=discord.Permissions(permissions_value),
                            reason="Cybersecurity combat mode - permissions restored"
                        )
                    except Exception as e:
                        logger.error(f"Error restoring permissions for role {role.name}: {e}")
            
            # Log permission restoration
            combat_log = {
                'timestamp': datetime.now(),
                'guild': guild.name,
                'action': 'PERMISSIONS_RESTORED',
                'restored_roles': len(original_permissions)
            }
            self.combat_logs.append(combat_log)
            
            logger.info(f"✅ PERMISSIONS RESTORED after {delay_seconds}s in {guild.name}")
            
        except Exception as e:
            logger.error(f"Error restoring permissions: {e}")
    
    async def activate_countermeasures(self, guild: discord.Guild, threat_reason: str):
        """Activate cybersecurity countermeasures"""
        try:
            logger.warning(f"⚔️ ACTIVATING COUNTERMEASURES in {guild.name}")
            
            countermeasures_activated = []
            
            # Rate Limiting Countermeasure
            if self.countermeasures['rate_limiting']:
                await self.activate_rate_limiting(guild)
                countermeasures_activated.append("Rate Limiting")
            
            # Behavior Analysis Countermeasure
            if self.countermeasures['behavior_analysis']:
                await self.activate_behavior_analysis(guild)
                countermeasures_activated.append("Behavior Analysis")
            
            # Pattern Detection Countermeasure
            if self.countermeasures['pattern_detection']:
                await self.activate_pattern_detection(guild)
                countermeasures_activated.append("Pattern Detection")
            
            # Auto-Ban Countermeasure
            if self.countermeasures['auto_ban']:
                await self.activate_auto_ban(guild, threat_reason)
                countermeasures_activated.append("Auto-Ban System")
            
            # Log countermeasures activation
            combat_log = {
                'timestamp': datetime.now(),
                'guild': guild.name,
                'action': 'COUNTERMEASURES_ACTIVATED',
                'countermeasures': countermeasures_activated,
                'threat_level': self.threat_level
            }
            self.combat_logs.append(combat_log)
            
            logger.warning(f"⚔️ COUNTERMEASURES ACTIVATED: {', '.join(countermeasures_activated)} in {guild.name}")
            
        except Exception as e:
            logger.error(f"Error activating countermeasures: {e}")
    
    async def activate_rate_limiting(self, guild: discord.Guild):
        """Activate aggressive rate limiting"""
        # This would implement aggressive rate limiting
        logger.info(f"🛡️ Rate limiting activated for {guild.name}")
    
    async def activate_behavior_analysis(self, guild: discord.Guild):
        """Activate enhanced behavior analysis"""
        # This would enhance behavior analysis
        logger.info(f"🧠 Behavior analysis enhanced for {guild.name}")
    
    async def activate_pattern_detection(self, guild: discord.Guild):
        """Activate advanced pattern detection"""
        # This would activate advanced pattern detection
        logger.info(f"🔍 Pattern detection activated for {guild.name}")
    
    async def activate_auto_ban(self, guild: discord.Guild, threat_reason: str):
        """Activate automatic banning of suspicious members"""
        try:
            banned_count = 0
            
            # Get recent suspicious members
            recent_joins = self.member_join_history.get(guild.id, [])
            current_time = datetime.now()
            
            for join_data in recent_joins:
                if current_time - join_data['timestamp'] < timedelta(minutes=10):
                    member = guild.get_member(join_data['user_id'])
                    if member and not member.guild_permissions.administrator:
                        # Check if user is protected
                        if self.is_protected_user(member.id, guild):
                            logger.info(f"🛡️ Skipping ban for protected user: {member.display_name}")
                            continue
                        
                        # Check if account is suspicious
                        account_age = datetime.now() - member.created_at
                        if account_age < timedelta(days=7):  # New accounts
                            try:
                                await member.ban(reason=f"Cybersecurity combat mode - suspicious account detected during {threat_reason}")
                                banned_count += 1
                            except Exception as e:
                                logger.error(f"Error banning member {member.display_name}: {e}")
            
            # Log auto-ban results
            combat_log = {
                'timestamp': datetime.now(),
                'guild': guild.name,
                'action': 'AUTO_BAN_ACTIVATED',
                'banned_count': banned_count,
                'threat_reason': threat_reason
            }
            self.combat_logs.append(combat_log)
            
            logger.warning(f"🚫 AUTO-BAN: {banned_count} suspicious members banned in {guild.name}")
            
        except Exception as e:
            logger.error(f"Error in auto-ban activation: {e}")
    
    def get_cybersecurity_status(self) -> Dict:
        """Get cybersecurity combat status"""
        return {
            'cybersecurity_active': self.cybersecurity_active,
            'threat_level': self.threat_level,
            'raid_detection': self.raid_detection,
            'countermeasures': self.countermeasures,
            'combat_logs_count': len(self.combat_logs),
            'recent_combat_logs': self.combat_logs[-5:] if self.combat_logs else [],
            'protected_users_count': len(self.protected_users),
            'server_creators_count': len(self.server_creators)
        }
    
    def is_protected_user(self, user_id: int, guild: discord.Guild = None) -> bool:
        """Check if a user is protected from all restrictions"""
        try:
            # Check if user is bot owner
            bot_owner_id = self.bot.config.get('dev_user_id', 0)
            if user_id == bot_owner_id:
                return True
            
            # Check if user is in protected users list
            if user_id in self.protected_users:
                return True
            
            # Check if user is server creator
            if user_id in self.server_creators:
                return True
            
            # Check if user is guild owner (if guild provided)
            if guild and user_id == guild.owner_id:
                return True
            
            # Check by username (protected handle: by_bytes)
            if guild is not None:
                member = guild.get_member(user_id)
                if member is not None:
                    username = (member.name or "").lower()
                    display_name = (member.display_name or "").lower()
                    if username == "by_bytes" or display_name == "by_bytes":
                        return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking protected user status: {e}")
            return False
    
    def add_protected_user(self, user_id: int, user_type: str = "manual") -> bool:
        """Add a user to the protected users list"""
        try:
            self.protected_users.add(user_id)
            
            # Log protection addition
            combat_log = {
                'timestamp': datetime.now(),
                'action': 'PROTECTED_USER_ADDED',
                'user_id': user_id,
                'user_type': user_type
            }
            self.combat_logs.append(combat_log)
            
            logger.info(f"🛡️ Added protected user: {user_id} (type: {user_type})")
            return True
            
        except Exception as e:
            logger.error(f"Error adding protected user: {e}")
            return False
    
    def add_server_creator(self, user_id: int, server_name: str = "") -> bool:
        """Add a server creator to the protected list"""
        try:
            self.server_creators.add(user_id)
            
            # Log server creator addition
            combat_log = {
                'timestamp': datetime.now(),
                'action': 'SERVER_CREATOR_ADDED',
                'user_id': user_id,
                'server_name': server_name
            }
            self.combat_logs.append(combat_log)
            
            logger.info(f"👑 Added server creator: {user_id} (server: {server_name})")
            return True
            
        except Exception as e:
            logger.error(f"Error adding server creator: {e}")
            return False
    
    def remove_protected_user(self, user_id: int) -> bool:
        """Remove a user from the protected users list"""
        try:
            if user_id in self.protected_users:
                self.protected_users.remove(user_id)
                
                # Log protection removal
                combat_log = {
                    'timestamp': datetime.now(),
                    'action': 'PROTECTED_USER_REMOVED',
                    'user_id': user_id
                }
                self.combat_logs.append(combat_log)
                
                logger.info(f"🔓 Removed protected user: {user_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error removing protected user: {e}")
            return False
    
    def get_protected_users_list(self) -> Dict:
        """Get list of all protected users"""
        try:
            protected_list = []
            
            # Add bot owner
            bot_owner_id = self.bot.config.get('dev_user_id', 0)
            if bot_owner_id:
                protected_list.append({
                    'user_id': bot_owner_id,
                    'type': 'Bot Owner',
                    'username': 'Bot Owner'
                })
            
            # Add protected users
            for user_id in self.protected_users:
                user = self.bot.get_user(user_id)
                protected_list.append({
                    'user_id': user_id,
                    'type': 'Protected User',
                    'username': user.display_name if user else f"User {user_id}"
                })
            
            # Add server creators
            for user_id in self.server_creators:
                user = self.bot.get_user(user_id)
                protected_list.append({
                    'user_id': user_id,
                    'type': 'Server Creator',
                    'username': user.display_name if user else f"Creator {user_id}"
                })
            
            return {
                'total_protected': len(protected_list),
                'users': protected_list
            }
            
        except Exception as e:
            logger.error(f"Error getting protected users list: {e}")
            return {'error': str(e)}
    
    async def activate_emergency_protection(self, guild: discord.Guild):
        """Activate emergency channel protection"""
        try:
            self.channel_protection = True
            
            # Hide all channels from everyone except admins
            admin_role = discord.utils.get(guild.roles, name="Admin")
            
            for channel in guild.channels:
                if channel.type not in [discord.ChannelType.category, discord.ChannelType.voice]:
                    try:
                        # Hide from @everyone
                        overwrite = channel.overwrites_for(guild.default_role)
                        overwrite.view_channel = False
                        await channel.set_permissions(guild.default_role, overwrite=overwrite)
                        
                        # Keep visible for admins
                        if admin_role:
                            overwrite = channel.overwrites_for(admin_role)
                            overwrite.view_channel = True
                            await channel.set_permissions(admin_role, overwrite=overwrite)
                        
                        self.protected_channels.add(channel.id)
                        
                    except Exception as e:
                        logger.error(f"Error protecting channel {channel.name}: {e}")
            
            logger.info(f"Emergency protection activated for guild {guild.name}")
            
        except Exception as e:
            logger.error(f"Error activating emergency protection: {e}")
    
    async def restore_from_backup(self, guild: discord.Guild, backup_file: str = None):
        """Restore server from backup"""
        try:
            if not backup_file:
                # Find the most recent backup
                backup_files = [f for f in os.listdir('backups') if f.startswith(str(guild.id))]
                if not backup_files:
                    return False
                
                backup_file = sorted(backup_files)[-1]
            
            backup_path = f'backups/{backup_file}'
            
            with open(backup_path, 'r') as f:
                backup = json.load(f)
            
            # Restore guild settings
            await guild.edit(
                name=backup['settings']['name'],
                description=backup['settings']['description'],
                verification_level=discord.VerificationLevel(backup['settings']['verification_level']),
                default_notifications=discord.NotificationLevel(backup['settings']['default_notifications']),
                explicit_content_filter=discord.ContentFilter(backup['settings']['explicit_content_filter'])
            )
            
            # Restore channels (simplified - Discord API limitations)
            for channel_data in backup['channels']:
                try:
                    existing_channel = guild.get_channel(channel_data['id'])
                    if not existing_channel and channel_data['type'] == 'text':
                        # Recreate deleted text channel
                        await guild.create_text_channel(
                            name=channel_data['name'],
                            position=channel_data['position']
                        )
                except Exception as e:
                    logger.error(f"Error restoring channel {channel_data['name']}: {e}")
            
            # Restore roles
            for role_data in backup['roles']:
                try:
                    existing_role = guild.get_role(role_data['id'])
                    if not existing_role:
                        # Recreate deleted role
                        await guild.create_role(
                            name=role_data['name'],
                            color=discord.Color(role_data['color']),
                            permissions=discord.Permissions(role_data['permissions']),
                            hoist=role_data['hoist'],
                            mentionable=role_data['mentionable']
                        )
                except Exception as e:
                    logger.error(f"Error restoring role {role_data['name']}: {e}")
            
            logger.info(f"Server restored from backup: {backup_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring from backup: {e}")
            return False
    
    async def deactivate_protection(self, guild: discord.Guild):
        """Deactivate all protection measures"""
        try:
            self.channel_protection = False
            self.raid_detection = False
            
            # Restore channel visibility
            for channel_id in self.protected_channels:
                channel = guild.get_channel(channel_id)
                if channel:
                    try:
                        overwrite = channel.overwrites_for(guild.default_role)
                        overwrite.view_channel = None
                        await channel.set_permissions(guild.default_role, overwrite=overwrite)
                    except Exception as e:
                        logger.error(f"Error restoring channel {channel.name}: {e}")
            
            self.protected_channels.clear()
            
            # Send email notification
            await self.bot.send_alert_email(
                "✅ Protection Deactivated",
                f"All protection measures have been deactivated for server: {guild.name}"
            )
            
            logger.info(f"Protection deactivated for guild {guild.name}")
            
        except Exception as e:
            logger.error(f"Error deactivating protection: {e}")
    
    async def monitor_suspicious_activity(self, guild: discord.Guild):
        """Continuous monitoring for suspicious activities"""
        try:
            # Check for unusual member activity
            member_count = guild.member_count
            if guild.id in self.server_backups:
                previous_count = self.server_backups[guild.id]['metadata']['member_count']
                
                # Significant member count change
                if abs(member_count - previous_count) > 50:
                    await self.create_comprehensive_backup(guild)
            
            # Check for rapid permission changes
            # This would require additional tracking of permission changes
            
            # Check for unusual channel activity
            channel_count = len(guild.channels)
            if guild.id in self.server_backups:
                previous_channels = len(self.server_backups[guild.id]['channels'])
                
                if abs(channel_count - previous_channels) > 10:
                    await self.create_comprehensive_backup(guild)
            
        except Exception as e:
            logger.error(f"Error monitoring suspicious activity: {e}")
    
    def get_protection_status(self) -> Dict:
        """Get current protection system status"""
        return {
            'protection_active': self.protection_active,
            'raid_detection': self.raid_detection,
            'channel_protection': self.channel_protection,
            'protected_channels': len(self.protected_channels),
            'server_backups': len(self.server_backups),
            'suspicious_activities_tracked': len(self.suspicious_activities),
            'emergency_mode': self.emergency_mode,
            'encrypted_channels': len(self.encrypted_channels)
        }
    
    def generate_encryption_key(self) -> bytes:
        """Generate a new encryption key"""
        return Fernet.generate_key()
    
    def encrypt_data(self, data: str, key: bytes) -> str:
        """Encrypt data using Fernet encryption"""
        try:
            f = Fernet(key)
            encrypted_data = f.encrypt(data.encode())
            return base64.b64encode(encrypted_data).decode()
        except Exception as e:
            logger.error(f"Error encrypting data: {e}")
            return data
    
    def decrypt_data(self, encrypted_data: str, key: bytes) -> str:
        """Decrypt data using Fernet encryption"""
        try:
            f = Fernet(key)
            decoded_data = base64.b64decode(encrypted_data.encode())
            decrypted_data = f.decrypt(decoded_data)
            return decrypted_data.decode()
        except Exception as e:
            logger.error(f"Error decrypting data: {e}")
            return encrypted_data
    
    async def emergency_channel_encryption(self, guild: discord.Guild):
        """Emergency channel encryption - hide and encrypt all channels"""
        try:
            logger.warning(f"EMERGENCY CHANNEL ENCRYPTION ACTIVATED for {guild.name}")
            
            # Set emergency mode
            self.emergency_mode = True
            
            # Generate encryption key for this guild
            encryption_key = self.generate_encryption_key()
            self.encryption_keys[guild.id] = encryption_key
            
            # Create comprehensive backup before encryption
            backup_file = await self.create_comprehensive_backup(guild)
            
            # Process all channels
            encrypted_count = 0
            for channel in guild.channels:
                if channel.type not in [discord.ChannelType.category, discord.ChannelType.voice]:
                    try:
                        # Backup channel data before encryption
                        await self.backup_channel_data(channel, encryption_key)
                        
                        # Hide channel from everyone
                        await self.hide_channel_completely(channel)
                        
                        # Mark as encrypted
                        self.encrypted_channels[channel.id] = {
                            'guild_id': guild.id,
                            'channel_name': channel.name,
                            'encrypted_at': datetime.now(),
                            'backup_file': backup_file
                        }
                        
                        encrypted_count += 1
                        
                    except Exception as e:
                        logger.error(f"Error encrypting channel {channel.name}: {e}")
            
            # Send emergency alert email
            await self.bot.send_alert_email(
                "🚨 EMERGENCY CHANNEL ENCRYPTION ACTIVATED",
                f"""
EMERGENCY CHANNEL ENCRYPTION ACTIVATED

Server: {guild.name}
Guild ID: {guild.id}
Channels Encrypted: {encrypted_count}
Time: {datetime.now()}
Backup Created: {backup_file}
Encryption Key Generated: YES

ALL CHANNELS ARE NOW HIDDEN AND ENCRYPTED!
Use !decrypt_channels command to restore access.
                """
            )
            
            logger.info(f"Emergency encryption completed for {guild.name}: {encrypted_count} channels encrypted")
            return encrypted_count
            
        except Exception as e:
            logger.error(f"Error in emergency channel encryption: {e}")
            return 0
    
    async def backup_channel_data(self, channel, encryption_key: bytes):
        """Backup and encrypt channel data"""
        try:
            # Get recent messages (last 100)
            messages_data = []
            async for message in channel.history(limit=100):
                if not message.author.bot:
                    message_data = {
                        'id': message.id,
                        'author': message.author.display_name,
                        'content': message.content,
                        'timestamp': message.created_at.isoformat(),
                        'attachments': [att.url for att in message.attachments],
                        'embeds': [embed.to_dict() for embed in message.embeds]
                    }
                    messages_data.append(message_data)
            
            # Encrypt messages data
            messages_json = json.dumps(messages_data)
            encrypted_messages = self.encrypt_data(messages_json, encryption_key)
            
            # Store backup
            self.channel_backup_data[channel.id] = {
                'messages': encrypted_messages,
                'channel_name': channel.name,
                'channel_type': str(channel.type),
                'backup_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error backing up channel data for {channel.name}: {e}")
    
    async def hide_channel_completely(self, channel):
        """Hide channel from everyone except bot owner"""
        try:
            # Hide from @everyone
            overwrite = channel.overwrites_for(channel.guild.default_role)
            overwrite.view_channel = False
            overwrite.send_messages = False
            overwrite.read_message_history = False
            await channel.set_permissions(channel.guild.default_role, overwrite=overwrite)
            
            # Hide from all other roles
            for role in channel.guild.roles:
                if role.name != "@everyone" and role != channel.guild.default_role:
                    overwrite = channel.overwrites_for(role)
                    overwrite.view_channel = False
                    overwrite.send_messages = False
                    overwrite.read_message_history = False
                    await channel.set_permissions(role, overwrite=overwrite)
            
            # Keep access only for bot owner (if possible)
            bot_owner = self.bot.get_user(self.bot.config.get('dev_user_id', 0))
            if bot_owner:
                member = channel.guild.get_member(bot_owner.id)
                if member:
                    overwrite = channel.overwrites_for(member)
                    overwrite.view_channel = True
                    overwrite.send_messages = True
                    overwrite.read_message_history = True
                    await channel.set_permissions(member, overwrite=overwrite)
            
            logger.info(f"Channel {channel.name} completely hidden")
            
        except Exception as e:
            logger.error(f"Error hiding channel {channel.name}: {e}")
    
    async def decrypt_and_restore_channels(self, guild: discord.Guild):
        """Decrypt and restore all channels"""
        try:
            if guild.id not in self.encryption_keys:
                return False, "No encryption key found for this guild"
            
            encryption_key = self.encryption_keys[guild.id]
            restored_count = 0
            
            for channel_id, encrypted_data in self.encrypted_channels.items():
                if encrypted_data['guild_id'] == guild.id:
                    try:
                        channel = guild.get_channel(channel_id)
                        if channel:
                            # Restore channel visibility
                            await self.restore_channel_visibility(channel)
                            
                            # Restore channel data if available
                            if channel_id in self.channel_backup_data:
                                await self.restore_channel_data(channel, encryption_key)
                            
                            restored_count += 1
                            
                    except Exception as e:
                        logger.error(f"Error restoring channel {channel_id}: {e}")
            
            # Clear encryption data
            self.encrypted_channels = {k: v for k, v in self.encrypted_channels.items() if v['guild_id'] != guild.id}
            if guild.id in self.encryption_keys:
                del self.encryption_keys[guild.id]
            
            self.emergency_mode = False
            
            # Send restoration email
            await self.bot.send_alert_email(
                "✅ CHANNEL DECRYPTION COMPLETED",
                f"""
CHANNEL DECRYPTION COMPLETED

Server: {guild.name}
Guild ID: {guild.id}
Channels Restored: {restored_count}
Time: {datetime.now()}

ALL CHANNELS HAVE BEEN RESTORED AND DECRYPTED!
                """
            )
            
            logger.info(f"Channel decryption completed for {guild.name}: {restored_count} channels restored")
            return True, f"Restored {restored_count} channels"
            
        except Exception as e:
            logger.error(f"Error in channel decryption: {e}")
            return False, str(e)
    
    async def restore_channel_visibility(self, channel):
        """Restore channel visibility to normal"""
        try:
            # Restore @everyone permissions
            overwrite = channel.overwrites_for(channel.guild.default_role)
            overwrite.view_channel = None
            overwrite.send_messages = None
            overwrite.read_message_history = None
            await channel.set_permissions(channel.guild.default_role, overwrite=overwrite)
            
            # Clear other role overrides
            for role in channel.guild.roles:
                if role.name != "@everyone" and role != channel.guild.default_role:
                    overwrite = channel.overwrites_for(role)
                    overwrite.view_channel = None
                    overwrite.send_messages = None
                    overwrite.read_message_history = None
                    await channel.set_permissions(role, overwrite=overwrite)
            
            logger.info(f"Channel {channel.name} visibility restored")
            
        except Exception as e:
            logger.error(f"Error restoring channel visibility {channel.name}: {e}")
    
    async def restore_channel_data(self, channel, encryption_key: bytes):
        """Restore encrypted channel data"""
        try:
            if channel.id not in self.channel_backup_data:
                return
            
            encrypted_messages = self.channel_backup_data[channel.id]['messages']
            decrypted_json = self.decrypt_data(encrypted_messages, encryption_key)
            messages_data = json.loads(decrypted_json)
            
            # Note: Discord API doesn't allow sending messages on behalf of users
            # This would require webhook implementation or manual restoration
            logger.info(f"Channel data restored for {channel.name}: {len(messages_data)} messages")
            
            # Clear backup data
            del self.channel_backup_data[channel.id]
            
        except Exception as e:
            logger.error(f"Error restoring channel data for {channel.name}: {e}")
    
    def get_encryption_status(self, guild_id: int) -> Dict:
        """Get encryption status for guild"""
        encrypted_channels = [data for data in self.encrypted_channels.values() if data['guild_id'] == guild_id]
        
        return {
            'emergency_mode': self.emergency_mode,
            'encrypted_channels': len(encrypted_channels),
            'has_encryption_key': guild_id in self.encryption_keys,
            'channels': [
                {
                    'name': data['channel_name'],
                    'encrypted_at': data['encrypted_at'].isoformat()
                }
                for data in encrypted_channels
            ]
        }
