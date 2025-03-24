import time
import random
import RPi.GPIO as GPIO
import Adafruit_DHT
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from gpiozero import servo

# Pin Setup
Waterlevel_Pin =18 #waterlevel sensor, need to convert to analogue 
Light_Pin = 17 #replay for lights
Feeding_Pin = 27 #servomotor for fish food

#Analog to digital converter for PH sensor
i2c = busio.I2C(board.SCL, board.SDA)
ads= ADS.ADS1115(i2c)
ph_sensor = AnalogIn(ads,ADS.P0)

#getting the Temp sensors setup
DHT_SENSOR = ADAfruit_DHT.DHT22
DHT_PIN = 4 

#settingup feeding servo
feeding_servo = Servo(FEEDER_PIN)

#function to read water temp
def water_temp():
humidity, temperature, = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
if temperature is not None:
return round(temperature,1) # rounding the temp to whole number in Celcius
else:
return "No Sensor Readings"

#function to read ph level
def read_phlevel():
voltage = ph_sensor.voltage #getting voltage  readings from sensor
ph_value = (voltage * 2.9)
return round(ph_value 2) # two decimal points

#function to read water level
def read_waterlevel():
return "Normal" if GPIO.input(WATER_LEVEL_PIN) else "Low"

# function to control lights
def lights_control():
current_hour = time.localtime().tm_hour
if 18 <= current_hour <= 23: #lights on from 6pm to 11pm
GPIO.output(LIGHT_PIN, GPIO.HIGH)
return "Lights are On"
else:
GPIO.output(LIGHT_PIN, GPIO.LOW)
return "Lights are Off"

#funtion to control feeder
def feeder_control():
current hour = time.localtime().tm_hour
if 8 == current hour:
feeding_servo.max()
time.sleep(3) # 3 secs
feeding_servo.min() #servo goes to normal position
return "Feeder On"
return "Feeder Off"

#Main Loop
try:
while True:
#read data
water_temperature = water_temp()
ph = read_phlevel()
water_level =  read_waterlevel()

#control system
light_status =  lights_control()
feeder_status = feeder_control()

#printing readings
print(f" Aquarium Readings: ")
print(f" Water Temperature: {water_temp}celsius")
print(f"PH Level: {ph}")
print(f"Water Level: {water_level}")
print(f"Lighting: {light_status}")
print(f"Feeder: {feeder_status}")
Print("-" * 40)

time.sleep(5) #Wait before next reading

except KeyboardInterrupt:
print("\nExiting program. Cleaning GPIO.")
GPIO.cleanup()
