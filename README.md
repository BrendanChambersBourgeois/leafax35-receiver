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

## Installation

1. Clone this repository:
```
git clone https://github.com/BrendanChambersBourgeois/Leafax35Receiver.git
```
2. Change to the project directory:
```
cd Leafax35Receiver
```
3. Install the required Python packages:
```
pip install -r requirements.txt
```


## Usage

1. Connect the USB modem to an available USB port on your computer or microcontroller.
2. Connect the modem to an analog phone line.
3. Run the receiver script:

```
python leafax35_receiver.py
```

The script will configure the modem, wait for incoming image data, decode it, and save the received image as a JPEG file.

## Contributing

Contributions to this project are welcome. Please open an issue to discuss your ideas or submit a pull request with your proposed changes.
