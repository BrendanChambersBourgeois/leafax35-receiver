# Leafax 35 Receiver

This project aims to create a modern-day receiver for the Leafax 35, a compact portable photo scanner and transmitter from the 1980s.

## Background

The Leafax 35 was a powerful photojournalistic tool in the late 1980s. It allowed photographers to transmit photo negatives across analog phone lines in a matter of minutes. With the advent of digital satellite transmission services and the decline of analog phone lines, the Leafax 35 has become outdated. This project provides a solution for receiving Leafax 35 transmissions using current technology.

## Prerequisites

To run the Leafax 35 receiver, you'll need the following hardware components:

1. Analog telephone interface (e.g., U.S. Robotics USR5637 USB modem)
2. Computer or microcontroller with an available USB port
3. Analog phone line

Additionally, you'll need Python 3.x installed on your system.

## Requirements

Install the required Python libraries using the following command:

```bash
pip install -r requirements.txt
```

## Leafax 35 Receiver (`leafax35_receiver.py`)

This script is designed to receive and decode images transmitted by the Leafax 35. You need to connect the Leafax 35 to an analog telephone interface (e.g., U.S. Robotics USR5637 USB modem) and an analog phone line.

Usage:

```bash
python leafax35_receiver.py --port <modem_port>
```

Replace `<modem_port>` with the appropriate port for your modem (e.g., `/dev/ttyUSB0` or `COM3`).

## Leafax 35 Data Capture (`leafax35_data_capture.py`)

This script captures data transmitted by the Leafax 35 and saves it to a file for further analysis. You need to connect the Leafax 35 to an analog telephone interface (e.g., U.S. Robotics USR5637 USB modem) and an analog phone line.

Usage:

```bash
python leafax35_data_capture.py --port <modem_port>
```

Replace `<modem_port>` with the appropriate port for your modem (e.g., `/dev/ttyUSB0` or `COM3`).

After capturing the data, you can analyze the `captured_data.bin` file to determine the Leafax 35 specifications, such as image format, encoding, and other relevant details.

## Contributing

Contributions to this project are welcome. Please open an issue to discuss your ideas or submit a pull request with your proposed changes.
