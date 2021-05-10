from machine import Pin, PWM

try:
    import uasyncio
except ImportError:
    import asyncio as uasyncio

# Pin Number definitions
LEFT_IN1_NUM = 16
LEFT_IN2_NUM = 17

RIGHT_IN1_NUM = 22
RIGHT_IN2_NUM = 4

# PWM Parameters
PWM_FREQ = 20000

# PWM object definitions
LEFT_IN1_PWM = PWM(Pin(LEFT_IN1_NUM, value=0), freq=PWM_FREQ, duty=0)
LEFT_IN2_PWM = PWM(Pin(LEFT_IN2_NUM, value=0), freq=PWM_FREQ, duty=0)

RIGHT_IN1_PWM = PWM(Pin(RIGHT_IN1_NUM, value=0), freq=PWM_FREQ, duty=0)
RIGHT_IN2_PWM = PWM(Pin(RIGHT_IN2_NUM, value=0), freq=PWM_FREQ, duty=0)

status_led = Pin(2, Pin.OUT)

# Definitions for Motor Speed
MAX_SPEED = 1023
SLOW_SPEED = int(0.75 * MAX_SPEED)
FAST_SPEED = int(0.90 * MAX_SPEED) 

# Flag to tell whether the robot is moving
robot_moving = False

def motor_standby():
    """Reset all motor inputs"""

    robot_moving = False

    LEFT_IN1_PWM.duty(0)
    RIGHT_IN1_PWM.duty(0)
    LEFT_IN2_PWM.duty(0)
    RIGHT_IN2_PWM.duty(0)


async def move_forwards(speed, duration):
    """Moves the robot forward for time given in duration"""
    global robot_moving

    robot_moving = True
        
    # Set motor inputs
    LEFT_IN1_PWM.duty(speed)
    RIGHT_IN1_PWM.duty(speed)

    # Give control of processor to another thread
    await uasyncio.sleep(duration)

    # Reset motor inputs
    motor_standby()


async def move_backwards(speed, duration):
    """Moves the robot backwards for time given in duration"""
    global robot_moving

    robot_moving = True
        
    # Set motor inputs
    LEFT_IN2_PWM.duty(speed)
    RIGHT_IN2_PWM.duty(speed)

    # Give control of processor to another thread
    await uasyncio.sleep(duration)

    # Reset motor inputs
    motor_standby()


async def turn_left(speed, duration):
    """Turns the robot to left for time given in duration"""
    global robot_moving

    robot_moving = True
        
    # Set motor inputs
    LEFT_IN2_PWM.duty(speed)
    RIGHT_IN1_PWM.duty(speed)

    # Give control of processor to another thread
    await uasyncio.sleep(duration)

    # Reset motor inputs
    motor_standby()


async def turn_right(speed, duration):
    """Turns the robot to right for time given in duration"""
    global robot_moving

    robot_moving = True
        
    # Set motor inputs
    LEFT_IN1_PWM.duty(speed)
    RIGHT_IN2_PWM.duty(speed)

    # Give control of processor to another thread
    await uasyncio.sleep(duration)

    # Reset motor inputs
    motor_standby()


async def motor_driver_test():

    await uasyncio.sleep(3)

    while(1):

        await move_forwards(SLOW_SPEED, 1)
        await move_backwards(SLOW_SPEED, 1)
        await turn_left(SLOW_SPEED, 1)
        await turn_right(SLOW_SPEED, 1)


async def random_movement_task(speed):
    import random

    try:
        from ulab import numpy as np

    except ImportError:
        import numpy as np

    movement_funcs = [move_forwards, move_backwards, turn_left, turn_right]

    move_duration_range = np.arange(0.5,2, 0.1)
    sleep_duration_range = range(3, 6)
    try:
        while 1:
            
            sleep_dur = random.choice(sleep_duration_range)

            # Decide whether to move or to sit still
            if random.random() < 0.5:
                sleep_dur = random.choice(sleep_duration_range)
                await uasyncio.sleep(sleep_dur)
                continue
            
            # Get a random movement and duration
            move_func = random.choice(movement_funcs)
            move_dur = random.choice(move_duration_range)

            # Do that movement
            await move_func(speed, move_dur)
            await uasyncio.sleep(sleep_dur)

    except uasyncio.CancelledError as e:
        motor_standby()