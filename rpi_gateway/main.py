# This is BLE GATT Client application for Raspberry Pi -server. 
# Python-client works as central device (Central/Client): 
#   It scans devices, connects to Nordic MCU and subscribes BLE (datastream) notifications.
import asyncio  
from bleak import BleakScanner  
from bleak import BleakClient


# CODE DEMO AND TESTING 7.11.
# https://github.com/hbldh/bleak

MODEL_NBR_UUID = "2A00"
UNKNOWN_CHARS = "00001526-1212-efde-1523-785feabcd123" # under uuid we find Value: (0x) 00-00-00-00 etc..


async def scanner():
    print(f"starting scanner")
    devices = await BleakScanner.discover(timeout=5.0)
    return devices

def connected(): # func if connection is established
    pass


def notify_handler(sender,data): # func to receive data
    # byte_val = data
    int_result = int.from_bytes(data,"little") # data is bytearray, little for 'Little Endian'
    print(f"Received from {sender}: {data}, int value = {int_result}") 
    


async def main():
    print(f"starting main")
    found_devices = await scanner()
    device_address = None
    for d in found_devices:
        print(f"address: {d.address},  name: {d.name}")
        if d.name == "Nordic_VK":
            device_address = d.address
            print("success")
            exit
    
    if device_address == None:
        print("Se on yhistetty johonki tai pois päältä")
        print("Reduce, Reuse, EKEKE")
        exit

    client = BleakClient(device_address)


    (await client.connect())
    model_number = await client.read_gatt_char(MODEL_NBR_UUID)
    print("Model Number: {0}".format("".join(map(chr, model_number))))
    if BleakClient.is_connected == 0:
        print("Client connected")
    print(model_number)

    await client.start_notify("00001526-1212-efde-1523-785feabcd123",notify_handler)
    await asyncio.sleep(30)   # keep receiving for 30s
    await client.stop_notify(UNKNOWN_CHARS)
    #incoming_values = await client.read_gatt_char(UNKNOWN_CHARS) # check line 13 for more info!

    #print(incoming_values)

    #gatt_read_value = await BleakClient.read_gatt_char("00001524-1212-efde-1523-785feabcd123","2902")
    #print(gatt_read_value)

    client.disconnect() # sometimes error "RuntimeWarning: coroutine 'BleakClient.disconnect' was never awaited"

    return 1


if __name__ == "__main__":
    try:
        if 1 == asyncio.run(main()):
            print("Hell yeah")
        else:
            print("Hell naw iamma go hang my self")
    except KeyboardInterrupt:
        print("Stopped")
