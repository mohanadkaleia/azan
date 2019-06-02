# Azan
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

Heyo 👋 
Azan is an open source project that helps in scheduling Azan prayers based on the city you are in. 
The app is built by calling this API `adhan library` which supports multiple methods (e.g., ISNA)

### Excited to run the app? 🚀
The app is still in progress, it has the following dependecies:
* Python 2.7+ (required) 
* Virtual environment (preferred but not required)


### Install dependencies: 
```sh
pip install -r requirements.txt
```

* Pygame: 

Raspberry pi comes loaded with Pygame, for other platforms please follow Pygame's docs to isntall it: https://www.pygame.org/wiki/GettingStarted#Pygame%20Installation

#### Configure the app: 
To configure the app, navigate to `convifg.py` and set the `city`, `state`, and other configurations, example:
```sh
default = {
    "city": "San Francisco",
    "state": "CA",
    "country": "United States",
    "method": "ISNA",
    "lat": 37.778160,
    "long": -122.412560, 
    "tz_offest": -7,
    "pioled": False,
}
```

#### Run app: 
```sh
> python scheduler.py
```

Example for the output:
```sh
Schedule Dhuhr at 2019-04-07 13:12:25.716128
Schedule Asr at 2019-04-07 16:49:25.716324
Schedule Maghrib at 2019-04-07 19:38:25.716398
Schedule Isha at 2019-04-07 20:53:25.716456
```

## Run the app on boot:
It is important to run the app when the Pi restarts, to do so, you can add the following line to your rc.local file:
```sh
> sudo nano /etc/rc.local
python3 <path-to-azan-folder>/azan/scheduler.py
```

## Integrate PiOLED to display Azan schedule on LED screen (Raspberry Pi only)
You wann something cool! 😎.. try to integrate PiOLED into your pi and you can see the Azan schedule displayed on your little small LED display. you will need the following: 
* PiOLED you can buy it from Amazon or Adafruit directly 
* Follow this link to install the required libraries: 
https://www.adafruit.com/product/3527
* Don't forget to enable PiOLED from the config file
![image](https://user-images.githubusercontent.com/3438755/58767419-8c9c5400-853f-11e9-90c2-30f5f335ef28.png)

## NOTE:
The app still in progress (keep tune for more changes).

License
----

GPL3 -- it seems good to me 😁

