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

#### Configure the app: 
To configure the app, navigate to `convifg.py` and set the `city`, `state`, and the `cuontry`, example:
```sh
default = {
    "city": "San Francisco",
    "state": "CA",
    "country": "United States",
    "method": "2",
    "azan_end_point": "http://api.aladhan.com/v1/calendarByCity"
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

## NOTE:
The app still in progress (keep tune for more changes).

License
----

GPL3 -- it seems good to me 😁

