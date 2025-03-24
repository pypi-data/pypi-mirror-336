import requests
from bs4 import BeautifulSoup
import random

class LyricsFinder:
    def __init__(self, song_title, artist):
        self.song_title = song_title
        self.artist = artist
        self.base_url = f"https://www.azlyrics.com/lyrics/{artist.lower().replace(' ', '')}/{song_title.lower().replace(' ', '')}.html"

        # List of common User-Agent strings to rotate
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
        ]

    def find_lyrics(self):
        # Directly construct the AZLyrics URL for the song
        song_url = self.base_url
        
        # Randomize User-Agent for every request
        headers = {
            "User-Agent": random.choice(self.user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "TE": "Trailers"
        }

        # Send a GET request to the lyrics page with headers to avoid 403 errors
        response = requests.get(song_url, headers=headers)
        
        if response.status_code != 200:
            return f"Failed to retrieve lyrics page (status code {response.status_code})"
        
        # Parse the HTML response
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the lyrics container (AZLyrics page structure)
        lyrics_container = soup.find('div', class_='col-xs-12 col-lg-8 text-center')  # AZLyrics pattern
        
        if lyrics_container:
            # Get the text and clean it
            lyrics = lyrics_container.get_text(strip=True)
            return lyrics
        
        return "Lyrics not found."