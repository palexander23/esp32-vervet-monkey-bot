try:
   from ulab import numpy as np
except ImportError:
   import numpy as np

test_samples = np.array([
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    325,
    443,
    522,
    532,
    767,
    776,
    372,
    293,
    569,
    511,
    182,
    586,
    665,
    389,
    767,
    633,
    515,
    436,
    426,
    511,
    182,
    586,
    665,
    389,
    767,
    633,
    515,
    436,
    426,
    511,
    182,
    586,
    665,
    389,
    767,
    633,
    515,
    436,
    426,
    511,
    182,
    586,
    665,
    389,
    767,
    633,
    515,
    436,
    426,
    511,
    182,
    586,
    665,
    389,
    767,
    633,
    515,
    436,
    426,
    511,
    182,
    586,
    665,
    389,
    767,
    633,
    515,
    436,
    426,
    511,
    182,
    586,
    665,
    389,
    767,
    633,
    515,
    436,
    426,
    511,
    182,
    586,
    665,
    389,
    767,
    633,
    515,
    436,
    426,
    511,
    182,
    586,
    665,
    389,
    767,
    633,
    515,
    436,
    426,
    511,
    182,
    586,
    665,
    389,
    767,
    633,
    515,
    436,
    426,
    511,
    182,
    586,
    665,
    389,
    767,
    633,
    515,
    436,
    426,
    511,
    182,
    586,
    665,
    389,
    767,
    633,
    515,
    436,
    426,
    511,
    182,
    586,
    665,
    389,
])