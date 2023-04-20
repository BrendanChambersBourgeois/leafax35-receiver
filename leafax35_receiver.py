from PIL import Image
import argparse
import os
import serial
import sys
import time
import io
import uuid


def parse_arguments():
    parser = argparse.ArgumentParser(description="Receive and decode images transmitted by the Leafax 35 or capture data transmitted by the device.")
    parser.add_argument('-p', '--port', help='The modem port (e.g., /dev/ttyUSB0 or COM3)', required=True)
    parser.add_argument('-m', '--mode', help='The mode of operation: "receive" (default) to receive and decode images, or "capture" to capture transmitted data.', default='receive')
    return parser.parse_args()


def configure_modem(serial_port):
    serial_port.write(b'ATZ\r')  # Reset modem
    time.sleep(1)
    serial_port.write(b'ATM0\r')  # Set modem to data mode
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


def save_image(image_data, output_dir):
    filename = os.path.join(output_dir, 'received_image.jpg')

    # If a file with the same name already exists, append a GUID to the filename
    if os.path.exists(filename):
        guid = uuid.uuid4().hex
        filename_without_ext, ext = os.path.splitext(filename)
        filename = f"{filename_without_ext}_{guid}{ext}"

    with open(filename, 'wb') as f:
        f.write(image_data)
    print(f"Image received and saved as '{filename}'.")


def decode_image_data(image_data, width, height, output_dir):
    with open(os.path.join(output_dir, 'received_image.raw'), 'wb') as f:
        f.write(base64.b64decode(image_data))

    with io.BytesIO(base64.b64decode(image_data)) as image_stream:
        img = Image.open(image_stream)
        img.save(os.path.join(output_dir, 'received_image.jpg'), 'JPEG')
    print(f"Image decoded and saved as 'received_image.jpg'.")


def receive_image_data(serial_port, output_dir, width, height):
    configure_modem(serial_port)
    print("Modem configured. Waiting for incoming transmission...")

    image_data = read_image_data(serial_port)

    if len(image_data) == 0:
        raise Exception("Error: Received image data is empty.")

    save_image(image_data, output_dir)
    decode_image_data(image_data, width, height, output_dir)


def capture_data(serial_port, output_dir):
    with open(os.path.join(output_dir, 'captured_data.bin'), 'wb') as f:
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
    output_dir = 'data'

    try:
        with serial.Serial(modem_port, baud_rate, timeout=5) as serial_port:
            if args.mode == 'receive':
                width = 640
                height = 480
                receive_image_data(serial_port, output_dir, width, height)
            elif args.mode == 'capture':
                capture_data(serial_port, output_dir)
            else:
                raise ValueError(f"Invalid mode: {args.mode}")
    except serial.serialutil.SerialException as e:
        print(f"Error: Could not open the serial port '{modem_port}'. Please check the port and try again.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
