from PIL import Image
import argparse
import serial
import sys
import time
import io
import uuid

def parse_arguments():
    parser = argparse.ArgumentParser(description="Receive and decode images transmitted by the Leafax 35 or capture data transmitted by the device.")
    parser.add_argument('-p', '--port', help='The modem port (e.g., /dev/ttyUSB0 or COM3)', required=True)
    parser.add_argument('-m', '--mode', help='The mode of operation: "receive" (default) to receive and decode images, or "capture" to capture transmitted data.', default='receive')
    parser.add_argument('-w', '--width', help='The width of the received image in pixels (default: 640).', default=640, type=int)
    parser.add_argument('-h', '--height', help='The height of the received image in pixels (default: 480).', default=480, type=int)
    return parser.parse_args()


def configure_modem(serial_port, transmission_format):
    serial_port.write(b'ATZ\r')  # Reset modem
    time.sleep(1)
    serial_port.write(b'ATM0\r')  # Set modem to data mode
    time.sleep(1)
    if transmission_format == 'AP':
        serial_port.write(b'ATS11=144\r')  # Set LPM to 144
    elif transmission_format == 'CCITT_60':
        serial_port.write(b'ATS11=60\r')  # Set LPM to 60
    elif transmission_format == 'CCITT_120':
        serial_port.write(b'ATS11=120\r')  # Set LPM to 120
    elif transmission_format == 'UPI':
        serial_port.write(b'ATS11=120\r')  # Set LPM to 120
    time.sleep(1)
    serial_port.write(b'AT+MS=V32B,0,9600\r')  # Set modulation scheme
    time.sleep(1)


def read_image_data(serial_port):
    image_data = b''
    while True:
        line = serial_port.readline()
        if line.startswith(b'END'):
            break
        image_data += line
    return image_data


def save_and_decode_image(image_data, filename):
    unique_filename = f"{filename}_{uuid.uuid4().hex}.jpg"

    with open(unique_filename, 'wb') as f:
        f.write(image_data)
    print(f"Image received and saved as '{unique_filename}'.")

    with open(unique_filename, 'rb') as f:
        with io.BytesIO(f.read()) as image_stream:
            img = Image.open(image_stream)
            img.save(f"data/{unique_filename}", 'JPEG')
    print(f"Image decoded and saved as '{unique_filename}'.")



def receive_image_data(serial_port, width, height, transmission_format):
    configure_modem(serial_port, transmission_format)
    print("Modem configured. Waiting for incoming transmission...")

    image_data = read_image_data(serial_port)

    if len(image_data) == 0:
        raise Exception("Error: Received image data is empty.")

    filename = "received_image"
    save_and_decode_image(image_data, filename)



	
def capture_data(serial_port):
    with open("data/captured_data.bin", 'wb') as f:
        start_time = time.time()
        while time.time() - start_time < 300:  # Capture data for 5 minutes (adjust as needed)
            data = serial_port.read(1024)
            if data:
                f.write(data)
            start_time = time.time()  # Reset timer if data is received
    print("Data captured and saved as 'captured_data.bin'.")


def main():
    args = parse_arguments()
    modem_port = args.port
    baud_rate = 9600
    serial_port = None

    # Add a new command-line argument for transmission format
    transmission_format = input("Enter the transmission format (AP, CCITT_60, CCITT_120, or UPI): ")

    try:
        serial_port = serial.Serial(modem_port, baud_rate, timeout=5)
        if args.mode == 'receive':
            receive_image_data(serial_port, args.width, args.height, transmission_format)
        elif args.mode == 'capture':
            capture_data(serial_port)
        else:
            raise ValueError(f"Invalid mode: {args.mode}")
    except serial.serialutil.SerialException as e:
        print(f"Error: Could not open the serial port '{modem_port}'. Please check the port and try again.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        if serial_port is not None:
            serial_port.close()

if __name__ == "__main__":
    main()
