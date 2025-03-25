# pixhawk_lib/decorators.py
import functools

class LowBatteryError(Exception):
    pass

class GPSLockError(Exception):
    pass

def check_battery_level(min_level=20):
    """Ensure battery level is above min_level before proceeding."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.vehicle.battery.level < min_level:
                self.play_tune('DANGER')
                raise LowBatteryError(f"Battery too low: {self.vehicle.battery.level}%")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def check_gps_lock(func):
    """Ensure GPS is locked before proceeding."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.vehicle.gps_0.fix_type < 2:  # Less than 2 means no lock
            self.play_tune('DANGER')
            raise GPSLockError("No GPS lock")
        return func(self, *args, **kwargs)
    return wrapper