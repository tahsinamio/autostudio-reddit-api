import random

import requests
from requests.exceptions import JSONDecodeError

from utils import settings

voices = [
    "Dan"
    # "Scarlett",
    # "Liv",
    # "Will",
    # "Amy"
]

class unrealspeech:
    def __init__(self):
        self.url = "https://api.v6.unrealspeech.com/speech"
        self.max_chars = 3000
        self.voices = voices

    def run(self, text, filepath, random_voice: bool = False):
        if random_voice:
            voice = self.randomvoice()
        else:
            voice = str(settings.config["settings"]["tts"]["unrealspeech_voice_name"]).capitalize()

        if settings.config["settings"]["tts"]["unrealspeech_api_key"]:
            api_key = settings.config["settings"]["tts"]["unrealspeech_api_key"]
        else:
            raise ValueError(
                "You didn't set an UnrealSpeech API key! Please set the config variable UNREALSPEECH_API_KEY to a valid API key."
            )

        payload = {
            "Text": text,
            "VoiceId": voice,
            "Bitrate": "192k",
            "Speed": "0",
            "Pitch": "1",
            "TimestampType": "word"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": "Bearer " + api_key
        }

        response = requests.post(self.url, json=payload, headers=headers)

        try:
            voice_data = requests.get(response.json()["OutputUri"])
            with open(filepath, "wb") as f:
                f.write(voice_data.content)
        except (KeyError, JSONDecodeError):
            try:
                if response.json()["error"] == "No text specified!":
                    raise ValueError("Please specify a text to convert to speech.")
            except (KeyError, JSONDecodeError):
                print("Error occurred calling UnrealSpeech")


    def randomvoice(self):
        return random.choice(self.voices)