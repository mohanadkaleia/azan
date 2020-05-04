import time
from util.soundplayer import SoundPlayer


p = SoundPlayer("./assets/azan.mp3", 1)  
p.play(volume=1, blocking=True)

print("hi")
time.sleep(5)