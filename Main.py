import serial
import time
import glob
import Adafruit_CharLCD as LCD

# Initialize your display here
lcd = LCD.Adafruit_CharLCDPlate()

# ... [Other functions remain the same] ...

# Check if the measured values are within the desired ranges
def check_values(conductivity, ph, temperature):
    alert_message = ""

    # Check temperature
    if temperature < 76:
        alert_message += "Check Temp: Too Low!\n"
    elif temperature > 80:
        alert_message += "Check Temp: Too High!\n"

    # Check conductivity
    if conductivity < 100:
        alert_message += "Check Cond: Too Low!\n"
    elif conductivity > 300:
        alert_message += "Check Cond: Too High!\n"

    # Check pH
    if ph < 6.5:
        alert_message += "Check pH: Too Low!\n"
    elif ph > 8:
        alert_message += "Check pH: Too High!\n"

    return alert_message

# Main function
def main():
    conductivity_serial = init_conductivity_probe()
    ph_serial = init_ph_probe()

    # Find DS18B20 device file
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

    while True:
        # Read conductivity
        conductivity_serial.write(b'R')
        conductivity = float(conductivity_serial.readline().decode('utf-8').strip())

        # Read pH
        ph_serial.write(b'R')
        ph = float(ph_serial.readline().decode('utf-8').strip())

        # Read temperature
        temperature = read_temp(device_file)

        # Check if the values are within the desired ranges
        alert_message = check_values(conductivity, ph, temperature)

        # Prepare display string
        display_string = f"Cond: {conductivity} uS/cm\npH: {ph}\nTemp: {temperature} C\n"

        # If there are alerts, add them to the display string
        if alert_message:
            display_string += alert_message

        # Clear the display and then print the new values and alerts if any
        lcd.clear()
        lcd.message(display_string)

        time.sleep(5)  # Delay of 5 seconds

if __name__ == "__main__":
    main()
