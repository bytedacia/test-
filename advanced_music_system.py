"""
Advanced Professional Music System with Security
Handles multiple platforms with link validation and security checks
"""

import discord
import asyncio
import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import hashlib
import requests
import urllib.parse
from typing import Dict, List, Optional, Union, Tuple
import logging
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AdvancedMusicSystem:
    def __init__(self, bot):
        self.bot = bot
        self.voice_clients = {}
        self.music_queues = {}
        self.now_playing = {}
        self.playback_controls = {}
        self.link_cache = {}
        self.suspicious_links = set()
        
        # Platform configurations
        self.platforms = {
            'youtube': {
                'domains': ['youtube.com', 'youtu.be', 'm.youtube.com'],
                'extractor': 'youtube',
                'enabled': True
            },
            'spotify': {
                'domains': ['open.spotify.com', 'spotify.com'],
                'extractor': 'spotify',
                'enabled': True
            },
            'soundcloud': {
                'domains': ['soundcloud.com'],
                'extractor': 'soundcloud',
                'enabled': True
            },
            'amazon_music': {
                'domains': ['music.amazon.com', 'amazon.com/music'],
                'extractor': 'amazon',
                'enabled': True
            },
            'apple_music': {
                'domains': ['music.apple.com', 'itunes.apple.com'],
                'extractor': 'apple',
                'enabled': True
            },
            'deezer': {
                'domains': ['deezer.com'],
                'extractor': 'deezer',
                'enabled': True
            },
            'tidal': {
                'domains': ['tidal.com'],
                'extractor': 'tidal',
                'enabled': True
            }
        }
        
        # Security settings
        self.security_config = {
            'max_url_length': 2000,
            'allowed_schemes': ['http', 'https'],
            'suspicious_patterns': [
                r'bit\.ly', r'tinyurl\.com', r'short\.link',
                r'redirect', r'phishing', r'malware',
                r'javascript:', r'data:', r'file:'
            ],
            'cache_duration': 3600,  # 1 hour
            'max_requests_per_minute': 10
        }
        
        # yt-dlp options with security
        self.ytdl_options = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'nocheckcertificate': False,  # Enable certificate checking
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
            'socket_timeout': 30,
            'http_chunk_size': 10485760,  # 10MB chunks
            'extract_flat': False,
            'writethumbnail': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'embedsubtitles': False
        }
        
        # Rate limiting
        self.rate_limits = {}
        
        # Initialize platforms
        self.init_platforms()
    
    def init_platforms(self):
        """Initialize supported music platforms"""
        try:
            # Initialize Spotify if credentials are available
            if (self.bot.config.get('spotify_client_id') and 
                self.bot.config.get('spotify_client_secret')):
                
                client_credentials_manager = SpotifyClientCredentials(
                    client_id=self.bot.config['spotify_client_id'],
                    client_secret=self.bot.config['spotify_client_secret']
                )
                self.spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
                logger.info("Spotify integration initialized successfully")
            else:
                logger.warning("Spotify credentials not provided")
                
        except Exception as e:
            logger.error(f"Error initializing platforms: {e}")
    
    def validate_and_sanitize_url(self, url: str) -> Tuple[bool, str, str]:
        """
        Validate and sanitize URL for security
        Returns: (is_valid, sanitized_url, platform)
        """
        try:
            # Basic length check
            if len(url) > self.security_config['max_url_length']:
                return False, "", "invalid"
            
            # Parse URL
            parsed = urllib.parse.urlparse(url)
            
            # Check scheme
            if parsed.scheme not in self.security_config['allowed_schemes']:
                return False, "", "invalid"
            
            # Check for suspicious patterns
            url_lower = url.lower()
            for pattern in self.security_config['suspicious_patterns']:
                if re.search(pattern, url_lower):
                    logger.warning(f"Suspicious URL pattern detected: {pattern} in {url}")
                    self.suspicious_links.add(url)
                    return False, "", "suspicious"
            
            # Identify platform
            domain = parsed.netloc.lower()
            platform = self.identify_platform(domain)
            
            if not platform:
                return False, "", "unsupported"
            
            # Check if platform is enabled
            if not self.platforms[platform]['enabled']:
                return False, "", "disabled"
            
            # Sanitize URL (remove tracking parameters, etc.)
            sanitized_url = self.sanitize_url(url, platform)
            
            return True, sanitized_url, platform
            
        except Exception as e:
            logger.error(f"Error validating URL {url}: {e}")
            return False, "", "error"
    
    def identify_platform(self, domain: str) -> Optional[str]:
        """Identify music platform from domain"""
        for platform, config in self.platforms.items():
            for platform_domain in config['domains']:
                if platform_domain in domain:
                    return platform
        return None
    
    def sanitize_url(self, url: str, platform: str) -> str:
        """Remove tracking parameters and sanitize URL"""
        try:
            parsed = urllib.parse.urlparse(url)
            
            # Remove common tracking parameters
            tracking_params = [
                'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
                'fbclid', 'gclid', 'ref', 'source', 'campaign'
            ]
            
            query_params = urllib.parse.parse_qs(parsed.query)
            clean_params = {}
            
            for param, value in query_params.items():
                if param.lower() not in tracking_params:
                    clean_params[param] = value
            
            # Rebuild URL
            clean_query = urllib.parse.urlencode(clean_params, doseq=True)
            clean_url = urllib.parse.urlunparse((
                parsed.scheme, parsed.netloc, parsed.path,
                parsed.params, clean_query, parsed.fragment
            ))
            
            return clean_url
            
        except Exception as e:
            logger.error(f"Error sanitizing URL: {e}")
            return url
    
    def check_rate_limit(self, user_id: int) -> bool:
        """Check if user has exceeded rate limits"""
        try:
            current_time = time.time()
            minute = int(current_time // 60)
            
            if user_id not in self.rate_limits:
                self.rate_limits[user_id] = {}
            
            user_limits = self.rate_limits[user_id]
            
            # Clean old entries
            for old_minute in list(user_limits.keys()):
                if old_minute < minute - 1:
                    del user_limits[old_minute]
            
            # Check current minute
            if minute not in user_limits:
                user_limits[minute] = 0
            
            if user_limits[minute] >= self.security_config['max_requests_per_minute']:
                return False
            
            user_limits[minute] += 1
            return True
            
        except Exception as e:
            logger.error(f"Error checking rate limit: {e}")
            return True  # Allow on error
    
    async def search_and_play(self, ctx, query: str):
        """Advanced search and play with security validation"""
        try:
            # Check rate limits
            if not self.check_rate_limit(ctx.author.id):
                await ctx.send("⏰ Troppi richieste! Aspetta un momento prima di richiedere altra musica.")
                return
            
            # Join voice channel
            voice_client, error = await self.join_voice_channel(ctx)
            if error:
                return await ctx.send(error)
            
            # Check if it's a URL
            if self.is_url(query):
                # Validate URL
                is_valid, sanitized_url, platform = self.validate_and_sanitize_url(query)
                
                if not is_valid:
                    if platform == "suspicious":
                        await ctx.send("🚫 Link sospetto rilevato! Non posso processare questo link per motivi di sicurezza.")
                        await self.bot.send_alert_email(
                            "🚨 SUSPICIOUS LINK DETECTED",
                            f"Suspicious link detected from {ctx.author.display_name} ({ctx.author.id})\nLink: {query}\nServer: {ctx.guild.name}"
                        )
                        return
                    elif platform == "unsupported":
                        await ctx.send("❌ Piattaforma non supportata! Prova con YouTube, Spotify, SoundCloud, Amazon Music, Apple Music, Deezer o Tidal.")
                        return
                    elif platform == "disabled":
                        await ctx.send("❌ Questa piattaforma è temporaneamente disabilitata.")
                        return
                    else:
                        await ctx.send("❌ Link non valido!")
                        return
                
                # Process platform-specific URL
                await self.handle_platform_url(ctx, sanitized_url, platform, voice_client)
            else:
                # Search query
                await self.handle_search_query(ctx, query, voice_client)
                
        except Exception as e:
            logger.error(f"Error in search_and_play: {e}")
            await ctx.send(f"❌ Errore durante la riproduzione: {e}")
    
    def is_url(self, text: str) -> bool:
        """Check if text is a URL"""
        try:
            parsed = urllib.parse.urlparse(text)
            return bool(parsed.scheme and parsed.netloc)
        except:
            return False
    
    async def handle_platform_url(self, ctx, url: str, platform: str, voice_client):
        """Handle platform-specific URLs"""
        try:
            if platform == 'youtube':
                await self.handle_youtube_url(ctx, url, voice_client)
            elif platform == 'spotify':
                await self.handle_spotify_url(ctx, url, voice_client)
            elif platform == 'soundcloud':
                await self.handle_soundcloud_url(ctx, url, voice_client)
            elif platform == 'amazon_music':
                await self.handle_amazon_music_url(ctx, url, voice_client)
            elif platform == 'apple_music':
                await self.handle_apple_music_url(ctx, url, voice_client)
            elif platform == 'deezer':
                await self.handle_deezer_url(ctx, url, voice_client)
            elif platform == 'tidal':
                await self.handle_tidal_url(ctx, url, voice_client)
            else:
                await ctx.send(f"❌ Piattaforma {platform} non supportata!")
                
        except Exception as e:
            logger.error(f"Error handling {platform} URL: {e}")
            await ctx.send(f"❌ Errore processando link {platform}!")
    
    async def handle_youtube_url(self, ctx, url: str, voice_client):
        """Handle YouTube URLs with enhanced security"""
        try:
            # Check cache first
            url_hash = hashlib.md5(url.encode()).hexdigest()
            if url_hash in self.link_cache:
                cache_data = self.link_cache[url_hash]
                if time.time() - cache_data['timestamp'] < self.security_config['cache_duration']:
                    # Use cached data
                    track_info = cache_data['data']
                    await self.add_to_queue(ctx.guild.id, track_info, voice_client)
                    return
            
            ytdl = yt_dlp.YoutubeDL(self.ytdl_options)
            
            # Extract info with timeout
            try:
                info = ytdl.extract_info(url, download=False)
            except Exception as e:
                logger.error(f"Error extracting YouTube info: {e}")
                await ctx.send("❌ Errore estraendo informazioni dal video YouTube!")
                return
            
            if not info:
                await ctx.send("❌ Non riesco a ottenere informazioni dal video!")
                return
            
            # Validate extracted info
            if not self.validate_track_info(info):
                await ctx.send("❌ Informazioni del video non valide!")
                return
            
            track_info = self.create_track_info(info, ctx.author, 'youtube')
            
            # Cache the result
            self.link_cache[url_hash] = {
                'data': track_info,
                'timestamp': time.time()
            }
            
            await self.add_to_queue(ctx.guild.id, track_info, voice_client)
            
        except Exception as e:
            logger.error(f"Error handling YouTube URL: {e}")
            await ctx.send("❌ Errore processando link YouTube!")
    
    async def handle_spotify_url(self, ctx, url: str, voice_client):
        """Handle Spotify URLs"""
        try:
            if not self.spotify:
                await ctx.send("❌ Spotify non configurato!")
                return
            
            track_id = self.extract_spotify_id(url)
            if not track_id:
                await ctx.send("❌ Link Spotify non valido!")
                return
            
            track = self.spotify.track(track_id)
            track_name = f"{track['name']} by {track['artists'][0]['name']}"
            
            # Search on YouTube
            search_query = f"{track_name} official audio"
            await self.handle_search_query(ctx, search_query, voice_client, spotify_info=track)
            
        except Exception as e:
            logger.error(f"Error handling Spotify URL: {e}")
            await ctx.send("❌ Errore processando link Spotify!")
    
    async def handle_soundcloud_url(self, ctx, url: str, voice_client):
        """Handle SoundCloud URLs"""
        try:
            ytdl = yt_dlp.YoutubeDL(self.ytdl_options)
            info = ytdl.extract_info(url, download=False)
            
            if not info:
                await ctx.send("❌ Non riesco a ottenere informazioni da SoundCloud!")
                return
            
            track_info = self.create_track_info(info, ctx.author, 'soundcloud')
            await self.add_to_queue(ctx.guild.id, track_info, voice_client)
            
        except Exception as e:
            logger.error(f"Error handling SoundCloud URL: {e}")
            await ctx.send("❌ Errore processando link SoundCloud!")
    
    async def handle_amazon_music_url(self, ctx, url: str, voice_client):
        """Handle Amazon Music URLs"""
        try:
            # Extract track info from URL or search
            track_name = self.extract_amazon_track_info(url)
            if track_name:
                search_query = f"{track_name} amazon music"
                await self.handle_search_query(ctx, search_query, voice_client, platform_info={'platform': 'amazon', 'url': url})
            else:
                await ctx.send("❌ Non riesco a estrarre informazioni dal link Amazon Music!")
                
        except Exception as e:
            logger.error(f"Error handling Amazon Music URL: {e}")
            await ctx.send("❌ Errore processando link Amazon Music!")
    
    async def handle_apple_music_url(self, ctx, url: str, voice_client):
        """Handle Apple Music URLs"""
        try:
            track_name = self.extract_apple_track_info(url)
            if track_name:
                search_query = f"{track_name} apple music"
                await self.handle_search_query(ctx, search_query, voice_client, platform_info={'platform': 'apple', 'url': url})
            else:
                await ctx.send("❌ Non riesco a estrarre informazioni dal link Apple Music!")
                
        except Exception as e:
            logger.error(f"Error handling Apple Music URL: {e}")
            await ctx.send("❌ Errore processando link Apple Music!")
    
    async def handle_deezer_url(self, ctx, url: str, voice_client):
        """Handle Deezer URLs"""
        try:
            track_name = self.extract_deezer_track_info(url)
            if track_name:
                search_query = f"{track_name} deezer"
                await self.handle_search_query(ctx, search_query, voice_client, platform_info={'platform': 'deezer', 'url': url})
            else:
                await ctx.send("❌ Non riesco a estrarre informazioni dal link Deezer!")
                
        except Exception as e:
            logger.error(f"Error handling Deezer URL: {e}")
            await ctx.send("❌ Errore processando link Deezer!")
    
    async def handle_tidal_url(self, ctx, url: str, voice_client):
        """Handle Tidal URLs"""
        try:
            track_name = self.extract_tidal_track_info(url)
            if track_name:
                search_query = f"{track_name} tidal"
                await self.handle_search_query(ctx, search_query, voice_client, platform_info={'platform': 'tidal', 'url': url})
            else:
                await ctx.send("❌ Non riesco a estrarre informazioni dal link Tidal!")
                
        except Exception as e:
            logger.error(f"Error handling Tidal URL: {e}")
            await ctx.send("❌ Errore processando link Tidal!")
    
    def extract_spotify_id(self, url: str) -> Optional[str]:
        """Extract track ID from Spotify URL"""
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
    
    def extract_amazon_track_info(self, url: str) -> Optional[str]:
        """Extract track info from Amazon Music URL"""
        # This would need to be implemented based on Amazon Music URL structure
        # For now, return a generic search term
        return "amazon music track"
    
    def extract_apple_track_info(self, url: str) -> Optional[str]:
        """Extract track info from Apple Music URL"""
        # Extract from iTunes/Apple Music URLs
        patterns = [
            r'id=(\d+)',
            r'/album/[^/]+/(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return f"apple music {match.group(1)}"
        return "apple music track"
    
    def extract_deezer_track_info(self, url: str) -> Optional[str]:
        """Extract track info from Deezer URL"""
        patterns = [
            r'/track/(\d+)',
            r'/album/[^/]+/(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return f"deezer {match.group(1)}"
        return "deezer track"
    
    def extract_tidal_track_info(self, url: str) -> Optional[str]:
        """Extract track info from Tidal URL"""
        patterns = [
            r'/track/(\d+)',
            r'/album/[^/]+/(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return f"tidal {match.group(1)}"
        return "tidal track"
    
    def validate_track_info(self, info: Dict) -> bool:
        """Validate extracted track information"""
        try:
            required_fields = ['title', 'duration']
            for field in required_fields:
                if field not in info or not info[field]:
                    return False
            
            # Check duration (max 10 hours)
            if info.get('duration', 0) > 36000:
                return False
            
            # Check title length
            if len(info.get('title', '')) > 200:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating track info: {e}")
            return False
    
    def create_track_info(self, info: Dict, requester: discord.Member, source: str) -> Dict:
        """Create standardized track info"""
        return {
            'title': info.get('title', 'Unknown Title'),
            'url': info.get('url') or info.get('webpage_url'),
            'duration': info.get('duration', 0),
            'requester': requester,
            'source': source,
            'thumbnail': info.get('thumbnail'),
            'uploader': info.get('uploader', 'Unknown'),
            'view_count': info.get('view_count', 0),
            'description': info.get('description', '')[:200] if info.get('description') else '',
            'created_at': datetime.now()
        }
    
    async def handle_search_query(self, ctx, query: str, voice_client, spotify_info=None, platform_info=None):
        """Handle search queries with enhanced security"""
        try:
            # Sanitize search query
            sanitized_query = self.sanitize_search_query(query)
            
            ytdl = yt_dlp.YoutubeDL(self.ytdl_options)
            
            # Search with timeout
            search_results = ytdl.extract_info(f"ytsearch:{sanitized_query}", download=False)
            
            if not search_results or 'entries' not in search_results:
                await ctx.send("❌ Nessun risultato trovato!")
                return
            
            # Get first result
            video_info = search_results['entries'][0]
            
            if not self.validate_track_info(video_info):
                await ctx.send("❌ Risultato non valido!")
                return
            
            track_info = self.create_track_info(video_info, ctx.author, 'youtube')
            
            # Add platform-specific info
            if spotify_info:
                track_info['spotify_info'] = spotify_info
            if platform_info:
                track_info['platform_info'] = platform_info
            
            await self.add_to_queue(ctx.guild.id, track_info, voice_client)
            
        except Exception as e:
            logger.error(f"Error handling search query: {e}")
            await ctx.send("❌ Errore durante la ricerca!")
    
    def sanitize_search_query(self, query: str) -> str:
        """Sanitize search query for security"""
        # Remove potentially harmful characters
        sanitized = re.sub(r'[<>"\']', '', query)
        # Limit length
        sanitized = sanitized[:100]
        return sanitized.strip()
    
    async def join_voice_channel(self, ctx):
        """Join voice channel with error handling"""
        try:
            if not ctx.author.voice:
                return None, "❌ Devi essere in un canale vocale per ascoltare musica!"
            
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
            return None, f"❌ Errore unendosi al canale vocale: {e}"
    
    async def add_to_queue(self, guild_id: int, track_info: dict, voice_client):
        """Add track to queue with enhanced controls"""
        try:
            if guild_id not in self.music_queues:
                self.music_queues[guild_id] = []
            
            # Add track to queue
            self.music_queues[guild_id].append(track_info)
            
            # Initialize playback controls
            if guild_id not in self.playback_controls:
                self.playback_controls[guild_id] = {
                    'paused': False,
                    'volume': 0.5,
                    'loop': False,
                    'shuffle': False
                }
            
            # If first track, start playing
            if len(self.music_queues[guild_id]) == 1:
                await self.play_next(guild_id, voice_client)
            else:
                # Send enhanced queue notification
                await self.send_queue_notification(voice_client, track_info)
            
        except Exception as e:
            logger.error(f"Error adding to queue: {e}")
    
    async def send_queue_notification(self, voice_client, track_info: dict):
        """Send enhanced queue notification"""
        try:
            embed = discord.Embed(
                title="🎵 Aggiunto alla Coda",
                description=f"**{track_info['title']}**",
                color=0x00ff00
            )
            
            # Add platform-specific info
            if track_info.get('spotify_info'):
                spotify = track_info['spotify_info']
                embed.add_field(
                    name="🎧 Spotify",
                    value=f"**{spotify['name']}** by {spotify['artists'][0]['name']}",
                    inline=False
                )
            
            if track_info.get('platform_info'):
                platform = track_info['platform_info']
                embed.add_field(
                    name="🌐 Piattaforma",
                    value=platform['platform'].title(),
                    inline=True
                )
            
            embed.add_field(
                name="⏱️ Durata",
                value=self.format_duration(track_info['duration']),
                inline=True
            )
            embed.add_field(
                name="👤 Richiesto da",
                value=track_info['requester'].mention,
                inline=True
            )
            
            embed.add_field(
                name="📍 Posizione",
                value=f"#{len(self.music_queues[voice_client.guild.id])}",
                inline=True
            )
            
            # Add thumbnail if available
            if track_info.get('thumbnail'):
                embed.set_thumbnail(url=track_info['thumbnail'])
            
            channel = voice_client.channel
            if channel:
                await channel.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error sending queue notification: {e}")
    
    async def play_next(self, guild_id: int, voice_client):
        """Play next track with enhanced controls"""
        try:
            if guild_id not in self.music_queues or not self.music_queues[guild_id]:
                return
            
            track_info = self.music_queues[guild_id][0]
            
            # Create audio source with enhanced options
            ytdl = yt_dlp.YoutubeDL(self.ytdl_options)
            
            def after_playing(error):
                if error:
                    logger.error(f"Error in audio playback: {error}")
                else:
                    # Play next track when current finishes
                    asyncio.create_task(self.on_track_finished(guild_id, voice_client))
            
            try:
                info = ytdl.extract_info(track_info['url'], download=False)
                url = info.get('url')
                
                if url:
                    # Enhanced audio source with better error handling
                    audio_source = discord.FFmpegPCMAudio(
                        url,
                        before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -bufsize 1024k",
                        options="-vn -b:a 128k"
                    )
                    
                    voice_client.play(audio_source, after=after_playing)
                    
                    # Set now playing
                    self.now_playing[guild_id] = track_info
                    
                    # Send enhanced now playing message
                    await self.send_now_playing_message(voice_client, track_info)
                    
                else:
                    logger.error("Could not extract audio URL")
                    await self.on_track_finished(guild_id, voice_client)
                    
            except Exception as e:
                logger.error(f"Error creating audio source: {e}")
                await self.on_track_finished(guild_id, voice_client)
            
        except Exception as e:
            logger.error(f"Error playing next track: {e}")
    
    async def send_now_playing_message(self, voice_client, track_info: dict):
        """Send enhanced now playing message"""
        try:
            embed = discord.Embed(
                title="🎵 Ora in Riproduzione",
                description=f"**{track_info['title']}**",
                color=0x00ff00
            )
            
            # Add platform-specific info
            if track_info.get('spotify_info'):
                spotify = track_info['spotify_info']
                embed.add_field(
                    name="🎧 Spotify",
                    value=f"**{spotify['name']}** by {spotify['artists'][0]['name']}",
                    inline=False
                )
            
            if track_info.get('platform_info'):
                platform = track_info['platform_info']
                embed.add_field(
                    name="🌐 Fonte",
                    value=platform['platform'].title(),
                    inline=True
                )
            
            embed.add_field(
                name="⏱️ Durata",
                value=self.format_duration(track_info['duration']),
                inline=True
            )
            embed.add_field(
                name="👤 Richiesto da",
                value=track_info['requester'].mention,
                inline=True
            )
            
            # Add uploader info for YouTube
            if track_info.get('uploader'):
                embed.add_field(
                    name="📺 Canale",
                    value=track_info['uploader'],
                    inline=True
                )
            
            # Add thumbnail
            if track_info.get('thumbnail'):
                embed.set_thumbnail(url=track_info['thumbnail'])
            
            channel = voice_client.channel
            if channel:
                await channel.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error sending now playing message: {e}")
    
    async def on_track_finished(self, guild_id: int, voice_client):
        """Handle track finishing with loop support"""
        try:
            controls = self.playback_controls.get(guild_id, {})
            
            if controls.get('loop') and guild_id in self.music_queues and self.music_queues[guild_id]:
                # Loop current track
                await self.play_next(guild_id, voice_client)
                return
            
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
    
    # Enhanced playback controls
    async def pause_music(self, guild_id: int, voice_client):
        """Pause music playback"""
        try:
            if voice_client and voice_client.is_playing():
                voice_client.pause()
                if guild_id in self.playback_controls:
                    self.playback_controls[guild_id]['paused'] = True
                return True
            return False
        except Exception as e:
            logger.error(f"Error pausing music: {e}")
            return False
    
    async def resume_music(self, guild_id: int, voice_client):
        """Resume music playback"""
        try:
            if voice_client and voice_client.is_paused():
                voice_client.resume()
                if guild_id in self.playback_controls:
                    self.playback_controls[guild_id]['paused'] = False
                return True
            return False
        except Exception as e:
            logger.error(f"Error resuming music: {e}")
            return False
    
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
            
            if guild_id in self.playback_controls:
                self.playback_controls[guild_id]['paused'] = False
                self.playback_controls[guild_id]['loop'] = False
            
            return True
            
        except Exception as e:
            logger.error(f"Error stopping music: {e}")
            return False
    
    def toggle_loop(self, guild_id: int):
        """Toggle loop mode"""
        try:
            if guild_id not in self.playback_controls:
                self.playback_controls[guild_id] = {'loop': False}
            
            self.playback_controls[guild_id]['loop'] = not self.playback_controls[guild_id]['loop']
            return self.playback_controls[guild_id]['loop']
        except Exception as e:
            logger.error(f"Error toggling loop: {e}")
            return False
    
    def toggle_shuffle(self, guild_id: int):
        """Toggle shuffle mode"""
        try:
            if guild_id not in self.playback_controls:
                self.playback_controls[guild_id] = {'shuffle': False}
            
            self.playback_controls[guild_id]['shuffle'] = not self.playback_controls[guild_id]['shuffle']
            
            # Apply shuffle to current queue
            if self.playback_controls[guild_id]['shuffle'] and guild_id in self.music_queues:
                queue = self.music_queues[guild_id]
                if len(queue) > 1:
                    # Keep first track, shuffle the rest
                    first_track = queue[0]
                    remaining = queue[1:]
                    import random
                    random.shuffle(remaining)
                    self.music_queues[guild_id] = [first_track] + remaining
            
            return self.playback_controls[guild_id]['shuffle']
        except Exception as e:
            logger.error(f"Error toggling shuffle: {e}")
            return False
    
    async def remove_track_from_queue(self, guild_id: int, position: int):
        """Remove specific track from queue"""
        try:
            if guild_id in self.music_queues and 0 < position <= len(self.music_queues[guild_id]):
                removed_track = self.music_queues[guild_id].pop(position - 1)
                return removed_track
            return None
        except Exception as e:
            logger.error(f"Error removing track from queue: {e}")
            return None
    
    def format_duration(self, seconds: int) -> str:
        """Format duration in seconds to MM:SS or HH:MM:SS"""
        try:
            if seconds == 0:
                return "Sconosciuto"
            
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            
            if hours > 0:
                return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                return f"{minutes:02d}:{seconds:02d}"
            
        except Exception:
            return "Sconosciuto"
    
    def get_queue_info(self, guild_id: int) -> Dict:
        """Get comprehensive queue information"""
        try:
            queue = self.music_queues.get(guild_id, [])
            now_playing = self.now_playing.get(guild_id)
            controls = self.playback_controls.get(guild_id, {})
            
            return {
                'now_playing': now_playing,
                'queue_length': len(queue),
                'queue': queue,
                'is_playing': now_playing is not None,
                'is_paused': controls.get('paused', False),
                'is_looping': controls.get('loop', False),
                'is_shuffled': controls.get('shuffle', False),
                'volume': controls.get('volume', 0.5)
            }
            
        except Exception as e:
            logger.error(f"Error getting queue info: {e}")
            return {'error': str(e)}
