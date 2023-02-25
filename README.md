# st-meter
DTS6619-017 energy metter by SINOTIMER

ESPHome library

Librory for receiving data via ModBus RTU rs485 from the energy meter by SINOTIMER DTS6619-017 counter (and similar super duper Chinese ones)+rs485 to TTL+ESP8266. 
It could be integrated to a smart home or just stare as a web page with current data.
Teste on 3 phase energy metter.

Example in YAML:

uart:
  rx_pin: D2
  tx_pin: D1
  baud_rate: 9600 #if your energy meter is SDM230M or SDM120M than change the baud_rate: 2400
  parity: EVEN
  stop_bits: 1

modbus:
  flow_control_pin: D4

sensor:
  - platform: st_meter
    phase_a:
      current:
        name: "phase A Current"
      voltage:
        name: "phase A Voltage"
      active_power:
        name: "phase A Power"
      power_factor:
        name: "phase A Power Factor"
      reactive_power:
        name: "phase A Reactive Power"
    phase_b:
      current:
        name: "phase B Current"
      voltage:
        name: "phase B Voltage"
      active_power:
        name: "phase B Power"
      power_factor:
        name: "phase B Power Factor"
      reactive_power:
        name: "phase B Reactive Power"
    phase_c:
      current:
        name: "phase C Current"
      voltage:
        name: "phase C Voltage"
      active_power:
        name: "phase C Power"
      power_factor:
        name: "phase C Power Factor"
      reactive_power:
        name: "phase C Reactive Power"
    frequency:
      name: "Frequency"
    total_active_power:
      name: "Total Active Power"
    total_active_electricity_power:
      name: "Total Active Electricity Power"
    total_reactive_power:
      name: "Total Reactive Power"
    total_reactive_electricity_power:
      name: "Total Reactive Electricity Power"
    update_interval: 10s

![energy_metter](https://user-images.githubusercontent.com/75520956/221355320-505307ea-e2f1-496f-99da-437b1421b627.jpg)
![STMetter](https://user-images.githubusercontent.com/75520956/221355321-ed0e3c2d-2868-4eba-8697-b4e419542620.jpg)
