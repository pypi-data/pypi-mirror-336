# PixHawk Library


A simple Python library for controlling Pixhawk drones easy. It provides an easy-to-use interface for basic flight commands, state retrieval, safety checks, and playing tunes on the Pixhawk buzzer.

## ⚠️ Danger
This is under develop project and not stable

## Installation

```bash
pip install pixhawk-lib
```

## Usage

```python
from pixhawk_lib import PixHawk

# Initialize with default settings (non-blocking)
drone = PixHawk(connection_string='/dev/ttyACM0')

# Take off and rotate
drone.takeoff(5)  # Take off to 5 meters
drone.clockwise(90)  # Rotate 90 degrees clockwise
drone.land()  # Land the drone

# With waiting enabled
drone = PixHawk(wait_until_done=True)
drone.takeoff(5)  # Waits until 5 meters is reached
drone.play_tune('HAPPY_BIRTHDAY')  # Play a tune
drone.disconnect()
```

## Features

- Basic flight commands: takeoff, land, clockwise, counterclockwise
- Movement: move_forward, move_left, etc. (in centimeters)
- Continuous movement: forward, stop, etc.
- State retrieval: drone.state.battery(), drone.state.gps(), etc.
- Safety decorators: Battery and GPS checks
- Tunes: Predefined tunes like HAPPY_BIRTHDAY, DANGER

## Requirements

- Python 3.9+
- DroneKit
- PyMAVLink
- pyserial

## License

- MIT License

