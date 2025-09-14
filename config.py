default = {
    "city": "San Francisco",
    "state": "CA",
    "country": "United States",
    "method": "ISNA",
    "lat": 37.778160,
    "long": -122.412560,
    "pioled": False,
    "fajr": True,
    "zuhr": False, 
    "asr": False,
    "maghrib": True, 
    "isha": True,
    # Audio configuration
    "audio_device": "default",  # Can be "default", "hw:1,0", "plughw:1,0" etc.
    "audio_method": "auto",     # "auto", "simpleaudio", "aplay", "omxplayer"
    "audio_volume": 100,        # Volume level (0-100) for omxplayer
    "audio_retry_attempts": 3,  # Number of retry attempts for flaky USB audio
    "usb_audio_wakeup": True,   # Enable USB audio wake-up for flaky devices
}
