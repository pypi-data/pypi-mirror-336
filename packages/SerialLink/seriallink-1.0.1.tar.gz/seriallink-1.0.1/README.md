# SerialLink
SerialLink is a Python library designed to simplify serial communication with microcontrollers. It enables efficient and seamless data exchange without blocking code execution. By using configurable start and end markers, SerialLink ensures reliable message framing, making it an ideal tool for developers working with embedded systems or serial communication.

### Notes: Need the [arduino](https://github.com/Michael-Jalloh/Arduino-SerialLink) companion library

Key Features:

- Non-blocking Reads: No need for methods like readUntil("\n") that can hinder code flow.
- Marker-Based Communication: Automatically detects the start and end of data packets, reducing parsing complexity.
- Ease of Use: Simplified API for quick integration into projects.

SerialLink is perfect for anyone needing robust, non-blocking serial communication for real-time applications.

## Installation
Installing SerialLink is straightforward. It’s available via `pip` for easy installation.

### Using `pip`

Run the following command in your terminal or command prompt:

``` bash
pip install seriallink
```

### Manual Installation

If you prefer to install manually:

1. Clone the repository:
``` bash
git clone https://github.com/your-username/seriallink.git
```
2. Navigate to the project directory:
``` bash
cd seriallink
```
3. Install the library using setup.py:
``` bash
python setup.py install
```

## Getting Started

Using SerialLink to communicate with a microcontroller is simple and intuitive. This quick guide will help you set up and send your first message. 

Note: Needs the companion arduino library at [Arduino SerialLink]()

### Step 1: Import SerialLink

Begin by importing the library in your Python script:
``` python
from seriallink import SerialLink
```

### Step 2: Initialize the Serial Connection

Create a SerialLink object by specifying the port and baud rate:
``` python
serial = SerialLink("/dev/ttyUSB0", 115200)
```
``` python
serial = SerialLink("/dev/ttyUSB0")
```
the default buadrate is 115200 and the startMarker is `<` and the endMarker is `>`.

### Step 3: Send Data

Send a message to your microcontroller:
``` python
serial.send("on")
```

### Step 4: Read Data

Receive data from the microcontroller without blocking:
``` python
serial.poll()
if serial.new_data:
    data = serial.get_data()
    print(f"Received {data})
```

### Step 5: Close the Connection

Always close the connection when done:
``` python
serial.close()
```

### Get serial ports
``` python
from seriallink import get_ports

ports = get_ports("USB") # Gets ports with usb devices connected in a list
print(ports[0])
```

## API Reference
The SerialLink library provides a straightforward API for serial communication. Below is a detailed reference to its primary methods and attributes.

`SerialLink` Class

Initialization
```
SerialLink(port: str, baudrate: int = 115200, start_marker: str = "<", end_marker: str = ">")
```

### Parameters:

- port (str): The serial port (e.g., "COM3", "/dev/ttyUSB0").
- baudrate (int): Communication speed (default: 9600).
- start_marker (str): Character marking the start of a message (default: <).
- end_marker (str): Character marking the end of a message (default: >).

### Methods

1. send(data: str)
    
    Sends a message through the serial port.
        
    - Parameters:
        - data (str): The string message to send.
    - Example:
    ``` python
    serial.send("on")
    ```
2. poll()

    Polls the serial port buffer for new data and buffers the data to be read.
    ``` python
    serial.poll()
    ```
3. get_data()

    Get new data from the buffer
    ``` python
    if serial.new_data:
        data = serial.get_data()
        print(data)
    ```
4. flush_port()

    Read and clear all data from the serial port buffer
    ``` python
    serial.flush_port()
    ```
5. close()

    close the serial port
    ``` python
    serial.close()
    ```

### Attributes

- port: The port used for communication.
- baudrate: The baud rate of the connection.
- start_marker: The character marking the start of a message.
- end_marker: The character marking the end of a message.

## Examples
1. Basic Communication

    Send a message to a microcontroller and read its response:

    ``` python
    from seriallink import SerialLink  

    # Initialize SerialLink  
    serial = SerialLink(port="/dev/ttyUSB0", baudrate=115200)  

    # Send a message  
    serial.send("Hello, Microcontroller!")  

    # Poll for a response
    serial.poll()
    if serial.new_data:
        response = serial.get_data()    
        print(f"Received: {response}")  

    # Close the connection  
    serial.close()  
    ```

2. Custom Start and End Markers

    Use custom markers to frame messages: 
    ``` python
    from seriallink import SerialLink  

    # Initialize with custom markers  
    serial = SerialLink(port="/dev/ttyUSB0", baudrate=115200, start_marker="{", end_marker="}")  

    # Send a message  
    serial.send("temp")  

    # Poll for the response 
    serial.poll()
    if serial.new_data:
        data = serial.get_data()    
        print(f"Sensor Data: {data}")  

    # Close the connection  
    serial.close()  
    ```

3. Continuous Reading

    Read messages in a loop without blocking the main program:
    ``` python
    from seriallink import SerialLink  
    import time  

    # Initialize SerialLink  
    serial = SerialLink(port="/dev/ttyUSB", baudrate=9600)  

    try:  
        while True:  
            # Check for incoming data
            serial.poll()  
              
            if serial.new_data:
                data = serial.get_data()  
                print(f"Received: {data}")  
            time.sleep(0.1)  # Avoid tight looping  
    except KeyboardInterrupt:  
        print("Stopping communication.")  
    finally:  
        serial.close()  
    ```
