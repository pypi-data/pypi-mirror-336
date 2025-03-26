# edgetpu-compiler-log-parser

Parse the result of edgetpu_compiler!

## Build (Optional)

```sh
python -m build
```

## Install

```sh
python3 -m pip install -e .
```

## example

```python
# tests/example.py
from pprint import pprint

import subprocess
from edgetpu_compiler_log_parser import EdgeTPUCompilerLogParser

model_path_1 = "tests/model/efficientnet-edgetpu-M_quant.tflite"
model_path_2 = "tests/model/efficientnet-edgetpu-S_quant.tflite"

if __name__ == "__main__":
    cmd = "edgetpu_compiler "
    cmd += model_path_1 + " "
    cmd += model_path_2 + " "

    output = subprocess.check_output(cmd, shell=True)

    log_parser = EdgeTPUCompilerLogParser(output)
    pprint(log_parser.get_compile_infos())
```

```sh
python3 tests/example.py
```

```json
{
  "compile_time": "2037ms",
  "compiled_info": [
    {
      "input_model": "tests/model/efficientnet-edgetpu-M_quant.tflite",
      "input_size": 7639.04,
      "num_of_edge_tpu_subgraphs": 1,
      "off_chip_memory_used": 4259.84,
      "on_chip_memory_remaining": 0.0,
      "on_chip_memory_used": 4311.04,
      "operation_log": "efficientnet-edgetpu-M_quant_edgetpu.log",
      "output_model": "efficientnet-edgetpu-M_quant_edgetpu.tflite",
      "output_size": 8847.36,
      "total_num_of_operations": 86
    },
    {
      "input_model": "tests/model/efficientnet-edgetpu-S_quant.tflite",
      "input_size": 6000.64,
      "num_of_edge_tpu_subgraphs": 1,
      "off_chip_memory_used": 3450.88,
      "on_chip_memory_remaining": 0.0,
      "on_chip_memory_used": 3276.8,
      "operation_log": "efficientnet-edgetpu-S_quant_edgetpu.log",
      "output_model": "efficientnet-edgetpu-S_quant_edgetpu.tflite",
      "output_size": 6952.96,
      "total_num_of_operations": 66
    }
  ],
  "compiler_version": "16.0.384591198"
}
```
