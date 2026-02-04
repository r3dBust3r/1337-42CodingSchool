from typing import Any, List, Dict, Union
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    def format_output(self, result: str) -> str:
        return result


class NumericProcessor(DataProcessor):
    def validate(self, data: List[int]) -> bool:
        try:
            for n in data:
                int(n)
            return True
        except (ValueError, TypeError):
            return False

    def process(self, data: List[int]) -> str:
        if (self.validate(data)):
            total: int = 0
            count: int = 0
            for n in data:
                count += 1
                total += n
            result: str = f"Processed {count} numeric "
            result += f"values, sum={total}, avg={total/count}"
            return self.format_output(result)
        else:
            return self.format_output("Invalid data")

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class TextProcessor(DataProcessor):
    def validate(self, data: str) -> bool:
        if (data.strip() == ""):
            return False
        return True

    def count_letters(self, data: str) -> int:
        lc: int = 0
        for _ in data:
            lc += 1
        return lc

    def count_words(self, data: str) -> int:
        wc: int = 0
        in_word: bool = False
        for c in data:
            if c != " " and not in_word:
                wc += 1
                in_word = True
            elif c == " ":
                in_word = False
        return wc

    def process(self, data: str) -> str:
        if (self.validate(data)):
            result: str = f"Processed text: {self.count_letters(data)} "
            result += f"characters, {self.count_words(data)} words"
            return self.format_output(result)
        else:
            return self.format_output("Invalid text data")

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class LogProcessor(DataProcessor):
    def validate(self, data: str) -> bool:
        if (data.strip() == ""):
            return False
        level: str = ""
        for c in data:
            if (c == ":"):
                break
            level += c
        if (level not in ["INFO", "WARNING", "ERROR"]):
            return False
        return True

    def process(self, data: str) -> str:
        if (self.validate(data)):
            level: str = ""
            msg: str = ""
            extracting_lvl: bool = True
            for c in data:
                if (extracting_lvl):
                    if (c == ":"):
                        extracting_lvl = False
                        continue
                    level += c
                else:
                    msg += c
            kind: str = ""
            if (level in ["WARNING", "ERROR"]):
                kind = "ALERT"
            else:
                kind = "INFO"
            result = f"[{kind}] {level} level detected:{msg}"
            return self.format_output(result)
        else:
            return self.format_output("Invalid log")

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")
print("Initializing Numeric Processor...")
numproc: NumericProcessor = NumericProcessor()
data: List[int] = [1, 2, 3, 4, 5]
print(f"Processing data: {data}")
result: str = numproc.process(data)
print("Validation: Numeric data verified")
print(result)

print()
print("Initializing Text Processor...")
txtproc: TextProcessor = TextProcessor()
data: str = "Hello Nexus World"
print(f"Processing data: \"{data}\"")
result: str = txtproc.process(data)
print("Validation: Text data verified")
print(result)

print()
print("Initializing Log Processor...")
logproc: LogProcessor = LogProcessor()
data: str = "ERROR: Connection timeout"
print(f"Processing data: \"{data}\"")
result: str = logproc.process(data)
print("Validation: Log entry verified")
print(result)

print()
print("=== Polymorphic Processing Demo ===")
print("Processing multiple data types through same interface...")
processors: Dict[
        Union
        [
            NumericProcessor,
            TextProcessor,
            LogProcessor
        ],
        Union
        [
            List[int],
            str
        ]
    ] = {
    NumericProcessor(): [1, 2, 3],
    TextProcessor(): "Hello World!",
    LogProcessor(): "INFO: System ready"
}
i: int = 1
for processor, data in processors.items():
    result = processor.process(data)
    print(f"Result {i}: {result}")
    i += 1

print("\nFoundation systems online. Nexus ready for advanced streams.")
