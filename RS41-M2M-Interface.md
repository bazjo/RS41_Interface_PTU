# Vaisala RS41 M2M Interface

The machine-to-machine Interface of the RS41 radiosonde is primarily used to perform wireless configuration an ground check of the radiosonde via it's NFC interface. At this time, the exact specification of this interface is not yet known publicly. However, there is a way of interacting with this interface via the serial (UART) XDATA interface (described in the [hardware repo](https://github.com/bazjo/RS41_Hardware#xdata-and-programming-connectors)).

The default parameters for the serial interface are `9600 Baud, 8N1, \r Line Ending`.

The M2M Interface shares some configuration options with the service menu, while others are only available in one or the other. Interfacing with this menu is recommended for M2M communication whenever possible as it is much better suited for the task.

The service menu can be entered by sending `\rHXmcr\r` after the radiosonde is turned on and printed the device status information.

It is likely that Vaisala will change this code in an upcoming firmware revision or remove this menu altogether. However, as the security of the STM32 MCU [is fundamentally broken](https://hackaday.com/2020/03/24/breaking-into-a-secure-facility-stm32-flash/), any new code can be extracted from the radiosonde firmware.

As of 2021, Sondes with a serial starting with `T` and software version `2.02.15` are confirmed to have the service menu enabled.

*Note: In the console logs, lines with user input are indicated by the `➜` character at the beginning of the line*

```latex
Vaisala RS41 Radiosonde SW V2.02.14\r
Copyright (c) Vaisala Oyj 2016. All rights reserved.\r
Serial number: P0110001\r
Pressure module serial number: P0110001 SW V2.01\r
Transmitter frequency: 403.00 MHz\r
Transmitter power: 3/7\r
\r
Enabled TX\r
➜ \r
➜ HXmcr\r
0 P0110001 1 1 64BF\r
➜ 10 0 2B8D\r
10 P0110001 8 P0110001 EEFD\r
```

The protocol follows a request/response approach, where a command request is sent to the sonde, which then sends back a command response.

The ASCII encoded commands contain several fields, which are separated by a single whitespace character `0x20` and each message is terminated by a `\r` character.

A command contains the following blocks. Usually, all fields are necessary, but for some commands, certain blocks are omitted.

| Field Name     | Length [Byte] | Description                                                  |
| -------------- | ------------- | ------------------------------------------------------------ |
| command        | 1-2           | Command ID of the desired command as described below         |
| serial         | 8             | Serial number of the sonde. For serial interactions, this can always be replaced with `00000000` |
| payload length | 1-3           | Number of characters in the payload field as ASCII encoded Hex |
| payload        | 0-n           | Command payload                                              |
| crc            | 4             | CRC16 checksum over the first command character to the last payload character, including all white-spaces but not the whitespace after the payload field (generator polynomial: ???) |

## Command IDs

| ID     | Name                                 | Payload Length | Payload Values                                               |
| ------ | ------------------------------------ | -------------- | ------------------------------------------------------------ |
| `0x00` | Default                              |                |                                                              |
| `0x10` | Read Serial                          |                |                                                              |
| `0x11` | Write Serial                         |                |                                                              |
| `0x15` | Write Radio Frequency                |                |                                                              |
| `0x16` | Write Radio Power                    |                |                                                              |
| `0x17` | Write Launched Mode Altitude         |                |                                                              |
| `0x18` | Write Timerkill Time                 |                |                                                              |
| `0x19` | Write Kill Altitude Difference       |                |                                                              |
| `0x1A` | Write Burstkill Status               |                |                                                              |
| `0x1B` | Write Failurekill Status             |                |                                                              |
| `0x1C` | Write Humidity Heating Status        |                |                                                              |
| `0x1E` | Write Parameter by Data ID           |                |                                                              |
| `0x1F` | Read DGPS Data                       |                |                                                              |
| `0x20` | Write DGPS Data                      |                |                                                              |
| `0x22` | Read GPS Nav Result                  |                |                                                              |
| `0x23` | Erase Subframe Page                  |                |                                                              |
| `0x24` | Read Subframe Data                   |                |                                                              |
| `0x25` | Write Subframe Data                  |                |                                                              |
| `0x26` | Update Radiosonde Firmware           |                |                                                              |
| `0x27` | Write Radio Status                   | `0x1`          | `0` - Radio disabled<br />`1` - Radio enabled                |
| `0x28` | Write GPS Status                     |                |                                                              |
| `0x2A` | Write XDATA Status                   | `0x1`          | `0` - XDATA disabled<br />`1`..`n` - XDATA enabled with `n` sensors |
| `0x2B` | Read Regeneration Time               |                |                                                              |
| `0x2C` | Read Complete Subframe               |                |                                                              |
| `0x2D` | Read Parameter by Data ID            |                |                                                              |
| `0x2E` | Read Radio Register                  |                |                                                              |
| `0x2F` | Write Radio Register                 |                |                                                              |
| `0x30` | Write Power Status                   |                |                                                              |
| `0x31` | Write LED Status                     |                |                                                              |
| `0x32` | Read TU Measurement                  |                | request `32 00000000 0 9546`<br />response `32 P0110001 26 2.628210E+01 3.119977E+01 4.216598E+01 6973`<br />Payload seems to be ignored |
| `0x33` | Start Regeneration                   |                |                                                              |
| `0x34` | Write Humidity Heating               |                |                                                              |
| `0x35` | Read NFC RSSI                        |                |                                                              |
| `0x37` | Read/Write Pressure Module           |                |                                                              |
| `0x38` | Write Continuous Transmission Status |                |                                                              |
| `0x39` | Write Reference Heating Status       |                |                                                              |
| `0x3A` | Write Power Switch Status            |                |                                                              |
| `0x3B` | Start Temperature Self Check         |                |                                                              |
| `0x3C` | Stop Sequence                        |                |                                                              |
| `0x3D` | Write GPS Message Checking Status    |                |                                                              |
| `0x3E` | Disable GPS Messages                 |                |                                                              |
| `0x3F` | Write Power Switch Delay Status      |                |                                                              |
| `0x41` | Read PTU Measurement                 |                | request `41 00000000 0 5AD1`<br />response `41 P0110001 63 0C00 000000 01F66B 02D8C6 087619 076336 087199 02E417 01F66A 02D8C7 04EA13 046A8F 065528 0000 34.91 54D0`<br />Payload seems to be ignored |
| `0x50` | Write Serial Baud Rate               |                |                                                              |
| `0x51` | Enable Engineering Mode              |                |                                                              |
| `0x52` | Disable Engineering Mode             |                |                                                              |
| `0x53` | Write GPS Command                    |                |                                                              |
| `0x54` | Write Telemetry Status               |                |                                                              |

