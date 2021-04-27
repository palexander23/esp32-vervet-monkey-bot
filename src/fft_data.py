
try:
    from ulab import numpy as np
except ImportError:
    import numpy as np

"""The number of samples/frequency bins used in the FFT"""
N = 128

"""The sampling frequency in Hz"""
Fs = 1000

"""Note Names"""
note_names = [
    "C3",
    "Csh3",
    "D3",
    "Dsh3",
    "E3",
    "F3",
    "Fsh3",
    "G3",
    "Gsh3",
    "A3",
    "Ash3",
    "B3",
    "C4",
    "Csh4",
    "D4",
    "Dsh4",
    "E4",
    "F4",
    "Fsh4",
    "G4",
    "Gsh4",
    "A4",
    "Ash4",
    "B4",
]

"""The frequencies for notes C3 to B4"""
note_frequency_array = np.array([
    130.81,
    138.59,
	146.83,
    155.56,
    164.81,
    174.61,
    185.00,
    196.00,
    207.65,
    220.00,
    233.08,
    246.94,
    261.63,
    277.18,
    293.66,
    311.13,
    329.63,
    349.23,
    369.99,
    392.00,
    415.30,
    440.00,
    466.16,
    493.88,
], dtype=np.float)

"""The blocks of the FFT corresponding to the notes C3 - B4"""
note_fft_blocks = np.array(np.around(note_frequency_array*((N/Fs)) - 1), dtype=np.int16)

"""Define a binary mask to select which bins correspond to useful frequencies"""
fft_blocks_mask = np.zeros(N, dtype=np.uint8)

# Testing showed that the mask needed to be sensitive to the bin above the id calculated
# in note_fft_blocks
for idx in note_fft_blocks:
    fft_blocks_mask[idx + 1] = 1


if __name__ == "__main__":
    print("FFT Blocks:\n", note_fft_blocks)
    print("FFT Block Mask:\n", fft_blocks_mask)
    
    print(dict(zip(note_names, [0] * len(note_names))))