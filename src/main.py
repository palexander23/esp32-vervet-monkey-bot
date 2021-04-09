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
    from motor_control import motor_driver_test

    from frequency_detection import fft_module_test,
    from frequency_detection import left_fft_complete_event, right_fft_complete_event
    from frequency_detection import left_fft_outputs, right_fft_outputs
    from frequency_detection import fft_task, fft_trigger_event

    try:
        machine.freq(240000000)

        # Set up sample retrieval
        initialize_sample_retrieval()
        print("I2C initialised")

        # Set up event loop
        loop = uasyncio.get_event_loop()

        # Start Anti-aliasing filters
        lpf_clk = machine.Pin(15)
        lpf_clk_pwm = machine.PWM(lpf_clk, freq=50000, duty=512)

        # Load tasks onto event loop
        loop.create_task(heartbeat())
        loop.create_task(motor_driver_test())
        loop.create_task(fft_task(fft_trigger_event))
        loop.create_task(fft_module_test(left_fft_complete_event, left_fft_outputs))

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