import uasyncio

import utime

# @timed_function
# Print time taken by a function call

def timed_function(f, *args, **kwargs):
    def new_func(*args, **kwargs):
        t = utime.ticks_us()
        result = f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t) 
        print('{:6.3f}'.format(delta/5), end=" ")
        return result
    return new_func


def timed_function_print(f, *args, **kwargs):
    def new_func(*args, **kwargs):
        t = utime.ticks_us()
        result = f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t) 
        print('Function {} is {:6.3f}ms'.format(f.__name__, delta/1000))
        return result
    return new_func


async def waveform_generation_test():
    from test_samples import test_samples

    while True:
        for idx, sample in enumerate(test_samples):
            print(sample, idx)
            await uasyncio.sleep(0.001)

try:
    from ulab import scipy as spy
except ImportError:
    import scipy as spy

@timed_function
def run_fft(samples, hamming_window):
    #samples = samples * hamming_window
    return spy.signal.spectrogram(samples)

from machine import ADC, Pin
adc_pin = ADC(Pin(32))

@timed_function_print
def adc_read():
    blob = adc_pin.read()


async def fft_test():

    from test_samples import test_samples
    from hamming_window import hamming_window

    # Index of array 
    arr_idx = 0

    # Number of samples
    N = const(128)

    # Clear serial plotter
    print(b'\x0c'[0])

    # Setup a legend on arduino plotter
    print("FFT_time Sample Array_Index Magnitude_200Hz Magnitude_400Hz")

    adc_read()

    while True:

        # Get a new set of samples of length N to test
        samples = test_samples[arr_idx:arr_idx+N:1]

        # Apply a hamming window to the samples
        #samples = samples * hamming_window

        # Get the frequency spectrum of the samples
        # spectrum = spy.signal.spectrogram(samples)
        spectrum = run_fft(samples, hamming_window)

        # Get the values of the bins for 200 Hz and 400 Hz
        mag_200 = spectrum[50]
        mag_400 = spectrum[101]

        # Print the results
        print(samples[-1]*10, arr_idx, mag_200, mag_400)

        # Update the array index within the bounds of the test_samples array
        arr_idx += 1

        if arr_idx > len(test_samples):
            arr_idx = 0
        
        await uasyncio.sleep(0.01)
