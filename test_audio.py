#!/usr/bin/env python3
"""
Audio Test Script for Azan App
Run this script to test different audio methods and troubleshoot audio issues
"""

import os
import sys
import subprocess
import logger

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from util.prayer import play

log = logger.get_logger(__name__)


def check_audio_devices():
    """Check available audio devices"""
    print("🔍 Checking available audio devices...")
    
    try:
        result = subprocess.run(['aplay', '-l'], capture_output=True, text=True, check=True)
        print("Available audio devices:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running aplay -l: {e}")
    except FileNotFoundError:
        print("❌ aplay command not found. Install alsa-utils: sudo apt install alsa-utils")
    
    print("-" * 50)


def test_specific_device(device_name):
    """Test a specific audio device"""
    print(f"🎵 Testing audio device: {device_name}")
    
    try:
        # Use speaker-test for quick audio test
        cmd = ['speaker-test', '-c2', '-t', 'sine', '-f', '1000', '-l', '1']
        if device_name != "default":
            cmd.extend(['-D', device_name])
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Device {device_name} works!")
        else:
            print(f"❌ Device {device_name} failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print(f"✅ Device {device_name} played sound (timeout is normal)")
    except subprocess.CalledProcessError as e:
        print(f"❌ Device {device_name} failed: {e}")
    except FileNotFoundError:
        print("❌ speaker-test not found. Install alsa-utils: sudo apt install alsa-utils")
    
    print("-" * 50)


def test_azan_audio():
    """Test the azan audio playback using the app's method"""
    print("🕌 Testing Azan audio playback...")
    
    # Check if audio file exists
    audio_file = os.path.join(os.path.dirname(__file__), 'assets', 'azan.wav')
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        return False
    
    # Test the play function
    try:
        success = play(azan_name="test")
        if success:
            print("✅ Azan audio playback successful!")
            return True
        else:
            print("❌ Azan audio playback failed!")
            return False
    except Exception as e:
        print(f"❌ Error during azan playback: {e}")
        return False


def show_audio_config():
    """Show current audio configuration"""
    print("⚙️  Current Audio Configuration:")
    print(f"   Audio Device: {config.default.get('audio_device', 'default')}")
    print(f"   Audio Method: {config.default.get('audio_method', 'auto')}")
    print(f"   Audio Volume: {config.default.get('audio_volume', 100)}%")
    print("-" * 50)


def main():
    """Main test function"""
    print("🎵 AZAN AUDIO TROUBLESHOOTER 🎵")
    print("=" * 50)
    
    # Show current config
    show_audio_config()
    
    # Check available devices
    check_audio_devices()
    
    # Test common devices
    devices_to_test = ["default", "hw:1,0", "plughw:1,0", "hw:0,0"]
    for device in devices_to_test:
        test_specific_device(device)
    
    # Test actual azan playback
    test_azan_audio()
    
    print("\n📋 TROUBLESHOOTING RECOMMENDATIONS:")
    print("1. If no USB device appears in 'aplay -l', check USB connection")
    print("2. If device appears but fails, try different device names (hw:X,Y)")
    print("3. Update your config.py with working device name")
    print("4. Consider using 'aplay' or 'omxplayer' method instead of 'simpleaudio'")
    print("5. Ensure your user is in the 'audio' group: sudo usermod -a -G audio $USER")
    print("6. Reboot after audio configuration changes")


if __name__ == "__main__":
    main()
