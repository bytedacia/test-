"""
Advanced Music System
Handles Spotify, YouTube, and other music sources
"""

import discord
import asyncio
import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
from typing import Dict, List, Optional, Union
import logging

logger = logging.getLogger(__name__)

class MusicSystem:
    def __init__(self, bot):
        self.bot = bot
        self.voice_clients = {}
        self.music_queues = {}
        self.now_playing = {}
        self.spotify = None
        self.ytdl_options = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }
        
        # Initialize Spotify if credentials are available
        self.init_spotify()
    
    def init_spotify(self):
        """Initialize Spotify integration"""
        try:
            if (self.bot.config.get('spotify_client_id') and 
                self.bot.config.get('spotify_client_secret')):
                
                client_credentials_manager = SpotifyClientCredentials(
                    client_id=self.bot.config['spotify_client_id'],
                    client_secret=self.bot.config['spotify_client_secret']
                )
                self.spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
                logger.info("Spotify integration initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Spotify: {e}")
    
    async def join_voice_channel(self, ctx):
        """Join the user's voice channel"""
        try:
            if not ctx.author.voice:
                return None, "You need to be in a voice channel to play music!"
            
            voice_channel = ctx.author.voice.channel
            
            if ctx.voice_client is None:
                voice_client = await voice_channel.connect()
            elif ctx.voice_client.channel != voice_channel:
                await ctx.voice_client.move_to(voice_channel)
                voice_client = ctx.voice_client
            else:
                voice_client = ctx.voice_client
            
            return voice_client, None
            
        except Exception as e:
            logger.error(f"Error joining voice channel: {e}")
            return None, f"Error joining voice channel: {e}"
    
    async def search_and_play(self, ctx, query: str):
        """Search for and play music from various sources"""
        try:
            voice_client, error = await self.join_voice_channel(ctx)
            if error:
                return await ctx.send(error)
            
            # Check if it's a Spotify URL
            if 'spotify.com' in query and self.spotify:
                return await self.handle_spotify_url(ctx, query, voice_client)
            
            # Check if it's a YouTube URL
            elif 'youtube.com' in query or 'youtu.be' in query:
                return await self.handle_youtube_url(ctx, query, voice_client)
            
            # Search for the query
            else:
                return await self.search_and_play_query(ctx, query, voice_client)
                
        except Exception as e:
            logger.error(f"Error in search_and_play: {e}")
            return await ctx.send(f"Error playing music: {e}")
    
    async def handle_spotify_url(self, ctx, url: str, voice_client):
        """Handle Spotify URLs"""
        try:
            # Extract track ID from Spotify URL
            track_id = self.extract_spotify_id(url)
            if not track_id:
                return await ctx.send("Invalid Spotify URL!")
            
            # Get track information from Spotify
            track = self.spotify.track(track_id)
            track_name = f"{track['name']} by {track['artists'][0]['name']}"
            
            # Search for the track on YouTube
            search_query = f"{track_name} audio"
            return await self.search_and_play_query(ctx, search_query, voice_client, spotify_info=track)
            
        except Exception as e:
            logger.error(f"Error handling Spotify URL: {e}")
            return await ctx.send("Error processing Spotify URL!")
    
    def extract_spotify_id(self, url: str) -> Optional[str]:
        """Extract track ID from Spotify URL"""
        try:
            patterns = [
                r'spotify:track:([a-zA-Z0-9]+)',
                r'spotify\.com/track/([a-zA-Z0-9]+)',
                r'open\.spotify\.com/track/([a-zA-Z0-9]+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(1)
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting Spotify ID: {e}")
            return None
    
    async def handle_youtube_url(self, ctx, url: str, voice_client):
        """Handle YouTube URLs"""
        try:
            ytdl = yt_dlp.YoutubeDL(self.ytdl_options)
            info = ytdl.extract_info(url, download=False)
            
            if not info:
                return await ctx.send("Could not extract video information!")
            
            title = info.get('title', 'Unknown Title')
            duration = info.get('duration', 0)
            
            # Add to queue
            track_info = {
                'title': title,
                'url': url,
                'duration': duration,
                'requester': ctx.author,
                'source': 'youtube'
            }
            
            await self.add_to_queue(ctx.guild.id, track_info, voice_client)
            
        except Exception as e:
            logger.error(f"Error handling YouTube URL: {e}")
            return await ctx.send("Error processing YouTube URL!")
    
    async def search_and_play_query(self, ctx, query: str, voice_client, spotify_info=None):
        """Search for music using query and play it"""
        try:
            ytdl = yt_dlp.YoutubeDL(self.ytdl_options)
            
            # Search for the query
            search_results = ytdl.extract_info(f"ytsearch:{query}", download=False)
            
            if not search_results or 'entries' not in search_results:
                return await ctx.send("No results found!")
            
            # Get the first result
            video_info = search_results['entries'][0]
            
            title = video_info.get('title', 'Unknown Title')
            duration = video_info.get('duration', 0)
            url = video_info.get('url') or video_info.get('webpage_url')
            
            # Create track info
            track_info = {
                'title': title,
                'url': url,
                'duration': duration,
                'requester': ctx.author,
                'source': 'youtube',
                'spotify_info': spotify_info
            }
            
            await self.add_to_queue(ctx.guild.id, track_info, voice_client)
            
        except Exception as e:
            logger.error(f"Error searching for music: {e}")
            return await ctx.send("Error searching for music!")
    
    async def add_to_queue(self, guild_id: int, track_info: dict, voice_client):
        """Add track to queue and start playing if queue is empty"""
        try:
            # Initialize queue if it doesn't exist
            if guild_id not in self.music_queues:
                self.music_queues[guild_id] = []
            
            # Add track to queue
            self.music_queues[guild_id].append(track_info)
            
            # If this is the first track, start playing
            if len(self.music_queues[guild_id]) == 1:
                await self.play_next(guild_id, voice_client)
            else:
                # Send queue update message
                embed = discord.Embed(
                    title="🎵 Added to Queue",
                    description=f"**{track_info['title']}**",
                    color=0x00ff00
                )
                
                if track_info.get('spotify_info'):
                    spotify = track_info['spotify_info']
                    embed.add_field(
                        name="🎧 Spotify Track",
                        value=f"**{spotify['name']}** by {spotify['artists'][0]['name']}",
                        inline=False
                    )
                
                embed.add_field(
                    name="⏱️ Duration",
                    value=self.format_duration(track_info['duration']),
                    inline=True
                )
                embed.add_field(
                    name="👤 Requested by",
                    value=track_info['requester'].mention,
                    inline=True
                )
                embed.add_field(
                    name="📍 Position",
                    value=f"#{len(self.music_queues[guild_id])}",
                    inline=True
                )
                
                channel = voice_client.channel
                if channel:
                    await channel.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error adding to queue: {e}")
    
    async def play_next(self, guild_id: int, voice_client):
        """Play the next track in the queue"""
        try:
            if guild_id not in self.music_queues or not self.music_queues[guild_id]:
                return
            
            track_info = self.music_queues[guild_id][0]
            
            # Create audio source
            ytdl = yt_dlp.YoutubeDL(self.ytdl_options)
            
            def after_playing(error):
                if error:
                    logger.error(f"Error in audio playback: {error}")
                else:
                    # Play next track when current finishes
                    asyncio.create_task(self.on_track_finished(guild_id, voice_client))
            
            # Download and play audio
            try:
                info = ytdl.extract_info(track_info['url'], download=False)
                url = info.get('url')
                
                if url:
                    audio_source = discord.FFmpegPCMAudio(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
                    
                    voice_client.play(audio_source, after=after_playing)
                    
                    # Set now playing
                    self.now_playing[guild_id] = track_info
                    
                    # Send now playing message
                    await self.send_now_playing_message(voice_client, track_info)
                    
                else:
                    logger.error("Could not extract audio URL")
                    await self.on_track_finished(guild_id, voice_client)
                    
            except Exception as e:
                logger.error(f"Error creating audio source: {e}")
                await self.on_track_finished(guild_id, voice_client)
            
        except Exception as e:
            logger.error(f"Error playing next track: {e}")
    
    async def on_track_finished(self, guild_id: int, voice_client):
        """Handle track finishing"""
        try:
            # Remove finished track from queue
            if guild_id in self.music_queues and self.music_queues[guild_id]:
                self.music_queues[guild_id].pop(0)
            
            # Clear now playing
            if guild_id in self.now_playing:
                del self.now_playing[guild_id]
            
            # Play next track if available
            if guild_id in self.music_queues and self.music_queues[guild_id]:
                await self.play_next(guild_id, voice_client)
            else:
                # No more tracks, disconnect after delay
                await asyncio.sleep(300)  # Wait 5 minutes
                if not voice_client.is_playing():
                    await voice_client.disconnect()
            
        except Exception as e:
            logger.error(f"Error handling track finish: {e}")
    
    async def send_now_playing_message(self, voice_client, track_info: dict):
        """Send now playing message"""
        try:
            embed = discord.Embed(
                title="🎵 Now Playing",
                description=f"**{track_info['title']}**",
                color=0x00ff00
            )
            
            if track_info.get('spotify_info'):
                spotify = track_info['spotify_info']
                embed.add_field(
                    name="🎧 Spotify Track",
                    value=f"**{spotify['name']}** by {spotify['artists'][0]['name']}",
                    inline=False
                )
            
            embed.add_field(
                name="⏱️ Duration",
                value=self.format_duration(track_info['duration']),
                inline=True
            )
            embed.add_field(
                name="👤 Requested by",
                value=track_info['requester'].mention,
                inline=True
            )
            
            channel = voice_client.channel
            if channel:
                await channel.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error sending now playing message: {e}")
    
    def format_duration(self, seconds: int) -> str:
        """Format duration in seconds to MM:SS"""
        try:
            if seconds == 0:
                return "Unknown"
            
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{minutes:02d}:{seconds:02d}"
            
        except Exception:
            return "Unknown"
    
    async def skip_track(self, guild_id: int, voice_client):
        """Skip current track"""
        try:
            if voice_client and voice_client.is_playing():
                voice_client.stop()
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error skipping track: {e}")
            return False
    
    async def stop_music(self, guild_id: int, voice_client):
        """Stop music and clear queue"""
        try:
            if voice_client:
                voice_client.stop()
            
            if guild_id in self.music_queues:
                self.music_queues[guild_id].clear()
            
            if guild_id in self.now_playing:
                del self.now_playing[guild_id]
            
            return True
            
        except Exception as e:
            logger.error(f"Error stopping music: {e}")
            return False
    
    def get_queue_info(self, guild_id: int) -> Dict:
        """Get queue information"""
        try:
            queue = self.music_queues.get(guild_id, [])
            now_playing = self.now_playing.get(guild_id)
            
            return {
                'now_playing': now_playing,
                'queue_length': len(queue),
                'queue': queue,
                'is_playing': now_playing is not None
            }
            
        except Exception as e:
            logger.error(f"Error getting queue info: {e}")
            return {'error': str(e)}
    
    async def shuffle_queue(self, guild_id: int):
        """Shuffle the music queue"""
        try:
            if guild_id in self.music_queues and len(self.music_queues[guild_id]) > 1:
                # Keep first track (currently playing) and shuffle the rest
                current_track = self.music_queues[guild_id][0]
                remaining_tracks = self.music_queues[guild_id][1:]
                
                import random
                random.shuffle(remaining_tracks)
                
                self.music_queues[guild_id] = [current_track] + remaining_tracks
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error shuffling queue: {e}")
            return False
    
    async def clear_queue(self, guild_id: int):
        """Clear the music queue"""
        try:
            if guild_id in self.music_queues:
                # Keep only the currently playing track
                if len(self.music_queues[guild_id]) > 1:
                    self.music_queues[guild_id] = self.music_queues[guild_id][:1]
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error clearing queue: {e}")
            return False
