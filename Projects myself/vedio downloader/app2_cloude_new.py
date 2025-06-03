import streamlit as st
import yt_dlp
import os
import tempfile
import time
import threading
from io import BytesIO
import base64

# Page configuration
st.set_page_config(
    page_title="Multi-Platform Video Downloader",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI and responsiveness
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .platform-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        margin: 0.25rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: bold;
    }
    
    .youtube { background-color: #ff0000; color: white; }
    .facebook { background-color: #1877f2; color: white; }
    .linkedin { background-color: #0077b5; color: white; }
    .unknown { background-color: #6c757d; color: white; }
    
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        height: 3rem;
        font-weight: bold;
    }
    
    .download-section {
        background-color: #6c757d;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
    }
    
    .info-section {
        background-color: #6c757d;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2196f3;
    }
    
    .error-section {
        background-color: #6c757d;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #f44336;
    }
    
    .video-container {
        background-color: #6c757d;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #6c757d;
        margin-bottom: 1rem;
    }
    
    .video-container iframe {
        width: 100% !important;
        height: 315px !important;
        max-height: 315px !important;
        border-radius: 8px;
    }
    
    .thumbnail-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #dee2e6;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .thumbnail-container img {
        max-height: 250px !important;
        width: auto !important;
        border-radius: 8px;
    }
    
    /* Real-time progress bar styling */
    .progress-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
    
    .custom-progress {
        background-color: #e9ecef;
        border-radius: 10px;
        height: 20px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    
    .custom-progress-bar {
        background: linear-gradient(90deg, #28a745, #20c997);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 0.8rem;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem 0;
        }
        
        .main-header h1 {
            font-size: 1.5rem !important;
        }
        
        .stButton > button {
            height: 2.5rem;
            font-size: 0.9rem;
        }
        
        .video-container iframe {
            height: 200px !important;
        }
        
        .thumbnail-container img {
            max-height: 180px !important;
        }
        
        .platform-badge {
            font-size: 0.75rem;
            padding: 0.2rem 0.5rem;
        }
        
        .stSidebar {
            width: 100% !important;
        }
        
        .download-section, .info-section, .error-section {
            padding: 1rem;
        }
    }
    
    /* Tablet responsiveness */
    @media (min-width: 769px) and (max-width: 1024px) {
        .video-container iframe {
            height: 250px !important;
        }
        
        .thumbnail-container img {
            max-height: 200px !important;
        }
    }
    
    /* Desktop optimization */
    @media (min-width: 1025px) {
        .main-header h1 {
            font-size: 2.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

class StreamlitVideoDownloader:
    def __init__(self):
        self.supported_platforms = {
            'youtube': ['youtube.com', 'youtu.be'],
            'facebook': ['facebook.com', 'fb.com', 'fb.watch'],
            'linkedin': ['linkedin.com']
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
            'unknown': ('❓ Unknown', 'unknown')
        }
        
        label, css_class = platform_info.get(platform, ('❓ Unknown', 'unknown'))
        return f'<span class="platform-badge {css_class}">{label}</span>'
    
    def progress_hook(self, d):
        """Progress hook for yt-dlp to track download progress"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percentage = (d['downloaded_bytes'] / d['total_bytes']) * 100
            elif 'total_bytes_estimate' in d:
                percentage = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
            else:
                percentage = 0
            
            speed = d.get('speed', 0)
            speed_str = f"{speed/1024/1024:.1f} MB/s" if speed else "Unknown"
            
            # Store progress in session state instead of instance variable
            st.session_state.download_progress = {
                'percentage': min(percentage, 100),
                'downloaded': d['downloaded_bytes'],
                'total': d.get('total_bytes', d.get('total_bytes_estimate', 0)),
                'speed': speed_str,
                'status': 'downloading'
            }
        elif d['status'] == 'finished':
            st.session_state.download_progress = {
                'percentage': 100,
                'status': 'finished',
                'filename': d['filename']
            }
    
    def get_platform_specific_options(self, platform):
        """Get platform-specific yt-dlp options"""
        base_opts = {
            'quiet': False,
            'no_warnings': True,
            'progress_hooks': [self.progress_hook],
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
    
    def format_bytes(self, bytes_value):
        """Format bytes to human readable format"""
        if not bytes_value:
            return "Unknown"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024
        return f"{bytes_value:.1f} TB"
    
    def get_video_info(self, url, platform):
        """Get video information"""
        try:
            ydl_opts = self.get_platform_specific_options(platform)
            # Remove progress hooks for info extraction
            ydl_opts.pop('progress_hooks', None)
            ydl_opts['quiet'] = True
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info, None
        except Exception as e:
            return None, str(e)
    
    def download_video(self, url, platform, quality, format_type, temp_dir):
        """Download video and return file path with progress tracking"""
        try:
            # Initialize progress in session state
            st.session_state.download_progress = {'status': 'starting'}
            
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
                        format_selector = 'best[ext=mp4]/best'
                    else:
                        format_selector = f'best[height<={quality}][ext=mp4]/best[height<={quality}]/best[ext=mp4]/best'
                elif platform == 'facebook':
                    if quality == 'best':
                        format_selector = 'best'
                    else:
                        format_selector = f'best[height<={quality}]/best'
                elif platform == 'linkedin':
                    format_selector = 'best'
                
                ydl_opts.update({
                    'format': format_selector,
                })
            
            # Download with progress tracking
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # Find downloaded file
                for file in os.listdir(temp_dir):
                    if file.endswith(('.mp4', '.mp3', '.webm', '.mkv', '.avi', '.mov')):
                        return os.path.join(temp_dir, file), info, None
                
                return None, info, "No file found after download"
        
        except Exception as e:
            return None, None, str(e)

def display_progress_bar(downloader):
    """Display progress bar using session state data"""
    if 'download_progress' in st.session_state and st.session_state.download_progress:
        data = st.session_state.download_progress
        
        if data.get('status') == 'downloading':
            percentage = data.get('percentage', 0)
            downloaded = data.get('downloaded', 0)
            total = data.get('total', 0)
            speed = data.get('speed', 'Unknown')
            
            # Display progress bar
            st.markdown(f"""
            <div class="progress-container">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span><strong>Downloading...</strong></span>
                    <span><strong>{percentage:.1f}%</strong></span>
                </div>
                <div class="custom-progress">
                    <div class="custom-progress-bar" style="width: {percentage}%;">
                        {percentage:.1f}%
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: #6c757d;">
                    <span>Downloaded: {downloader.format_bytes(downloaded)}</span>
                    <span>Speed: {speed}</span>
                </div>
                {f'<div style="text-align: center; font-size: 0.9rem; color: #6c757d;">Total: {downloader.format_bytes(total)}</div>' if total > 0 else ''}
            </div>
            """, unsafe_allow_html=True)
            
            return f"📥 Downloading at {speed}..."
            
        elif data.get('status') == 'finished':
            st.markdown(f"""
            <div class="progress-container">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span><strong>Download Complete!</strong></span>
                    <span><strong>100%</strong></span>
                </div>
                <div class="custom-progress">
                    <div class="custom-progress-bar" style="width: 100%;">
                        Complete!
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            return "✅ Download completed successfully!"
    
    return None

def main():
    # Initialize downloader
    downloader = StreamlitVideoDownloader()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎥 Multi-Platform Video Downloader</h1>
        <p>Download videos from YouTube, Facebook, and LinkedIn</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'video_info' not in st.session_state:
        st.session_state.video_info = None
    if 'download_ready' not in st.session_state:
        st.session_state.download_ready = False
    if 'download_progress' not in st.session_state:
        st.session_state.download_progress = {}
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Settings")
        
        # Quality selection
        quality = st.selectbox(
            "📊 Video Quality",
            options=['best', '1080', '720', '480', '360', '240', '144'],
            format_func=lambda x: 'Best Available' if x == 'best' else f'{x}p',
            index=2  # Default to 720p
        )
        
        # Format selection
        format_type = st.selectbox(
            "📦 Format",
            options=['mp4', 'mp3'],
            format_func=lambda x: 'MP4 (Video)' if x == 'mp4' else 'MP3 (Audio Only)'
        )
        
        st.markdown("---")
        
        # Supported platforms
        st.markdown("### 🌐 Supported Platforms")
        st.markdown("""
        - 📺 **YouTube** (youtube.com, youtu.be)
        - 📘 **Facebook** (facebook.com, fb.watch)
        - 💼 **LinkedIn** (linkedin.com)
        """)
        
        st.markdown("---")
        
        # Tips
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Use direct video links for best results
        - Some videos may require public access
        - Higher quality = larger file size
        - Real-time progress tracking included
        """)
    
    # Main content - responsive layout
    if st.session_state.get('mobile_view', False):
        # Mobile layout - single column
        col1 = st.container()
        col2 = st.container()
    else:
        # Desktop/tablet layout - two columns
        col1, col2 = st.columns([1, 1])
    
    with col1:
        # URL input
        st.markdown("### 🔗 Enter Video URL")
        url = st.text_input(
            "Paste your video URL here:",
            placeholder="https://www.youtube.com/watch?v=...",
            label_visibility="collapsed"
        )
        
        # Platform detection
        if url:
            platform = downloader.detect_platform(url)
            badge_html = downloader.get_platform_badge(platform)
            st.markdown(f"**Detected Platform:** {badge_html}", unsafe_allow_html=True)
            
            if platform == 'unknown':
                st.error("❌ Unsupported platform. Please use YouTube, Facebook, or LinkedIn URLs.")
        
        # Action buttons
        col_info, col_download = st.columns(2)
        
        with col_info:
            if st.button("🔍 Get Video Info", disabled=not url or downloader.detect_platform(url) == 'unknown'):
                platform = downloader.detect_platform(url)
                
                with st.spinner(f"🔍 Fetching video information from {platform.title()}..."):
                    info, error = downloader.get_video_info(url, platform)
                    
                    if error:
                        st.error(f"❌ Error: {error}")
                        st.session_state.video_info = None
                    else:
                        st.session_state.video_info = info
                        st.success("✅ Video information loaded!")
        
        with col_download:
            download_disabled = not url or downloader.detect_platform(url) == 'unknown'
            if st.button("⬇️ Download Video", disabled=download_disabled):
                platform = downloader.detect_platform(url)
                
                # Create temporary directory
                temp_dir = tempfile.mkdtemp()
                
                # Create placeholders for progress updates
                progress_placeholder = st.empty()
                status_placeholder = st.empty()
                
                try:
                    # Reset progress
                    st.session_state.download_progress = {'status': 'starting'}
                    
                    status_placeholder.info(f"🚀 Starting download from {platform.title()}...")
                    
                    # Show initial progress
                    progress_placeholder.markdown("""
                    <div class="progress-container">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                            <span><strong>Preparing download...</strong></span>
                            <span><strong>0%</strong></span>
                        </div>
                        <div class="custom-progress">
                            <div class="custom-progress-bar" style="width: 0%;">
                                Starting...
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Download video
                    file_path, info, error = downloader.download_video(
                        url, platform, quality, format_type, temp_dir
                    )
                    
                    # Display final progress
                    progress_status = display_progress_bar(downloader)
                    if progress_status:
                        if "completed" in progress_status:
                            status_placeholder.success(progress_status)
                        else:
                            status_placeholder.info(progress_status)
                    
                    if error:
                        progress_placeholder.empty()
                        status_placeholder.error(f"❌ Download failed: {error}")
                    elif file_path:
                        # Prepare file for download
                        with open(file_path, 'rb') as file:
                            file_data = file.read()
                        
                        filename = os.path.basename(file_path)
                        file_size = len(file_data) / (1024 * 1024)  # MB
                        
                        st.success(f"🎉 Download ready! File size: {file_size:.2f} MB")
                        
                        # Download button
                        st.download_button(
                            label="💾 Download to Computer",
                            data=file_data,
                            file_name=filename,
                            mime="application/octet-stream"
                        )
                        
                        # Clear progress after successful download
                        st.session_state.download_progress = {}
                    
                except Exception as e:
                    progress_placeholder.empty()
                    status_placeholder.error(f"❌ Unexpected error: {str(e)}")
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
            st.markdown("### 🎬 Video Preview")
            
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
                
                # For Facebook videos, show thumbnail if available
                elif platform == 'facebook':
                    thumbnail_url = info.get('thumbnail')
                    if thumbnail_url:
                        st.markdown("""
                        <div class="thumbnail-container">
                        """, unsafe_allow_html=True)
                        st.image(thumbnail_url, caption="📘 Facebook Video Thumbnail")
                        st.markdown("""
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"[🔗 Open in Facebook]({url})")
                    else:
                        st.info("📘 Facebook video detected. Click link to view on Facebook.")
                        st.markdown(f"[🔗 View on Facebook]({url})")
                
                # For LinkedIn videos, show thumbnail if available
                elif platform == 'linkedin':
                    thumbnail_url = info.get('thumbnail')
                    if thumbnail_url:
                        st.markdown("""
                        <div class="thumbnail-container">
                        """, unsafe_allow_html=True)
                        st.image(thumbnail_url, caption="💼 LinkedIn Video Thumbnail")
                        st.markdown("""
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"[🔗 Open in LinkedIn]({url})")
                    else:
                        st.info("💼 LinkedIn video detected. Click link to view on LinkedIn.")
                        st.markdown(f"[🔗 View on LinkedIn]({url})")
                
            except Exception as e:
                st.warning("⚠️ Unable to load video preview")
            
            st.markdown("---")
            
            # Video Information Section
            st.markdown("""
            <div class="info-section">
                <h3>📹 Video Information</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"**📝 Title:** {info.get('title', 'N/A')}")
            
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
                    st.markdown(f"**📊 Available:** {format_text}")
        else:
            st.markdown("""
            <div class="info-section">
                <h3>💡 How to Use</h3>
                <ol>
                    <li>Paste a video URL above</li>
                    <li>Select quality and format in sidebar</li>
                    <li>Click "Get Video Info" to preview</li>
                    <li>Click "Download Video" to start</li>
                    <li>Watch real-time progress during download</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 1rem 0;">
        <p>🎥 Multi-Platform Video Downloader | Built with Streamlit</p>
        <p><small>Supports YouTube, Facebook, and LinkedIn | Real-time Progress Tracking</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()