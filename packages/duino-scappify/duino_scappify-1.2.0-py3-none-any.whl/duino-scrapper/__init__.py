# duino_scapper/__init__.py

import subprocess
import re
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import sys

class DuinoScrapper:
    def __init__(self):
        self.banner = r"""
          _____                    _____                    _____                    _____                   _______
         /\    \                  /\    \                  /\    \                  /\    \                 /::\    \
        /::\    \                /::\____\                /::\    \                /::\____\               /::::\    \
       /::::\    \              /:::/    /                \:::\    \              /::::|   |              /::::::\    \
      /::::::\    \            /:::/    /                  \:::\    \            /:::::|   |             /::::::::\    \
     /:::/\:::\    \          /:::/    /                    \:::\    \          /::::::|   |            /:::/~~\:::\    \
    /:::/  \:::\    \        /:::/    /                      \:::\    \        /:::/ |::|   |           /:::/    \:::\    \
   /:::/    \:::\    \      /:::/    /                       /::::\    \      /:::/  |::|   |          /:::/    / \:::\    \
  /:::/    / \:::\    \    /:::/    /      _____    ____    /::::::\    \    /:::/   |::|   | _____   /:::/____/   \:::\____\
 /:::/    /   \:::\ ___\  /:::/____/      /\    \  /\   \  /:::/\:::\    \  /:::/    |::|   |/\    \ |:::|    |     |:::|    |
/:::/____/     \:::|    ||:::|    /      /::\____\/::\   \/:::/  \:::\____\/:: /    /|::|  /::\____\|:::|____|     |:::|    |
\:::\    \     /:::|____||:::|____\     /:::/    /\:::\  /:::/    \::/    /\::/    / |::| /:::/    / \:::\    \   /:::/    /
 \:::\    \   /:::/    /  \:::\    \   /:::/    /  \:::\/:::/    / \/____/  \/____/  |::|/:::/    /   \:::\    \ /:::/    /
  \:::\    \ /:::/    /    \:::\    \ /:::/    /    \::::::/    /                   |::::::/    /     \:::\    /:::/    /
   \:::\    /:::/    /      \:::\    /:::/    /      \::::/____/                    |:::::/    /       \:::\__/:::/    /
    \:::\  /:::/    /        \:::\__/:::/    /        \:::\    \                    |::::/    /         \::::::::/    /
     \:::\/:::/    /          \::::::::/    /          \:::\    \                   |:::/    /           \::::::/    /
      \::::::/    /            \::::::/    /            \:::\    \                  /:::/    /             \::::/    /
       \::::/    /              \::::/    /              \:::\____\                /:::/    /               \::/____/
        \::/____/                \::/____/                \::/    /                \::/____/                 ~~
         ~~                       ~~                       \/____/                  \/____/

    \033[92mCIA/NSA-Grade Duino-OSINT Platform - All-Source Intelligence\033[0m
        """

    def run_crwl(self, url):
        """Execute web scraping with crawl4ai"""
        print(f"🚀 Launching web crawler for: {url}")
        command = ["crwl", url, "-o", "markdown"]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"❌ Error: {e.stderr}")
            return None

    def clean_link(self, raw_link):
        """Extract valid URLs from text"""
        return re.search(r'(https?://[^\s›]+)', raw_link).group(1) if re.search(r'https?://', raw_link) else None

    def extract_links(self, markdown_text):
        """Extract all valid links from Markdown"""
        return [self.clean_link(line) for line in markdown_text.splitlines() 
                if line.strip().startswith("http")]

    def is_youtube_url(self, url):
        """Check if URL is YouTube video"""
        parsed = urlparse(url)
        return any((
            parsed.hostname == 'youtu.be',
            parsed.hostname.endswith('youtube.com') and 'v=' in parsed.query
        ))

    def get_video_id(self, url):
        """Extract YouTube video ID"""
        parsed = urlparse(url)
        return parsed.path[1:] if parsed.hostname == 'youtu.be' else parse_qs(parsed.query).get('v', [None])[0]

    def fetch_subtitles(self, video_id):
        """Fetch YouTube subtitles with timestamps"""
        print(f"🔍 Fetching subtitles for video ID: {video_id}")
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            subtitles_md = []
            
            for transcript in transcript_list:
                lang = transcript.language_code
                print(f"Formatting {lang} subtitles 🌐")
                subtitles = transcript.fetch()
                formatted = "\n".join(
                    f"⏰ [{entry.start:.2f}s] {entry.text}" 
                    for entry in subtitles
                )
                subtitles_md.append(f"### {lang} 🇬🇧\n{formatted}")
                
            return "\n\n".join(subtitles_md) if subtitles_md else "🚫 No subtitles found"
            
        except Exception as e:
            return f"🔥 Error: {str(e)}"

    def process_url(self, url):
        """Process URLs - fetch subtitles or scrape content"""
        if self.is_youtube_url(url):
            print(f"🎥 Detected YouTube URL: {url}")
            video_id = self.get_video_id(url)
            return self.fetch_subtitles(video_id) if video_id else "❌ Invalid YouTube URL"
        
        print(f"📄 Scraping regular URL: {url}")
        return self.run_crwl(url) or "❌ Failed to scrape content"

    def write_and_display_markdown(self, results):
        """Write to file and show preview"""
        try:
            with open("results.md", "w", encoding="utf-8") as f:
                f.write("\n\n".join(results))
                
            print("\n\n🎉 Results Preview 🎉")
            print("====================")
            print("\n\n".join(results))
            print("\n\n✅ Full results saved to results.md")
            
        except Exception as e:
            print(f"❌ File Error: {e}")

    def process_user_input(self, user_input):
        """Extract URLs from input"""
        urls = []
        for token in user_input.split():
            token = token.strip(",.;")
            if re.match(r'https?://', token):
                urls.append(token)
                continue
            if '.' in token:
                urls.append(f"http://{token}")
        return urls

    def run(self, user_input):
        """Main execution method"""
        print(self.banner)
        
        if not user_input.strip():
            print("❌ No input provided. Exiting.")
            return

        results = []
        urls_to_process = []

        # Process input type
        extracted_urls = self.process_user_input(user_input)
        if extracted_urls:
            print(f"\n🔗 Processing {len(extracted_urls)} URLs:")
            urls_to_process = extracted_urls
            results.append(f"# URL Results 📡\n\nProcessing: {', '.join(urls_to_process)}")
        else:
            print("\n🔎 Performing Google search...")
            search_url = f"https://www.google.com/search?q={user_input.replace(' ', '+')}"
            search_results = self.run_crwl(search_url)
            if not search_results:
                print("❌ Failed to get search results.")
                return
            results.append(f"# Google Search Results 🔍\n\n{search_results}")
            urls_to_process = self.extract_links(search_results)[:10]

        # Process each URL
        for url in urls_to_process:
            print(f"\n\n🚀 Processing: {url}")
            content = self.process_url(url)
            results.append(f"## 📄 {url}\n\n{content}")

        self.write_and_display_markdown(results)

# Entry point
if __name__ == "__main__":
    scrapper = DuinoScrapper()
    scrapper.run(sys.argv[1] if len(sys.argv) > 1 else input("\n.Enter keyword(s) or URL(s) 🎯: "))