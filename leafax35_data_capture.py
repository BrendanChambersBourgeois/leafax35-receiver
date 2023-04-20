import serial
import sys
import time
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Capture data transmitted by the Leafax 35.")
    parser.add_argument('-p', '--port', help='The modem port (e.g., /dev/ttyUSB0 or COM3)', required=True)
    return parser.parse_args()

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

def capture_data(serial_port):
    """
    Capture data transmitted by the Leafax 35 and save it to a file.
    """
    with open('captured_data.bin', 'wb') as f:
        start_time = time.time()
        while time.time() - start_time < 300:  # Capture data for 5 minutes (adjust as needed)
            data = serial_port.read(1024)
            if data:
                f.write(data)
                start_time = time.time()  # Reset timer if data is received

def main():
    args = parse_arguments()
    modem_port = args.port
    baud_rate = 9600

    try:
        with serial.Serial(modem_port, baud_rate, timeout=5) as serial_port:
            configure_modem(serial_port)
            print("Modem configured. Waiting for data from Leafax 35...")
            capture_data(serial_port)
            print("Data captured and saved as 'captured_data.bin'.")
    except serial.serialutil.SerialException as e:
        print(f"Error: Could not open the serial port '{modem_port}'. Please check the port and try again.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
