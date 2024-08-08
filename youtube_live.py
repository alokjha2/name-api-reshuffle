# youtube_live.py

import requests
from bs4 import BeautifulSoup

def get_live_stream_url(channel_url):
    try:
        response = requests.get(channel_url + "/live")
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the live stream URL
        stream_url = soup.find('meta', {'property': 'og:url'})
        if stream_url:
            return stream_url['content']

        # Check if the channel is live using the title
        title = soup.find('title').text
        if 'is live now' in title.lower():
            return channel_url + "/live"
        
    except Exception as e:
        print(f"Error fetching live stream URL for {channel_url}: {e}")
    
    return None

def get_live_streams_from_channels(channels):
    live_channels = {}

    for channel_url in channels:
        live_stream_url = get_live_stream_url(channel_url)
        if live_stream_url:
            live_channels[channel_url] = live_stream_url

    return live_stream_url
