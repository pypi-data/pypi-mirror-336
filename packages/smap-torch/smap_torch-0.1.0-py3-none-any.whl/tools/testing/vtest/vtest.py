# A tool for visual testing gradient flows. 
import unittest, vtest_types
import importlib.util
import torch

class OutputHook:
    def __init__(self, is_forward=True):
        self.is_forward = is_forward
        self.outputs = []
        
        # static self.order
        
    def __call__(self, module, module_in, module_out):
        if self.is_forward==False:
            torch.save(module_in, f"module_in_{self.order}.pt")
        else:
            module = torch.load(f"module_in_{self.order}.pt")
        self.outputs.append((module.depth, module_out))
        
        
    def clear(self):
        self.outputs = []

# Define the module path
module_path = "../smap/smap.py"

# the test case
class SMapTestCase(unittest.TestCase):
    def setUp(self):
        self.smap = SMap3X3()
        self.smap.unit_test_service = vtest_types.WeightOut()
        hook = OutputHook(is_forward=True)
        for layer in smap.modules():
        if isinstance(layer, vtest_types.WeightOut):
            handle = layer.register_forward_hook(hook)
            hook_handles.append(handle)

    def test_plot_title(self):
        test_input = torch.zeros(5,5)
        test_input[3,3] = 1
        actual = self.ax.get_title()
        expected = "Rise in Sea Level"
        self.assertEqual(actual, expected, "Expected line plot title to be 'Rise in Sea Level'")


def main():
    # Load the module using importlib.util
    spec = importlib.util.spec_from_file_location("smap", module_path)
    smap_module = importlib.util.module_from_spec(spec)
    sys.modules["smap"] = smap_module
    spec.loader.exec_module(smap_module)
    
    unittest.main()

if __name__ == "__main__":
    main()