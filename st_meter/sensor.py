from esphome.components.atm90e32.sensor import CONF_PHASE_A, CONF_PHASE_B, CONF_PHASE_C
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, modbus
from esphome.const import (
    CONF_ACTIVE_POWER,
    CONF_CURRENT,
    CONF_FREQUENCY,
    CONF_ID,
    CONF_POWER_FACTOR,
    CONF_REACTIVE_POWER,
    CONF_VOLTAGE,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_POWER_FACTOR,
    DEVICE_CLASS_VOLTAGE,
    ICON_CURRENT_AC,
    ICON_FLASH,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
    UNIT_AMPERE,
    UNIT_DEGREES,
    UNIT_HERTZ,
    UNIT_KILOVOLT_AMPS_REACTIVE_HOURS,
    UNIT_KILOWATT_HOURS,
    UNIT_VOLT,
    UNIT_VOLT_AMPS,
    UNIT_VOLT_AMPS_REACTIVE,
    UNIT_WATT,
)

CONF_TOTAL_ACTIVE_ELECTRICITY_POWER = "total_active_electricity_power"
CONF_TOTAL_REACTIVE_ELECTRICITY_POWER = "total_reactive_electricity_power"
CONF_TOTAL_ACTIVE_POWER = "total_active_power"
CONF_TOTAL_REACTIVE_POWER = "total_reactive_power"


AUTO_LOAD = ["modbus"]
CODEOWNERS = ["@polyfaces", "@jesserockz", "@lemurs"]

st_meter_ns = cg.esphome_ns.namespace("st_meter")
STMeter = st_meter_ns.class_("STMeter", cg.PollingComponent, modbus.ModbusDevice)

PHASE_SENSORS = {
    CONF_VOLTAGE: sensor.sensor_schema(
        unit_of_measurement=UNIT_VOLT,
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_VOLTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    CONF_CURRENT: sensor.sensor_schema(
        unit_of_measurement=UNIT_AMPERE,
        accuracy_decimals=3,
        device_class=DEVICE_CLASS_CURRENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    CONF_ACTIVE_POWER: sensor.sensor_schema(
        unit_of_measurement=UNIT_WATT,
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    CONF_REACTIVE_POWER: sensor.sensor_schema(
        unit_of_measurement=UNIT_VOLT_AMPS_REACTIVE,
        accuracy_decimals=2,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    CONF_POWER_FACTOR: sensor.sensor_schema(
        accuracy_decimals=3,
        device_class=DEVICE_CLASS_POWER_FACTOR,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
}

PHASE_SCHEMA = cv.Schema(
    {cv.Optional(sensor): schema for sensor, schema in PHASE_SENSORS.items()}
)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(STMeter),
            cv.Optional(CONF_PHASE_A): PHASE_SCHEMA,
            cv.Optional(CONF_PHASE_B): PHASE_SCHEMA,
            cv.Optional(CONF_PHASE_C): PHASE_SCHEMA,
            cv.Optional(CONF_FREQUENCY): sensor.sensor_schema(
                unit_of_measurement=UNIT_HERTZ,
                icon=ICON_CURRENT_AC,
                accuracy_decimals=3,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_TOTAL_ACTIVE_POWER): sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT_HOURS,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_ENERGY,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            cv.Optional(CONF_TOTAL_ACTIVE_ELECTRICITY_POWER): sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT_HOURS,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_ENERGY,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            cv.Optional(CONF_TOTAL_REACTIVE_POWER): sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOVOLT_AMPS_REACTIVE_HOURS,
                accuracy_decimals=2,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            cv.Optional(CONF_TOTAL_REACTIVE_ELECTRICITY_POWER): sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOVOLT_AMPS_REACTIVE_HOURS,
                accuracy_decimals=2,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
        }
    )
    .extend(cv.polling_component_schema("10s"))
    .extend(modbus.modbus_device_schema(0x01))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await modbus.register_modbus_device(var, config)


    if CONF_FREQUENCY in config:
        sens = await sensor.new_sensor(config[CONF_FREQUENCY])
        cg.add(var.set_frequency_sensor(sens))

    if CONF_TOTAL_ACTIVE_POWER in config:
        sens = await sensor.new_sensor(config[CONF_TOTAL_ACTIVE_POWER])
        cg.add(var.set_total_active_power_sensor(sens))

    if CONF_TOTAL_ACTIVE_ELECTRICITY_POWER in config:
        sens = await sensor.new_sensor(config[CONF_TOTAL_ACTIVE_ELECTRICITY_POWER])
        cg.add(var.set_total_active_electricity_power_sensor(sens))

    if CONF_TOTAL_REACTIVE_POWER in config:
        sens = await sensor.new_sensor(config[CONF_TOTAL_REACTIVE_POWER])
        cg.add(var.set_total_reactive_power_sensor(sens))

    if CONF_TOTAL_REACTIVE_ELECTRICITY_POWER in config:
        sens = await sensor.new_sensor(config[CONF_TOTAL_REACTIVE_ELECTRICITY_POWER])
        cg.add(var.set_total_reactive_electricity_power_sensor(sens))

    for i, phase in enumerate([CONF_PHASE_A, CONF_PHASE_B, CONF_PHASE_C]):
        if phase not in config:
            continue

        phase_config = config[phase]
        for sensor_type in PHASE_SENSORS:
            if sensor_type in phase_config:
                sens = await sensor.new_sensor(phase_config[sensor_type])
                cg.add(getattr(var, f"set_{sensor_type}_sensor")(i, sens))
