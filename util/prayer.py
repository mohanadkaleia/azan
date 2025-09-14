import datetime
import os
import sys
import logger
import subprocess
import time
import config

try:
    import simpleaudio
    HAS_SIMPLEAUDIO = True
except ImportError:
    HAS_SIMPLEAUDIO = False

log = logger.get_logger(__name__)


def play_with_aplay(file_path, retry_count=3):
    """Fallback method using aplay (ALSA's command-line player) with retry logic"""
    audio_device = config.default.get("audio_device", "default")
    
    for attempt in range(retry_count):
        try:
            log.info(f"Attempting to play audio using aplay (attempt {attempt + 1}/{retry_count})...")
            
            # Sometimes USB audio needs time to initialize
            if attempt > 0:
                log.info(f"Waiting 2 seconds before retry...")
                time.sleep(2)
                
                # Try to reset/wake up the audio device
                try:
                    subprocess.run(['amixer', 'sset', 'PCM', '100%'], 
                                 capture_output=True, text=True, timeout=5)
                except:
                    pass  # Ignore amixer errors
            
            cmd = ['aplay']
            if audio_device != "default":
                cmd.extend(['-D', audio_device])
            cmd.append(file_path)
            
            log.info(f"Running aplay command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=30)
            log.info("Audio played successfully using aplay")
            return True
            
        except subprocess.CalledProcessError as e:
            log.error(f"aplay failed (attempt {attempt + 1}): {e}")
            log.error(f"aplay stderr: {e.stderr}")
            
            # On failure, try to reset ALSA
            if attempt < retry_count - 1:
                try:
                    log.info("Attempting to reset ALSA...")
                    subprocess.run(['sudo', 'alsa', 'force-reload'], 
                                 capture_output=True, text=True, timeout=10)
                except:
                    pass
                    
        except subprocess.TimeoutExpired:
            log.error(f"aplay timed out (attempt {attempt + 1})")
            
        except FileNotFoundError:
            log.error("aplay command not found")
            return False
    
    return False


def play_with_omxplayer(file_path, retry_count=2):
    """Fallback method using omxplayer (Raspberry Pi's media player) with retry logic"""
    audio_volume = config.default.get("audio_volume", 100)
    
    # Convert volume to omxplayer format (0-100 to millibels, roughly)
    volume_mb = int((audio_volume - 100) * 100)  # 100% = 0mb, 0% = -10000mb
    
    for attempt in range(retry_count):
        try:
            log.info(f"Attempting to play audio using omxplayer (attempt {attempt + 1}/{retry_count})...")
            
            if attempt > 0:
                log.info("Waiting 1 second before retry...")
                time.sleep(1)
            
            cmd = ['omxplayer', '--no-osd', '-o', 'alsa', '--vol', str(volume_mb), file_path]
            log.info(f"Running omxplayer command: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=60)
            log.info("Audio played successfully using omxplayer")
            return True
            
        except subprocess.CalledProcessError as e:
            log.error(f"omxplayer failed (attempt {attempt + 1}): {e}")
            if e.stderr:
                log.error(f"omxplayer stderr: {e.stderr}")
                
        except subprocess.TimeoutExpired:
            log.error(f"omxplayer timed out (attempt {attempt + 1})")
            
        except FileNotFoundError:
            log.error("omxplayer command not found")
            return False
    
    return False


def wake_up_usb_audio():
    """Try to wake up USB audio devices that might be sleeping"""
    if not config.default.get("usb_audio_wakeup", True):
        return True
        
    try:
        log.info("Attempting to wake up USB audio devices...")
        
        # Try to list audio devices to wake them up
        subprocess.run(['aplay', '-l'], capture_output=True, text=True, timeout=5)
        
        # Try a quick test tone to initialize audio
        subprocess.run(['speaker-test', '-c1', '-t', 'sine', '-f', '1000', '-l', '1'], 
                      capture_output=True, text=True, timeout=3)
        
        log.info("USB audio wake-up completed")
        return True
    except:
        log.info("USB audio wake-up had issues (this is normal)")
        return False


def play_with_simpleaudio(file_path, retry_count=2):
    """Original method using simpleaudio with retry logic"""
    for attempt in range(retry_count):
        try:
            log.info(f"Attempting to play audio using simpleaudio (attempt {attempt + 1}/{retry_count})...")
            
            if attempt > 0:
                log.info("Waiting 1 second before retry...")
                time.sleep(1)
                wake_up_usb_audio()
            
            wave_obj = simpleaudio.WaveObject.from_wave_file(file_path)
            play_obj = wave_obj.play()
            play_obj.wait_done()
            log.info("Audio played successfully using simpleaudio")
            return True
            
        except Exception as e:
            log.error(f"simpleaudio failed (attempt {attempt + 1}): {e}")
    
    return False


def play(name=None, azan_name=None):
    if not name:
        name = 'azan.wav'

    path = os.path.dirname(os.path.abspath(__file__))
    file_path = '{}/../assets/{}'.format(path, name)
    
    # Check if audio file exists
    if not os.path.exists(file_path):
        log.error(f"Audio file not found: {file_path}")
        return False
    
    log.info('Calling {} azan now from file: {}'.format(azan_name or 'test', file_path))
    
    # Get preferred audio method from config
    preferred_method = config.default.get("audio_method", "auto").lower()
    
    # Get retry count from config
    retry_count = config.default.get("audio_retry_attempts", 3)
    
    # Define all available methods
    all_methods = []
    if HAS_SIMPLEAUDIO:
        all_methods.append(("simpleaudio", lambda: play_with_simpleaudio(file_path, retry_count)))
    all_methods.extend([
        ("aplay", lambda: play_with_aplay(file_path, retry_count)),
        ("omxplayer", lambda: play_with_omxplayer(file_path, retry_count))
    ])
    
    # Order methods based on preference
    audio_methods = []
    
    if preferred_method != "auto":
        # Try preferred method first
        for method_name, method_func in all_methods:
            if method_name == preferred_method:
                audio_methods.append((method_name, method_func))
                break
        
        # Add remaining methods as fallback
        for method_name, method_func in all_methods:
            if method_name != preferred_method:
                audio_methods.append((method_name, method_func))
    else:
        # Auto mode: use default order
        audio_methods = all_methods
    
    # Pre-flight check: try to wake up USB audio for flaky devices
    log.info("Pre-flight audio check...")
    wake_up_usb_audio()
    time.sleep(0.5)  # Brief pause after wake-up
    
    # Try each method until one succeeds
    for method_name, method_func in audio_methods:
        log.info(f"Trying audio method: {method_name}")
        try:
            if method_func():
                log.info(f"Successfully played audio using {method_name}")
                return True
        except Exception as e:
            log.error(f"Failed to play audio using {method_name}: {e}")
            continue
    
    log.error("All audio playback methods failed!")
    return False  
