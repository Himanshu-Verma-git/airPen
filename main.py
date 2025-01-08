from client import Client
import calculation
import body
import time
import struct
import asyncio
import bleak
import asyncio
import pyautogui

pyautogui.PAUSE = 0.0

accel_data:list = [0, 0, 0]
gyro_data:list = [0, 0, 0]
magnet_data:list = [0, 0, 0]

kalman_roll = body.KalmanFilter()
kalman_pitch = body.KalmanFilter()
kalman_yaw = body.KalmanFilter()
dt = 0.01

kalman_filters = [kalman_roll, kalman_pitch, kalman_yaw]

async def setData(Character, data: bytearray):
    data = getData(data)
    if(Character.uuid == "00000011-0000-1000-8000-00805f9b34fb"): gyro_data[0] = data
    if(Character.uuid == "00000012-0000-1000-8000-00805f9b34fb"): gyro_data[1] = data
    if(Character.uuid == "00000013-0000-1000-8000-00805f9b34fb"): gyro_data[2] = data
    if(Character.uuid == "00000021-0000-1000-8000-00805f9b34fb"): accel_data[0] = data
    if(Character.uuid == "00000022-0000-1000-8000-00805f9b34fb"): accel_data[1] = data
    if(Character.uuid == "00000023-0000-1000-8000-00805f9b34fb"): accel_data[2] = data
    if(Character.uuid == "00000031-0000-1000-8000-00805f9b34fb"): magnet_data[0] = data
    if(Character.uuid == "00000032-0000-1000-8000-00805f9b34fb"): magnet_data[1] = data
    if(Character.uuid == "00000033-0000-1000-8000-00805f9b34fb"): magnet_data[2] = data
# async def printdata(Character, data: bytearray):
#     print(Character.uuid)
#     print(type(Character))

def getData(byte_array, byte_order='little'):
    return struct.unpack('f', byte_array)[0]

async def cursor_x(CHARACTER, data: bytearray)->None:
    # pyautogui.mouseDown(button="left")
    accel = getData(byte_array=data)
    print("X: ",accel)
    pixels_x = calculation.compute_displacement(accel)
    pyautogui.move(pixels_x, 0)
    # pyautogui.mouseUp(button="left")

async def cursor_y(CHARACTER, data: bytearray)->None:
    # pyautogui.mouseDown(button="left")
    accel = getData(byte_array=data)
    print("Y: ",accel)
    pixels_y = calculation.compute_displacement(accel)
    pyautogui.move(0, pixels_y)
    # pyautogui.mouseUp(button="left")

async def main():
    CHAR_GX = "00000011-0000-1000-8000-00805f9b34fb"
    CHAR_GY = "00000012-0000-1000-8000-00805f9b34fb"
    CHAR_GZ = "00000013-0000-1000-8000-00805f9b34fb"
    CHAR_AX = "00000021-0000-1000-8000-00805f9b34fb"
    CHAR_AY = "00000022-0000-1000-8000-00805f9b34fb"
    CHAR_AZ = "00000023-0000-1000-8000-00805f9b34fb"
    CHAR_MX = "00000031-0000-1000-8000-00805f9b34fb"
    CHAR_MY = "00000032-0000-1000-8000-00805f9b34fb"
    CHAR_MZ = "00000033-0000-1000-8000-00805f9b34fb"
    CHAR_FLAG = "00002a57-0000-1000-8000-00805f9b34fb"

    print("Scanning..")
    client = Client()
    await Client.scan()
    server_add = await Client.scan_device("Nano33BLE_SingleValue")
    # server_add = "06:70:DB:B3:CD:E8"

    if(not server_add):
        print("No Device Found")
        return

    # print("Server Add: ", server_add)
    # print("-------------------------------------------------------------------------------------------")

    try:
        await client.connect_device(server_add)
    except bleak.exc.BleakError as e:
        print(f"Connection failed: {e}")
    except TimeoutError as e:
        print(f"Timeout error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    if(client.connected):print("Connected")
    else:
        print("Connection Failed.")
        return

    print("-------------------------------------------------------------------------------------------")
    await client.servAndChar()
    print("-------------------------------------------------------------------------------------------")

    try:
        await client.start_notification(CHAR_GX, handler=setData)
        await client.start_notification(CHAR_GY, handler=setData)
        await client.start_notification(CHAR_GZ, handler=setData)
        await client.start_notification(CHAR_AX, handler=setData)
        await client.start_notification(CHAR_AY, handler=setData)
        await client.start_notification(CHAR_AZ, handler=setData)
        await client.start_notification(CHAR_MX, handler=setData)
        await client.start_notification(CHAR_MY, handler=setData)
        await client.start_notification(CHAR_MZ, handler=setData)
    except Exception as e:print(e)
    print("Conformation Sent.")

    await client.writeToChar(CHAR_FLAG, b'\x01')
    while(client.connected):
        pitch, roll, yaw = body.calculate_orientation(accel_data, gyro_data, magnet_data, 0, kalman_filters)
        # print("PRY")
        print(pitch, "\t", roll, "\t", yaw, "\t")
        await asyncio.sleep(0.1)

    # await client.stop_notification(char_uuid=CHAR_AX)
    # await client.stop_notification(char_uuid=CHAR_AY)
    await client.stop_notification(CHAR_GX)
    await client.stop_notification(CHAR_GY)
    await client.stop_notification(CHAR_GY)
    await client.stop_notification(CHAR_AX)
    await client.stop_notification(CHAR_AY)
    await client.stop_notification(CHAR_AY)
    await client.stop_notification(CHAR_MX)
    await client.stop_notification(CHAR_MY)
    await client.stop_notification(CHAR_MY)
    await client.disconnect_device()
    print("Disconnected")


if __name__ == "__main__":
    #try:
        asyncio.run(main())
    # except Exception as e:
    #     print(e)
    # finally:
    #     pyautogui.mouseUp(button="left")