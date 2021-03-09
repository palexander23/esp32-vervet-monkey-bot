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
    from sample_retrieval import initialize_sample_retrieval

    try:
        machine.freq(240000000)

        # Set up sample retrieval
        initialize_sample_retrieval()

        # Set up event loop
        loop = uasyncio.get_event_loop()

        # Load tasks onto event loop
        loop.create_task(heartbeat())

        # Start Event loop
        # THIS FUNCTION SHOULD NEVER RETURN
        loop.run_forever()

    except KeyboardInterrupt:
        print("")
        print("Keyboard Interrupt")
        print("")

    except Exception as e:
        print("")
        print(e)
        print("")

    finally:
        # Stop the sample timer
        from machine import Timer
        sample_timer = Timer(0)
        sample_timer.deinit()
        
        # Stop the event loop if it has been defined
        if "loop" in locals():
            loop.stop() 


if __name__ == "__main__":
    main()