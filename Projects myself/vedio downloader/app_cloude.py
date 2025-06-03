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

# Custom CSS for better UI
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
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
    }
    
    .info-section {
        background-color: #6c757d;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2196f3;
    }
    
    .error-section {
        background-color: #ffebee;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #f44336;
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
    
    def get_platform_specific_options(self, platform):
        """Get platform-specific yt-dlp options"""
        base_opts = {
            'quiet': True,
            'no_warnings': True,
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
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
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
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.text(f"🚀 Starting download from {platform.title()}...")
                    progress_bar.progress(25)
                    
                    file_path, info, error = downloader.download_video(
                        url, platform, quality, format_type, temp_dir
                    )
                    
                    if error:
                        st.error(f"❌ Download failed: {error}")
                    elif file_path:
                        progress_bar.progress(100)
                        status_text.text("✅ Download completed!")
                        
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
                    
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")
                finally:
                    # Cleanup
                    import shutil
                    try:
                        shutil.rmtree(temp_dir)
                    except:
                        pass
    
    with col2:
        # Video information display
        if st.session_state.video_info:
            info = st.session_state.video_info
            
            st.markdown("""
            <div class="info-section">
                <h3>📹 Video Information</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"**📝 Title:** {info.get('title', 'N/A')}")
            
            # Platform-specific info
            platform = downloader.detect_platform(url)
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
                </ol>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 1rem 0;">
        <p>🎥 Multi-Platform Video Downloader | Built with Streamlit</p>
        <p><small>Supports YouTube, Facebook, and LinkedIn</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()