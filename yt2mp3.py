#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import sys
import re

# Force stdout and stderr to use UTF-8 to prevent encoding issues on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import colorama
from colorama import Fore, Style


# Try to load static-ffmpeg to auto-configure ffmpeg path on Windows/macOS/Linux
try:
    import static_ffmpeg
    static_ffmpeg.add_paths()
except ImportError:
    pass

import yt_dlp

####################################
# Author: l0n3m4n                  #
# Description: Youtube converter   #
# Version: 1.5.0 (yt-dlp native)   #
####################################



colorama.init(autoreset=True)

class colors:
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT
    GREEN = Fore.LIGHTGREEN_EX
    RED = Fore.LIGHTRED_EX
    YELLOW = Fore.LIGHTYELLOW_EX
    CYAN = Fore.LIGHTCYAN_EX
    MAGENTA = Fore.LIGHTMAGENTA_EX
    BLUE = Fore.LIGHTBLUE_EX


class AlignedHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog, indent_increment=2, max_help_position=30, width=None):
        super().__init__(prog, indent_increment, max_help_position, width)

    def _format_action_item(self, action):
        item = super()._format_action_item(action)
        if action.help:
            item = item.replace('\n', ' ')
        return item

    def _format_action(self, action):
        if action.help:
            action.help = action.help.replace('\n', ' ')
        return super()._format_action(action)


class CustomFormatter(AlignedHelpFormatter, argparse.RawDescriptionHelpFormatter):
    def _format_usage(self, usage, actions, groups, prefix):
        usage_text = super()._format_usage(usage, actions, groups, prefix)
        return f"{colors.CYAN}{usage_text}{colors.RESET}"

    def _format_action_invocation(self, action):
        if not action.option_strings:
            return f"{colors.YELLOW}{super()._format_action_invocation(action)}{colors.RESET}"
        else:
            return f"{colors.YELLOW}{', '.join(action.option_strings)}{colors.RESET}"

    def _expand_help(self, action):
        return f"{colors.BLUE}{super()._expand_help(action)}{colors.RESET}"


def download_and_convert(url, output_dir, output_filename, download_format, download_quality, verbose=False, download_playlist=True, playlist_items=None, download_type='audio'):
    try:
        if '\\' in url:
            url = url.replace('\\', '')
        ydl_opts_info = {
            'quiet': not verbose,
            'no_warnings': not verbose,
            'noplaylist': not download_playlist,
            'extract_flat': True,
            'extractor_args': {'youtube': {'player_client': ['default']}}
        }
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info_dict = ydl.extract_info(url, download=False)

        if not verbose:
            type_label = "video" if download_type == "video" else "audio"
            print(f"{colors.CYAN}📥 Downloading and converting to {download_format.upper()} ({type_label}){colors.RESET}")

        is_playlist = info_dict.get('_type') == 'playlist'

        if is_playlist:
            if not output_filename:
                playlist_title = info_dict.get('title', 'playlist')
                output_filename = re.sub(r'[\\/*?:"<>|]', "", playlist_title)
            
            output_dir = os.path.join(output_dir, output_filename)
            os.makedirs(output_dir, exist_ok=True)
            
            output_template = os.path.join(output_dir, '%(title)s')
            final_message_path = output_dir
        else:  
            if not output_filename:
                video_title = info_dict.get('title', None)
                if video_title:
                    output_filename = re.sub(r'[\\/*?:"<>|]', "", video_title)
                else:
                    print(f"{colors.RED}Could not retrieve video title.{colors.RESET}")
                    return False
            else:
                if output_filename.endswith(f'.{download_format}'):
                    output_filename = output_filename[:-len(download_format)-1]
            
            output_template = os.path.join(output_dir, output_filename)
            final_message_path = f"{output_template}.{download_format}"

        current_title = ""
        def progress_hook(d):
            nonlocal current_title
            info = d.get('info_dict', {})
            video_title = info.get('title', 'Unknown Title')
            playlist_index = info.get('playlist_index')
            n_entries = info.get('n_entries')
            
            if video_title != current_title:
                current_title = video_title
                prefix = ""
                if playlist_index is not None and n_entries is not None:
                    prefix = f"[{playlist_index}/{n_entries}] "
                sys.stdout.write(f"\n{colors.YELLOW}🎵 Downloading: {prefix}{video_title}{colors.RESET}\n")
                sys.stdout.flush()

            if d['status'] == 'downloading':
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded_bytes = d.get('downloaded_bytes', 0)
                if total_bytes > 0:
                    percent = downloaded_bytes / total_bytes * 100
                    speed = d.get('speed')
                    eta = d.get('eta')

                    status_line = f"\r{colors.CYAN}Downloading: {colors.GREEN}{percent:.1f}%{colors.RESET}"
                    if speed:
                        status_line += f" at {speed / 1024 / 1024:.2f}MiB/s"
                    if eta is not None:
                        status_line += f" ETA {eta}s"
                    sys.stdout.write(status_line)
                    sys.stdout.flush()
            elif d['status'] == 'finished':
                sys.stdout.write(f"\r{colors.CYAN}Download complete. Post-processing...{colors.RESET}\n")
                sys.stdout.flush()
        
        progress_hooks = []
        if not verbose:
            progress_hooks.append(progress_hook)

        from yt_dlp.utils import sanitize_filename

        def my_match_filter(info_dict, *, incomplete):
            video_title = info_dict.get('title')
            if not video_title:
                return None
            
            safe_title = sanitize_filename(video_title)
            
            if not is_playlist and output_filename:
                check_name = output_filename
                if not check_name.endswith(f'.{download_format}'):
                    check_name = f"{check_name}.{download_format}"
                check_path = os.path.join(output_dir, check_name)
            else:
                check_path = os.path.join(output_dir, f"{safe_title}.{download_format}")
            
            if os.path.exists(check_path):
                return 'Already downloaded (file exists)'
            return None

        format_selector = 'bestaudio/best'
        postprocessors = []

        if download_type == 'video':
            height_map = {
                '480p': 480, '480': 480,
                '720p': 720, '720': 720,
                '1080p': 1080, '1080': 1080,
                '2k': 1440, '1440p': 1440, '1440': 1440,
                '4k': 2160, '2160p': 2160, '2160': 2160
            }
            height = height_map.get(download_quality.lower())
            if height:
                format_selector = f'bestvideo[height<={height}]+bestaudio[ext=m4a]/bestaudio/best'
            else:
                format_selector = 'bestvideo+bestaudio[ext=m4a]/bestaudio/best'
        else:
            format_selector = 'bestaudio/best'
            postprocessors.append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': download_format,
                'preferredquality': download_quality,
            })

        ydl_opts = {
            'format': format_selector,
            'embedthumbnail': True,
            'addmetadata': True,
            'outtmpl': output_template,
            'progress_hooks': progress_hooks,
            'quiet': not verbose,   
            'no_warnings': not verbose,
            'extractor_args': {'youtube': {'player_client': ['default']}},
            'match_filter': my_match_filter,
            'noplaylist': not download_playlist,
        }
        if postprocessors:
            ydl_opts['postprocessors'] = postprocessors
        if download_type == 'video':
            ydl_opts['merge_output_format'] = download_format

        if playlist_items:
            ydl_opts['playlist_items'] = playlist_items
        elif not download_playlist:
            ydl_opts['playlist_items'] = '1'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        emoji = "📹" if download_type == "video" else "🎧"
        verb = "download" if download_type == "video" else "conversion"
        if is_playlist:
            print(f"{colors.CYAN}{emoji} Playlist {verb} complete. {download_format.upper()}s saved in: {final_message_path}{colors.RESET}")
        else:
            print(f"{colors.CYAN}{emoji} {verb.capitalize()} complete. {download_format.upper()} saved at: {final_message_path}{colors.RESET}")
        return True

    except yt_dlp.utils.DownloadError as e:
        print(f"{colors.RED}Error during download: {e}{colors.RESET}")
        return False
    except yt_dlp.utils.ExtractorError as e:
        print(f"{colors.RED}Error extracting video information: {e}{colors.RESET}")
        return False
    except FileNotFoundError:
        print(f"{colors.RED}Error: yt-dlp or ffmpeg not found. Please ensure yt-dlp and ffmpeg are installed and in your system's PATH.{colors.RESET}")
        return False
    except KeyboardInterrupt:
        print(f'\n{colors.RED}Download interrupted by user.{colors.RESET}')
        return False
    except Exception as e:
        print(f"{colors.RED}Unexpected error occurred: {e}{colors.RESET}")
        return False


def main(urls, output_filename, download_format, download_quality, verbose=False, download_playlist=True, playlist_items=None, download_type='audio'):
    output_dir = './video' if download_type == 'video' else './music'
    os.makedirs(output_dir, exist_ok=True)

    if len(urls) > 1 and output_filename:
        print(f"{colors.YELLOW}Warning: Multiple URLs provided with a single output name. The -o/--output flag will be ignored.{colors.RESET}")
        output_filename = None

    for url in urls:
        if not download_and_convert(url, output_dir, output_filename, download_format, download_quality, verbose, download_playlist, playlist_items, download_type):
            print(f"{colors.RED}\nFailed to download or convert: {url}{colors.RESET}")
    
    print(f"\n{colors.GREEN}All tasks complete.{colors.RESET}")


if __name__ == "__main__":
    print(f"{colors.CYAN}", end="")
    print(r'''
        __   ______                  ______
.--.--.|  |_|__    |.--------.-----.|__    |
|  |  ||   _|    __||        |  _  ||__    |
|___  ||____|______||__|__|__|   __||______| 
|_____|                      |__|
        Author: l0n3m4n | ⚙️  v1.5.0
''', end="")
    print(f"{colors.RESET}")

    parser = argparse.ArgumentParser(
        description='Download a YouTube video and convert to MP3 or MP4.',
        epilog=f"""
{colors.MAGENTA}Examples:{colors.RESET}
  {colors.MAGENTA}Download a single video as MP3 (default):{colors.RESET}
    yt2mp3.py -u "https://www.youtube.com/watch?v=id"

  {colors.MAGENTA}Download a single video as MP4 video (1080p default):{colors.RESET}
    yt2mp3.py -u "https://www.youtube.com/watch?v=id" -t video

  {colors.MAGENTA}Download a single video as MP4 in 720p quality:{colors.RESET}
    yt2mp3.py -u "https://www.youtube.com/watch?v=id" -t video -q 720p

  {colors.MAGENTA}Download a playlist to the default music directory:{colors.RESET}
    yt2mp3.py -u "https://www.youtube.com/playlist?list=id"

  {colors.MAGENTA}Download a video in FLAC format with 320 quality:{colors.RESET}
    yt2mp3.py -u "https://www.youtube.com/watch?v=id" -f flac -q 320

  {colors.MAGENTA}Download multiple videos from a text file:{colors.RESET}
    yt2mp3.py -l url_list.txt

  {colors.MAGENTA}Download multiple videos from the command line:{colors.RESET}
    yt2mp3.py -u "https://youtu.be/id1" "https://youtu.be/id2"

  {colors.MAGENTA}Download with verbose output for debugging:{colors.RESET}
    yt2mp3.py -u "https://www.youtube.com/watch?v=id" -v
""",
        formatter_class=CustomFormatter
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-u', '--url', type=str, nargs='+', help='One or more YouTube video URLs')
    group.add_argument('-l', '--list-file', type=str, help='Path to a text file containing YouTube URLs (one per line)')

    parser.add_argument('-o', '--output', type=str, required=False, metavar='', help='Output filename (default: video title)')
    parser.add_argument('-f', '--format', type=str, default=None, help='Format (audio: mp3, flac, wav [default: mp3]; video: mp4, mkv [default: mp4])')
    parser.add_argument('-q', '--quality', type=str, default=None, help='Quality (audio: 128, 192, 256, 320 [default: 192]; video: 480p, 720p, 1080p, 2K, 4K [default: 1080p])')
    parser.add_argument('-t', '--type', type=str, choices=['audio', 'video'], default='audio', help='Download type: audio or video (default: audio)')
    parser.add_argument('-i', '--interactive', action='store_true', help='Enable interactive mode')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-p', '--playlist', action='store_true', default=True, help='Download the entire playlist (default: True)')
    parser.add_argument('--no-playlist', dest='playlist', action='store_false', help='Do not download the playlist, only the first video')
    parser.add_argument('-r', '--range', type=str, required=False, help='Playlist range to download (e.g. 1-10, 5- or 1,3,5)')
    parser.set_defaults(playlist=True)
    args = parser.parse_args()

    if args.interactive:
        try:
            url_input = input("Enter one or more YouTube URLs (separated by spaces): ")
            if not url_input:
                print(f"{colors.RED}URL(s) cannot be empty.{colors.RESET}")
                exit()
            urls = url_input.split()
            
            output_filename = input("Enter the output filename (optional, press Enter for auto): ")
            
            # Interactive type selection
            type_input = input("Choose download type: (A)udio or (V)ideo [default: A]: ").strip().lower()
            if type_input in ('v', 'video'):
                download_type = 'video'
                download_format = input("Enter the video format (mp4, mkv) [default: mp4]: ").strip().lower() or 'mp4'
                
                print("\nSelect video quality:")
                print("  [1] 480p")
                print("  [2] 720p")
                print("  [3] 1080p (Full HD - recommended)")
                print("  [4] 2K (1440p)")
                print("  [5] 4K (2160p)")
                q_input = input("Enter option number or quality value [default: 3]: ").strip()
                if q_input == '1': download_quality = '480p'
                elif q_input == '2': download_quality = '720p'
                elif q_input == '3' or q_input == '': download_quality = '1080p'
                elif q_input == '4': download_quality = '2K'
                elif q_input == '5': download_quality = '4K'
                else: download_quality = q_input or '1080p'
            else:
                download_type = 'audio'
                download_format = input("Enter the audio format (mp3, flac, wav) [default: mp3]: ").strip().lower() or 'mp3'
                
                print("\nSelect audio quality:")
                print("  [1] 128 kbps (Lower size)")
                print("  [2] 192 kbps (Standard quality - recommended)")
                print("  [3] 256 kbps (High quality)")
                print("  [4] 320 kbps (Maximum quality)")
                q_input = input("Enter option number or quality value [default: 2]: ").strip()
                if q_input == '1': download_quality = '128'
                elif q_input == '2' or q_input == '': download_quality = '192'
                elif q_input == '3': download_quality = '256'
                elif q_input == '4': download_quality = '320'
                else: download_quality = q_input or '192'
            
            verbose = input("\nEnable verbose mode? (y/n): ").lower() == 'y'
            playlist = input("Download entire playlist? (y/n) [default: y]: ").lower() != 'n'
            playlist_items = None
            if playlist:
                range_input = input("Enter playlist range (e.g. 1-10, 5- or press Enter for all): ").strip()
                if range_input:
                    playlist_items = range_input

            main(urls, output_filename, download_format, download_quality, verbose, playlist, playlist_items, download_type)
            exit()
        except KeyboardInterrupt:
            print(f"\n{colors.RED}Process interrupted by user.{colors.RESET}")
            exit()
        except Exception as e:
            print(f"\n{colors.RED}An error occurred: {e}{colors.RESET}")
            exit()

    urls = []
    if args.url:
        urls = args.url
    elif args.list_file:
        try:
            with open(args.list_file, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
            if not urls:
                print(f"{colors.YELLOW}Warning: The file '{args.list_file}' is empty.{colors.RESET}")
                exit()
        except FileNotFoundError:
            print(f"{colors.RED}Error: The file '{args.list_file}' was not found.{colors.RESET}")
            exit(1)
        except Exception as e:
            print(f"{colors.RED}Error reading file '{args.list_file}': {e}{colors.RESET}")
            exit(1)
    
    if not urls:
        parser.print_help()
        exit()

    download_type = args.type or 'audio'
    if download_type == 'video':
        download_format = args.format or 'mp4'
        download_quality = args.quality or '1080p'
    else:
        download_format = args.format or 'mp3'
        download_quality = args.quality or '192'

    try:
        main(urls, args.output, download_format, download_quality, args.verbose, args.playlist, args.range, download_type)
    except KeyboardInterrupt:
        print(f"\n{colors.RED}Process interrupted by user.{colors.RESET}")
    except Exception as e:
        print(f"\n{colors.RED}An error occurred: {e}{colors.RESET}")
