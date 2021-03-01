import uasyncio

async def waveform_generation_test():
    from test_samples import test_samples

    while True:
        for idx, sample in enumerate(test_samples):
            print(sample, idx)
            await uasyncio.sleep(0.001)
