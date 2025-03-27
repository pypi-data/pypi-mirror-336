from __future__ import annotations

import flatbuffers
import numpy as np

import flatbuffers
import typing

uoffset: typing.TypeAlias = flatbuffers.number_types.UOffsetTFlags.py_type

class Operator(object):
  _SOFTMAX: int
  _TO_COPY: int
  _UNSAFE_VIEW: int
  ADD_TENSOR: int
  ADDMM: int
  ARANGE: int
  ARANGE_START: int
  BMM: int
  CAT: int
  CLONE: int
  COS: int
  EMBEDDING: int
  EXPAND: int
  FULL: int
  GT_TENSOR: int
  LT_TENSOR: int
  MASKED_FILL_SCALAR: int
  MEAN_DIM: int
  MM: int
  MUL_SCALAR: int
  MUL_TENSOR: int
  NATIVE_LAYER_NORM: int
  NEG: int
  PERMUTE: int
  POW_TENSOR_SCALAR: int
  RSQRT: int
  SILU: int
  SIN: int
  SLICE_TENSOR: int
  SPLIT_TENSOR: int
  T: int
  TANH: int
  TRANSPOSE_INT: int
  TRIU: int
  UNSQUEEZE: int
  VIEW: int

