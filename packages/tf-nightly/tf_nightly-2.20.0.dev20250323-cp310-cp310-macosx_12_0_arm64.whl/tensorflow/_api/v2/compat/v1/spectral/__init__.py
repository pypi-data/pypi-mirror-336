# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.spectral namespace
"""

import sys as _sys

from tensorflow.python.ops.gen_spectral_ops import fft # line: 353
from tensorflow.python.ops.gen_spectral_ops import fft2d # line: 442
from tensorflow.python.ops.gen_spectral_ops import fft3d # line: 531
from tensorflow.python.ops.gen_spectral_ops import ifft # line: 724
from tensorflow.python.ops.gen_spectral_ops import ifft2d # line: 813
from tensorflow.python.ops.gen_spectral_ops import ifft3d # line: 902
from tensorflow.python.ops.signal.dct_ops import dct # line: 50
from tensorflow.python.ops.signal.dct_ops import idct # line: 212
from tensorflow.python.ops.signal.fft_ops import irfft # line: 411
from tensorflow.python.ops.signal.fft_ops import irfft2d # line: 417
from tensorflow.python.ops.signal.fft_ops import irfft3d # line: 423
from tensorflow.python.ops.signal.fft_ops import rfft # line: 408
from tensorflow.python.ops.signal.fft_ops import rfft2d # line: 414
from tensorflow.python.ops.signal.fft_ops import rfft3d # line: 420

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "spectral", public_apis=None, deprecation=False,
      has_lite=False)
