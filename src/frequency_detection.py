import uasyncio

async def waveform_generation_test():
    from test_samples import test_samples

    while True:
        for idx, sample in enumerate(test_samples):
            print(sample, idx)
            await uasyncio.sleep(0.001)


async def fft_test():
    try:
        from ulab import scipy as spy
    except ImportError:
        import scipy as spy

    from test_samples import test_samples
    from hamming_window import hamming_window

    # Index of array 
    arr_idx = 0

    # Number of samples
    N = 64

    # Clear serial plotter
    print(b'\x0c'[0])

    # Setup a legend on arduino plotter
    print("Sample Array_Index Magnitude_200Hz Magnitude_400Hz")

    while True:

        # Get a new set of samples of length N to test
        samples = test_samples[arr_idx:arr_idx+N:1]

        # Apply a hamming window to the samples
        samples = samples * hamming_window

        # Get the frequency spectrum of the samples
        spectrum = spy.signal.spectrogram(samples)

        # Get the values of the bins for 200 Hz and 400 Hz
        mag_200 = spectrum[12]
        mag_400 = spectrum[25]

        # Print the results
        print(samples[-1], arr_idx, mag_200, mag_400)

        # Update the array index within the bounds of the test_samples array
        arr_idx += 1

        if arr_idx > len(test_samples):
            arr_idx = 0
        
        await uasyncio.sleep(0.01)
