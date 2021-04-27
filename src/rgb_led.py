from machine import Pin, PWM

RED_LED_PIN_NUM = 13
GRE_LED_PIN_NUM = 14
BLU_LED_PIN_NUM = 12

PWM_FREQ = 20000

RED_LED_PWM = PWM(Pin(RED_LED_PIN_NUM, value=0), freq=PWM_FREQ, duty=0)
GRE_LED_PWM = PWM(Pin(GRE_LED_PIN_NUM, value=0), freq=PWM_FREQ, duty=0)
BLU_LED_PWM = PWM(Pin(BLU_LED_PIN_NUM, value=0), freq=PWM_FREQ, duty=0)


def set_rgb_led_off():
    """Turn off RGB LED"""

    RED_LED_PWM.duty(0)
    GRE_LED_PWM.duty(0)
    BLU_LED_PWM.duty(0)


def set_rgb_led(red, gre, blu):
    """Set values of Common Cathode RGB LED
    Takes values between 0 and 255.
    """

    red = red * 4
    blu = blu * 4
    gre = gre * 4

    for value in [red, gre, blu]:

        if value > 1023:
            value = 1023
        
        if value < 0:
            value = 0

    RED_LED_PWM.duty(red)
    GRE_LED_PWM.duty(gre)
    BLU_LED_PWM.duty(blu)


async def rgb_led_test():

    try:
        import uasyncio
    except ImportError:
        import asyncio as uasyncio

    while(1):
        set_rgb_led(255, 0, 0)
        await uasyncio.sleep(1)

        set_rgb_led(0, 255, 0)
        await uasyncio.sleep(1)

        set_rgb_led(0, 0, 255)
        await uasyncio.sleep(1)

        set_rgb_led(255, 191, 0)
        await uasyncio.sleep(1)