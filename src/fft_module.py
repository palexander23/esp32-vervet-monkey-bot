try:
    from ulab import numpy as np
    from ulab import scipy as spy

except ImportError:
    import numpy as np
    import scipy as spy

from hamming_window import hamming_window

from fft_data import note_names, fft_blocks_mask


class FFTModule:
    def __init__(
        self, 
        _sample_rec_func, 
        _output_dict: dict,
        _completed_event,
        _hamming=False
    ):

        self.sample_rec_func = _sample_rec_func
        """A function that can be called to get a list of the most recent samples"""

        self.output_dict = _output_dict
        """The dict where the FFT results are placed alongside note names"""

        self.completed_event = _completed_event
        """An async event called when a new calculation is complete"""

        self.hamming = _hamming
        """Tells the module whether or not to apply the hamming window"""


    def calculate_fft(self):
        """Called by an external function, pulls in new samples and places FFT 
        results in the output dict.
        """

        # Get latest samples
        sample_arr = self.sample_rec_func()

        # Apply a hamming window to the samples if asked
        if self.hamming:
            sample_arr = sample_arr * hamming_window

        # Get the frequency spectrum of the samples
        spectrum = spy.signal.spectrogram(sample_arr)

        # Extract the bins corresponding to note frequencies from the samples
        note_amplitudes: ndarray = spectrum[fft_blocks_mask == 1]

        self.output_dict.update(dict(zip(note_names, note_amplitudes)))

        self.completed_event.set()
        