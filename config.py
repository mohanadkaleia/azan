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
    # Audio configuration - Optimized for your USB speaker
    "audio_device": "hw:1,0",   # Your USB2.0 Device (confirmed working)
    "audio_method": "aplay",    # aplay works perfectly with your setup
    "audio_volume": 100,        # Volume level (0-100) for omxplayer
    "audio_retry_attempts": 3,  # Number of retry attempts for flaky USB audio
    "usb_audio_wakeup": True,   # Enable USB audio wake-up for flaky devices
}
