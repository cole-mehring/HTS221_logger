#!/usr/bin/python

import smbus
import time

def twos_comp(val,bits):
    if (val & (1 << (bits-1))) !=0:
        val = val - (1 << bits)
    return val

#Using I2C channel 1 here
bus = smbus.SMBus(1)

#Device address
DEVICE_ADDRESS = 0x5F

#Register addresses
WHO_AM_I = 0x0F
AV_CONF = 0x10
CTRL_REG1 = 0x20
CTRL_REG2 = 0x21
CTRL_REG3 = 0x22
STATUS_REG =0x27
HUMIDITY_ADDRESS_L = 0x28
HUMIDITY_ADDRESS_H = 0x29
TEMPERATURE_ADDRESS_L = 0x2A
TEMPERATURE_ADDRESS_H = 0x2B

#Register addresses for calibration registers
CALIBRATION_H0 = 0x30
CALIBRATION_H1 = 0x31
CALIBRATION_T0 = 0x32
CALIBRATION_T1 = 0x33
CALIBRATION_TMSB = 0x35 #Bits 3:2 are T1 MSB, 1:0 are T0 MSB
H0_T0_OUT_L = 0x36
H0_T0_OUT_H = 0x37
H1_T1_OUT_L = 0x3A
H1_T1_OUT_H = 0x3B
T0_OUT_L = 0x3C
T0_OUT_H = 0x3D
T1_OUT_L = 0x3E
T1_OUT_H = 0x3F

#power on device
bus.write_byte_data(DEVICE_ADDRESS, CTRL_REG1, 0x80)

#max out number of samples for internal average
bus.write_byte_data(DEVICE_ADDRESS, AV_CONF, 0x3F)

#do a conversion, one shot
bus.write_byte_data(DEVICE_ADDRESS, CTRL_REG2, 0x1) #bit 1 indicates one shot
time.sleep(0.05) #100ms should give enough time for conversion
bus.read_byte_data(DEVICE_ADDRESS, CTRL_REG2) #read back, if 0 the conversion is done#power on device

#conversion is done, grab registers for temperature
raw_temp_L=bus.read_byte_data(DEVICE_ADDRESS, TEMPERATURE_ADDRESS_L)
raw_temp_H=bus.read_byte_data(DEVICE_ADDRESS, TEMPERATURE_ADDRESS_H)
calib_temp_meas_0_L=bus.read_byte_data(DEVICE_ADDRESS, T0_OUT_L)
calib_temp_meas_0_H=bus.read_byte_data(DEVICE_ADDRESS, T0_OUT_H)
calibrated_value_0_LSB=bus.read_byte_data(DEVICE_ADDRESS, CALIBRATION_T0)
calibrated_value_1_LSB=bus.read_byte_data(DEVICE_ADDRESS, CALIBRATION_T1)
calibrated_values_MSB=bus.read_byte_data(DEVICE_ADDRESS, CALIBRATION_TMSB)
calib_temp_meas_1_L=bus.read_byte_data(DEVICE_ADDRESS, T1_OUT_L)
calib_temp_meas_1_H=bus.read_byte_data(DEVICE_ADDRESS, T1_OUT_H)

#do some math on the registers to get temp
#prep variables: shift high byte over 8, logical or the two to concatenate
raw_temp=twos_comp((raw_temp_H <<8) | raw_temp_L, 16) #interpret as twos comp
calib_temp_meas_0 = (calib_temp_meas_0_H <<8) | calib_temp_meas_0_L
calib_temp_meas_1 = (calib_temp_meas_1_H <<8) | calib_temp_meas_1_L

#grab most significant bits from calibrated values, concat onto registes, divide by 8
calib_temp_value_0 = (((calibrated_values_MSB & 0b0011) << 8) | calibrated_value_0_LSB) >>3
calibrated_value_1 = (((calibrated_values_MSB & 0b1100) << 6) | calibrated_value_1_LSB) >>3

#Do some math for temp
calibration_value_offset=calib_temp_value_0

calibrated_value_delta=calibrated_value_1-calib_temp_value_0
calibrated_measurement_delta=calib_temp_meas_1-calib_temp_meas_0
correction_factor=calibrated_value_delta/calibrated_measurement_delta

calibration_measurement_offset=calib_temp_meas_0
zeroed_measured_temp=raw_temp-calibration_measurement_offset

temp_adjusted_c=(zeroed_measured_temp*correction_factor)+calibration_value_offset
temp_f = (temp_adjusted_c * 9/5) + 32


#humidity below

#conversion is done, grab registers for humidity
raw_hum_L=bus.read_byte_data(DEVICE_ADDRESS, HUMIDITY_ADDRESS_L)
raw_hum_H=bus.read_byte_data(DEVICE_ADDRESS, HUMIDITY_ADDRESS_H)
calib_hum_value_0=bus.read_byte_data(DEVICE_ADDRESS, CALIBRATION_H0)
calib_hum_value_1=bus.read_byte_data(DEVICE_ADDRESS, CALIBRATION_H1)
calib_hum_meas_0_L=bus.read_byte_data(DEVICE_ADDRESS, H0_T0_OUT_L)
calib_hum_meas_0_H=bus.read_byte_data(DEVICE_ADDRESS, H0_T0_OUT_H)
calib_hum_meas_1_L=bus.read_byte_data(DEVICE_ADDRESS, H1_T1_OUT_L)
calib_hum_meas_1_H=bus.read_byte_data(DEVICE_ADDRESS, H1_T1_OUT_H)

#prep variables: shift high byte over 8, logical or the two to concatenate
raw_hum=twos_comp((raw_hum_H <<8) | raw_hum_L, 16) #interpret as twos comp
calib_hum_value_0 = calib_hum_value_0 >> 1
calib_hum_value_1 = calib_hum_value_1 >> 1
calib_hum_meas_0 = (calib_hum_meas_0_H <<8) | calib_hum_meas_0_L
calib_hum_meas_1 = (calib_hum_meas_1_H <<8) | calib_hum_meas_1_L

#Do some math
calibrated_value_delta_hum = calib_hum_value_1 - calib_hum_value_0
calibrated_measurement_delta_hum = calib_hum_meas_1 - calib_hum_meas_0

calibration_value_offset_hum = calib_hum_meas_0
calibrated_measurement_offset_hum = calib_hum_meas_0
zeroed_measured_humidity = raw_hum - calibrated_measurement_offset_hum

correction_factor_humidity = calibrated_value_delta_hum / calibrated_measurement_delta_hum

humidity_adjusted = (zeroed_measured_humidity * correction_factor_humidity) + calibration_value_offset

# Announce the results!
print "Relative Humidity : %.2f %%" %humidity_adjusted
print "Temperature in Farenheit: : %.2f F" %temp_f

#power down device when done
#bus.write_byte_data(DEVICE_ADDRESS, CTRL_REG1, 0x00)
