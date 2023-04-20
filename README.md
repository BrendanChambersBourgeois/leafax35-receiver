# Leafax 35 Receiver

This project aims to create a modern-day receiver for the Leafax 35, a compact portable photo scanner and transmitter from the 1980s for 35mm color or black and white negatives or positives.

## Background

The Leafax 35 was a powerful photojournalistic tool in the late 1980s, allowing photographers to transmit photo negatives across analog phone lines in a matter of minutes. With the advent of digital satellite transmission services and the decline of analog phone lines, the Leafax 35 has become outdated. This project provides a solution for receiving Leafax 35 transmissions using current technology.

## Specifications

- Analog Transmission Formats
  - AP AM 144 LPM
  - CCITT AM, FM 60 and 120 LPM
  - UPI AM, FM 120 LPM
- Digital Interface
  - GPIB IEEE-488
- Resolution
  - 2000 x 3000 pixels over the entire negative
- Dynamic Range
  - 12 or 8 bits per color (user-selected)

## Prerequisites

To run the Leafax 35 receiver, you'll need the following hardware components:

1. Analog telephone interface (e.g., U.S. Robotics USR5637 USB modem)
2. Computer or microcontroller with an available USB port
3. Analog phone line

Additionally, you'll need Python 3.x installed on your system.

## Installation and Usage

1. Clone this repository on your local machine.
2. Navigate to the cloned directory and run the following command to install the required Python libraries:

```bash
pip install -r requirements.txt
```

Usage:

To run the Leafax 35 Receiver and Data Capture script, use the following command:

```bash
python leafax35.py --port <modem_port> --mode <operation_mode> --transmission_format <transmission_format>
```

Replace `<modem_port>` with the appropriate port for your modem (e.g., `/dev/ttyUSB0` or `COM3`).

The --mode parameter specifies the operation mode. It accepts two values:

- `receive` to receive and decode images transmitted by the Leafax 35.
- `capture` to capture transmitted data for further analysis.

Replace `<transmission_format>` with the desired transmission format (e.g., `AP`, `CCITT_60`, `CCITT_120`, or `UPI`).

The script will automatically create a `data` folder in the current directory, where it will store received images and captured data.

## Contributing

Contributions to this project are welcome. Please open an issue to discuss your ideas or submit a pull request with your proposed changes.
