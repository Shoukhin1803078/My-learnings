import streamlit as st
import yt_dlp
import os
import tempfile
from io import BytesIO
import base64
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Multi-Platform Video Downloader",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    :root {
        --primary: #6c5ce7;
        --secondary: #a29bfe;
        --accent: #fd79a8;
        --success: #00b894;
        --info: #0984e3;
        --warning: #fdcb6e;
        --danger: #d63031;
        --light: #f8f9fa;
        --dark: #343a40;
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .platform-badge {
        display: inline-block;
        padding: 0.35rem 1rem;
        margin: 0.25rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .youtube { background-color: #ff0000; color: white; }
    .facebook { background-color: #1877f2; color: white; }
    .linkedin { background-color: #0077b5; color: white; }
    .unknown { background-color: var(--dark); color: white; }
    
    .stButton > button {
        width: 100%;
        border-radius: 25px;
        height: 3rem;
        font-weight: bold;
        transition: all 0.3s ease;
        border: none;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:disabled {
        background: #e9ecef;
        color: #6c757d;
    }
    
    .download-section {
        background-color: var(--light);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid var(--success);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    
    .info-section {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid var(--info);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    
    .error-section {
        background-color: #fff5f5;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid var(--danger);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .video-container {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .video-container iframe {
        width: 100% !important;
        height: 315px !important;
        max-height: 315px !important;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .thumbnail-container {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .thumbnail-container img {
        max-height: 250px !important;
        width: auto !important;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .progress-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid var(--warning);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: var(--dark);
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    .feature-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border-left: 4px solid var(--primary);
    }
    
    .feature-card h4 {
        color: var(--primary);
        margin-top: 0;
    }
    
    .feature-card p {
        color: var(--dark);
        margin-bottom: 0;
    }
    
    .footer {
        text-align: center;
        color: var(--dark);
        padding: 2rem 0;
        margin-top: 2rem;
        border-top: 1px solid #e9ecef;
    }
    
    /* Animation for buttons */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header {
            padding: 1.5rem 0;
        }
        
        .video-container iframe {
            height: 200px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

class StreamlitVideoDownloader:
    def __init__(self):
        self.supported_platforms = {
            'youtube': ['youtube.com', 'youtu.be'],
            'facebook': ['facebook.com', 'fb.com', 'fb.watch'],
            'linkedin': ['linkedin.com'],
            'instagram': ['instagram.com']
        }
        
    def detect_platform(self, url):
        """Detect which platform the URL belongs to"""
        if not url:
            return 'unknown'
            
        url_lower = url.lower()
        for platform, domains in self.supported_platforms.items():
            for domain in domains:
                if domain in url_lower:
                    return platform
        return 'unknown'
    
    def get_platform_badge(self, platform):
        """Get HTML badge for platform"""
        platform_info = {
            'youtube': ('📺 YouTube', 'youtube'),
            'facebook': ('📘 Facebook', 'facebook'),
            'linkedin': ('💼 LinkedIn', 'linkedin'),
            'instagram': ('📷 Instagram', 'instagram'),
            'unknown': ('❓ Unknown', 'unknown')
        }
        
        label, css_class = platform_info.get(platform, ('❓ Unknown', 'unknown'))
        return f'<span class="platform-badge {css_class}">{label}</span>'
    
    def get_platform_specific_options(self, platform):
        """Get platform-specific yt-dlp options"""
        base_opts = {
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True
        }
        
        if platform == 'facebook':
            base_opts.update({
                'extractor_args': {
                    'facebook': {
                        'skip_dash_manifest': True,
                    }
                }
            })
        elif platform == 'linkedin':
            base_opts.update({
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            })
        elif platform == 'instagram':
            base_opts.update({
                'cookiefile': 'cookies.txt'  # Instagram may require login
            })
        
        return base_opts
    
    def format_duration(self, seconds):
        """Format duration from seconds to readable format"""
        if not seconds:
            return "Unknown"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    def format_file_size(self, bytes):
        """Format file size in human-readable format"""
        if bytes < 1024:
            return f"{bytes} B"
        elif bytes < 1024 * 1024:
            return f"{bytes / 1024:.1f} KB"
        elif bytes < 1024 * 1024 * 1024:
            return f"{bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{bytes / (1024 * 1024 * 1024):.1f} GB"
    
    def get_video_info(self, url, platform):
        """Get video information"""
        try:
            ydl_opts = self.get_platform_specific_options(platform)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info, None
        except Exception as e:
            return None, str(e)
    
    def download_video(self, url, platform, quality, format_type, temp_dir):
        """Download video and return file path"""
        try:
            # Get platform-specific options
            ydl_opts = self.get_platform_specific_options(platform)
            ydl_opts['outtmpl'] = os.path.join(temp_dir, '%(title)s.%(ext)s')
            
            if format_type == 'mp3':
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                # Video format selection
                if platform == 'youtube':
                    if quality == 'best':
                        format_selector = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
                    else:
                        format_selector = f'bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality}][ext=mp4]/best[ext=mp4]/best'
                elif platform == 'facebook':
                    if quality == 'best':
                        format_selector = 'best'
                    else:
                        format_selector = f'best[height<={quality}]/best'
                elif platform == 'linkedin':
                    format_selector = 'best'
                elif platform == 'instagram':
                    format_selector = 'best'
                
                ydl_opts.update({
                    'format': format_selector,
                })
            
            # Progress hook function
            def progress_hook(d):
                if d['status'] == 'downloading':
                    if 'downloaded_bytes' in d and 'total_bytes' in d:
                        percent = d['downloaded_bytes'] / d['total_bytes']
                        st.session_state.download_progress = percent * 100
            
            ydl_opts['progress_hooks'] = [progress_hook]
            
            # Download
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # Find downloaded file
                for file in os.listdir(temp_dir):
                    if file.endswith(('.mp4', '.mp3', '.webm', '.mkv', '.avi', '.mov')):
                        return os.path.join(temp_dir, file), info, None
                
                return None, info, "No file found after download"
        
        except Exception as e:
            return None, None, str(e)

def main():
    # Initialize downloader
    downloader = StreamlitVideoDownloader()
    
    # Header with animated gradient
    st.markdown("""
    <div class="main-header">
        <h1 style="margin-bottom: 0.5rem;">🎥 Multi-Platform Video Downloader</h1>
        <p style="font-size: 1.1rem; opacity: 0.9;">Download videos from YouTube, Facebook, LinkedIn, and more</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'video_info' not in st.session_state:
        st.session_state.video_info = None
    if 'download_ready' not in st.session_state:
        st.session_state.download_ready = False
    if 'download_progress' not in st.session_state:
        st.session_state.download_progress = 0
    
    # Sidebar with enhanced UI
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <h2>🎛️ Settings</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Quality selection with tooltip
        st.markdown("""
        <div class="tooltip">
            <label style="font-weight: bold; margin-bottom: 0.5rem; display: block;">📊 Video Quality</label>
            <span class="tooltiptext">Select the desired video resolution. 'Best Available' will download the highest quality.</span>
        </div>
        """, unsafe_allow_html=True)
        quality = st.selectbox(
            "Video Quality",
            options=['best', '1080', '720', '480', '360', '240', '144'],
            format_func=lambda x: 'Best Available' if x == 'best' else f'{x}p',
            index=2,  # Default to 720p
            label_visibility="collapsed"
        )
        
        # Format selection with tooltip
        st.markdown("""
        <div class="tooltip">
            <label style="font-weight: bold; margin-bottom: 0.5rem; display: block;">📦 Format</label>
            <span class="tooltiptext">Choose between video (MP4) or audio-only (MP3) format.</span>
        </div>
        """, unsafe_allow_html=True)
        format_type = st.selectbox(
            "Format",
            options=['mp4', 'mp3'],
            format_func=lambda x: 'MP4 (Video)' if x == 'mp4' else 'MP3 (Audio Only)',
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Supported platforms with cards
        st.markdown("""
        <div style="text-align: center;">
            <h3>🌐 Supported Platforms</h3>
        </div>
        """, unsafe_allow_html=True)
        
        platforms = [
            {"name": "YouTube", "icon": "📺", "color": "#ff0000", "domains": "youtube.com, youtu.be"},
            {"name": "Facebook", "icon": "📘", "color": "#1877f2", "domains": "facebook.com, fb.watch"},
            {"name": "LinkedIn", "icon": "💼", "color": "#0077b5", "domains": "linkedin.com"},
            {"name": "Instagram", "icon": "📷", "color": "#e1306c", "domains": "instagram.com"}
        ]
        
        for platform in platforms:
            st.markdown(f"""
            <div style="background-color: {platform['color']}10; border-radius: 10px; padding: 0.75rem; margin-bottom: 0.75rem; border-left: 4px solid {platform['color']}">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.5rem; margin-right: 0.75rem;">{platform['icon']}</span>
                    <div>
                        <strong>{platform['name']}</strong>
                        <div style="font-size: 0.8rem; color: #6c757d;">{platform['domains']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Tips section with feature cards
        st.markdown("""
        <div style="text-align: center;">
            <h3>💡 Tips & Tricks</h3>
        </div>
        """, unsafe_allow_html=True)
        
        tips = [
            {
                "title": "Direct Links Work Best",
                "icon": "🔗",
                "content": "Use direct video links instead of playlist or channel URLs for best results."
            },
            {
                "title": "Check Privacy Settings",
                "icon": "🔒",
                "content": "Some videos may require public access or login credentials."
            },
            {
                "title": "Quality vs Size",
                "icon": "⚖️",
                "content": "Higher quality means larger file size. Choose wisely based on your needs."
            }
        ]
        
        for tip in tips:
            with st.expander(f"{tip['icon']} {tip['title']}"):
                st.markdown(tip['content'])
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # URL input with floating label effect
        st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h3 style="margin-bottom: 0.5rem;">🔗 Paste Video URL</h3>
            <p style="font-size: 0.9rem; color: #6c757d; margin-top: 0;">Works with YouTube, Facebook, LinkedIn, and more</p>
        </div>
        """, unsafe_allow_html=True)
        
        url = st.text_input(
            "Video URL",
            placeholder="https://www.youtube.com/watch?v=...",
            label_visibility="collapsed"
        )
        
        # Platform detection with animated badge
        if url:
            platform = downloader.detect_platform(url)
            badge_html = downloader.get_platform_badge(platform)
            st.markdown(f"**Detected Platform:** {badge_html}", unsafe_allow_html=True)
            
            if platform == 'unknown':
                st.markdown("""
                <div class="error-section">
                    <p style="margin: 0;">❌ <strong>Unsupported platform</strong>. Please use YouTube, Facebook, LinkedIn, or Instagram URLs.</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Action buttons with improved layout
        st.markdown("""
        <div style="margin-top: 1.5rem; margin-bottom: 1.5rem;">
            <h3 style="margin-bottom: 0.5rem;">⚡ Actions</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col_info, col_download = st.columns(2)
        
        with col_info:
            if st.button("🔍 Get Video Info", 
                        disabled=not url or downloader.detect_platform(url) == 'unknown',
                        key="info_button"):
                platform = downloader.detect_platform(url)
                
                with st.spinner(f"🔍 Fetching video information from {platform.title()}..."):
                    info, error = downloader.get_video_info(url, platform)
                    
                    if error:
                        st.markdown(f"""
                        <div class="error-section">
                            <p style="margin: 0;">❌ <strong>Error:</strong> {error}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.session_state.video_info = None
                    else:
                        st.session_state.video_info = info
                        st.markdown("""
                        <div class="download-section">
                            <p style="margin: 0;">✅ <strong>Video information loaded!</strong> Check the preview section.</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        with col_download:
            download_disabled = not url or downloader.detect_platform(url) == 'unknown'
            download_button = st.button("⬇️ Download Video", 
                                      disabled=download_disabled,
                                      key="download_button")
            
            if download_button:
                platform = downloader.detect_platform(url)
                
                # Create temporary directory
                temp_dir = tempfile.mkdtemp()
                
                # Reset progress
                st.session_state.download_progress = 0
                
                # Show progress container
                with st.empty():
                    st.markdown("""
                    <div class="progress-container">
                        <h4 style="margin-top: 0;">🚀 Download Progress</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    progress_bar = st.progress(st.session_state.download_progress)
                    status_text = st.empty()
                    
                    try:
                        status_text.markdown("""
                        <div style="margin-bottom: 1rem;">
                            <p style="margin: 0;">Preparing download from {platform.title()}...</p>
                        </div>
                        """.format(platform=platform.title()), unsafe_allow_html=True)
                        
                        file_path, info, error = downloader.download_video(
                            url, platform, quality, format_type, temp_dir
                        )
                        
                        if error:
                            st.markdown(f"""
                            <div class="error-section">
                                <p style="margin: 0;">❌ <strong>Download failed:</strong> {error}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        elif file_path:
                            progress_bar.progress(100)
                            status_text.markdown("""
                            <div style="margin-bottom: 1rem;">
                                <p style="margin: 0;">✅ <strong>Download completed!</strong></p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Prepare file for download
                            with open(file_path, 'rb') as file:
                                file_data = file.read()
                            
                            filename = os.path.basename(file_path)
                            file_size = len(file_data)
                            
                            # Show success message with file info
                            st.markdown(f"""
                            <div class="download-section">
                                <div style="display: flex; align-items: center; justify-content: space-between;">
                                    <div>
                                        <p style="margin: 0; font-size: 1.1rem;">🎉 <strong>Download ready!</strong></p>
                                        <p style="margin: 0; font-size: 0.9rem; color: #6c757d;">
                                            {filename} • {downloader.format_file_size(file_size)}
                                        </p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Download button with pulse animation
                            st.download_button(
                                label="💾 Download to Computer",
                                data=file_data,
                                file_name=filename,
                                mime="application/octet-stream",
                                key="download_file_button",
                                help="Click to save the file to your computer"
                            )
                        
                    except Exception as e:
                        st.markdown(f"""
                        <div class="error-section">
                            <p style="margin: 0;">❌ <strong>Unexpected error:</strong> {str(e)}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    finally:
                        # Cleanup
                        import shutil
                        try:
                            shutil.rmtree(temp_dir)
                        except:
                            pass
    
    with col2:
        # Video preview and information display
        if url and st.session_state.video_info:
            info = st.session_state.video_info
            platform = downloader.detect_platform(url)
            
            # Video Preview Section
            st.markdown("""
            <div style="margin-bottom: 1.5rem;">
                <h3 style="margin-bottom: 0.5rem;">🎬 Video Preview</h3>
                <p style="font-size: 0.9rem; color: #6c757d; margin-top: 0;">Preview of the video you're about to download</p>
            </div>
            """, unsafe_allow_html=True)
            
            try:
                # For YouTube videos, show embedded video
                if platform == 'youtube':
                    # Extract video ID from different YouTube URL formats
                    video_id = None
                    if 'youtube.com/watch?v=' in url:
                        video_id = url.split('watch?v=')[1].split('&')[0]
                    elif 'youtu.be/' in url:
                        video_id = url.split('youtu.be/')[1].split('?')[0]
                    
                    if video_id:
                        # Embed YouTube video in a fixed-size container
                        st.markdown("""
                        <div class="video-container">
                        """, unsafe_allow_html=True)
                        st.video(f"https://www.youtube.com/watch?v={video_id}")
                        st.markdown("""
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("📺 YouTube video detected but unable to preview")
                
                # For other platforms, show thumbnail if available
                else:
                    thumbnail_url = info.get('thumbnail')
                    if thumbnail_url:
                        st.markdown("""
                        <div class="thumbnail-container">
                        """, unsafe_allow_html=True)
                        st.image(thumbnail_url, caption=f"{platform.title()} Video Thumbnail")
                        st.markdown("""
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"""
                        <div style="text-align: center; margin-bottom: 1.5rem;">
                            <a href="{url}" target="_blank" style="text-decoration: none;">
                                <button style="background-color: #6c5ce7; color: white; border: none; padding: 0.5rem 1rem; border-radius: 25px; cursor: pointer;">
                                    🔗 Open in {platform.title()}
                                </button>
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info(f"{platform.title()} video detected. Click below to view on {platform.title()}.")
                        st.markdown(f"""
                        <div style="text-align: center; margin-bottom: 1.5rem;">
                            <a href="{url}" target="_blank" style="text-decoration: none;">
                                <button style="background-color: #6c5ce7; color: white; border: none; padding: 0.5rem 1rem; border-radius: 25px; cursor: pointer;">
                                    🔗 View on {platform.title()}
                                </button>
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
                
            except Exception as e:
                st.warning("⚠️ Unable to load video preview")
            
            # Video Information Section
            st.markdown("""
            <div style="margin-top: 1.5rem; margin-bottom: 1.5rem;">
                <h3 style="margin-bottom: 0.5rem;">📊 Video Details</h3>
                <p style="font-size: 0.9rem; color: #6c757d; margin-top: 0;">Detailed information about the video</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-section">
            """, unsafe_allow_html=True)
            
            # Title with copy button
            col_title, col_copy = st.columns([4, 1])
            with col_title:
                st.markdown(f"**📝 Title:** {info.get('title', 'N/A')}")
            with col_copy:
                if st.button("📋", key="copy_title"):
                    st.session_state.copied_title = info.get('title', 'N/A')
                    st.toast("Title copied to clipboard!", icon="📋")
            
            # Platform-specific info
            if platform == 'youtube':
                st.markdown(f"**👤 Channel:** {info.get('uploader', 'N/A')}")
                views = info.get('view_count', 0)
                if views:
                    st.markdown(f"**👀 Views:** {views:,}")
            else:
                st.markdown(f"**👤 Uploader:** {info.get('uploader', 'N/A')}")
            
            duration = downloader.format_duration(info.get('duration', 0))
            st.markdown(f"**⏱️ Duration:** {duration}")
            
            upload_date = info.get('upload_date', 'N/A')
            if upload_date != 'N/A' and len(upload_date) == 8:
                formatted_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
                st.markdown(f"**📅 Upload Date:** {formatted_date}")
            
            # Available formats
            formats = info.get('formats', [])
            if formats:
                video_formats = set()
                for f in formats:
                    if f.get('vcodec') != 'none' and f.get('height'):
                        video_formats.add(f.get('height'))
                
                if video_formats:
                    sorted_formats = sorted(video_formats, reverse=True)
                    format_text = ", ".join([f"{h}p" for h in sorted_formats])
                    st.markdown(f"**📊 Available Resolutions:** {format_text}")
            
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)
        else:
            # How to use section with feature cards
            st.markdown("""
            <div style="margin-bottom: 1.5rem;">
                <h3 style="margin-bottom: 0.5rem;">✨ How to Use</h3>
                <p style="font-size: 0.9rem; color: #6c757d; margin-top: 0;">Simple steps to download your videos</p>
            </div>
            """, unsafe_allow_html=True)
            
            steps = [
                {
                    "icon": "1️⃣",
                    "title": "Paste Video URL",
                    "content": "Copy and paste any video URL from supported platforms into the input field."
                },
                {
                    "icon": "2️⃣",
                    "title": "Adjust Settings",
                    "content": "Select your preferred quality and format in the sidebar settings."
                },
                {
                    "icon": "3️⃣",
                    "title": "Get Video Info",
                    "content": "Click the 'Get Video Info' button to preview the video and check details."
                },
                {
                    "icon": "4️⃣",
                    "title": "Download",
                    "content": "Click 'Download Video' to save it to your device in your chosen format."
                }
            ]
            
            for step in steps:
                with st.expander(f"{step['icon']} {step['title']}", expanded=True):
                    st.markdown(step['content'])
    
    # Footer with copyright and version
    st.markdown("""
    <div class="footer">
        <p style="margin: 0.5rem 0;">🎥 <strong>Multi-Platform Video Downloader</strong></p>
        <p style="margin: 0.5rem 0; font-size: 0.9rem;">Built with Streamlit • Supports YouTube, Facebook, LinkedIn, and more</p>
        <p style="margin: 0.5rem 0; font-size: 0.8rem; color: #adb5bd;">© {year} Video Downloader • v1.1.0</p>
    </div>
    """.format(year=datetime.now().year), unsafe_allow_html=True)

if __name__ == "__main__":
    main()