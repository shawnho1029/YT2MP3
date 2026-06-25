import streamlit as st
import tempfile
import os
import shutil
import zipfile
import re
import yt_dlp
# Automatically initialize and configure ffmpeg paths
# On Streamlit Cloud (Linux), ffmpeg is pre-installed via packages.txt.
# On Windows, we fall back to static-ffmpeg.
if not shutil.which('ffmpeg'):
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths()
    except Exception as e:
        st.error(f"Failed to configure FFmpeg: {e}")

# Set page configuration
st.set_page_config(
    page_title="yt2mp3 - YouTube Audio Downloader",
    page_icon="🎧",
    layout="centered"
)

# App Title
st.title("🎧 yt2mp3 Web Application")
st.write("Download YouTube videos or playlists and convert them to high-quality audio files.")

# Input Form
url = st.text_input("Enter YouTube URL (Video or Playlist):", placeholder="https://www.youtube.com/...")

col1, col2 = st.columns(2)
with col1:
    audio_format = st.selectbox("Audio Format:", ["mp3", "flac", "wav"])
with col2:
    audio_quality = st.selectbox("Audio Quality (kbps):", ["192", "320", "256", "128"])

# Range Option
playlist_range = st.text_input(
    "Playlist Range (Optional):", 
    placeholder="e.g. 1-10, 5-, or leave empty for all",
    help="Only applicable if downloading a playlist. You can specify a range (e.g. 1-10), start from a song (e.g. 5-), or list specific songs (e.g. 1,3,5)."
)

# Download Action
if st.button("Extract and Download", type="primary"):
    if not url:
        st.warning("Please enter a valid YouTube URL.")
    else:
        status_container = st.container()
        with status_container:
            st.info("Fetching video/playlist metadata...")
            
            # 1. Fetch metadata using extract_flat to be fast
            ydl_opts_info = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
                'extractor_args': {'youtube': {'player_client': ['android', 'android_music', 'web_embedded']}}
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                
                is_playlist = info_dict.get('_type') == 'playlist'
                title = info_dict.get('title', 'audio_download')
                safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
                
                if is_playlist:
                    st.success(f"Detected Playlist: {title}")
                else:
                    st.success(f"Detected Video: {title}")
                
                # 2. Download files inside a temporary directory
                with tempfile.TemporaryDirectory() as tmpdir:
                    st.info("Starting download and conversion. Please wait...")
                    
                    # Create streamlit progress widgets
                    prog_bar = st.progress(0.0)
                    prog_text = st.empty()
                    
                    # Current file download hook
                    current_state = {"title": ""}
                    def progress_hook(d):
                        info = d.get('info_dict', {})
                        video_title = info.get('title', 'Unknown Title')
                        playlist_index = info.get('playlist_index')
                        n_entries = info.get('n_entries')
                        
                        if video_title != current_state["title"]:
                            current_state["title"] = video_title
                            prefix = f"[{playlist_index}/{n_entries}] " if playlist_index and n_entries else ""
                            prog_text.markdown(f"🎵 **Processing:** {prefix}{video_title}")
                        
                        if d['status'] == 'downloading':
                            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                            downloaded_bytes = d.get('downloaded_bytes', 0)
                            if total_bytes > 0:
                                percent = downloaded_bytes / total_bytes
                                prog_bar.progress(percent)
                        elif d['status'] == 'finished':
                            prog_bar.progress(1.0)
                    
                    # Setup yt-dlp download options
                    out_template = os.path.join(tmpdir, '%(title)s.%(ext)s')
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': audio_format,
                            'preferredquality': audio_quality,
                        }],
                        'embedthumbnail': True,
                        'addmetadata': True,
                        'outtmpl': out_template,
                        'progress_hooks': [progress_hook],
                        'quiet': True,
                        'no_warnings': True,
                        'extractor_args': {'youtube': {'player_client': ['android', 'android_music', 'web_embedded']}},
                    }
                    
                    # Handle playlist items range
                    if is_playlist:
                        if playlist_range:
                            ydl_opts['playlist_items'] = playlist_range
                    else:
                        ydl_opts['noplaylist'] = True
                    
                    # Run download
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    
                    # Get list of converted files
                    files = [f for f in os.listdir(tmpdir) if f.endswith(f'.{audio_format}')]
                    
                    if not files:
                        st.error("No audio files were downloaded or converted.")
                    else:
                        # 3. Package output files
                        if len(files) == 1:
                            # Single file download
                            filepath = os.path.join(tmpdir, files[0])
                            with open(filepath, "rb") as f:
                                file_data = f.read()
                            
                            st.success("Conversion complete! Click below to download your file:")
                            st.download_button(
                                label="⬇️ Download Audio",
                                data=file_data,
                                file_name=files[0],
                                mime=f"audio/{audio_format}"
                            )
                        else:
                            # Multiple files (Playlist) -> Package as ZIP
                            zip_filename = f"{safe_title}.zip"
                            zip_path = os.path.join(tmpdir, zip_filename)
                            
                            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                                for file in files:
                                    filepath = os.path.join(tmpdir, file)
                                    zipf.write(filepath, file)
                            
                            with open(zip_path, "rb") as f:
                                zip_data = f.read()
                            
                            st.success(f"All items converted! Click below to download the ZIP archive ({len(files)} files):")
                            st.download_button(
                                label=f"⬇️ Download {zip_filename}",
                                data=zip_data,
                                file_name=zip_filename,
                                mime="application/zip"
                            )
                            
            except Exception as e:
                st.error(f"An error occurred: {e}")
