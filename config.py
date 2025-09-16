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
    "audio_device": "plughw:1,0", # Use plughw for automatic sample rate conversion
                                 # This should fix speed issues without format parameters
    "audio_method": "aplay",     # Back to aplay - omxplayer hangs
    "audio_volume": 100,        # Volume for omxplayer (0-100)
    "audio_retry_attempts": 3,  # Retry count for flaky USB audio
    "usb_audio_wakeup": True,   # Wake up sleeping USB devices
}
