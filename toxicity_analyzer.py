"""
Toxicity Analysis System
Uses Gemini AI to analyze messages and assign toxicity levels
"""

import discord
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)

class ToxicityAnalyzer:
    def __init__(self, bot, gemini_model):
        self.bot = bot
        self.gemini_model = gemini_model
        self.user_toxicity = {}
        self.message_history = {}
        self.toxicity_roles = {
            'low_risk': '✅ Clean User',
            'medium_risk': '⚠️ Watch List',
            'high_risk': '🚨 Toxic User',
            'extreme_risk': '🔴 Banned User'
        }
        self.thresholds = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.8,
            'extreme': 0.95
        }
    
    async def analyze_message(self, message: discord.Message) -> float:
        """Analyze a message for toxicity using Gemini AI"""
        try:
            if not self.gemini_model or len(message.content.strip()) < 5:
                return 0.0
            
            # Prepare analysis prompt
            prompt = f"""
            Analyze the following Discord message for toxicity, harassment, hate speech, or inappropriate content.
            
            Message: "{message.content}"
            
            Consider these factors:
            - Direct insults or personal attacks
            - Hate speech or discriminatory language
            - Threats or intimidation
            - Spam or excessive repetition
            - Inappropriate sexual content
            - Encouraging self-harm or violence
            
            Rate the toxicity level from 0.0 (completely safe) to 1.0 (extremely toxic).
            Respond with only a decimal number between 0.0 and 1.0.
            """
            
            response = self.gemini_model.generate_content(prompt)
            toxicity_score = float(response.text.strip())
            
            # Validate score
            if not 0.0 <= toxicity_score <= 1.0:
                return 0.0
            
            return toxicity_score
            
        except Exception as e:
            logger.error(f"Error analyzing message toxicity: {e}")
            return 0.0
    
    async def update_user_toxicity(self, user: discord.User, message: discord.Message, toxicity_score: float):
        """Update user's toxicity level based on message analysis"""
        try:
            user_id = user.id
            
            # Initialize user data if not exists
            if user_id not in self.user_toxicity:
                self.user_toxicity[user_id] = {
                    'current_level': 0.0,
                    'message_count': 0,
                    'toxic_messages': 0,
                    'last_updated': datetime.now(),
                    'history': []
                }
            
            user_data = self.user_toxicity[user_id]
            
            # Update statistics
            user_data['message_count'] += 1
            if toxicity_score > 0.3:  # Consider messages above 0.3 as potentially toxic
                user_data['toxic_messages'] += 1
            
            # Calculate new toxicity level using weighted average
            weight = 0.1  # How much new score affects overall level
            user_data['current_level'] = (1 - weight) * user_data['current_level'] + weight * toxicity_score
            
            # Add to history
            user_data['history'].append({
                'score': toxicity_score,
                'timestamp': datetime.now().isoformat(),
                'message_preview': message.content[:100] + "..." if len(message.content) > 100 else message.content
            })
            
            # Keep only last 50 messages in history
            if len(user_data['history']) > 50:
                user_data['history'] = user_data['history'][-50:]
            
            user_data['last_updated'] = datetime.now()
            
            # Check if role needs to be updated
            await self.update_toxicity_role(user, user_data['current_level'])
            
            # Log high toxicity
            if toxicity_score > 0.7:
                logger.warning(f"High toxicity detected from {user.display_name}: {toxicity_score}")
                await self.handle_high_toxicity(user, message, toxicity_score)
            
        except Exception as e:
            logger.error(f"Error updating user toxicity: {e}")
    
    async def update_toxicity_role(self, user: discord.User, toxicity_level: float):
        """Update user's toxicity role based on current level"""
        try:
            # Find user's guild (assuming they're in at least one guild with the bot)
            guild = None
            for g in self.bot.guilds:
                if g.get_member(user.id):
                    guild = g
                    break
            
            if not guild:
                return
            
            member = guild.get_member(user.id)
            if not member:
                return
            
            # Determine new role based on toxicity level
            new_role_name = None
            if toxicity_level >= self.thresholds['extreme']:
                new_role_name = self.toxicity_roles['extreme_risk']
            elif toxicity_level >= self.thresholds['high']:
                new_role_name = self.toxicity_roles['high_risk']
            elif toxicity_level >= self.thresholds['medium']:
                new_role_name = self.toxicity_roles['medium_risk']
            elif toxicity_level < self.thresholds['low']:
                new_role_name = self.toxicity_roles['low_risk']
            
            # Remove old toxicity roles
            for role_name in self.toxicity_roles.values():
                old_role = discord.utils.get(guild.roles, name=role_name)
                if old_role and old_role in member.roles:
                    await member.remove_roles(old_role)
            
            # Add new role if needed
            if new_role_name:
                role = discord.utils.get(guild.roles, name=new_role_name)
                if not role:
                    # Create role if it doesn't exist
                    role = await self.create_toxicity_role(guild, new_role_name, toxicity_level)
                
                if role and role not in member.roles:
                    await member.add_roles(role)
            
        except Exception as e:
            logger.error(f"Error updating toxicity role: {e}")
    
    async def create_toxicity_role(self, guild: discord.Guild, role_name: str, toxicity_level: float):
        """Create a toxicity role with appropriate color and settings"""
        try:
            # Determine role color based on toxicity level
            if toxicity_level >= 0.8:
                color = discord.Color.red()
            elif toxicity_level >= 0.6:
                color = discord.Color.orange()
            elif toxicity_level >= 0.3:
                color = discord.Color.yellow()
            else:
                color = discord.Color.green()
            
            role = await guild.create_role(
                name=role_name,
                color=color,
                mentionable=False,
                hoist=True,
                reason="Automatic toxicity role assignment"
            )
            
            logger.info(f"Created toxicity role: {role_name} in guild {guild.name}")
            return role
            
        except Exception as e:
            logger.error(f"Error creating toxicity role: {e}")
            return None
    
    async def handle_high_toxicity(self, user: discord.User, message: discord.Message, toxicity_score: float):
        """Handle cases of high toxicity with additional measures"""
        try:
            # Send alert to admin channels
            for guild in self.bot.guilds:
                member = guild.get_member(user.id)
                if member:
                    # Find admin channel
                    admin_channel = discord.utils.get(guild.channels, name='admin-alerts')
                    if admin_channel:
                        embed = discord.Embed(
                            title="🚨 High Toxicity Alert",
                            description=f"User {user.display_name} has been flagged for toxic behavior",
                            color=0xff0000,
                            timestamp=datetime.now()
                        )
                        
                        embed.add_field(name="Toxicity Score", value=f"{toxicity_score:.2%}", inline=True)
                        embed.add_field(name="User ID", value=str(user.id), inline=True)
                        embed.add_field(name="Message Preview", value=message.content[:200], inline=False)
                        
                        await admin_channel.send(embed=embed, delete_after=300)  # Delete after 5 minutes
            
            # Send email alert if toxicity is extreme
            if toxicity_score > 0.9:
                await self.bot.send_alert_email(
                    "🚨 EXTREME TOXICITY DETECTED",
                    f"""
EXTREME TOXICITY ALERT

User: {user.display_name} ({user.id})
Server: {message.guild.name if message.guild else 'Unknown'}
Toxicity Score: {toxicity_score:.2%}
Message: {message.content}

IMMEDIATE ACTION REQUIRED!
                    """
                )
            
        except Exception as e:
            logger.error(f"Error handling high toxicity: {e}")
    
    async def get_toxicity_report(self, user: discord.User) -> Dict:
        """Generate a detailed toxicity report for a user"""
        try:
            user_id = user.id
            
            if user_id not in self.user_toxicity:
                return {
                    'error': 'No toxicity data found for this user',
                    'toxicity_level': 0.0,
                    'message_count': 0,
                    'toxic_messages': 0
                }
            
            user_data = self.user_toxicity[user_id]
            
            # Calculate additional statistics
            toxic_percentage = (user_data['toxic_messages'] / user_data['message_count']) * 100 if user_data['message_count'] > 0 else 0
            
            # Recent activity (last 24 hours)
            recent_toxicity = []
            cutoff_time = datetime.now() - timedelta(hours=24)
            
            for entry in user_data['history']:
                entry_time = datetime.fromisoformat(entry['timestamp'])
                if entry_time > cutoff_time:
                    recent_toxicity.append(entry['score'])
            
            avg_recent_toxicity = sum(recent_toxicity) / len(recent_toxicity) if recent_toxicity else 0
            
            report = {
                'user_id': user_id,
                'username': user.display_name,
                'current_toxicity_level': user_data['current_level'],
                'message_count': user_data['message_count'],
                'toxic_messages': user_data['toxic_messages'],
                'toxic_percentage': toxic_percentage,
                'avg_recent_toxicity': avg_recent_toxicity,
                'last_updated': user_data['last_updated'].isoformat(),
                'risk_level': self.get_risk_level(user_data['current_level']),
                'recent_messages': len(recent_toxicity)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating toxicity report: {e}")
            return {'error': str(e)}
    
    def get_risk_level(self, toxicity_level: float) -> str:
        """Get human-readable risk level"""
        if toxicity_level >= self.thresholds['extreme']:
            return "EXTREME RISK"
        elif toxicity_level >= self.thresholds['high']:
            return "HIGH RISK"
        elif toxicity_level >= self.thresholds['medium']:
            return "MEDIUM RISK"
        elif toxicity_level >= self.thresholds['low']:
            return "LOW RISK"
        else:
            return "CLEAN"
    
    async def reset_user_toxicity(self, user: discord.User):
        """Reset a user's toxicity level (admin function)"""
        try:
            user_id = user.id
            
            if user_id in self.user_toxicity:
                self.user_toxicity[user_id] = {
                    'current_level': 0.0,
                    'message_count': 0,
                    'toxic_messages': 0,
                    'last_updated': datetime.now(),
                    'history': []
                }
                
                # Remove all toxicity roles
                for guild in self.bot.guilds:
                    member = guild.get_member(user.id)
                    if member:
                        for role_name in self.toxicity_roles.values():
                            role = discord.utils.get(guild.roles, name=role_name)
                            if role and role in member.roles:
                                await member.remove_roles(role)
                
                logger.info(f"Toxicity level reset for user {user.display_name}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error resetting user toxicity: {e}")
            return False
    
    def get_system_stats(self) -> Dict:
        """Get overall toxicity system statistics"""
        try:
            total_users = len(self.user_toxicity)
            high_risk_users = sum(1 for data in self.user_toxicity.values() 
                                if data['current_level'] >= self.thresholds['high'])
            medium_risk_users = sum(1 for data in self.user_toxicity.values() 
                                  if self.thresholds['medium'] <= data['current_level'] < self.thresholds['high'])
            
            total_messages = sum(data['message_count'] for data in self.user_toxicity.values())
            total_toxic_messages = sum(data['toxic_messages'] for data in self.user_toxicity.values())
            
            return {
                'total_users_tracked': total_users,
                'high_risk_users': high_risk_users,
                'medium_risk_users': medium_risk_users,
                'total_messages_analyzed': total_messages,
                'total_toxic_messages': total_toxic_messages,
                'system_uptime': 'Active'
            }
            
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return {'error': str(e)}
