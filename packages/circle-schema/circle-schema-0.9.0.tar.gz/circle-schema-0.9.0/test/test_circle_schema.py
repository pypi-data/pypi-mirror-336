'''Test circle schema package'''

import unittest

import circle_schema  # type: ignore

import numpy as np
import flatbuffers  # type: ignore
from pathlib import Path
import shutil
import subprocess
import tempfile

_res_dir = Path(__file__).parent.resolve() / 'res'

_tflchef_file = Path('/usr/share/one/bin/tflchef-file')
_tflite2circle = Path('/usr/share/one/bin/tflite2circle')
_circle_interpreter = Path('/usr/share/one/bin/circle-interpreter')


class CircleInterpreter:
  '''Simple circle interpreter class for testing (Without sufficient validation)'''

  def __init__(self, circle_path, out_signature):
    self._circle_path = Path(circle_path)
    self._out_signature = out_signature  # TODO Get this from circle model

  def infer(self, *inputs):
    with tempfile.TemporaryDirectory() as d:
      input_prefix = str(Path(d) / 'input')
      output_prefix = str(Path(d) / 'output')

      for idx, inp in enumerate(inputs):
        inp.tofile(input_prefix + str(idx))

      subprocess.check_call([_circle_interpreter, self._circle_path, input_prefix, output_prefix])

      outputs = []
      for idx, (dtype, shape) in enumerate(self._out_signature):
        outputs.append(np.reshape(np.fromfile(output_prefix + str(idx), dtype=dtype), shape))

    if len(outputs) == 1:
      return outputs[0]
    else:
      return tuple(outputs)


class CircleTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):

    def _recipe2circle(workspace, recipe):
      recipe_path = Path(recipe)
      tflite_path = workspace / recipe.with_suffix('.tflite').name
      circle_path = workspace / recipe.with_suffix('.circle').name

      subprocess.check_call([_tflchef_file, recipe_path, tflite_path])
      subprocess.check_call([_tflite2circle, tflite_path, circle_path])

    cls.ws = Path(tempfile.mkdtemp(prefix='circle_schema_test_'))
    for recipe in _res_dir.glob('*.recipe'):
      _recipe2circle(cls.ws, recipe)

  @classmethod
  def tearDownClass(cls):
    shutil.rmtree(str(cls.ws))

  def test_submodule_exposed(self):
    # Q. What is this test for ?
    # A. It checks if circle_schema.circle.Model module is imported under circle_schema.circle.
    #    NOTE This is not the default feature from flatbuffers-compiler.
    self.assertTrue(hasattr(circle_schema.circle, 'Model'))
    self.assertFalse(hasattr(circle_schema.circle, 'circle_schema'))
    self.assertTrue(hasattr(circle_schema.circle.Model, 'Model'))
    self.assertTrue(hasattr(circle_schema.circle.Model.Model, 'GetRootAsModel'))
    self.assertTrue(hasattr(circle_schema.circle.Model, 'ModelStart'))
    self.assertTrue(hasattr(circle_schema.circle.Model, 'ModelT'))
    self.assertTrue(hasattr(circle_schema.circle.Model.ModelT, 'Pack'))

  def test_multiple_schemas(self):
    # Q. What is this test for ?
    # A. It checks if multiple modules with different schema versions are correctly exposed.
    #    NOTE Some of these are not the default feature from flatbuffers-compiler.
    for versioned_module_name in ['v0_4', 'v0_5', 'v0_6', 'v0_7', 'v0_8', 'v0_9']:

      self.assertTrue(hasattr(circle_schema, versioned_module_name))

      versioned_module = getattr(circle_schema, versioned_module_name)
      self.assertTrue(hasattr(versioned_module, 'circle'))

      circle_module = getattr(versioned_module, 'circle')
      self.assertTrue(hasattr(circle_module, 'Model'))

      circle_model_module = getattr(circle_module, 'Model')
      self.assertTrue(hasattr(circle_model_module, 'Model'))

      circle_model_class = getattr(circle_model_module, 'Model')
      self.assertTrue(hasattr(circle_model_class, 'GetRootAs'))

  def test_model_building_api_create_empty_circle(self):
    builder = flatbuffers.Builder()
    circle_schema.circle.Model.ModelStart(builder)
    orc = circle_schema.circle.Model.ModelEnd(builder)
    builder.Finish(orc, file_identifier=str.encode('CIR0'))

    self.assertIn('CIR0', builder.Output().decode())

  def test_if_buffer_is_synchronized(self):
    # Q) What is this test for?
    #
    # A) This test ensures that the `circle.Model.Model` directly access the user-given input buffer
    #    instead of accessing a new internal copy.
    #    See the below contents from https://google.github.io/flatbuffers for details.
    #
    #    > Why use FlatBuffers?
    #    >
    #    > "Memory efficiency and speed"
    #    >
    #    > The only memory needed to access your data is that of the buffer.
    #    > It requires 0 additional allocations (in C++, other languages may vary).
    #
    #    Note that it does not guarantee the characteristics for Python.
    #    Let's enable testing this feature!

    # Build a buffer
    builder = flatbuffers.Builder()
    circle_schema.circle.Model.ModelStart(builder)
    circle_schema.circle.Model.AddVersion(builder, 123)
    orc = circle_schema.circle.Model.ModelEnd(builder)
    builder.Finish(orc, file_identifier=str.encode('CIR0'))
    buf = builder.Output()

    # Create a valid model object from the buffer
    model = circle_schema.circle.Model.Model.GetRootAsModel(buf, 0)
    self.assertEqual(model.Version(), 123)

    # Update the buffer in-place
    for idx in range(len(buf)):
      buf[idx] = 255

    # `model` is now invalid because the flatbuffer does not maintain a separate buffer.
    with self.assertRaises(Exception):
      model.Version()

  def test_object_api_round_trip(self):

    def _rebuild_circle(*, orig_path, new_path):
      with open(orig_path, 'rb') as f:
        schema = circle_schema.circle.Model.Model.GetRootAsModel(f.read(), 0)
      model = circle_schema.circle.Model.ModelT.InitFromObj(schema)
      builder = flatbuffers.Builder()
      model_offset = model.Pack(builder)
      builder.Finish(model_offset, file_identifier=str.encode('CIR0'))
      with open(new_path, 'wb') as f:
        f.write(builder.Output())

    # Load the original circle to memory, then export it again to a new file with the object API.
    _rebuild_circle(orig_path=self.ws / 'Add_000.circle', new_path=self.ws / 'Add_000.v2.circle')

    # Prepare interpreter and sample inputs
    shape = (1, 4, 4, 3)
    interp = CircleInterpreter(self.ws / 'Add_000.v2.circle', [(np.float32, shape)])
    lhs = np.random.random_sample(shape).astype(np.float32)
    rhs = np.random.random_sample(shape).astype(np.float32)

    # Test if the reconstructed circle is still valid
    self.assertTrue(np.allclose(interp.infer(lhs, rhs), lhs + rhs))


if __name__ == '__main__':
  unittest.main()
