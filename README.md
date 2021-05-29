# Home Assistant Addon: Alpha ESS to MQTT
## A simple way to get the current monitoring data from [alphaess.com](https://alphaess.com) via MQTT

## About

This Addon is based on the reverse engineered API alphaess.com uses to show your current metrics on their web interface / mobile app. The obtained data that is sent via MQTT to the configured broker (or directly to the Home Assistant instance this addon is running on).

## Installation

1. Add `https://github.com/DasLetzteEinhorn/AlphaESS_Monitor_Hass` as a new repository.
2. Install the Addon
3. Add your Username and Password (used on the alphaess.com webinterface) in the corresponding fields and save your configuration.
4. Start the Addon

## Configuration

Default configuration:

```yaml
log_level: info
base_topic: alphaess
timeout: 60
username: <your username>
password: <your password>
```

By default, the addon connects to your Home Assistant's broker (e.g. [Mosquitto](https://github.com/home-assistant/addons/blob/master/mosquitto/DOCS.md)), on which the addon is installed. If the broker is installed somewhere else, the following settings must be added:

```yaml
mqtt_host: <your host>
mqtt_port: <your port, default 1883>
mqtt_username: <your mqtt username>
mqtt_password: <your mqtt password>
```

If everything is configured correctly and no errors appear in the log, you can listen on `alphaess/#` for your first data.

By default, you should receive data for all available serial numbers. If you want to specify only serial numbers (e.g. you have multiple systems in your account), you can do this by adding the following lines to your config (currenty untested, if this doesn't work, please open an issue):

```yaml
serial_numbers:
  - <serial number 1>
  - <serial number 2>
```

To get your specific serial numbers you can either look them up in the Alpha ESS Dashboard or extract them from the first mqtt responses if you already configured and started the addon correctly.

Currently the addon only delivers all available metrics. Maybe we add the automatic creation of sensors in the future. For now, I use the following package (please refer to  [Packages Documentation](https://www.home-assistant.io/docs/configuration/packages/)):

<details>
  <summary>alphaess.yaml</summary>

```yaml
sensor:

  - platform: mqtt
    name: "Solar Grid I/O L1"
    icon: mdi:transmission-tower
    state_topic: "alphaess/<serial number>"
    unit_of_measurement: 'W'
    value_template: "{{ value_json.pmeter_l1 }}"
  
  - platform: mqtt
    name: "Solar Grid I/O L2"
    icon: mdi:transmission-tower
    state_topic: "alphaess/<serial number>"
    unit_of_measurement: 'W'
    value_template: "{{ value_json.pmeter_l2 }}"

  - platform: mqtt
    name: "Solar Grid I/O L3"
    icon: mdi:transmission-tower
    state_topic: "alphaess/<serial number>"
    unit_of_measurement: 'W'
    value_template: "{{ value_json.pmeter_l3 }}"

  - platform: template
    sensors:
      solar_grid_i_o_total:
        friendly_name: "Solar Grid I/O Total"
        # icon: mdi:transmission-tower
        unit_of_measurement: 'W'
        value_template: "{{ states('sensor.solar_grid_i_o_l1') | float + states('sensor.solar_grid_i_o_l2') | float + states('sensor.solar_grid_i_o_l3') | float }}"

  - platform: mqtt
    name: "Solar Generation"
    state_topic: "alphaess/<serial number>"
    value_template: "{{ value_json.ppv1 + value_json.ppv2 + value_json.pmeter_dc }}"
    unit_of_measurement: 'W'
    icon: mdi:solar-panel-large

  - platform: mqtt
    name: "Solar Battery SOC"
    state_topic: "alphaess/<serial number>"
    unit_of_measurement: '%'
    icon: mdi:battery
    value_template: "{{ value_json.soc }}"

  - platform: mqtt
    name: "Solar Battery I/O"
    state_topic: "alphaess/<serial number>"
    unit_of_measurement: 'W'
    icon: mdi:battery
    value_template: "{{ value_json.pbat }}"
```
</details>

The received data should look something like this:
<details>
  <summary>example data</summary>

```json
{
    "_id": "<some ID>",
    "createtime": "<some timestamp>",
    "uploadtime": "<some timestamp>",
    "sn": "<some serial number>",
    "ppv1": 1151,
    "ppv2": 1302,
    "ppv3": null,
    "preal_l1": 362,
    "preal_l2": 0,
    "preal_l3": 0,
    "pmeter_l1": -247,
    "pmeter_l2": -84,
    "pmeter_l3": 324,
    "pmeter_dc": 926,
    "soc": 86,
    "factory_flag": 0,
    "pbat": -1908.2,
    "sva": 524,
    "varac": 0,
    "vardc": 0,
    "ev1_power": 0,
    "ev1_chgenergy_real": 0,
    "ev1_mode": 0,
    "ev2_power": 0,
    "ev2_chgenergy_real": 0,
    "ev2_mode": 0,
    "ev3_power": 0,
    "ev3_chgenergy_real": 0,
    "ev3_mode": 0,
    "ev4_power": 0,
    "ev4_chgenergy_real": 0,
    "ev4_mode": 0,
    "poc_meter_l1": 0,
    "poc_meter_l2": 0,
    "poc_meter_l3": 0
}
```
</details>

## Notes
Until we figure out how to create the image with github actions, the addon needs to be built on your machine. If you reading this know anything about this, help is appreciated :)
  
  If you have any suggestions, found some bugs or simply need help with this addon, feel free to [open an issue](https://github.com/DasLetzteEinhorn/AlphaESS_Monitor_Hass/issues/new).

# Credits
Almost the entire code comes from the brain and fingers of [MarioCakeDev](https://github.com/MarioCakeDev). If you like this addon, you can leave him a small [donation](http://paypal.me/DavidPayLein).
