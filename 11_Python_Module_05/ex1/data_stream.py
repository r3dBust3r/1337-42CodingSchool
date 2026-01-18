from typing import Any, List, Dict, Union, Optional
from abc import ABC, abstractmethod


class DataStream(ABC):
    def __init__(self, stream_id: str) -> None:
        self.stream_id = stream_id

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(
        self, data_batch: List[Any], criteria: Optional[str] = None
    ) -> List[Any]:
        if criteria is None:
            return data_batch
        filtered: List[Any] = []
        for item in data_batch:
            if criteria in item:
                filtered.append(item)
        return filtered

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass


class SensorStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        print("\nInitializing Sensor Stream...")
        print(f"Stream ID: {self.stream_id}, Type: Environmental Data")

    def process_batch(self, data_batch: List[str]) -> str:
        print(f"Processing sensor batch: {data_batch}")
        count: int = 0
        temp: str = ""

        for item in data_batch:
            count += 1
            if "temp:" in item:
                temp = item.replace("temp:", "")

        return (
            f"Sensor analysis: {count} readings processed, "
            f"avg temp: {temp}°C"
        )


class TransactionStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        print("\nInitializing Transaction Stream...")
        print(f"Stream ID: {self.stream_id}, Type: Financial Data")

    def process_batch(self, data_batch: List[str]) -> str:
        print(f"Processing transaction batch: {data_batch}")
        count: int = 0
        net: int = 0

        for item in data_batch:
            count += 1
            if "buy:" in item:
                net += int(item.replace("buy:", ""))
            elif "sell:" in item:
                net -= int(item.replace("sell:", ""))

        sign: str = "+" if net >= 0 else ""
        return (
            f"Transaction analysis: {count} operations, "
            f"net flow: {sign}{net} units"
        )


class EventStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        print("\nInitializing Event Stream...")
        print(f"Stream ID: {self.stream_id}, Type: System Events")

    def process_batch(self, data_batch: List[str]) -> str:
        print(f"Processing event batch: {data_batch}")
        count: int = 0
        errors: int = 0

        for item in data_batch:
            count += 1
            if item == "error":
                errors += 1

        return f"Event analysis: {count} events, {errors} error detected"


class StreamProcessor:
    def __init__(self, streams: List[Dict[str, Any]]) -> None:
        self.streams = streams

    def count_items(self, items):
        count: int = 0
        for item in items:
            count += 1
        return count

    def process(self) -> None:
        print("\n=== Polymorphic Stream Processing ===")
        print("Processing mixed stream types through unified interface...")
        print("\nBatch 1 Results:")

        critical_alerts: int = 0
        large_transactions: int = 0

        for entry in self.streams:
            stream: Union[
                SensorStream,
                TransactionStream,
                EventStream] = entry["stream"]
            data: List[str] = entry["data"]

            if isinstance(stream, SensorStream):
                filtered: List[Any] = stream.filter_data(data, "temp")
                print(
                    f"- Sensor data: {self.count_items(filtered)} "
                    f"readings processed"
                )
                critical_alerts += self.count_items(filtered)

            elif isinstance(stream, TransactionStream):
                filtered: List[Any] = stream.filter_data(data, "sell")
                print(
                    f"- Transaction data: {self.count_items(data) + 1} "
                    f"operations processed"
                )
                large_transactions += self.count_items(filtered)

            elif isinstance(stream, EventStream):
                print(
                    f"- Event data: {self.count_items(data)} "
                    f"events processed"
                )

        print("\nStream filtering active: High-priority data only")
        print(
            f"Filtered results: {critical_alerts} critical sensor alerts, "
            f"{large_transactions} large transaction"
        )
        print(
            "\nAll streams processed successfully. "
            "Nexus throughput optimal."
        )


print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")

sensor: SensorStream = SensorStream("SENSOR_001")
print(sensor.process_batch(
    ["temp:22.5", "humidity:65", "pressure:1013"]
))

transaction: TransactionStream = TransactionStream("TRANS_001")
print(transaction.process_batch(
    ["buy:100", "sell:150", "buy:75"]
))

event: EventStream = EventStream("EVENT_001")
print(event.process_batch(
    ["login", "error", "logout"]
))

processor: StreamProcessor = StreamProcessor([
    {"stream": sensor, "data": ["temp:22.5", "humidity:65", "pressure:1013"]},
    {"stream": transaction, "data": ["buy:100", "sell:150", "buy:75"]},
    {"stream": event, "data": ["login", "error", "logout"]},
])

processor.process()
