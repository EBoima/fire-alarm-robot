from pybricks.parameters import Color

# General robot movement
WHEEL_DIAMETER = 56            # in mm, adjust to your robot's wheel diameter
AXLE_TRACK = 114               # in mm, distance between wheels
GRID_SIZE = 305                # in mm, if relevant for specific grid-based navigation

# Wandering behavior
WANDER_TURN_ANGLE = 90         # angle to turn randomly during wandering, in degrees

# Wall-following behavior
WALL_DETECT_THRESHOLD = 100    # distance threshold for detecting a wall, in mm
WALL_FOLLOW_DISTANCE = 150  # minimum distance from wall, in mm
WALL_FOLLOW_MAX_DISTANCE = 250  # maximum distance from wall, in mm
WALL_FOLLOW_ADJUST_ANGLE = 30  # angle adjustment when following wall, in degrees
# step size to move forward while following wall, in mm
WALL_FOLLOW_STEP = 125

# Fire detection
FIRE_AREA_COLOR = Color.RED    # color of the paper below the candle
ALARM_FREQUENCY = 2000         # alarm beep frequency in Hz
ALARM_DURATION = 500           # alarm duration in ms

# Extinguish behavior
FAN_SPEED = 1000               # speed of fan motor to extinguish the fire
FAN_RUN_TIME = 3000            # time to run the fan, in ms

# Cooldown or delay after extinguishing fire
# in ms, optional cooldown time after extinguishing
COOLDOWN_AFTER_EXTINGUISH = 5000

# Backup movement when touch sensor is triggered
# distance to back up when the touch sensor is pressed, in mm
BACKUP_DISTANCE = 70

# Flame detection threshold
# light intensity threshold for detecting the flame direction
FLAME_DETECTION_THRESHOLD = 50

# Wall-following distance and turn angle
# target distance to maintain from the wall in wall-following, in mm
WALL_FOLLOW_DISTANCE = 100
# angle to turn while adjusting distance from the wall, in degrees
WALL_FOLLOW_TURN_ANGLE = 30
MIN_ANGLE_ADJUST = 30
MAX_ANGLE_ADJUST = 45

# Approach Flame
APPROACH_FLAME_STEP_DISTANCE = 50  # step size to move toward the flame, in mm

# Goal Detection (Red Color Threshold)
# Color constant for detecting the goal area (red area under flame)
GOAL_COLOR = FIRE_AREA_COLOR

# Obstacle Detection (Ultrasonic Sensor)
OBSTACLE_TURN_ANGLE = 90  # angle to turn when an obstacle is detected, in degrees