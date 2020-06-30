<div align="center">
  <img src="/images/logo.png?raw=true" alt="Homebridge and Magic Home logos" width="275">
  <h1>Homebridge Magic Home Sync</h1>
  <span align="center">
</div>

### Sync your Magic Home device to your display and control it all via Homebridge
This [Homebridge](https://github.com/homebridge/homebridge) plugin provides a simple switch that enables and disables a Python script on a host display. The script finds the most dominant colour on the display ands sends it to a Magic Home light. 

The result is a much more immersive viewing experience.

<div align='center'>
  <img src="https://media.giphy.com/media/VCnndOVcAY2aAEgRT6/giphy.gif" alt="Display sync demonstration">
</div>

## Installation
### Homebridge
Given that you already have [Homebridge](https://github.com/homebridge/homebridge) installed and set up, you can install this plugin with the following command: 
```
$ sudo npm install -g homebridge-magichome-sync
```

### Host Display
A [Python version >= 3](https://www.python.org) must be used to run the host application.

First you must clone the repository on the host machine using the following command:
```
$ git clone https://github.com/mjsamuel/Homebridge-MagicHome-Sync.git
```

After that, to create a virtual environment for all the projects dependencies to be installed into, use the following commands:
```
# Navigate to the host folder
$ cd Homebridge-MagicHome-Sync/host

# Create a Python virtual environment
$ python -m venv venv

# Activate the virtual environment
$ source ./venv/bin/activate

# Download the requirements
$ pip install -r requirements.txt
```

Once all the dependencies have been installed, to run the Python script use the following command:
```
$ python run.py
```

The Python application can also be configured to run on startup using tools such as `forever` or `launchctl`.

## Configuration
### Settings
- `name` is the name for the accessory, default is "Magic Home Sync"
- `host_ip` is the IP address of the host device that is running the sync program
- `host_port` is the host display port, default is "6006"
- `light_ip` is the IP address of the light to be synced with the host
- `light_type` is the Magic Home device type, being either "RGB", "RGBW" or" RGBWW", default is "RGBW"
- `polling interval` is the interval in seconds that the lights are updated in, default is 1

### Example Configuration
```json
"accessories": [
    {
        "accessory": "MagicHomeSync",
        "name": "MH Sync",
        "host_ip": "192.168.2.128",
        "host_port": 6006,
        "light_ip": "192.168.2.129",
        "light_type": "RGBWW",
        "polling_interval": 0.5
    }
]
```

## Acknowledgements 
Many thanks to:
- [Danielhiversen](https://github.com/Danielhiversen) for his [flux_led](https://github.com/Danielhiversen/flux_led) project which was stripped down and used to interface with Magic Home devices
