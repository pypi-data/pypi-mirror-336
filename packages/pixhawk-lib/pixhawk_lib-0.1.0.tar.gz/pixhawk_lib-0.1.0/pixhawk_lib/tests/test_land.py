# pixhawk_lib/tests/test_land.py
from pixhawk_lib import PixHawk, tunes

drone = PixHawk(connection_string='/dev/ttyACM0')

drone.takeoff(5)
drone.clockwise(90)
drone.move_forward(10)
drone.play_tune(tunes.HAPPY_BIRTHDAY)
drone.land()

drone.disconnect()