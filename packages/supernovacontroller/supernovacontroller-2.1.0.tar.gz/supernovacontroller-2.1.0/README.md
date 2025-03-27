# SupernovaController
Manages communications with the Supernova host-adapter USB HID device.

## Introduction
SupernovaController is a Python-based tool designed to interface with the Supernova host-adapter USB HID device. Offering a blocking API, it simplifies command sequences and interactions in the context of asynchronous operation environments like the one offered by the Supernova host-adapter. This approach enhances usability and efficiency, providing a streamlined experience for developers working with the Supernova device.

## Features
- **Blocking API:** A streamlined approach to interact with the Supernova device, minimizing the complexity of handling asynchronous callbacks.
- **Multi-Interface:** Easily communicate with SPI, UART, I2C and I3C Devices in an All-In-One package.
- **Communication:** Seamlessly manages command responses and notifications, facilitating easier and more intuitive command sequencing.
- **Examples:** Comprehensive examples demonstrating the practical application of the blocking API.

## Installation

To install the SupernovaController package, follow these steps:

1. **Prerequisites:**
   - Ensure that you have Python 3.10 or later installed on your system.
   - It's recommended to use a virtual environment for the installation to avoid any conflicts with other Python packages. You can create a virtual environment using tools like `venv` or `conda`.

2. **Install the Package:**
   - Open your command line interface (CLI).
   - Navigate to your project directory or the directory where you want to install the SupernovaController.
   - Run the following command:
     ```sh
     pip install supernovacontroller
     ```

    This command will download and install the SupernovaController package along with its dependencies (`transfer_controller` and `BinhoSupernova`) from PyPI.

3. **Updating the Package:**
   - To update the SupernovaController to the latest version, run:
     ```sh
     pip install --upgrade supernovacontroller
     ```

4. **Troubleshooting:**
   - If you encounter any issues during the installation, make sure that your Python and pip are up to date. You can update pip using:
     ```sh
     pip install --upgrade pip
     ```
   - For any other issues or support, please contact [techsupport@binho.io](mailto:techsupport@binho.io).

## Getting started

This section provides a quick guide to get you started with the `SupernovaController`.

### Prerequisites

Before proceeding, make sure you have installed the `SupernovaController` package as outlined in the Installation section.

## Device Management

The `SupernovaDevice` class provides methods to manage connected Supernova devices. These methods allow you to list all connected devices, open a single device, or open multiple devices programmatically.

### Listing All Connected Devices

The `getAllConnectedSupernovaDevices()` method retrieves a list of all connected Supernova devices.

**Example:**
```python
from supernovacontroller.sequential import SupernovaDevice

devices = SupernovaDevice.getAllConnectedSupernovaDevices()
for device in devices:
    print(f"Device Path: {device['path']}, Serial Number: {device['serial_number']}")
```

### Opening a Single Device

To open a single Supernova device, use the `open()` method. Optionally, specify the USB HID path if multiple devices are connected.

**Example:**
```python
from supernovacontroller.sequential import SupernovaDevice

device = SupernovaDevice()
device_info = device.open(usb_address='your_usb_hid_path')  # Replace with the actual USB HID path
print("Device Info:", device_info)
device.close()  # Close the device when done
```

### Opening All Connected Devices

The `openAllConnectedSupernovaDevices()` method opens all connected Supernova devices and returns a list of `SupernovaDevice` instances.

**Example:**
```python
from supernovacontroller.sequential import SupernovaDevice

devices = SupernovaDevice.openAllConnectedSupernovaDevices()
for device in devices:
    print("Opened device with the following info:")
    print(device.open())  # Prints device information
    device.close()  # Close the device when done
```

These methods simplify working with multiple devices, especially in scenarios where you need to manage several Supernova devices simultaneously.

## I3C protocol

### I3C features

This section provides a quick guide to get you started with the `SupernovaController` focusing on the I3C protocol.
In an I3C bus, the Supernova can act either as a controller or as a target.

* In controller mode the Supernova supports several features: 
    * Supernova initialization in I3C controller mode.
    * Bus initialization.
    * Setting of bus parameters.
    * Discovery of devices on the bus.
    * I3C read operations of up to 255 bytes and I3C write operations of up to 1024 bytes.
    * CCCs.
    * Handling of IBIs.

* In target mode the Supernova acts as non-circular and addressable memory that can have different layouts:
    - memory of 1024 registers of 1 byte size
    - memory of 512 registers of 2 bytes size
    - memory of 256 registers of 4 bytes size

    In this mode, it supports several features: 
    * Supernova initialization in I3C target mode.
    * Command to change its configuration after its initialization.
    * Write and Read commands to modify the memory via USB.
    * I3C Write and Read transfers of up to 1024 bytes.
    * Notifications that indicate the end of a transfer (that involves the Supernova) detection.
  
* Coming soon:
  * For the I3C controller mode:
    - Handling of Hot-Joins requests
    - Target Reset Pattern
  * For the I3C target mode:
    - Normal IBIs request
    - Hot-Join request

### Basic I3C Communication

#### Operations valid for the Supernovas in I3C target mode and I3C controller mode

1. ***Initializing the Supernova Device:***

   Imports and initializes the `SupernovaDevice`. Optionally, specifies the USB HID path if multiple devices are connected:

   ```python
   from supernovacontroller.sequential import SupernovaDevice

   device = SupernovaDevice()
   # Optionally specify the USB HID path
   device.open(usb_address='your_usb_hid_path')
   ```

   Call `open()` without parameters if you don't need to specify a particular device.

2. ***Creating an I3C Interface:***

   Creates an I3C controller interface:

   ```python
   i3c_controller = device.create_interface("i3c.controller")
   ```
    Or an I3C target interface:

   ```python
   i3c_target = device.create_interface("i3c.target")
   ```    

3. ***Closing the Device:***

   Closes the device when done:

   ```python
   device.close()
   ```

### Operations intended for the Supernova in I3C controller mode

1. ***Initializing the Supernova as an I3C controller:***

    Initializes the Supernova in controller mode:

    ```python
   success, status = i3c_controller.controller_init()
   ```
    By default, the Supernova is initialized by the open() method in controller mode, so it may not be needed to call it in most cases.

2. ***Setting Bus Voltage:***

   Sets the bus voltage (in mV) for the I3C bus. This step is required before initializing the bus if you don't specify the voltage parameter in `init_bus`:

   ```python
   success, data = i3c_controller.set_bus_voltage(3300)
   ```

3. ***Initializing the I3C Bus:***

   Initializes the I3C bus. The voltage parameter is optional here if already set via `set_bus_voltage`:

   ```python
   success, data = i3c_controller.init_bus()  # Voltage already set, so no need to specify it here
   ```

   If the bus voltage wasn't set earlier, you can initialize the bus with the voltage parameter:

   ```python
   success, data = i3c_controller.init_bus(3300)  # Setting the voltage directly in init_bus
   ```

4. ***Discovering Devices on the Bus:***

   Retrieves a list of connected I3C devices:

   ```python
   success, targets = i3c_controller.targets()
   if success:
       for target in targets:
           print(f"Found device: {target}")
   ```

5. ***Reading and Writing to a Device:***
   
   Performs I3C write and read operations on a target device: 

   ```python
   # Write data specifying address, mode, register and a list of bytes.
   i3c_controller.write(0x08, i3c_controller.TransferMode.I3C_SDR, [0x00, 0x00], [0xDE, 0xAD, 0xBE, 0xEF])

   # Read data specifying address, mode, register and buffer length.
   success, data = i3c_controller.read(0x08, i3c_controller.TransferMode.I3C_SDR, [0x00, 0x00], 4)
   if success:
       print(f"Read data: {data}")
   ```
    Replace `0x08` with the dynamic address of the device.

6. ***Performing CCCs:***

   Requests CCCs on the I3C bus, directed to an specific target or broadcast. They take different parameters depending on the command, examples of them can be:

   ```python
    # Send a GETPID CCC specifying the dynamic address.
    success, result = i3c_controller.ccc_getpid(0x08)

    # Send a SETMWL CCC specifying the dynamic address and maximum write length.
    i3c_controller.ccc_unicast_setmwl(0x08, 1024)
    # Send a GETMWL CCC specifying the dynamic address
    success, result = i3c_controller.ccc_getmwl(0x08)
   ```
    Replace `0x08` with the dynamic address of the device.

### Operations intended for the Supernova in I3C target mode

1. ***Initializing the Supernova as an I3C target:***

    Initializes the Supernova in target mode and sets its initial configuration which includes the internal memory layout, its maximum write length, maximum read length, seconds waited to allow an In-Band Interrupt (IBI) to drive SDA low when the controller is not doing so and some flags regarding the target behaviour in the I3C bus:

    ```python
    TARGET_CONF                 = I3cOffline.OFFLINE_UNFIT.value |  \
                                  PartNOrandom.PART_NUMB_DEFINED.value |  \
                                  DdrOk.ALLOWED_DDR.value |  \
                                  IgnoreTE0TE1Errors.IGNORE_ERRORS.value |  \
                                  MatchStartStop.NOT_MATCH.value |  \
                                  AlwaysNack.NOT_ALWAYS_NACK.value    
    
    # Init Supernova in target mode specifying:
    # memory layout, uSeconds to wait for IBI, MRL, MWL and configuration.
    success, status = i3c_target.target_init(I3cTargetMemoryLayout_t.MEM_1_BYTE, 0x69, 0x100, 0x100, TARGET_CONF)   
   ```
   The memory layout field can take `MEM_1_BYTE`, `MEM_2_BYTES` or `MEM_4_BYTES` value.

2. ***Set PID:***

    Sets the PID of the Supernova acting as an I3C target via USB:

    ```python
   success, error = i3c_target.set_pid([0x02, 0x03, 0x04, 0x05, 0x06, 0x07])
   ```

3. ***Set BCR:***

    Sets the BCR of the Supernova acting as an I3C target via USB:

    ```python
   success, error = i3c_target.set_bcr(I3cTargetMaxDataSpeedLimit_t.MAX_DATA_SPEED_LIMIT, I3cTargetIbiCapable_t.NOT_IBI_CAPABLE, 
                                I3cTargetIbiPayload_t.IBI_WITH_PAYLOAD, I3cTargetOfflineCap_t.OFFLINE_CAPABLE, 
                                I3cTargetVirtSupport_t.VIRTUAL_TARGET_SUPPORT, I3cTargetDeviceRole_t.I3C_TARGET)
   ```

    Note: The input parameters set the bits of the BCR one by one, taking into account their meaning as stated in section 5.1.1.2.1
    of the MIPI I3C Basic Specification v.1.1.1

4. ***Set DCR:***

    Sets the DCR of the Supernova acting as an I3C target via USB:

    ```python
   success, error = i3c_target.set_dcr(I3cTargetDcr_t.I3C_TARGET_MEMORY)
   ```

    The input parameter (of I3cTargetDcr_t) indicates the type of device the Supernova represents, which determines the [DCR value as defined by the MIPI alliance](https://www.mipi.org/hubfs/I3C-Public-Tables/MIPI-I3C-v1-1-Current-DCR-Table.pdf). For this case `I3cTargetDcr_t` can take the values `I3C_SECONDARY_CONTROLLER`, `I3C_TARGET_MEMORY` and `I3C_TARGET_MICROCONTROLLER`. 

5. ***Set Static Address:***

    Sets the static address of the Supernova acting as an I3C target via USB:

    ```python
   success, error = i3c_target.set_static_address(0x73)
   ```

6. ***Set Supernova configuration:***

    Sets the configuration of the Supernova such as its maximum write length, maximum read length, seconds waited to allow an In-Band Interrupt (IBI) to drive SDA low when the controller is not doing so and some flags regarding the target behaviour in the I3C bus:

    ```python
    TARGET_CONF                 = I3cOffline.OFFLINE_UNFIT.value |  \
                                  PartNOrandom.PART_NUMB_DEFINED.value |  \
                                  DdrOk.ALLOWED_DDR.value |  \
                                  IgnoreTE0TE1Errors.IGNORE_ERRORS.value |  \
                                  MatchStartStop.NOT_MATCH.value |  \
                                  AlwaysNack.NOT_ALWAYS_NACK.value

    # Configure the memory layout, uSeconds to wait for IBI, MRL, MWL and configuration of the target. 
    success, status = i3c_target.set_configuration(0x69, 0x300, 0x250, TARGET_CONF)
    ```

7. ***Write memory:***

    Writes the internal memory of the Supernova via USB:

    ```python
   success, error = i3c_target.write_memory(0x010A, [0xFF for i in range(0,10)])
   ```
    
8. ***Read memory:***

    Retrieves data from the Supernova internal memory via USB:

    ```python
   success, data = i3c_target.read_memory(0x0000, 255)
   ```
    
***Target Notification:***

When the Supernova acts in I3C target mode, it notifies everytime it detects the end of an I3C transfer it was involved in (not including CCCs).

The notification reports info about the last I3C transaction addressed to the target Supernova.

A typical target notification looks like:

```python
{'transfer_type': 'I3C_TARGET_READ', 'memory_address': 7, 'transfer_length': 5, 'usb_result': 'CMD_SUCCESSFUL', 'manager_result': 'I3C_TARGET_TRANSFER_SUCCESS', 'driver_result': ['NO_ERROR'], 'data': [238, 238, 238, 238, 238]}
```

  The `transfer_type` indicates if the transfer was a read or write operation from the target point of view, can take the values `I3C_TARGET_READ` or `I3C_TARGET_WRITE`.

**Border Cases**

The fact that the memory is not circular obligates to take into account border cases:

* If the user tries to start the transfer in an address surpassing the target memory range, the target will ignore the address and will start the transfer from the end of the the previous one.

* If the transfer starts in an allowed memory address but tries to surpass the range during the transaction, it will only modify the bytes in the allowed range and discard the rest. The end of the transfer is taken as the end of the memory.

## UART protocol

### UART features

This section describes how to get you started with the `SupernovaController` focusing on the UART protocol.

* The supported features are: 
    * Bus initialization.
    * Setting of bus parameters such as baudrate, hardware handshake, parity, data size and stop bit.
    * UART TX/RX transactions of up to 1024 bytes.

### Basic UART Communication

#### Generic operations

1. ***Initializing the Supernova Device:***

   Imports and initializes the `SupernovaDevice`. Optionally, specifies the USB HID path if multiple devices are connected:

   ```python
   from supernovacontroller.sequential import SupernovaDevice

   device = SupernovaDevice()
   # Optionally specify the USB HID path
   device.open(usb_address='your_usb_hid_path')
   ```

   Call `open()` without parameters if you don't need to specify a particular device.

2. ***Creating a UART controller Interface:***

   Creates a UART controller interface:

   ```python
   uart = device.create_interface("uart")
   ``` 

3. ***Closing the Device:***

   Closes the device when done:

   ```python
   device.close()
   ```

### Operations intended for the Supernova UART peripheral

1. ***Setting Bus Voltage:***

   Sets the bus voltage (in mV) for the UART bus. This step is required before initializing the bus:

   ```python
   success, response = uart.set_bus_voltage(3300)
   ```

2. ***Initializing the Supernova UART peripheral:***

    Initializes the Supernova UART peripheral:

    ```python
   success, response = uart.init_bus()
   ```
    Without any parameters, the UART peripheral initializes with the default values for baudrate (9600bps), parity (no parity), data size (8 bit), stop bit (one stop bit) and hardware handshake (no hardware handshake). Optionally, it is possible to set any of these parameters by specifying them in the init_bus function:

    ```python
   success, response = uart.init_bus(baudrate=UartControllerBaudRate.UART_BAUD_115200, parity=UartControllerParity.UART_EVEN_PARITY)
   ```
3. ***Modifying the UART peripheral parameters***

    It is also possible to configure/set any parameter after initialization (baudrate, parity, data size, stop bit and hardware handshake):

    ```python
   success, response = uart.set_parameters(stop_bit = UartControllerStopBit.UART_TWO_STOP_BIT, baudrate = UartControllerBaudRate.UART_BAUD_56000)
   ```

   If parameters are provided, it configures the parameters; otherwise, it retains the current settings.

4. ***Read the current UART peripheral configuration***

    The following method retrieves the current UART peripheral communication parameters, including baudrate, parity, data size, stop bit and hardware handshake.

    ```python
   success, response = uart.get_parameters()
   ```

    The variable ```response``` is a tuple containing the current UART controller communication parameters:
    *(baudrate, parity, data_size, stop_bit, hardware_handshake)*

5. ***Send data over UART bus***

    If the bus is initialized, sends the provided data over the UART TX channel. 

    ```python
    data = [0x00, 0x01, 0x02, 0x3, 0x04, 0x05, 0x06]
    success, response = uart.send(data, transferLength)
    ```
    - If no errors arises while sending the data, ```success``` will be _true_ and the ```response``` will be a success message.
    - If an error arises while sending the data, ```success``` will be _false_ and the ```response``` will be an error message.

6. ***Receive data over UART bus***

    If the bus is initialized, awaits reception of data over the UART RX channel. A timeout can be set to the waiting process to exit if no data is received in the timeout's time specified time (use None to ignore the timeout feature). 

    ```python
    success, response = uart.wait_for_notification(timeout = None)
    ```
    - If data is received before the configured timeout, ```success``` will be _true_ and the ```response``` will be the array of received data.
    - If data is not received before the configured timeout,  ```success``` will be _false_ and the ```response``` will be a timeout error message.
    - If an error arises while receiving the data, ```success``` will be _false_ and the ```response``` will be an error message.

## SPI protocol

### SPI features

This section describes how to get you started with the `SupernovaController` focusing on the SPI protocol.
In a SPI bus, the Supernova can act as a controller.

* In controller mode the Supernova supports several features: 
    * Supernova initialization in SPI controller mode.
    * Bus initialization.
    * Setting of bus parameters such as bit order, SPI mode, chip select, chip select polarity and frequency.
    * SPI transfers of up to 1024 bytes.
    * 8 bits data width frames.

* Coming soon:
  * For the SPI controller mode:
    - Pre and post delays.
    - Keep chip select active between transfers.
    - Support for 16 bits data width.
  * Support for SPI target mode.

### Basic SPI Communication

#### Generic operations

1. ***Initializing the Supernova Device:***

   Imports and initializes the `SupernovaDevice`. Optionally, specifies the USB HID path if multiple devices are connected:

   ```python
   from supernovacontroller.sequential import SupernovaDevice

   device = SupernovaDevice()
   
   # Optionally specify the USB HID path
   device.open(usb_address='your_usb_hid_path')
   ```

   Call `open()` without parameters if you don't need to specify a particular device.

2. ***Creating a SPI controller Interface:***

   Creates a SPI controller interface:

   ```python
   spi_controller = device.create_interface("spi.controller")
   ``` 

3. ***Closing the Device:***

   Closes the device when done:

   ```python
   device.close()
   ```

### Operations intended for the Supernova in SPI controller mode

1. ***Setting Bus Voltage:***

   Sets the bus voltage (in mV) for the SPI bus. This step is required before initializing the bus:

   ```python
   success, response = spi_controller.set_bus_voltage(3300)
   ```

2. ***Initializing the Supernova as a SPI controller:***

    Initializes the Supernova in SPI controller mode:

    ```python
   success, response = spi_controller.init_bus()
   ```
    Without any parameters, the SPI controller initializes with the default values for bit order (MSB first), mode (Mode 0), chip select (CS0), chip select polarity (Active low) and frequency (10 MHz). Optionally, it is possible to set any of these parameters by specifying in the init_bus function:

    ```python
   success, response = spi_controller.init_bus(bit_order=SpiControllerBitOrder.LSB, frequency=20000000)
   ```

3. ***Modifying the SPI controller parameters***

    It is possible to set a new configuration for each parameter (bit order, mode, chip select, chip select polarity and frequency):

    ```python
   success, response = spi_controller.set_parameters(bit_order = SpiControllerBitOrder.MSB, mode = SpiControllerMode.MODE_1)
   ```

   If parameters are provided, it configures the parameters; otherwise, it retains the current settings.

4. ***Read the current SPI controller configuration***

    The following method retrieves the current SPI controller communication parameters, including bit order, spi mode, data width, chip select, chip select polarity and frequency.

    ```python
   success, response = spi_controller.get_parameters()
   ```

    The variable ```response``` is a tuple containing the current SPI controller communication parameters:
    (bit_order, mode, data_width, chip_select, chip_select_pol, frequency)

5. ***Transfer data over SPI bus***

    Transfers the provided data over the SPI bus if the bus is initialized. It is necessary to indicate the length of the transfer to generate the SPI clock cycles. This length could be more than the length of the transferred data to a SPI target, in the cases where the response (data on the MISO line) consists of more bytes than the transferred.

    ```python
    data = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06]
    transfer_length = 6
    success, response = spi_controller.transfer(data, transfer_length)
    ```

    For a particular case of a SPI target device that interprets instructions via opcodes, an example of use could be the following:
    
    ```python
    # Read opcode: 0x03
    # Address to read: 0x0002
    # Transferred data: [opcode, address_H, address_L]
    data = [0x03, 0x00, 0x02]
    
    # Transfer length includes the length of the transferred data to the target and the read length to generate SPI clock cycles for the read operation
    # Read length: 6 bytes to read
    # Data to target: 3 bytes
    read_length = 6
    data_to_target = len(data)
    transfer_length = data_to_target + read_length

    success, response = spi_controller.transfer(data, transfer_length)

    # The response consists of the entire MISO line since the transfer started.
    # If the SPI target device doesn't send information while the instruction is transferred, the first bytes of the response are in IDLE state with the value 0x00
    # response: [0x00, 0x00, 0x00, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE, 0xFF]
    data_from_target = response[3:]
    ```

## GPIO

### GPIO features

This section describes how to get you started with the `SupernovaController` focusing on the GPIO protocol.

* The supported features are:
    * Setting of bus voltage.
    * Configuring pins as digital inputs or outputs.
    * Digital read/write operations.
    * Setting and disabling interrupts on pins.
    
### Basic GPIO Communication

#### Generic operations

1. ***Initializing the Supernova Device:***

   Imports and initializes the `SupernovaDevice`. Optionally, specifies the USB HID path if multiple devices are connected:

   ```python
   from supernovacontroller.sequential import SupernovaDevice

   device = SupernovaDevice()
   
   # Optionally specify the USB HID path
   device.open(usb_address='your_usb_hid_path')
   ```

   Call `open()` without parameters if you don't need to specify a particular device.

2. ***Creates a GPIO interface:***

    ```python
    gpio = device.create_interface("gpio")
    ```
 
3. ***Closing the Device:***

    Closes the device when done:

    ```python
    device.close()
    ```

### Operations intended for the Supernova GPIO peripheral

1. ***Setting Pins Voltage:***

    Sets the pins voltage (in mV) for the GPIO pins. This step is required before initializing the GPIO interface:

    ```python
    success, response = gpio.set_pins_voltage(3300)
    ```
    **Important note:**
    - If Supernova rev. B is used, voltage can be set in pins 1 and 2. Pins 3 to 6 are fixed at 3.3 V.
    - If Supernova rev. C is used, voltage is set for all pins.

2. ***Configuring a GPIO pin:***

    Configures a GPIO pin with the specified functionality. For example, configuring GPIO pin 6 as a digital output:

    ```python
    from BinhoSupernova.commands.definitions import GpioPinNumber, GpioFunctionality

    success, response = gpio.configure_pin(GpioPinNumber.GPIO_6, GpioFunctionality.DIGITAL_OUTPUT)
    ```

3. ***Digital Write:***

    Writes a digital logic level to a GPIO pin configured as a digital output. For example, setting GPIO pin 6 to LOW:

    ```python
    from BinhoSupernova.commands.definitions import GpioLogicLevel

    success, response = gpio.digital_write(GpioPinNumber.GPIO_6, GpioLogicLevel.LOW)
    ```

4. ***Digital Read:***

    Reads the digital logic level from a GPIO pin configured as a digital input. For example, reading the value from GPIO pin 5:

    ```python
    success, value = gpio.digital_read(GpioPinNumber.GPIO_5)
    ```

5. ***Set Interrupt:***

    Sets an interrupt on a GPIO pin configured as a digital input. For example, setting an interrupt on GPIO pin 5 for both rising and falling edges:

    ```python
    from BinhoSupernova.commands.definitions import GpioTriggerType

    success, response = gpio.set_interrupt(GpioPinNumber.GPIO_5, GpioTriggerType.TRIGGER_BOTH_EDGES)
    ```

6. ***Handle interruptions:***

    To manage GPIO notifications, we have to pass to the `on_notification()` method these functions:
     - Filter function: it checks if the notification is a GPIO interrupt.
     - Handler function: it processes the interruption, setting the gpio interruption event.

    The following code snippet illustrates a non-concurrent way of handling GPIO interruptions:

    ```python
    from threading import Event

    # Defines gpio interruption event
    gpio_interrupt_event = Event()

    # Defines filter and handler functions to be passed to the on_notification() method
    def is_gpio_interrupt(name, message):
        return message['name'].strip() == "GPIO INTERRUPTION"
    
    def handle_gpio_interrupt(name, message):
        gpio_interrupt_event.set()

    device.on_notification(name="GPIO INTERRUPTION", filter_func=is_gpio_interrupt, handler_func=handle_gpio_interrupt)

    # Asumes pin 6 initially at LOW level and pins 5 and 6 are connected to each other
    for level in [GpioLogicLevel.HIGH, GpioLogicLevel.LOW, GpioLogicLevel.HIGH, GpioLogicLevel.LOW]:
        gpio.digital_write(GpioPinNumber.GPIO_6, level)

        # Wait for the GPIO interrupt to be processed
        gpio_interrupt_event.wait()
        gpio_interrupt_event.clear()
    ```

7. ***Disable Interrupt:***

    Disables an interrupt on a GPIO pin. For example, disabling the interrupt on GPIO pin 5:

    ```python
    success, response = gpio.disable_interrupt(GpioPinNumber.GPIO_5)
    ```

## Next Steps

After installing the `SupernovaController` package, you can further explore its capabilities by trying out the examples included in the installation. These examples demonstrate practical applications of SPI, UART, I2C and I3C protocols:

- **Basic I3C Example (`basic_i3c_example.py`):** Learn the basics of I3C bus initialization and device communication using the Supernova as an I3C controller.
- **Basic I3C Target Mode Example (`basic_i3c_target_example.py`):** Learn the basics of I3C target mode implementation using two Supernovas, one as an I3C target and the other one as a controller.
- **Basic I2C Example (`basic_i2c_example.py`):** Get started with fundamental I2C operations.
- **Basic UART Example (`basic_uart_example.py`):** Try out the UART protocol Hands-On.
- **Basic SPI Controller Example (`basic_spi_controller_example.py`):** Explore the fundamental SPI controller operations communicating with a SPI Target device.
- **Hot-join example(`i3c_hot_join_example.py`):** Understand how to handle the hot-join procedure in I3C.
- **IBI Example (`i3c_ibi_example.py`):** Understand handling In-Band Interrupts (IBI) in I3C.
- **ICM42605 I3C Example (`ICM42605_i3c_example.py`):** Explore a real-world application of I3C with the ICM42605 sensor.

#### Accessing the Examples

The example scripts are installed in your site-packages folder as `supernovacontrollerexamples`, and you can access them just like you would any other package in Python. To find this directory, you can use the following Python commands:

```python
import sys
import os

examples_dir_name = "supernovacontrollerexamples"
examples_path = os.path.join(sys.prefix, "lib", "site-packages", examples_dir_name)
print(f"Examples are located in: {examples_path}")
```

This will print the path to the `SupernovaExamples` directory. Navigate to this directory to find the example scripts.

You can run an example directly from this directory using Python. For instance:

```sh
python /path/to/supernovacontrollerexamples/basic_i2c_example.py
```

Replace `/path/to/supernovacontrollerexamples/` with the actual path printed in the previous step and `basic_i2c_example.py` with the name of the example you wish to run.

Or by calling the main method from the example directly from your Python script, as so:

```python
from supernovacontrollerexamples import basic_i2c_example

basic_i2c_example.main()
```

#### Exploring Further

Each example is designed to provide insights into different aspects of the `SupernovaController` usage. By running and modifying these examples, you'll gain a deeper understanding of how to effectively use the package in various scenarios.

## Error Handling

When using the `SupernovaController`, it's important to distinguish between two types of errors: regular errors and exceptions. Regular errors are those that result from 'non-successful' operations of the host adapter, typically indicated by the success status in the operation's return value. Exceptions, on the other hand, are more severe and usually indicate issues with the device communication or incorrect usage of the API.

### Handling Regular Errors
Regular errors are part of normal operation and are often indicated by the return value of a method. For instance, an operation may return a success status of `False` to indicate a failure.

**Example:**
```python
success, result = i2c.write(0x50, [0x00,0x00], [0xDE, 0xAD, 0xBE, 0xEF])
if not success:
    print(f"Operation failed with error: {result}")
```

Regular errors should be checked after each operation and handled appropriately based on the context of your application.

### Handling Exceptions
Exceptions are raised when there are issues with the device's communication or incorrect usage of the API. These are more critical and need to be addressed immediately, often requiring changes in the code or the hardware setup.

Here are some common exceptions and how to handle them:

#### 1. DeviceOpenError
Occurs when the `open` method is called with an incorrect or inaccessible USB HID path.

**Example Handling:**
```python
try:
    device.open("incorrect_hid_path")
except DeviceOpenError:
    print("Failed to open device. Please check the HID path.")
```

#### 2. DeviceAlreadyMountedError
Raised when attempting to open a device that is already open.

**Example Handling:**
```python
try:
    device.open()
    device.open()
except DeviceAlreadyMountedError:
    print("Device is already open.")
```

#### 3. DeviceNotMountedError
Thrown when trying to perform operations on a device that has not been opened yet.

**Example Handling:**
```python
try:
    device.create_interface("i3c.controller")
except DeviceNotMountedError:
    print("Device not opened. Please open the device first.")
```

#### 4. UnknownInterfaceError
Occurs when an invalid interface name is passed to the `create_interface` method.

**Example Handling:**
```python
try:
    device.create_interface("invalid_interface")
except UnknownInterfaceError:
    print("Unknown interface. Please check the interface name.")
```

#### 5. BusNotInitializedError
Raised when attempting to perform bus operations without proper initialization.

**Example Handling:**
```python
try:
    i2c.read_from(0x50, [0x00,0x00], 4)
except BusNotInitializedError:
    print("Bus not initialized. Please initialize the bus first.")
```

#### 6. BackendError
Occurs when there is an issue at the backend level, often indicating deeper problems like hardware or driver issues.

**Example Handling:**
```python
try:
    # Some operation that might cause backend error
except BackendError as e:
    print(f"Backend error occurred: {e}")
```

### General Error Handling Advice
- Always validate inputs and states before performing operations.
- Use specific exception handling rather than a general catch-all where possible, as this leads to more informative error messages and debugging.
- Ensure that any cleanup or state reset logic is executed in the event of errors.

By understanding and properly handling both regular errors and exceptions, you can ensure stable and reliable operation of applications that utilize the `SupernovaController`.

## License
SupernovaController is licensed under a Proprietary License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any inquiries, support requests, or contributions regarding the `SupernovaController` package, please contact us:

- **Organization:** Binho LLC
- **Email:** [techsupport@binho.io](mailto:techsupport@binho.io)

We welcome feedback and we are happy to provide assistance with any issues you may encounter.

## Limitation of Responsibility

### Disclaimer

The `SupernovaController` is provided "as is" without warranty of any kind, either express or implied, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose. The entire risk as to the quality and performance of the `SupernovaController` is with you. Should the `SupernovaController` prove defective, you assume the cost of all necessary servicing, repair, or correction.

In no event will Binho LLC be liable to you for damages, including any general, special, incidental, or consequential damages arising out of the use or inability to use the `SupernovaController` (including but not limited to loss of data or data being rendered inaccurate or losses sustained by you or third parties or a failure of the `SupernovaController` to operate with any other software), even if Binho LLC has been advised of the possibility of such damages.

### Acknowledgement

By using the `SupernovaController`, you acknowledge that you have read this disclaimer, understood it, and agree to be bound by its terms.
