#!/bin/bash

# USB Audio Fixer Script for Raspberry Pi
# This script addresses common causes of flaky USB audio issues

echo "🔧 USB Audio Fixer for Raspberry Pi"
echo "===================================="

# Check if running as root for some operations
if [[ $EUID -eq 0 ]]; then
    IS_ROOT=true
    echo "✅ Running with root privileges"
else
    IS_ROOT=false
    echo "⚠️  Running without root privileges (some fixes may require sudo)"
fi

echo ""
echo "1. 🔍 Checking current audio devices..."
echo "Available audio devices:"
aplay -l || echo "❌ aplay command not found. Install with: sudo apt install alsa-utils"

echo ""
echo "2. 🔌 Checking USB power management..."

# Disable USB autosuspend for audio devices
if [ "$IS_ROOT" = true ] || sudo -n true 2>/dev/null; then
    echo "Disabling USB autosuspend for audio devices..."
    
    # Find USB audio devices and disable autosuspend
    for usb_device in /sys/bus/usb/devices/*/product; do
        if [ -f "$usb_device" ]; then
            device_name=$(cat "$usb_device" 2>/dev/null)
            device_dir=$(dirname "$usb_device")
            
            if echo "$device_name" | grep -iq "audio\|speaker\|sound"; then
                echo "Found USB audio device: $device_name"
                
                # Disable autosuspend
                autosuspend_file="$device_dir/power/autosuspend_delay_ms"
                control_file="$device_dir/power/control"
                
                if [ -f "$autosuspend_file" ]; then
                    if [ "$IS_ROOT" = true ]; then
                        echo -1 > "$autosuspend_file" 2>/dev/null && echo "  ✅ Disabled autosuspend delay"
                    else
                        echo -1 | sudo tee "$autosuspend_file" > /dev/null 2>&1 && echo "  ✅ Disabled autosuspend delay"
                    fi
                fi
                
                if [ -f "$control_file" ]; then
                    if [ "$IS_ROOT" = true ]; then
                        echo "on" > "$control_file" 2>/dev/null && echo "  ✅ Set power control to 'on'"
                    else
                        echo "on" | sudo tee "$control_file" > /dev/null 2>&1 && echo "  ✅ Set power control to 'on'"
                    fi
                fi
            fi
        fi
    done
else
    echo "❌ Cannot modify USB power settings without sudo access"
fi

echo ""
echo "3. 🎵 Setting up audio configuration..."

# Check and create .asoundrc if needed
ASOUNDRC="$HOME/.asoundrc"
if [ ! -f "$ASOUNDRC" ]; then
    echo "Creating .asoundrc file for USB audio..."
    cat > "$ASOUNDRC" << 'EOF'
# USB Audio Configuration
pcm.!default {
    type hw
    card 1
}
ctl.!default {
    type hw
    card 1
}

# Alternative configuration if card 1 doesn't work
# pcm.!default {
#     type plughw
#     card 1
# }
EOF
    echo "✅ Created $ASOUNDRC"
else
    echo "✅ $ASOUNDRC already exists"
fi

echo ""
echo "4. 🔧 Testing audio playback..."

# Test audio with different methods
test_tone_file="/tmp/test_beep.wav"

# Create a simple test tone
if command -v sox >/dev/null 2>&1; then
    sox -n -r 44100 -c 2 "$test_tone_file" synth 0.5 sine 1000 2>/dev/null
    echo "✅ Created test tone with sox"
elif command -v ffmpeg >/dev/null 2>&1; then
    ffmpeg -f lavfi -i "sine=frequency=1000:duration=0.5" -ar 44100 -ac 2 "$test_tone_file" -y >/dev/null 2>&1
    echo "✅ Created test tone with ffmpeg"
else
    echo "⚠️  No audio generator found (sox or ffmpeg). Skipping tone test."
    test_tone_file=""
fi

if [ -n "$test_tone_file" ] && [ -f "$test_tone_file" ]; then
    echo "Testing audio playback methods..."
    
    # Test aplay
    echo -n "  Testing aplay: "
    if timeout 3s aplay "$test_tone_file" >/dev/null 2>&1; then
        echo "✅ Works"
    else
        echo "❌ Failed"
    fi
    
    # Test with specific device
    echo -n "  Testing aplay with hw:1,0: "
    if timeout 3s aplay -D hw:1,0 "$test_tone_file" >/dev/null 2>&1; then
        echo "✅ Works"
    else
        echo "❌ Failed"
    fi
    
    # Test omxplayer if available
    if command -v omxplayer >/dev/null 2>&1; then
        echo -n "  Testing omxplayer: "
        if timeout 3s omxplayer --no-osd -o alsa "$test_tone_file" >/dev/null 2>&1; then
            echo "✅ Works"
        else
            echo "❌ Failed"
        fi
    else
        echo "  omxplayer not installed"
    fi
    
    # Cleanup
    rm -f "$test_tone_file"
fi

echo ""
echo "5. 📋 Recommendations for persistent fixes:"

echo "   Add to /boot/cmdline.txt to disable USB power management:"
echo "   usb-storage.delay_use=0 dwc_otg.lpm_enable=0"
echo ""
echo "   Add to /boot/config.txt for better USB audio:"
echo "   dtparam=audio=off"
echo "   hdmi_drive=2"
echo ""
echo "   Add to /etc/modprobe.d/alsa-base.conf:"
echo "   options snd-usb-audio index=0"
echo "   options snd-bcm2835 index=1"

echo ""
echo "6. 🔄 Service restart recommendations:"
echo "   sudo systemctl restart alsa-state"
echo "   sudo alsa force-reload"

echo ""
echo "✅ USB Audio Fixer completed!"
echo "   Reboot your Raspberry Pi for all changes to take effect."
echo "   Test your azan app with: python scheduler.py test"
