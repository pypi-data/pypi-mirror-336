"""
 Copyright (c) 2021 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,f
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
import math
import sys
import time

from tmx_nano2040_wifi import tmx_nano2040_wifi


# Enable and monitor the onboard IMU (accelerometer and gyroscope).
max_pitch = 0
max_roll = 0


def the_callback(data):
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[7]))
    global max_pitch
    global max_roll
    x = data[1]
    y = data[2]
    z = data[3]

    # print(f'IMU_REPORT at {formatted_time}: AX={data[1]} AY={data[2]} AZ={data[3]} GX'
    #       f'={data[4]}, '
    #       f'GY='
    #       f'{data[5]}, GZ={data[6]}')
    # pitch = 180 * atan2(accelX, sqrt(accelY*accelY + accelZ*accelZ))/PI;
    # roll = 180 * atan2(accelY, sqrt(accelX*accelX + accelZ*accelZ))/PI;
    pitch = 180 * math.atan2(x, math.sqrt(y*y + z*z))/math.pi
    roll = 180 * math.atan2(y, math.sqrt(x*x + z*z))/math.pi
    # xz = 180 * math.atan2(x, z) / math.pi
    # xy = 180 * math.atan2(x, y) / math.pi
    # yz = 180 * math.atan2(y, z) / math.pi
    pitch = int((pitch))
    roll = int((roll))
    print(f' pitch={pitch}  roll={roll}')
    if pitch > max_pitch:
        max_pitch = pitch
    if roll > max_roll:
        max_roll = roll
    # print(f'pitch = {max_pitch}  roll = {max_pitch}')


# Create a Telemetrix instance.
board = tmx_nano2040_wifi.TmxNano2040Wifi(ip_address='192.168.2.246')
try:

    # set the pin mode to imu, establish the callback.
    # data should appear in the console
    board.set_pin_mode_imu(callback=the_callback)

    while True:
        try:
            time.sleep(.1)
        except KeyboardInterrupt:
            board.shutdown()
            sys.exit(0)

except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
