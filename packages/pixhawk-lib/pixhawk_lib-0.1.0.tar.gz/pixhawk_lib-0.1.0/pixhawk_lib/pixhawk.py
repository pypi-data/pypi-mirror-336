# pixhawk_lib/pixhawk.py
from dronekit import connect, VehicleMode, Command, LocationGlobalRelative
import time
import logging
from .tunes import HAPPY_BIRTHDAY, DANGER, ALL_SAFE, EXPLODE
from .decorators import check_battery_level, check_gps_lock
from pymavlink import mavutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PixHawk:
    MAX_SPEED = 5  # Maximum speed in m/s

    def __init__(self, connection_string='/dev/ttyACM0', baud=115200, wait_until_done=False):
        """Initialize PixHawk with a connection string, baud rate, and wait_until_done flag.

        Args:
            connection_string (str): The connection string for the Pixhawk (default: '/dev/ttyACM0').
            baud (int): Baud rate for the connection (default: 115200).
            wait_until_done (bool): If True, methods wait for actions to complete (default: False).
        """
        self.connection_string = connection_string
        self.baud = baud
        self.wait_until_done = wait_until_done  # Controls whether methods block until completion
        self.vehicle = None
        self.current_speed = 0  # Current speed setting
        self.tunes = {
            'HAPPY_BIRTHDAY': HAPPY_BIRTHDAY,
            'DANGER': DANGER,
            'ALL_SAFE': ALL_SAFE,
            'EXPLODE': EXPLODE
        }
        self.connect()
        self.state = self.State(self.vehicle)  # Initialize state object

    ### Inner State Class ###
    class State:
        def __init__(self, vehicle):
            self.vehicle = vehicle

        def battery(self):
            """Return battery level in percentage."""
            return self.vehicle.battery.level

        def gps(self):
            """Return GPS fix type."""
            return self.vehicle.gps_0.fix_type

        def mode(self):
            """Return current mode."""
            return self.vehicle.mode.name

        def altitude(self):
            """Return altitude in meters."""
            return self.vehicle.location.global_relative_frame.alt

        def heading(self):
            """Return heading in degrees."""
            return self.vehicle.heading

        def __str__(self):
            """Return all state info as a string."""
            return (f"Battery: {self.battery()}%\n"
                    f"GPS Fix Type: {self.gps()} (3+ is 3D lock)\n"
                    f"Mode: {self.mode()}\n"
                    f"Altitude: {self.altitude()} meters\n"
                    f"Heading: {self.heading()} degrees")

    ### Connection Method ###
    def connect(self):
        """Connect to the Pixhawk."""
        try:
            self.vehicle = connect(self.connection_string, baud=self.baud, wait_ready=True)
            logger.info(f"Connected to Pixhawk on {self.connection_string}")
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise ConnectionError(f"Failed to connect: {e}")

    @check_battery_level(min_level=30)
    @check_gps_lock
    def takeoff(self, altitude):
        """Take off to the specified altitude (in meters).

        Args:
            altitude (float): Target altitude in meters.
        """
        logger.info(f"Taking off to {altitude} meters")
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True
        while not self.vehicle.armed:
            time.sleep(1)
        self.vehicle.simple_takeoff(altitude)
        if self.wait_until_done:
            while self.vehicle.location.global_relative_frame.alt < altitude * 0.95:  # 95% tolerance
                time.sleep(0.5)  # Poll every 0.5 seconds
            logger.info("Reached target altitude")

    def land(self):
        """Land the drone."""
        logger.info("Landing...")
        self.vehicle.mode = VehicleMode("LAND")
        if self.wait_until_done:
            while self.vehicle.armed:  # Wait until disarmed
                time.sleep(0.5)  # Poll every 0.5 seconds
            logger.info("Landed")

    ### Rotation Methods ###
    def clockwise(self, degrees):
        """Rotate clockwise by the specified degrees.

        Args:
            degrees (float): Degrees to rotate clockwise.
        """
        logger.info(f"Rotating clockwise by {degrees} degrees")
        current_heading = self.vehicle.heading
        target_heading = (current_heading + degrees) % 360
        self.vehicle.condition_yaw(target_heading, relative=False)
        if self.wait_until_done:
            while abs(self.vehicle.heading - target_heading) > 5:  # 5-degree tolerance
                time.sleep(0.5)  # Poll every 0.5 seconds
            logger.info("Rotation completed")

    def counterclockwise(self, degrees):
        """Rotate counterclockwise by the specified degrees.

        Args:
            degrees (float): Degrees to rotate counterclockwise.
        """
        logger.info(f"Rotating counterclockwise by {degrees} degrees")
        current_heading = self.vehicle.heading
        target_heading = (current_heading - degrees) % 360
        self.vehicle.condition_yaw(target_heading, relative=False)
        if self.wait_until_done:
            while abs(self.vehicle.heading - target_heading) > 5:  # 5-degree tolerance
                time.sleep(0.5)  # Poll every 0.5 seconds
            logger.info("Rotation completed")

    ### State Retrieval ###
    def get_state(self):
        """Print the current state of the Pixhawk."""
        print(self.state)

    def play_tune(self, tune_name):
        """Play a predefined tune by name.

        Args:
            tune_name (str): Name of the tune to play (e.g., 'HAPPY_BIRTHDAY').
        """
        if tune_name in self.tunes:
            tune_string = self.tunes[tune_name]
            for i in range(0, len(tune_string), 30):
                segment = tune_string[i:i+30]
                self.vehicle.play_tune(segment.encode('utf-8'))
            logger.info(f"Played tune: {tune_name}")
        else:
            logger.warning(f"Tune '{tune_name}' not found")

    def disconnect(self):
        """Disconnect from the Pixhawk."""
        if self.vehicle:
            self.vehicle.close()
            logger.info("Disconnected")

    ### Movement Commands ###
    def _move(self, direction, distance_cm):
        """Helper method to move in a specific direction by distance in cm.

        Args:
            direction (str): Direction to move ('forward', 'backward', 'left', 'right', 'up', 'down').
            distance_cm (float): Distance to move in centimeters.
        """
        distance_m = distance_cm / 100.0
        current_location = self.vehicle.location.global_relative_frame

        if direction == 'forward':
            target_location = LocationGlobalRelative(
                current_location.lat + (distance_m / 111111.0),
                current_location.lon,
                current_location.alt
            )
        elif direction == 'backward':
            target_location = LocationGlobalRelative(
                current_location.lat - (distance_m / 111111.0),
                current_location.lon,
                current_location.alt
            )
        elif direction == 'left':
            target_location = LocationGlobalRelative(
                current_location.lat,
                current_location.lon - (distance_m / (111111.0 * 0.7071)),
                current_location.alt
            )
        elif direction == 'right':
            target_location = LocationGlobalRelative(
                current_location.lat,
                current_location.lon + (distance_m / (111111.0 * 0.7071)),
                current_location.alt
            )
        elif direction == 'up':
            target_location = LocationGlobalRelative(
                current_location.lat,
                current_location.lon,
                current_location.alt + distance_m
            )
        elif direction == 'down':
            target_location = LocationGlobalRelative(
                current_location.lat,
                current_location.lon,
                current_location.alt - distance_m
            )
        else:
            raise ValueError(f"Invalid direction: {direction}")

        self.vehicle.simple_goto(target_location)
        if self.wait_until_done:
            while True:
                current_location = self.vehicle.location.global_relative_frame
                remaining_distance = self._get_distance(current_location, target_location)
                if remaining_distance < 0.1:  # 0.1-meter tolerance
                    break
                time.sleep(0.5)  # Poll every 0.5 seconds
            logger.info(f"Moved {direction} by {distance_cm} cm")

    def _get_distance(self, loc1, loc2):
        """Calculate distance between two locations in meters.

        Args:
            loc1 (LocationGlobalRelative): Starting location.
            loc2 (LocationGlobalRelative): Target location.

        Returns:
            float: Distance in meters.
        """
        dlat = loc2.lat - loc1.lat
        dlon = loc2.lon - loc1.lon
        return ((dlat * 111111.0)**2 + (dlon * 111111.0 * 0.7071)**2)**0.5

    def move_forward(self, distance_cm):
        """Move forward by the specified distance in cm."""
        self._move('forward', distance_cm)

    def move_backward(self, distance_cm):
        """Move backward by the specified distance in cm."""
        self._move('backward', distance_cm)

    def move_left(self, distance_cm):
        """Move left by the specified distance in cm."""
        self._move('left', distance_cm)

    def move_right(self, distance_cm):
        """Move right by the specified distance in cm."""
        self._move('right', distance_cm)

    def move_up(self, distance_cm):
        """Move up by the specified distance in cm."""
        self._move('up', distance_cm)

    def move_down(self, distance_cm):
        """Move down by the specified distance in cm."""
        self._move('down', distance_cm)

    ### Continuous Movement ###
    def _set_velocity(self, vx, vy, vz):
        """Set velocity in NED frame (vx: north, vy: east, vz: down).

        Args:
            vx (float): Velocity in north direction (m/s).
            vy (float): Velocity in east direction (m/s).
            vz (float): Velocity in down direction (m/s).
        """
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
            0, 0, 0,
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,
            0b0000111111000111,  # Only velocity
            0, 0, 0,  # Position
            vx, vy, vz,  # Velocity
            0, 0, 0, 0, 0  # Accel, yaw, yaw rate
        )
        self.vehicle.send_mavlink(msg)

    def forward(self, speed=None):
        """Move forward at the specified or current speed (m/s).

        Args:
            speed (float, optional): Speed in m/s. If None, uses current speed.
        """
        speed = self.current_speed if speed is None else speed
        self._set_velocity(speed, 0, 0)
        logger.info("Moving forward")

    def backward(self, speed=None):
        """Move backward at the specified or current speed (m/s).

        Args:
            speed (float, optional): Speed in m/s. If None, uses current speed.
        """
        speed = self.current_speed if speed is None else speed
        self._set_velocity(-speed, 0, 0)
        logger.info("Moving backward")

    def left(self, speed=None):
        """Move left at the specified or current speed (m/s).

        Args:
            speed (float, optional): Speed in m/s. If None, uses current speed.
        """
        speed = self.current_speed if speed is None else speed
        self._set_velocity(0, -speed, 0)
        logger.info("Moving left")

    def right(self, speed=None):
        """Move right at the specified or current speed (m/s).

        Args:
            speed (float, optional): Speed in m/s. If None, uses current speed.
        """
        speed = self.current_speed if speed is None else speed
        self._set_velocity(0, speed, 0)
        logger.info("Moving right")

    def up(self, speed=None):
        """Move up at the specified or current speed (m/s).

        Args:
            speed (float, optional): Speed in m/s. If None, uses current speed.
        """
        speed = self.current_speed if speed is None else speed
        self._set_velocity(0, 0, -speed)
        logger.info("Moving up")

    def down(self, speed=None):
        """Move down at the specified or current speed (m/s).

        Args:
            speed (float, optional): Speed in m/s. If None, uses current speed.
        """
        speed = self.current_speed if speed is None else speed
        self._set_velocity(0, 0, speed)
        logger.info("Moving down")

    def stop(self):
        """Stop the drone by setting velocity to 0."""
        self._set_velocity(0, 0, 0)
        logger.info("Stopped")

    ### Speed Control ###
    def speed(self, value=None):
        """Get or set the speed (0 to 1).

        Args:
            value (float, optional): Speed value between 0 and 1. If None, returns current speed.

        Returns:
            float: Current speed in m/s if no value provided.
        """
        if value is None:
            return self.current_speed
        elif 0 <= value <= 1:
            self.current_speed = value * self.MAX_SPEED
            logger.info(f"Speed set to {self.current_speed} m/s")
        else:
            raise ValueError("Speed must be between 0 and 1")