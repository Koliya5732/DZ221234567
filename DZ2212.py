from typing import Protocol, runtime_checkable
import random
import urllib.request
import json



@runtime_checkable
class TemperatureSensor(Protocol):

    def read_temperature(self) -> float:
        ...

    def get_sensor_id(self) -> str:
        ...



class WeatherAPISensor:

    def read_temperature(self) -> float:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=46.48&longitude=30.73"
            "&current=temperature_2m"
        )

        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))

            return float(data["current"]["temperature_2m"])

        except Exception as error:
            raise RuntimeError(
                f"Не удалось получить погоду: {error}"
            )

    def get_sensor_id(self) -> str:
        return "WAS26-Odesa"



class SimulatedSensor:

    def __init__(self, base: float, deviation: float):
        self.base = base
        self.deviation = deviation

    def read_temperature(self) -> float:
        return self.base + random.uniform(
            -self.deviation, self.deviation
        )

    def get_sensor_id(self) -> str:
        return "SIM-001"



class FakeAlways25:

    def read_temperature(self) -> float:
        return 25.0

    def get_sensor_id(self) -> str:
        return "Fake-25"



class BrokenSensor:

    def read_temperature(self) -> float:
        raise RuntimeError("Датчик зламаний!")

    def get_sensor_id(self) -> str:
        return "BROKEN-999"



class RealDHT22:

    def read_temperature(self) -> float:
        return 22.5

    def get_sensor_id(self) -> str:
        return "DHT22-001"



def monitor_room(sensors: list[TemperatureSensor]) -> None:

    for sensor in sensors:
        sensor_id = sensor.get_sensor_id()

        try:
            temperature = sensor.read_temperature()

            print(
                f"[{sensor_id}] "
                f"Температура: {temperature:.1f} °C"
            )

        except Exception as error:
            print(f"[{sensor_id}] ПОМИЛКА: {error}")



def main():

    sensors = [
        WeatherAPISensor(),
        SimulatedSensor(base=21.5, deviation=3.0),
        FakeAlways25(),
        BrokenSensor()
    ]



    monitor_room(sensors)



    print(
        isinstance(RealDHT22(), TemperatureSensor)
    )  

    print(
        isinstance({"temp": 22}, TemperatureSensor)
    )  


if __name__ == "__main__":
    main()
