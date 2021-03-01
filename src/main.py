import machine, uasyncio

async def heartbeat():
    """Flash the onboard LED in a heartbeat to show the event loop is running"""

    from machine import Pin

    status_led = Pin(2, Pin.OUT)

    while True:
        status_led.on()
        await uasyncio.sleep(0.05)
        status_led.off()
        await uasyncio.sleep(0.1)
        
        status_led.on()
        await uasyncio.sleep(0.05)
        status_led.off()
        await uasyncio.sleep(0.8)
        


def main():
    from frequency_detection import waveform_generation_test

    # Set up event loop
    loop = uasyncio.get_event_loop()

    loop.create_task(heartbeat())
    loop.create_task(waveform_generation_test())
    loop.run_forever()


if __name__ == "__main__":
    main()