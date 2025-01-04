from client import Client
import calculation
import time
import struct
import asyncio
import bleak
import asyncio
import pyautogui

pyautogui.PAUSE = 0.0

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
    CHAR_X = "00002b51-0000-1000-8000-00805f9b34fb"
    CHAR_Y = "00002b52-0000-1000-8000-00805f9b34fb"
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
    
    # await client.servAndChar()
    # print("-------------------------------------------------------------------------------------------")
    
    await client.writeToChar(CHAR_FLAG, b'\x01')
    await client.start_notification(CHAR_X, handler=cursor_x)
    await client.start_notification(CHAR_Y, handler=cursor_y)
    print("Conformation Sent.")
    
    while(client.connected): 
        # print("Keep ALive")
        await asyncio.sleep(1)
    
    await client.stop_notification(char_uuid=CHAR_X)
    await client.stop_notification(char_uuid=CHAR_Y)
    await client.disconnect_device()
    print("Disconnected")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(e)
    finally:
        pyautogui.mouseUp(button="left")