from pybricks.robotics import DriveBase
from pybricks.pupdevices import Motor, ColorSensor, ForceSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction, Color
from pybricks.hubs import PrimeHub
import constants

# State Constants
WANDER = 1
WALL_FOLLOWING = 2
EXTINGUISH = 3
COMPLETE = 4


class Robot:
    def __init__(self):
        # PrimeHub
        self.hub = PrimeHub()

        # Motors
        self.left_motor = Motor(Port.F, Direction.COUNTERCLOCKWISE)
        self.right_motor = Motor(Port.D, Direction.CLOCKWISE)
        self.fan_motor = Motor(Port.B)

        # Sensors
        self.color_sensor = ColorSensor(Port.C)
        self.force_sensor = ForceSensor(Port.E)
        self.side_sensor = UltrasonicSensor(Port.A)

        # Drive Bases
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
        if self.force_sensor.touched():
            self.drive_base.stop()
            return True
        return False

    def detect_wall_on_right(self):
        """Detect wall or opening on the right side for wall following."""
        return self.side_sensor.distance() < constants.WALL_FOLLOW_DISTANCE

    def detect_goal(self):
        """Detect if the robot is on the goal tile (Red)."""
        return self.color_sensor.color() == constants.GOAL_COLOR

    def wander(self):
        """Drive forward until an obstacle is hit, then switch to wall-following."""
        if self.detect_obstacle():
            self.drive_base.straight(-constants.WALL_FOLLOW_STEP)
            self.drive_base.turn(-90)
            self.transition_to(WALL_FOLLOWING)
        else:
            self.drive_base.drive(125, 0)

    def wall_following(self):
        """Wall-following behavior with smoother adjustments, prioritizing right-side corrections."""
        if self.detect_obstacle():
            # When ForceSensor detects contact, back up and make a minimal right turn to stay close to the wall
            self.drive_base.straight(-30)
            angle_adjustment = -constants.OBSTACLE_TURN_ANGLE  # Small left turn to avoid spinning
            self.drive_base.turn(angle_adjustment)

        elif not self.detect_wall_on_right():
            # If no wall is detected on the right, make a gradual right turn to search for the wall
            self.drive_base.turn(-constants.WALL_FOLLOW_ADJUST_ANGLE)
        else:
            # For consistent wall-following, calculate a gentle left adjustment based on distance error
            distance_error = constants.WALL_FOLLOW_DISTANCE - self.side_sensor.distance()
            angle_adjustment = max(min(distance_error * constants.WALL_FOLLOW_ADJUST_ANGLE, constants.MAX_ANGLE_ADJUST), constants.MIN_ANGLE_ADJUST)
            self.drive_base.drive(125, angle_adjustment)



    def extinguish(self):
        """Activate fan and cool down after extinguishing fire."""
        print("Extinguishing fire...")
        self.fan_motor.run_time(constants.FAN_SPEED, constants.FAN_RUN_TIME)
        self.transition_to(WANDER)
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
            self.wander()
            if self.detect_goal():
                self.transition_to(EXTINGUISH)

        elif self.current_state == WALL_FOLLOWING:
            self.wall_following()
            if self.detect_goal():
                self.transition_to(EXTINGUISH)

        elif self.current_state == EXTINGUISH:
            self.raise_alarm()
            self.extinguish()