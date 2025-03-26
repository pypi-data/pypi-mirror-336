from typing import Union
import re


SINGLE_LOG_LINE_NUM = 11


def get_KiB_size(line):
    pat = re.compile(r"\D+(\d+[.]\d+)(\D+)")
    mat = pat.search(line)
    size = float(mat.group(1))
    unit = mat.group(2)

    if unit == "MiB":
        size *= 1024
    elif unit == "B":
        size /= 1024
    elif unit == "KiB":
        pass
    else:
        raise RuntimeError("unknown byte unit")
    return size


class EdgeTPUCompilerLogParser:
    def __init__(self, log: Union[str, bytes]):
        self.log = log
        self.log_lines = None

        self.compiler_version = None
        self.compile_time = None
        self.compile_infos = {
            "compiler_version": self.compiler_version,
            "compile_time": self.compile_time,
            "compiled_infos": [],
            "executable_space": 0,
        }
        self.parse_log()
        self.calculate_executable_space()

    def get_compiled_infos(self):
        return self.compile_infos["compiled_infos"]

    def parse_log(self):
        self.decode_log()
        self.log_lines = self.log.splitlines()

        self.parse_compiler_version()
        self.parse_compile_time()

        starts = self.find_starts()
        self.parse_log_lines(starts)

    def decode_log(self):
        if isinstance(self.log, bytes):
            self.log: str = self.log.decode("utf-8")

    def parse_compiler_version(self):
        self.compiler_version = self.log_lines[0][26:]
        self.compile_infos["compiler_version"] = self.compiler_version

    def parse_compile_time(self):
        self.compile_time = self.log_lines[3][32:-4] + "ms"
        self.compile_infos["compile_time"] = self.compile_time

    def find_starts(self):
        starts = []
        for i, line in enumerate(self.log_lines):
            if line.startswith("Input model: "):
                starts.append(i)
        return starts

    def parse_log_lines(self, starts):
        for start in starts:
            compile_info = self.parse_log_line(start)
            self.add_compile_info(compile_info)

    def parse_log_line(self, start):
        compile_info = {}
        for line in self.log_lines[start : start + SINGLE_LOG_LINE_NUM]:
            if line.startswith("Input model: "):
                compile_info["input_model"] = line[13:]
            elif line.startswith("Input size: "):
                compile_info["input_size"] = get_KiB_size(line)
            elif line.startswith("Output model: "):
                compile_info["output_model"] = line[14:]
            elif line.startswith("Output size: "):
                compile_info["output_size"] = get_KiB_size(line)
            elif line.startswith("On-chip memory used for caching model parameters: "):
                compile_info["on_chip_memory_used"] = get_KiB_size(line)
            elif line.startswith("On-chip memory remaining for caching model parameters: "):
                compile_info["on_chip_memory_remaining"] = get_KiB_size(line)
            elif line.startswith("Off-chip memory used for streaming uncached model parameters: "):
                compile_info["off_chip_memory_used"] = get_KiB_size(line)
            elif line.startswith("Number of Edge TPU subgraphs: "):
                compile_info["num_of_edge_tpu_subgraphs"] = int(line[30:])
            elif line.startswith("Total number of operations: "):
                compile_info["total_num_of_operations"] = int(line[28:])
            elif line.startswith("Operation log: "):
                compile_info["operation_log"] = line[15:]

        return compile_info

    def add_compile_info(self, compile_info):
        self.compile_infos["compiled_infos"].append(compile_info)

    def calculate_executable_space(self):
        total_on_chip_memory_used = 0
        last_on_chip_memory_remaining = 0
        for i, compile_info in enumerate(self.compile_infos["compiled_infos"]):
            total_on_chip_memory_used += compile_info["on_chip_memory_used"]
            if i == len(self.compile_infos["compiled_infos"]) - 1:
                last_on_chip_memory_remaining = compile_info["on_chip_memory_remaining"]
        self.compile_infos["executable_space"] = round(
            8192 - (last_on_chip_memory_remaining + total_on_chip_memory_used), 2
        )

    def get_executable_space(self):
        return self.compile_infos["executable_space"]
