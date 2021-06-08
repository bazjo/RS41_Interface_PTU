# Vaisala RS41 Service Menu

The Service Menu of the RS41 Radiosonde was discovered in 2020 someone who is much better at ARM Assembly than me. It is accessible via the serial (UART) XDATA interface of the radiosonde. Refer to [the hardware repo](https://github.com/bazjo/RS41_Hardware#xdata-and-programming-connectors) for more detail.

The default parameters for the serial interface are `9600 Baud, 8N1, \r Line Ending`.



```diff
-### WARNING ###-
- The service menu gives you the power to quite easily delete the radiosondes calibration data, 
- send radio signals in frequency bands where they can cause interference with imortant stuff 
- and create wrong entries in radiosonde databases, if a forwarding receiver is nearby.

- Neither I nor Vaisala or anyone else is responsible if you screw things up. 
- Don't do stupid stuff and only send in HAM or any other radio bands if and how you are permitted to do so.
```



The service menu can be entered by sending `\rSTwsv\r` after the radiosonde is turned on and printed the device status information.

The interactions with the service menu feel a bit rough around the edges in a few cases and it is clear that this is only an engineering tool for Vaisala's RnD which was never meant to be known about by anyone outside the company.

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
➜ STwsv\r
\r
\r
\r
(S)ensors         Fre(q)uencies  (P)arameters    (A)lfa           TX p(o)wer\r
TX (f)requency    T(X) state     (T)X registers  TX contin(u)ous  TX ran(d)om\r
TX (c)arrier      (B)aud rate    Ser(i)al no     (R)ed LED info   (N)o menu\r
(K)eep test mode  S(W) version   (M)easurements  (L)aunch/Drop    (E)xit\r
>
```

There are 20 menu items which can be accessed by sending the letter (case insensitive) in (brackets), (not followed by `\r`), i. e. `S` to trigger a sensor readout.

If you enter more than 1 letter, the additional letters will be buffered and processed one after the other (i. e. `SSS` will print the sensors readout three times).

After a menu item is accessed, the sonde will echo the input letter followed by `\r` and then usually provide a further prinout.

There are several different types of menu items

* **Action Triggers** don't require any additional parameters and just trigger some action, usually a printout
* **Value Toggles** also don't require additional parameters and cycle through different configuration options. Unfortunately, the current cofiguration usually cannot be queried, at least not through the menu entry, without advancing one option
* **Value Entries** expect one ore more additional parameters. Those can be supplied after a response to the sent letter has been received, or directly with the letter (The sonde can't tell the difference). The parameters have to be terminated with `\r`.  If a write parameter should be omitted, an empty string can be provided. If the provided value can not be assigned, `Failed!\r` is printed after the input is echoed.

After a menu interaction, the service menu entries are printed again. The service menu entry prints are not shown in the description of the menu items.

Example of an action trigger menu interaction:

```latex
(S)ensors         Fre(q)uencies  (P)arameters    (A)lfa           TX p(o)wer\r
TX (f)requency    T(X) state     (T)X registers  TX contin(u)ous  TX ran(d)om\r
TX (c)arrier      (B)aud rate    Ser(i)al no     (R)ed LED info   (N)o menu\r
(K)eep test mode  S(W) version   (M)easurements  (L)aunch/Drop    (E)xit\r
>
➜ R
R\r
No add-on sensor data\r
PTU failure\r
\r
\r
(S)ensors         Fre(q)uencies  (P)arameters    (A)lfa           TX p(o)wer\r
TX (f)requency    T(X) state     (T)X registers  TX contin(u)ous  TX ran(d)om\r
TX (c)arrier      (B)aud rate    Ser(i)al no     (R)ed LED info   (N)o menu\r
(K)eep test mode  S(W) version   (M)easurements  (L)aunch/Drop    (E)xit\r
>
```



## Service Menu Items

| Letter | Name                              | Menu item type | Description                                                  |
| ------ | --------------------------------- | -------------- | ------------------------------------------------------------ |
| S      | [Sensors](#sensors)               | Action Trigger | Trigger and print a PTU sensor readout                       |
| Q      | [Frequencies](#frequencies)       | Action Trigger | Trigger a PTU sensor readout, print the measured frequencies |
| P      | [Parameters](#parameters)         | Value Entry    | Set various operating Parameters                             |
| A      | [Alfa](#alfa)                     | Value Entry    | Set the temperature sensor calibration value                 |
| O      | [TX power](#tx-power)             | Value Entry    | Set the transmitter power while not in `launched` or `dropping` mode |
| F      | [TX frequency](#tx-frequency)     | Value Entry    | Set the transmitter frequency within the range `400.00 .. 405.99 MHz` |
| X      | [TX state](#tx-state)             | Value Toggle   | Toggle the transmitter power status                          |
| T      | [TX registers](#tx-registers)     | Value Entry    | Access arbitrary registers of the Si4032 transmitter IC      |
| U      | [TX continuous](#tx-continuous)   | Value Toggle   | Toggle continuous transmission mode                          |
| D      | [TX random](#tx-random)           | Value Toggle   | Toggle random transmission mode                              |
| C      | [TX carrier](#tx-carrier)         | Value Toggle   | Toggle carrier-only transmission mode                        |
| B      | [Baud Rate](#baud-rate)           | Value Entry    | Set the baud rate of the XDATA UART Interface                |
| I      | [Serial No](#serial-no)           | Value Entry    | Set the serial number of the radiosonde                      |
| R      | [Red LED info](#red-led-info)     | Action Trigger | If red led is blinking, trigger a print of the error details |
| N      | [No menu](#no-menu)               | Value Toggle   | Toggle the print of the menu item list after each interaction |
| K      | [Keep test mode](#keep-test-mode) | Value Toggle   | Toggle to keep the service menu active after a software reset |
| W      | [SW Version](#sw-version)         | Action Trigger | Trigger a print of the device status information (that is also printed on startup) |
| M      | [Measurements](#measurements)     | Action Trigger | Enter a dedicated measurements submenu                       |
| L      | [Launch/Drop](#launchdrop)        | Value Toggle   | Toggle the operating mode of the sonde into `launched` or `dropping` mode |
| E      | [Exit](#exit)                     | Action Trigger | Exit the service Menu                                        |



### Action Trigger Menu Items

These menu items don't require any additional parameters and just trigger some action, usually a printout.

#### Sensors

The sonde performs a measurement and prints the self-calculated current PTU sensor values. Radio Telemetry is paused during the measurement, usually loosing one frame of telemetry.

```latex
RH:   44.56 RHtu:  36.29 Trh:  31.40 T: 23.93 Tref:  26.69 Tmcu:  30.24 C:  47.96 Rt:  -26.21 Rts: 1088.76 Tp:  0.0633 Cp:  0.4105 Pressure: 981.51 PressureT(NTC): 29.33\r
```

| Name           | Example Value | Unit | Explanation                                                  |
| -------------- | ------------- | ---- | ------------------------------------------------------------ |
| RH             | 44.56         | %RH  | Relative Humidity, that is for sure, but I don't know the details...<br/>I can reproduce the RHtu value, but not yet the RH value.<br/>I already can say that the calculation requires the measured raw value (and the humidity sensor temperature) plus a total of 52 (!) parameters from the sonde configuration. |
| RHtu           | 36.29         | %RH  |                                                              |
| Trh            | 31.40         | °C   | Temperature measured by the built-in sensor of the humidity sensor module.<br/>Calculation requires the measured raw value and six parameters from the sonde configuration. |
| T              | 23.93         | °C   | Temperature of the main sensor at the end of the sensor boom.<br />Calculation requires the measured raw value and six parameters from the sonde configuration. |
| Tref           | 26.69         | °C   | Temperature of the Reference Area (Cutout) on the PCB which is heated to a specific temperature.<br/>It is transmitted via radio only at a coarse resolution of 1 K. |
| Tmcu           | 30.24         | °C   | Temperature of the built-in STM32 temperature sensor.<br />I cannot say for sure whether the (raw)  is transmitted by the sonde, but it seems it's not. At least the single value in the sonde configuration block that is used for MCU temperature sensor calibration has been identified. |
| C              | 47.96         | pF   | Capacitance of the humidity sensor.<br/>Calculation requires the measured raw value and two parameters from the sonde configuration. |
| Rt             | 1018.76       | Ω    | Intermediate value of the main sensor temperature calculation. It represent the the uncalibrated resistance in Ohms of the sensor.<br/>Calculation requires the measured raw value and two parameters from the sonde configuration. |
| Rts            | 1088.76       | Ω    | Intermediate value of the humidity sensor temperature calculation. It represent the the uncalibrated resistance in Ohms of the sensor.<br/>Calculation requires the measured raw value and two parameters from the sonde configuration. |
| Tp             | 0.0633        | 1    | This value (without physical unit) is derived from the temperature measurement Trh for the humidity sensor. It is a simple linear transformation that brings Tp in the range required for determining RHtu.<br/>Calculation requires the humidity sensor temperature Trh and a couple of fixed constants (no parameters used).<br/>The simple formula is:  Tp = (Trh - 20) / 180 |
| Cp             | 0.4105        | 1    | This value (without physical unit) is derived from the capacitance of the humidity sensor, and it includes calibration. It is one of the two input values (in addition to temperature) that feed the equations for relative humidity calculation.<br/>Calculation requires the humidity sensor capacitance C and two parameters from the sonde configuration. |
| Pressure       | 981.51        | hPa  | Atmospheric pressure derived from the add-on pressure sensor module measurement.<br/>Calculation requires the measured raw value and 18 parameters from the sonde configuration. |
| PressureT(NTC) | 29.33         | °C   | Temperature measured by the add-on pressure sensor module. It is used as a correction input for the pressure calculations.<br/>It is transmitted directly by the sonde (in 1/100 degrees) and requires no parameters from the sonde configuration. |

#### Frequencies

The sonde performs a measurement and prints the raw PTU sensor frequencies. Radio Telemetry is paused during the measurement, usually loosing one frame of telemetry. These are most likely the same values that are transmitted over radio in the [7A-Meas](https://github.com/bazjo/RS41_Decoding/tree/master/RS41-SGP#7A-MEAS) Block.

```latex
Uref2: 553397 U: 554854 Uref1: 484150 TUref1: 128645 TU: 184914 TUref2: 186649 Tref1: 128644 T: 202916 Tref2: 186652 Pref2: 421076 P: 322529 Pref1: 287013\r
```

#### Red LED Info

Print the current error conditions of the sonde. If any error conditions are present, the red error led of the sonde will blink.

```latex
No add-on sensor data\r
PTU failure\r
```

If no error conditions are present, the sonde will print ??? (tbd)

There are several failure modes (not a complete list)

| Error Condition         | Explanation                                                  |
| ----------------------- | ------------------------------------------------------------ |
| `No add-on sensor data` | Transmission of XDATA messages is enabled, but no messages are received via the XDATA UART. |
| `PTU failure`           | The measured frequencies of the PTU sensors are outside the acceptable range.<br />This indicates a hardware sensor boom failure (sensor boom loose or temperature sensor broken). |
| `Low battery capacity`  | The estimated energy counter of the sonde has indicated that the remaining battry capacity has fallen below a certain threshold. |
| `P-module not detected` | The radiosonde model is`-SGP`, but the barometric pressure module could not be detected. |

#### SW version

Trigger a print of the device status information (that is also printed on startup).

```latex
\r
Vaisala RS41 Radiosonde SW V2.02.14\r
Copyright (c) Vaisala Oyj 2016. All rights reserved.\r
Serial number: P0110001\r
Pressure module serial number: P0110001 SW V2.01\r
Transmitter frequency: 403.00 MHz\r
Transmitter power: 3/7\r
```

#### Measurements

Enter the Measurements submenu. This is complete submenu inside the service menu, which can be exited by Exit (`E\r`) within the submenu.

```latex
\r
(S)ensors     Fre(q)uencies  S(W) reset       (D)efault params  (U)se sensor\r
(R)eg offset  Reg (c)heck    (T) self-check   St(o)p sequence   (H)eat ref\r
(G)PS         (N)MEA         D(I)rect GPS mode (E)xit\r
>\r

```

#### Exit

Exit the service Menu. No additional output is printed before exiting.

### Value Toggle Menu Items

These menu items don't require additional parameters and cycle through different configuration options. Unfortunately, the current configuration usually cannot be queried, at least not through the menu entry, without advancing one option.

#### TX Mode Menu Entries

These Menu items all control the state of the Transmission and enable various diagnostic modes. Some of those modes (especially TX Random and TX carrier) weirdly depend on the other states.

##### TX State

Toggle the TX States. 

Possible states are:

* `TX enabled`
* `TX disabled`

##### TX Continuous

Toggle the transmission of the carrier during the time in between frames. 

The TX State has no influence on this state. The continuous mode setting will be stored while the TX State is `TX disabled`.

Possible states are:

* `TX in continuous mode`
* `TX in normal mode`

##### TX Random

Possible states are:

* `TX in continuous mode (random data)`
* `TX in normal mode`

##### TX Carrier

Possible states are:

* `TX in carrier only mode`
* `TX in normal mode`

#### No menu

Toggle printing the menu items after each menu interaction. After sending `N` and receiving the echo, no additional information about the current state of this value will be provided,

With the mode enabled, a menu interaction will look like this

```latex
➜ R
R\r
No add-on sensor data\r
PTU failure\r
```

Possible states are:

* No menu enabled
* No menu disabled

#### Keep test mode

Once enabled will keep the serial client within the service menu after a reset. When a restart in this mode is performed, the red error led will stay lit until disabled.

Possible states are:

* `Keep test mode disabled`
* `Keep test mode enabled`

#### Launch/Drop

Manually overrides the sounding state detection/advancement based on the GNSS data. This makes it possible to simulate the behaviour of the sonde through an entire sounding without using simulated GNSS data. You are only able to cycle through each state once during a power cycle, so returning to 'not lauched' after `dropping ` is not possible.

Possible states are:

* not launched - this mode is active after startup and is not accessible once in the other modes

* `launched` - normally enabled after passing a certain height following release
* `dropping` - normally enabled once the altitude drops more than a certain threshold after release

### Value Entry Menu Items

#### Parameter

```latex
➜ P
P\r
Data ID >
➜ 480\r
480\r
Value 4093 >
➜ 9089\r
9089\r
```

Allows to read/write various parameters using the Data ID as a selector.

The example resets the remaining battery capacity to its default of 9089 Wh.

It is not exactly known if the Data ID has any additional meaning. It is entered as ASCII encoded hex and only certain hex values are valid.

| Data ID | Example Value | Muteable | Comment                                                      |
| :------ | :------------ | :------- | :----------------------------------------------------------- |
| `10`    | 5             | *        |                                                              |
| `20`    | 14            | *        | Bit field, bits [3:0] are used. 14: 3=1,2=1,1=1,0=0 <br />Bit 0: Enables the use of the pressure sensor (if installed) <br />Bit 1: <br />Bit 2: <br />Bit 3: Enables GPS (to be confirmed...) |
| `30`    | 0             | *        |                                                              |
| `40`    | 0             | *        |                                                              |
| `45`    | S0341201      | *        | Serial number                                                |
| `50`    | RS41-SG       | *        | RS41 model                                                   |
| `60`    | 20215         | ---      | Firmware version (V2.02.15)                                  |
| `70`    | 9089          | *        | Battery capacity in mWh at startup. Fresh batteries have 9089 mWh. Updated by controlled shutdown. |
| `80`    | 4             | ---      | ublox GPS Module Hardware Version, upper half (**0004**0005) |
| `90`    | 5             | ---      | ublox GPS Module Hardware Version, lower half (0004**0005**) |
| `A0`    | 703           | ---      | ublox GPS Module Software Version (703 = SW Version 7.03)    |
| `B0`    |               | ---      | ublox GPS Module Software Build Number                       |
| `C0`    | 6             | ---      | Radio Version. Content of Si4032 register 01h                |
| `D0`    | 600           | *        | Height [m] above launch site to which RS41 must climb before it is in flight mode. |
| `E0`    | 18            | *        | Low-battery voltage threshold [100 mV] below which sonde will shut down (if condition exists for some time). 18 = 1.8V |
| `100`   | 180           |          |                                                              |
| `110`   | 60            |          |                                                              |
| `120`   | 1700          |          |                                                              |
| `130`   | 20            |          | Target temperature in °C for PCB reference area heating      |
| `140`   | 135           |          | Threshold for low battery capacity detection. (Unit unclear; might be "Wmin") |
| `150`   | 50            |          |                                                              |
| `160`   | 1             |          | Parameter setup done (1=true 0=false)                        |
| `170`   | RSM412        |          | PCB Type                                                     |
| `180`   | R4550425      |          | PCB Serial                                                   |
| `190`   | 0000000000    |          |                                                              |
| `1A0`   |               |          |                                                              |
| `1A8`   |               |          |                                                              |
| `1B0`   |               |          |                                                              |
| `1B8`   |               |          |                                                              |
| `1C0`   |               |          |                                                              |
| `1C8`   |               |          |                                                              |
| `1D0`   |               |          |                                                              |
| `1D5`   |               |          |                                                              |
| `1D8`   |               |          |                                                              |
| `1E0`   |               |          |                                                              |
| `200`   | 29            | ---      | Current battery voltage [100 mV]. 29 = 2.9V                  |
| `210`   | 0             | ---      |                                                              |
| `220`   | 41            | ---      | Current CPU temperature [°C]                                 |
| `230`   | 48            | ---      | Current radio (Si4032) temperature [°C]                      |
| `240`   | 1             | ---      |                                                              |
| `250`   | 42            | ---      | Current reference area temperature [°C]                      |
| `255`   |               |          | Status (current duty cycle 0...1000) of humidity sensor heating |
| `260`   | 264           | ---      | Remaining battery capacity (unit Wmin?)                      |
| `270`   | 90            | ---      |                                                              |
| `280`   | 90            | ---      |                                                              |
| `290`   | 1.4258246     | ---      | Calibration for CPU temperature sensor [V]. This is the voltage that the sensor delivers @ 25°C. |
| `2A0`   |               |          |                                                              |
| `2B0`   | 0             |          | Current TX power (0...7)                                     |
| `2C0`   |               |          |                                                              |
| `2D0`   |               |          |                                                              |
| `2E0`   |               |          |                                                              |
| `2F0`   |               |          |                                                              |
| `300`   | 7             | ---      |                                                              |
| `310`   | 4             | ---      |                                                              |
| `320`   | 64            | ---      |                                                              |
| `330`   | 4             | ---      |                                                              |
| `400`   | 32640         | *        | TX frequency (f = 400.00 + 32640 / 6400 = 405.10 MHz). Stored as a 16-bit unsigned. <br />The formula assumes a 30MHz clock, but actually the radio runs with a 26MHz clock, <br />and the physically possible frequency range is 398.666666MHz...407.333333MHz. |
| `410`   | 3             | *        | TX power setting [0...7] in start phase. RS41 seems to always switch to level 7 in flight mode. |
| `420`   |               |          |                                                              |
| `430`   | 65535         |          | Maximum # frames in flight mode (flight time kill). 65535=OFF |
| `440`   |               |          |                                                              |
| `450`   | 0             | *        | Burst Kill. 0=OFF, 1=ON                                      |
| `455`   | 30600         | *        | # TX frames left after burst kill (this is a wild guess...)  |
| `460`   |               |          |                                                              |
| `470`   |               |          |                                                              |
| `480`   | 9089          | *        | Initial battery capacity at startup [mWh]. Default is 9089 mWh. ??? |
| `490`   | 1000          |          | Probably the factor between Watt and Milliwatt. Don't change... |
| `4A0`   | 0             | *        | XDATA protocol. 0=disabled, 1=enabled                        |
| `570`   | 1.23....      | *        | T sensor calibration ("Alpha")                               |
| `5A0`   | 45.79...      | *        | U sensor calibration (calibU[0])                             |
| `5B0`   | 4.96...       | *        | U sensor calibration (calibU[1])                             |
| `630`   | 1.24...       | *        | TU sensor (humidity sensor temperature) calibration ("Alpha") |
| `660`   |               |          |                                                              |
| `670`   |               |          |                                                              |
| `680`   |               |          |                                                              |
| `690`   |               |          |                                                              |
| `6A0`   |               | *        | Under yet unknown conditions this value can be used instead of calibU[0] (humidity sensor calibration) |
| `6B0`   |               |          |                                                              |
| `6C0`   |               |          |                                                              |
| `7C0`   |               |          |                                                              |
| `7D0`   |               |          |                                                              |
| `7E0`   |               |          |                                                              |
| `7F0`   |               |          |                                                              |
| `800`   |               |          |                                                              |
| `810`   |               |          |                                                              |
| `820`   |               |          |                                                              |
| `830`   |               |          |                                                              |
| `840`   |               |          |                                                              |
| `850`   |               |          |                                                              |
| `860`   | 979.1...      | *        | Pressure [hPa] at launch site?? (See ID 870)                 |
| `870`   | 979.8...      | *        | Pressure [hPa] at launch site?? (See ID 860)                 |
| `E00`   |               |          |                                                              |
| `E01`   |               |          |                                                              |
| `E02`   |               |          |                                                              |
| `E03`   |               |          |                                                              |

#### Alfa

```latex
➜ A
A\r
Temperature >
➜ 22.4\r
22.4\r
Alfa:Humidity alfa  1.2354\r
Alfa:T alfa -50.6420\r
```

**WARNING: This will probably mess with the calibration data!** 

Allows entering the actual temperature for calibration. No detail are known about the exact purpose of this setting

#### TX Power

```latex
➜ O
O\r
TX power (0-7) 0 >
➜ 7\r
7\r
```

The sonde prints the current TX power (`0` in the example) and accepts a new one. This power setting is only used while the sonde is not in `launched` mode.

TX power measured with a direct attached SMA-connector on the PCB in "TX continuous" mode relates to the set values like this

| TX Power Setting | TX Power |
| ---------------- | -------- |
| 0                | -1,9 dBm |
| 1                | 1,1 dBm  |
| 2                | 3,3 dBm  |
| 3                | 6,8 dBm  |
| 4                | 9,9 dBm  |
| 5                | 13,3 dBm |
| 6                | 16,2 dBm |
| 7                | 18,8 dBm |

#### TX Frequency

```latex
➜ F
F\r
TX frequency  403.00 >
➜ 405.00\r
405.00\r
```

The sonde prints the current TX frequency (`403.00 MHz` in the example) and accepts a new one. Only frequencies within the range `400.00 .. 405.99 MHz` are allowed and the provided value will be rounded to the nearest 10 kHz.

#### TX Registers

```latex
➜ T
T\r
Register number (00-7F) >
➜ 75\r
75\r
Register value 4F >
➜ 61\r
61\r
```

Allows to read/write registers of the Si4032 Transmitter IC directly. Obviously, these values are only retained until the sondes regular firmware accesses them directly.

It is possible to change the frequency of the sonde temporarily this way.

#### Baud Rate

```latex
➜ B
B\r
Baud rate (0=9600, 1=19200, 2=38400, 3=57600, 4=115200) 0 >
➜ 4\r
4\r
```

The sonde prints the current Baud Rate of UART interface (`9600 Baud` in the example) and accepts a new one, which is applied directly after the parameter was echoed back. It has not been tested how this interferes with providing XDATA messages to the sonde.

| Baud Rate Setting | Baud Rate |
| ----------------- | --------- |
| 0                 | 9600      |
| 1                 | 19200     |
| 2                 | 38400     |
| 3                 | 57600     |
| 4                 | 115200    |

#### Serial No

```latex
➜ I
I\r
Serial number P0110001 >\r
➜ TestTest\r
TestTest\r
```

The sonde prints it's current serial number and allows you to set a new one, which can be any 1-8 character long ASCII String (Actually, any binary data can be provided and will be stored). If more than 8 characters are provided, the last ones will be omitted.

## Measurements Submenu Items

| Letter | Name                                          | Menu item type | Description                                                  |
| ------ | --------------------------------------------- | -------------- | ------------------------------------------------------------ |
| S      | [Sensors](#sensors-measurements-menu)         | Value Entry    | Print a repeating PTU sensor print at a specified period     |
| Q      | [Frequencies](#frequencies-measurements-menu) | Value Entry    | Print a repeating PTU sensor print (measuerd frequencies) at a specified period |
| W      | [SW reset](#sw-reset)                         | Action Trigger | Trigger a software reset                                     |
| D      | [Default params](#default-params)             | Value Entry    | After a confirmation, reset the sonde to factory settings, (without any calibration?) |
| U      | [Use Sensor](#use-sensor)                     | Value Entry    | ?                                                            |
| R      | [Reg Offset](#reg-offset)                     | Action Trigger | Start a humidity sensor regeneration and update the offset value at the zero humidity point |
| C      | [Reg Check](#reg-check)                       | Action Trigger | Start a humidity sensor regeneration and check validity of a previously obtained offset value |
| T      | [T self-check](#t-self-check)                 | Action Trigger | Start a test procedure where the main temperature sensor is compared to the humidity temperature sensor |
| O      | [Stop sequence](#stop-sequence)               | Action Trigger | Terminate a running calibration process                      |
| H      | [Heat ref](#heat-ref)                         | Value Toggle   | Change the control parameters of the PCB reference heating   |
| G      | [GPS](#gps)                                   | Value Entry    | Specify and print a repeating printout of the GPS Values     |
| N      | [NMEA](#nmea)                                 | Action Trigger | Set the GPS in NMEA mode and relay its data                  |
| I      | [Direct GPS Mode](#direct-gps-mode)           | Action Trigger | Bidirectionally relay the GPS data, enabling direct communication to the GPS |
| E      | [Exit](#exit-measurements-menu)               | Action Trigger | Exit back to the main service menu                           |

### Action Trigger Menu Items

These menu items don't require any additional parameters and just trigger some action, usually a printout.

#### SW Reset

Triggers a software reset. After a software reset, the number of previous software rest will be included in the SW version printed on startup.

#### Reg offset

The humidity sensor will be heated to approx. 170 °C to set the zero humidity offset value. This will take few minutes without any message when finished.

**WARNING: You may burn yourself while touching the sensor during regeneration!**

Make sure to not cover the humidity sensor with any liquids or dirt as calibration result will cause  inaccurate readouts.

You can observe the regeneration procedure with the Sensor menu item `S`. You can observe both the RH sensor temperature rising and the RH going down. When the regeneration procedure is complete, the RH sensor heating resistor is turned off and the sensor will cool back to room temperature.

#### Reg check

The same procedure as with [Reg offset](#reg-offset) is performed, however the offset is not stored as the zero humidity calibration, but the obtained value will be compared to the current value. If the deviation is less than 2 %, the regeneration test passes, else it fails. The result is printed after regeneration is complete, no matter which menu interaction is currently performed.

Possible Results are (only numeric example values):

* `U offset error: 1.73 - OK\r\r`
* `U offset error: 5.11 - Failed!\r\r`

#### T self-check

A temperature sensor self test will be performed, where the temperature of the main temperature sensor is compared to the temperature of the humidity temperature sensor. The result is printed after the test is complete, no matter which menu interaction is currently performed.

Possible Results are (only numeric example values):

* `T difference: -0.56 - OK\r\r`
* `T difference: 4.39 - Failed!\r\r`

#### Stop sequence

Any current test/calibration procedure ([Reg offset](#reg-offset), [Reg check](#reg-check), [T self check](#t-self-check)) will be aborted.

#### NMEA

Restarts the GPS receiver, configures it to output NMEA messages and relays those to the XDATA serial port. While this mode is active, the radio will be turned off.

The NMEA sentences `RMC`, `VTG`, `GGA`, `GSA`, `GSV`, `GLL` and `ZDA` with the Talker ID `GP` are provided in a 1 Hz interval.

Additional `TXT` sentences are provided containing the u-blox Information messages.

This mode can be exit by triggering an `W` [SW reset](#sw-reset) at any time. Sometimes, the radiosonde will lock up and trigger a software reset by itself.

#### Direct GPS Mode

This mode is the same as the [NMEA](#nmea) mode, but in addition the user input on the XDATA serial port is also relayed to the GPS receiver, allowing direct control.

This mode can not be exit and a power cycle is the only way to restore normal functionality.

#### Exit (Measurements Menu)

Exits the measurements submenu, bringing the user back to the service menu. The List of service menu items is printed if enabled.

### Value Toggle Menu Items

These menu items don't require additional parameters and cycle through different configuration options. Unfortunately, the current configuration usually cannot be queried, at least not through the menu entry, without advancing one option.

#### Heat ref

Sets the control parameters for the PCB reference area (cut-out), which is comprised of a thermistor and heating resistors.

Possible values are:

* `Heat ref is NORMAL` (default)
* `Heat ref is HIGH`
* `Heat ref is LOW`

### Value Entry Menu items

#### Sensors (Measurements Menu)

```latex
➜ S
S\r
Period 1.0 >
➜ 1.0\r
1.0\r
\r
Press any key to stop\r
\r
RH:   44.56 RHtu:  36.29 Trh:  31.40 T: 23.93 Tref:  26.69 Tmcu:  30.24 C:  47.96 Rt:  -26.21 Rts: 1088.76 Tp:  0.0633 Cp:  0.4105 Pressure: 981.51 PressureT(NTC): 29.33\r
RH:   44.56 RHtu:  36.29 Trh:  31.40 T: 23.93 Tref:  26.69 Tmcu:  30.24 C:  47.96 Rt:  -26.21 Rts: 1088.76 Tp:  0.0633 Cp:  0.4105 Pressure: 981.51 PressureT(NTC): 29.33\ru
```

The same information as with [Sensors](#sensors) in the main menu are provided in a variable time interval. While the mode is active, radio telemetry is silenced.

The mode can be exit by sending any character to the sonde, which is not echoed back.

#### Frequencies (Measurements Menu)

```latex
➜ Q
Q\r
Period 1.0 >
➜ 1.0\r
1.0\r
\r
Press any key to stop\r
Uref2: 553397 U: 554854 Uref1: 484150 TUref1: 128645 TU: 184914 TUref2: 186649 Tref1: 128644 T: 202916 Tref2: 186652 Pref2: 421076 P: 322529 Pref1: 287013\r
Uref2: 553397 U: 554854 Uref1: 484150 TUref1: 128645 TU: 184914 TUref2: 186649 Tref1: 128644 T: 202916 Tref2: 186652 Pref2: 421076 P: 322529 Pref1: 287013\r
```

The same information as with [Frequencies](#frequencies) in the main menu are provided in a variable time interval. While the mode is active, radio telemetry is silenced.

The mode can be exit by sending any character to the sonde, which is not echoed back.

#### Default params

```➜ Q
➜ D\r
Are you sure? (Y/N)  N >
➜ N\r
N\r
```

After a confirmation, resets the sonde to factory settings. Probably the calibration data will also be lost.

#### Use sensor

```➜ Q
➜ U\r
Sensor (0=none, 1=U, 2=Ur2, 3=Ur1, 4=Tr1, 5=Tr2, 6=TU, 7=T, 8=TUr1, 9=TUr2, 10=all) 10 >
➜ 1\r
1\r
```

Sets the active sensor for the Frequency readouts, setting all other frequencies to zero. `10` is the default setting. 

For the `-SGP` model, pressure sensor frequencies are not affected with this setting.

The exact purpose oh this setting is not known.

#### GPS

```➜ Q
➜ G\r
GPS printout (0=None, 1=Raw, 2=Calculated, 3=Both) 3 >
➜ 2\r
2\r
```

Controls debug output of the GPS data interpreted by the sonde, which is transmitted in the [7C-GPSINFO](https://github.com/bazjo/RS41_Decoding/tree/master/RS41-SGP#7C-GPSINFO),  [7D-GPSRAW](https://github.com/bazjo/RS41_Decoding/tree/master/RS41-SGP#7D-GPSRAW) and [7B-GPSPOS](https://github.com/bazjo/RS41_Decoding/tree/master/RS41-SGP#7B-GPSPOS) Blocks over radio.

The output is printed every second (provided a sufficient baud rate) while the menu is still active and other menu items can be interacted with. To disable the output, `G0\r`has to be sent.

Example Raw output:

```
sv 42 mqi 7 str 0 minpr 12345678 agc mon 7 jamming 0 proff 123456789 delta 12345 doppler 1234.123456\r
sv 43 mqi 7 str 0 minpr 12345678 agc mon 7 jamming 0 proff 123456789 delta -12345 doppler -1234.123456\r
sv 44 mqi 7 str 0 minpr 12345678 agc mon 7 jamming 0 proff 123456789 delta 12345 doppler 1234.123456\r
sv 45 mqi 7 str 0 minpr 12345678 agc mon 7 jamming 0 proff 123456789 delta -12345 doppler -1234.123456\r
sv 46 mqi 7 str 0 minpr 12345678 agc mon 7 jamming 0 proff 123456789 delta 12345 doppler 1234.123456\r
sv 47 mqi 7 str 0 minpr 12345678 agc mon 7 jamming 0 proff 123456789 delta -12345 doppler -1234.123456\r
\r
```

Example Calculated output:

```sv 42 mqi 7 str 0 minpr 12345678 agc mon 7 jamming 0 proff 123456789 delta 12345 doppler 1234.123456\r
wk 4269 tow 42699000 x 123456789 y 123456789 z 123456789 vx -41 vy 43 vz -23 nsv 8 acc 8 pdop 19\r
\r
```

With option `3=Both`, both outputs are appended, but the trailing `\r` from the Raw output is omitted. 
