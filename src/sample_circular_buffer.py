try:
    from ulab import numpy as np
except ImportError:
    import numpy as np


class SampleCircularBuffer:
    def __init__(self, _N):

        self.N = _N
        """The number of elements in the circular array. Equal to the 
        number of samples used in the FFT.
        """

        self.circ_array = np.zeros(_N)
        """The circular array, implemented as a Numpy array"""

        self.temp_array = np.zeros(_N)
        """Temporary array used to declare memory used for producing intact array"""

        self.array_index = 0
        """The current index of the array, is incremented up N-1, then reset to 0"""


    def add_sample(self, sample: int):
        """Add a new sample to the circular array and increment the array index."""

        self.circ_array[self.array_index] = sample
        self.increment_index()


    def increment_index(self):
        """Increment the array index, wrap around to 0 if greater than N-1."""

        self.array_index += 1

        # Wrap around if greater than N-1
        if self.array_index >= self.N:
            self.array_index = 0

    
    def get_most_recent_sample(self):
        """Return the sample last entered into the array"""
        
        return self.circ_array[self.array_index - 1]


    def get_ordered_array(self):
        """Returns an array with the most recent sample first and oldest last.
        The array is divided down the middle by array_index.

        The elements from array_index+1 to N-1 are placed in the temporary array.
        The elements from 0 to array_index are placed after them, filling the remiander.
        The temporary array is returned.
        """
        idx = self.array_index
        N = self.N

        # Place the elements after array_index at the beginning of the temporary array
        self.temp_array[0:N-idx] = self.circ_array[idx:N]

        # Place elements before and including array_index into the rest of the array
        self.temp_array[N-idx:N] = self.circ_array[0:idx]

        return self.temp_array

    def get_unordered_array(self):
        """Returns the circular buffer as is without ordering the samples correctly
        Useful for implementing rolling averages where the order of the elements doesn't
        matter.
        """

        return self.circ_array.copy()


# Useful little test that run on hosted environment
if __name__ == "__main__":
    test_buff = SampleCircularBuffer(5)
    print(test_buff.get_ordered_array())

    test_buff.add_sample(1)
    print(test_buff.get_ordered_array())
    test_buff.add_sample(2)
    print(test_buff.get_ordered_array())
    test_buff.add_sample(3)
    print(test_buff.get_ordered_array())
    test_buff.add_sample(4)
    print(test_buff.get_ordered_array())
    test_buff.add_sample(5)
    print(test_buff.get_ordered_array())
    test_buff.add_sample(6)
    print(test_buff.get_ordered_array())



