# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.data namespace
"""

import sys as _sys

from tensorflow._api.v2.compat.v1.data import experimental
from tensorflow.python.data.ops.dataset_ops import AUTOTUNE # line: 103
from tensorflow.python.data.ops.dataset_ops import DatasetV1 as Dataset # line: 3710
from tensorflow.python.data.ops.dataset_ops import DatasetSpec # line: 4594
from tensorflow.python.data.ops.dataset_ops import INFINITE as INFINITE_CARDINALITY # line: 113
from tensorflow.python.data.ops.dataset_ops import NumpyIterator # line: 4759
from tensorflow.python.data.ops.dataset_ops import UNKNOWN as UNKNOWN_CARDINALITY # line: 114
from tensorflow.python.data.ops.dataset_ops import get_legacy_output_classes as get_output_classes # line: 4442
from tensorflow.python.data.ops.dataset_ops import get_legacy_output_shapes as get_output_shapes # line: 4464
from tensorflow.python.data.ops.dataset_ops import get_legacy_output_types as get_output_types # line: 4486
from tensorflow.python.data.ops.dataset_ops import make_initializable_iterator # line: 4353
from tensorflow.python.data.ops.dataset_ops import make_one_shot_iterator # line: 4318
from tensorflow.python.data.ops.iterator_ops import Iterator # line: 95
from tensorflow.python.data.ops.options import Options # line: 579
from tensorflow.python.data.ops.options import ThreadingOptions # line: 535
from tensorflow.python.data.ops.readers import FixedLengthRecordDatasetV1 as FixedLengthRecordDataset # line: 669
from tensorflow.python.data.ops.readers import TFRecordDatasetV1 as TFRecordDataset # line: 490
from tensorflow.python.data.ops.readers import TextLineDatasetV1 as TextLineDataset # line: 260

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "data", public_apis=None, deprecation=False,
      has_lite=False)
