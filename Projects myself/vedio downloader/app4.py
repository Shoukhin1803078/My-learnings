import streamlit as st
import yt_dlp
import os
import tempfile
import time
import base64
from io import BytesIO
from streamlit.components.v1 import html

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
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2196f3;
    }
    .error-section {
        background-color: #ffebee;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #f44336;
    }
    .video-container iframe {
        width: 100% !important;
        height: 315px !important;
        max-height: 315px !important;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .thumbnail-container img {
        max-height: 250px !important;
        width: auto !important;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def show_spinner():
    """Display animated spinner"""
    html_code = """
    <div style="text-align:center; margin-top: 20px;">
        <div class="spinner"></div>
        <p>Loading...</p>
    </div>
    <style>
        .spinner {
          border: 4px solid rgba(0, 0, 0, 0.1);
          width: 36px;
          height: 36px;
          border-radius: 50%;
          border-left-color: #28a745;
          animation: spin 1s linear infinite;
          margin: auto;
        }
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
    </style>
    """
    html(html_code)

class StreamlitVideoDownloader:
    def __init__(self):
        self.supported_platforms = {
            'youtube': ['youtube.com', 'youtu.be'],
            'facebook': ['facebook.com', 'fb.com', 'fb.watch'],
            'linkedin': ['linkedin.com']
        }

    def detect_platform(self, url):
        if not url:
            return 'unknown'
        url_lower = url.lower()
        for platform, domains in self.supported_platforms.items():
            for domain in domains:
                if domain in url_lower:
                    return platform
        return 'unknown'

    def get_platform_badge(self, platform):
        labels = {
            'youtube': ('📺 YouTube', 'youtube'),
            'facebook': ('📘 Facebook', 'facebook'),
            'linkedin': ('💼 LinkedIn', 'linkedin'),
            'unknown': ('❓ Unknown', 'unknown')
        }
        label, cls = labels.get(platform, ('❓ Unknown', 'unknown'))
        return f'<span class="platform-badge {cls}">{label}</span>'

    def get_platform_specific_options(self, platform):
        base_opts = {'quiet': True, 'no_warnings': True}
        if platform == 'facebook':
            base_opts.update({'extractor_args': {'facebook': {'skip_dash_manifest': True}}})
        elif platform == 'linkedin':
            base_opts.update({
                'http_headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            })
        return base_opts

    def format_duration(self, seconds):
        if not seconds: return "Unknown"
        h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
        return f"{h}h {m}m {s}s" if h else f"{m}m {s}s" if m else f"{s}s"

    def get_video_info(self, url, platform):
        try:
            ydl_opts = self.get_platform_specific_options(platform)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info, None
        except Exception as e:
            return None, str(e)

    def download_video(self, url, platform, quality, format_type, temp_dir):
        try:
            ydl_opts = self.get_platform_specific_options(platform)
            ydl_opts['outtmpl'] = os.path.join(temp_dir, '%(title)s.%(ext)s')

            if format_type == 'mp3':
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]
                })
            else:
                if platform == 'youtube':
                    fmt = 'best[ext=mp4]/best' if quality == 'best' else f'best[height<={quality}][ext=mp4]/best'
                elif platform == 'facebook':
                    fmt = 'best' if quality == 'best' else f'best[height<={quality}]'
                else:
                    fmt = 'best'
                ydl_opts.update({'format': fmt})

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                for file in os.listdir(temp_dir):
                    if file.endswith(('.mp4', '.mp3', '.webm', '.mkv', '.avi', '.mov')):
                        return os.path.join(temp_dir, file), info, None
                return None, info, "No file found after download"
        except Exception as e:
            return None, None, str(e)

def main():
    downloader = StreamlitVideoDownloader()

    st.markdown("""
    <div class="main-header">
        <h1>🎥 Multi-Platform Video Downloader</h1>
        <p>Download videos from YouTube, Facebook, and LinkedIn</p>
    </div>
    """, unsafe_allow_html=True)

    if 'video_info' not in st.session_state:
        st.session_state.video_info = None

    with st.sidebar:
        st.header("🎛️ Settings")
        quality = st.selectbox(
            "📊 Video Quality",
            options=['best', '1080', '720', '480', '360', '240', '144'],
            format_func=lambda x: 'Best Available' if x == 'best' else f'{x}p',
            index=2,
            help="Select maximum resolution for download"
        )
        format_type = st.selectbox(
            "📦 Format",
            options=['mp4', 'mp3'],
            format_func=lambda x: 'MP4 (Video)' if x == 'mp4' else 'MP3 (Audio Only)',
            help="Choose to download video or extract audio"
        )
        st.markdown("---")
        st.markdown("### 🌐 Supported Platforms")
        st.markdown("""
        - 📺 **YouTube** (youtube.com, youtu.be)
        - 📘 **Facebook** (facebook.com, fb.watch)
        - 💼 **LinkedIn** (linkedin.com)
        """)
        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Use direct video links
        - Some videos may require public access
        - Higher quality = larger file size
        """)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 🔗 Enter Video URL")
        url = st.text_input("Paste your video URL here:", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")

        if url:
            platform = downloader.detect_platform(url)
            badge_html = downloader.get_platform_badge(platform)
            st.markdown(f"**Detected Platform:** {badge_html}", unsafe_allow_html=True)
            if platform == 'unknown':
                st.error("❌ Unsupported platform. Please use YouTube, Facebook, or LinkedIn URLs.")

        st.markdown("### 🚀 Actions") 
        if st.session_state.video_info:
            st.success("✅ Video info is ready! You can now download.")
        else:
            st.info("ℹ️ Click 'Get Video Info' to preview before downloading.")

        col_info, col_download = st.columns([1, 1])
        with col_info:
            if st.button("🔍 Get Video Info", use_container_width=True, disabled=not url or downloader.detect_platform(url) == 'unknown'):
                platform = downloader.detect_platform(url)
                with st.spinner(f"🔍 Fetching video information from {platform.title()}..."):
                    info, error = downloader.get_video_info(url, platform)
                    if error:
                        st.markdown(f"<div class='error-section'>❌ Error: {error}</div>", unsafe_allow_html=True)
                        st.session_state.video_info = None
                    else:
                        st.session_state.video_info = info
                        st.success("✅ Video information loaded!")

        with col_download:
            download_disabled = not url or downloader.detect_platform(url) == 'unknown'
            if st.button("⬇️ Start Download", use_container_width=True, disabled=download_disabled):
                platform = downloader.detect_platform(url)
                temp_dir = tempfile.mkdtemp()
                progress_bar = st.progress(0)
                status_text = st.empty()
                show_spinner()

                try:
                    status_text.text(f"🚀 Starting download from {platform.title()}...")
                    progress_bar.progress(25)
                    file_path, info, error = downloader.download_video(url, platform, quality, format_type, temp_dir)

                    if error:
                        st.markdown(f"<div class='error-section'>❌ Download failed: {error}</div>", unsafe_allow_html=True)
                    elif file_path:
                        progress_bar.progress(100)
                        status_text.text("✅ Download completed!")
                        with open(file_path, 'rb') as file:
                            file_data = file.read()
                        filename = os.path.basename(file_path)
                        file_size = len(file_data) / (1024 * 1024)

                        st.success(f"🎉 Ready! File size: {file_size:.2f} MB")
                        st.download_button(
                            label="💾 Download to Computer",
                            data=file_data,
                            file_name=filename,
                            mime="application/octet-stream"
                        )
                except Exception as e:
                    st.markdown(f"<div class='error-section'>❌ Unexpected error: {str(e)}</div>", unsafe_allow_html=True)
                finally:
                    import shutil
                    try:
                        shutil.rmtree(temp_dir)
                    except:
                        pass

    with col2:
        if url and st.session_state.video_info:
            info = st.session_state.video_info
            platform = downloader.detect_platform(url)

            st.markdown("### 🎬 Video Preview")
            try:
                if platform == 'youtube':
                    video_id = None
                    if 'watch?v=' in url:
                        video_id = url.split('watch?v=')[1].split('&')[0]
                    elif 'youtu.be/' in url:
                        video_id = url.split('youtu.be/')[1].split('?')[0]
                    if video_id:
                        st.markdown("<div class='video-container'>", unsafe_allow_html=True)
                        st.video(f"https://www.youtube.com/watch?v={video_id}")
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.info("📺 YouTube video detected but unable to preview")
                elif platform == 'facebook':
                    thumbnail_url = info.get('thumbnail')
                    if thumbnail_url:
                        st.markdown("<div class='thumbnail-container'>", unsafe_allow_html=True)
                        st.image(thumbnail_url, caption="📘 Facebook Video Thumbnail")
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.markdown(f"[🔗 Open in Facebook]({url})")
                    else:
                        st.info("📘 Facebook video detected. Click link to view on Facebook.")
                        st.markdown(f"[🔗 View on Facebook]({url})")
                elif platform == 'linkedin':
                    thumbnail_url = info.get('thumbnail')
                    if thumbnail_url:
                        st.markdown("<div class='thumbnail-container'>", unsafe_allow_html=True)
                        st.image(thumbnail_url, caption="💼 LinkedIn Video Thumbnail")
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.markdown(f"[🔗 Open in LinkedIn]({url})")
                    else:
                        st.info("💼 LinkedIn video detected. Click link to view on LinkedIn.")
                        st.markdown(f"[🔗 View on LinkedIn]({url})")
            except Exception as e:
                st.warning("⚠️ Unable to load video preview")

            st.markdown("---")
            st.markdown("<div class='info-section'><h3>📹 Video Information</h3></div>", unsafe_allow_html=True)
            st.markdown(f"**📝 Title:** {info.get('title', 'N/A')}")

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

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 1rem 0;"> 
        <p>🎥 Multi-Platform Video Downloader | Built with Streamlit</p>
        <p><small>Supports YouTube, Facebook, and LinkedIn</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()