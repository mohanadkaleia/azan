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
    "audio_device": "plughw:1,0",  # Use plughw for automatic format conversion
    "audio_method": "auto",     # Try aplay first, fallback to omxplayer for sample rate issues
    "audio_volume": 100,        # Volume level (0-100) for omxplayer
    "audio_retry_attempts": 3,  # Number of retry attempts for flaky USB audio
    "usb_audio_wakeup": True,   # Enable USB audio wake-up for flaky devices
    # Audio format settings (matches your azan.wav file)
    "audio_sample_rate": 22050, # Sample rate in Hz (22050 for your file)
    "audio_channels": 2,        # Number of channels (2 = stereo)
    "audio_format": "S16_LE",   # Audio format (16-bit little-endian)
    
    # Alternative configurations if speed is still wrong:
    # "audio_device": "hw:1,0",        # Direct hardware access
    # "audio_method": "omxplayer",     # Use omxplayer instead
    # "audio_sample_rate": 44100,      # Force different sample rate
}
