from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from youtube_live import get_live_streams_from_channels

import random
import requests
import re
from youtube_live import get_live_streams_from_channels
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

# Load the CSV files
male_names = pd.read_csv('Indian-Male-Names.csv')
female_names = pd.read_csv('Indian-Female-Names.csv')

namelist = []

# Process female names
for names in female_names['name']:
    first_name = str(names).strip().split(' ')[0]
    namelist.append(first_name)

# Process male names
for names in male_names['name']:
    first_name = str(names).strip().split(' ')[0]
    namelist.append(first_name)

# Further processing on names
processed_name_list = []
s = 'abcdefghijklmnopqrstuvwxyz'

for name in namelist:
    name = name.split('@')[0]
    name = name.split('.')[-1]
    name = name.split('-')[-1]
    name = name.strip('`').strip()

    if len(name) > 2:
        if all(char in s for char in name):
            processed_name_list.append(name)

unique_names = set(processed_name_list)
processed_name_list = sorted(list(unique_names))

# Convert processed_name_list to lowercase for case-insensitive comparison
processed_name_list_lower = [name.lower() for name in processed_name_list]

# Function to check if a name exists in the processed list
def is_name_in_list(name, name_list):
    return name.lower() in name_list

@app.route('/check_name', methods=['GET'])
def check_name():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'Name parameter is required'}), 400
    
    exists = is_name_in_list(name, processed_name_list_lower)
    return jsonify({'name': name, 'exists': exists})

# Predefined list of YouTube channel URLs
channels = [
    "https://www.youtube.com/@WingsGaneshBhakti",
    "https://www.youtube.com/@SomnathTempleOfficialChannel",
    "https://www.youtube.com/@ungalsaimahi",
]

@app.route('/get_live_streams', methods=['GET'])
def get_live_streams():
    random_channel = random.choice(channels)
    
    # Fetch live streams from the selected channel
    live_streams = get_live_streams_from_channels([random_channel])
    # live_streams = get_live_streams_from_channels(channels)
    logger.info(f"live streams: {live_streams}")
    
    return jsonify(live_streams)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)