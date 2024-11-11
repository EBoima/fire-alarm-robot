from pybricks.robotics import DriveBase
from pybricks.pupdevices import Motor, ColorDistanceSensor, ForceSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction, Color
from pybricks.hubs import PrimeHub
import constants

# State Constants
WANDER = 1
WALL_FOLLOWING = 2
FIRE_DETECTION = 3
EXTINGUISH = 4
COMPLETE = 5


class Robot:
    def __init__(self):
        # PrimeHub
        self.hub = PrimeHub()

        # Motors
        self.left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
        self.right_motor = Motor(Port.B, Direction.CLOCKWISE)
        self.fan_motor = Motor(Port.F)

        # Sensors
        self.color_distance_sensor = ColorDistanceSensor(Port.C)
        self.touch_sensor = ForceSensor(Port.D)
        self.side_sensor = UltrasonicSensor(Port.E)

        # Drive Base
        self.drive_base = DriveBase(
            self.left_motor,
            self.right_motor,
            wheel_diameter=constants.WHEEL_DIAMETER,
            axle_track=constants.AXLE_TRACK
        )
        self.drive_base.use_gyro(True)

        # Initial State
        self.current_state = WANDER

    def detect_obstacle(self):
        """Detect if an obstacle is close by checking the touch sensor."""
        if self.touch_sensor.touched():
            self.drive_base.stop()
            return True
        return False

    def detect_wall_on_right(self):
        """Detect wall or opening on the right side for wall following."""
        return self.side_sensor.distance() < constants.WALL_FOLLOW_MIN_DISTANCE

    def detect_flame(self):
        """Detect flame by measuring ambient light intensity and proximity."""
        # Check if the ambient light intensity is above the threshold, indicating flame presence.
        return self.color_distance_sensor.ambient() > constants.FLAME_DETECTION_THRESHOLD

    def detect_goal(self):
        """Detect if the robot is on the goal tile (Red)."""
        return self.color_distance_sensor.color() == constants.GOAL_COLOR

    def initial_scan_for_flame(self):
        """Rotate 360 degrees to detect flame direction."""
        for _ in range(8):  # Divide 360° into eight 45° turns
            if self.detect_flame():
                print("Flame detected during initial scan")
                return True
            self.drive_base.turn(45)
        return False

    def approach_flame(self):
        """Move toward the flame's location until the robot detects the red goal area."""
        while not self.detect_goal():
            if self.touch_sensor.touched():
                self.drive_base.straight(-constants.WALL_FOLLOW_STEP)
                self.drive_base.turn(-90)  # Turn left to avoid obstacle
            else:
                self.drive_base.straight(
                    constants.APPROACH_FLAME_STEP_DISTANCE)
        self.extinguish()

    def wander(self):
        """Drive forward until an obstacle is hit, then switch to wall-following."""
        if self.detect_obstacle():
            self.drive_base.straight(-constants.WALL_FOLLOW_STEP)
            self.drive_base.turn(-90)
            self.transition_to(WALL_FOLLOWING)
        else:
            self.drive_base.straight(constants.WANDER_DISTANCE)

    def wall_following(self):
        """Wall-following behavior with smoother adjustments."""
        if self.detect_obstacle():
            self.drive_base.straight(-constants.WALL_FOLLOW_STEP)
            self.drive_base.turn(-90)
        elif not self.detect_wall_on_right():
            self.drive_base.turn(-90)
        else:
            distance_error = constants.WALL_FOLLOW_MIN_DISTANCE - self.side_sensor.distance()
            angle_adjustment = distance_error * constants.WALL_FOLLOW_ADJUST_ANGLE
            self.drive_base.turn(angle_adjustment)
            self.drive_base.straight(constants.WALL_FOLLOW_STEP)

    def fire_detection(self):
        """Rotate to find flame direction and approach."""
        self.initial_scan_for_flame()

    def extinguish(self):
        """Activate fan and cool down after extinguishing fire."""
        print("Extinguishing fire...")
        self.fan_motor.run_time(constants.FAN_SPEED, constants.FAN_RUN_TIME)
        self.current_state = COMPLETE
        print("Cooling down after extinguishing fire.")
        self.hub.light.on(Color.GREEN)

    def transition_to(self, new_state):
        """Transition to a new state."""
        self.current_state = new_state
        print(f"Transitioning to {new_state}")

    def raise_alarm(self):
        """Sound an alarm to indicate fire detection."""
        print("Alarm raised!")
        self.hub.speaker.beep(
            frequency=constants.ALARM_FREQUENCY, duration=constants.ALARM_DURATION)

    def update(self):
        """Main update method to handle state transitions and execute current behavior."""
        print(f"Current State: {self.current_state}")

        if self.current_state == WANDER:
            if not self.initial_scan_for_flame():
                print("No flame detected during initial scan. Wandering...")
                self.wander()
            else:
                self.transition_to(FIRE_DETECTION)

        elif self.current_state == WALL_FOLLOWING:
            self.wall_following()
            if self.detect_goal():
                self.transition_to(FIRE_DETECTION)

        elif self.current_state == FIRE_DETECTION:
            self.approach_flame()
            self.transition_to(EXTINGUISH)

        elif self.current_state == EXTINGUISH:
            self.extinguish()
            print("Cooldown period before returning to wander.")
            self.transition_to(WANDER)
