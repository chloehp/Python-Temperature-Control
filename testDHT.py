from time import sleep
from datetime import datetime
import board
import adafruit_dht
sensor = adafruit_dht.DHT11(board.D4)

print("Python Temperature Control setup and DHT sensor test")
print(f"""{"Temperature":15}{"Humidity":15}Time""")

while True:
    t = str(sensor.temperature)
    h = str(sensor.humidity)
    print(f"""{t + "°C":15}{h + "%":15}{datetime.now()}""")
    sleep(3)
