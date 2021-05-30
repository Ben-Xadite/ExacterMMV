import RPi.GPIO as GPIO
import time
import serial
import csv

serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)

# BCM pin 18, BOARD pin 12
input_pin = 18
# Wait a second to let the port initialize
time.sleep(1)

def main():
    # BCM pin-numbering scheme from Raspberry Pi
    GPIO.setmode(GPIO.BCM)  
    # set pin as an input pin
    GPIO.setup(input_pin, GPIO.IN)

    try:
        with open('Input_Data.csv', mode='w') as input_data:
            fieldnames = ['Distance in feet','Qualified bit','MMV']
            input_data_writer = csv.DictWriter(input_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=fieldnames)
            input_data_writer.writeheader()
            while True:
                inputString = input("Enter distance in feet: ")
                inputInt = int(inputString)
                if serial_port.inWaiting() > 0:
                    sigBit = GPIO.input(input_pin)
                    data = serial_port.read() 
                    binData = ord(data) & 0b1111111
                    intData = int(binData)
                    print("Qualified bit {} : MMV {}".format(sigBit, intData))
                    serial_port.write(data)
                    if data == "\r".encode():
                        serial_port.write("\n".encode())
                input_data_writer.writerow({'Distance in feet': inputInt, 'Qualified bit': sigBit, 'MMV': intData})

    except KeyboardInterrupt:
        print("Exiting Program")

    except Exception as exception_error:
        print("Error occurred. Exiting Program")
        print("Error: " + str(exception_error))

    finally:
        serial_port.close()
        GPIO.cleanup()
    pass

if __name__ == '__main__':
    main()
