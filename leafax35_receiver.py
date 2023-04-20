import serial
import sys
import time
from PIL import Image

# Configure the modem
def configure_modem(serial_port):
    serial_port.write(b'ATZ\r')  # Reset modem
    time.sleep(1)
    serial_port.write(b'ATM0\r')  # Set modem to data mode
    time.sleep(1)
    serial_port.write(b'AT+MS=V32B,0,9600\r')  # Set modulation scheme
    time.sleep(1)

# Read image data from the modem
def read_image_data(serial_port):
    image_data = b''
    while True:
        line = serial_port.readline()
        if line.startswith(b'END'):
            break
        image_data += line
    return image_data

# Decode the received image data
def decode_image_data(image_data):
    image_data = image_data.decode('base64')
    with open('received_image.raw', 'wb') as f:
        f.write(image_data)

    # Adjust the width, height, and color format according to the Leafax 35 specifications
    img = Image.frombytes('RGB', (width, height), image_data)
    img.save('received_image.jpg', 'JPEG')

def main():
    modem_port = '/dev/ttyUSB0'  # Change this to the correct port for your modem
    baud_rate = 9600

    with serial.Serial(modem_port, baud_rate, timeout=5) as serial_port:
        configure_modem(serial_port)
        print("Modem configured. Waiting for incoming transmission...")

        image_data = read_image_data(serial_port)
        decode_image_data(image_data)
        print("Image received and saved as 'received_image.jpg'.")

if __name__ == "__main__":
    main()
