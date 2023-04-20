import serial
import sys
import time
from PIL import Image
import base64
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Receive and decode images transmitted by the Leafax 35.")
    parser.add_argument('-p', '--port', help='The modem port (e.g., /dev/ttyUSB0 or COM3)', required=True)
    return parser.parse_args()

# Configure the modem
def configure_modem(serial_port):
    """
    Configure the modem connected to the serial port.
    """
    serial_port.write(b'ATZ\r')  # Reset modem
    time.sleep(1)
    serial_port.write(b'ATM0\r')  # Set modem to data mode
    time.sleep(1)
    serial_port.write(b'AT+MS=V32B,0,9600\r')  # Set modulation scheme
    time.sleep(1)

# Read image data from the modem
def read_image_data(serial_port):
    """
    Read image data from the modem connected to the serial port.
    """
    image_data = b''
    while True:
        line = serial_port.readline()
        if line.startswith(b'END'):
            break
        image_data += line
    return image_data

# Decode the received image data
def decode_image_data(image_data, width, height):
    """
    Decode the received image data and save it as a JPEG file.
    """
    image_data = base64.b64decode(image_data)

    with open('received_image.raw', 'wb') as f:
        f.write(image_data)

    img = Image.frombytes('RGB', (width, height), image_data)
    img.save('received_image.jpg', 'JPEG')

def main():
    args = parse_arguments()
    modem_port = args.port
    baud_rate = 9600

    try:
        with serial.Serial(modem_port, baud_rate, timeout=5) as serial_port:
            configure_modem(serial_port)
            print("Modem configured. Waiting for incoming transmission...")

            image_data = read_image_data(serial_port)
            # You might need to adjust the width, height, and color format according to the Leafax 35 specifications
            width = 640
            height = 480
            decode_image_data(image_data, width, height)
            print("Image received and saved as 'received_image.jpg'.")
    except serial.serialutil.SerialException as e:
        print(f"Error: Could not open the serial port '{modem_port}'. Please check the port and try again.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
