# This is BLE GATT Client application for Raspberry Pi -server. 
# Python-client works as central device (Central/Client): 
#   It scans devices, connects to Nordic MCU and subscribes BLE (datastream) notifications.
import asyncio  
from bleak import BleakScanner  

# CODE DEMO AND TESTING 7.11.
# https://github.com/hbldh/bleak

async def scanner():
    print(f"starting scanner")
    devices = await BleakScanner.discover(timeout=5.0)
    return devices


async def main():
    print(f"starting main")
    found_devices = await scanner()

    for d in found_devices:
        print(f"address: {d.address}, rssi: {d.rssi}, name: {d.name}, metadata: {d.metadata}")


if __name__ == "__main__":
    asyncio.run(main())



# FROM BLEAK GITHUB
# address = "24:71:89:cc:09:05"
# MODEL_NBR_UUID = "2A24"

# async def main(address):
#     async with BleakClient(address) as client:
#         model_number = await client.read_gatt_char(MODEL_NBR_UUID)
#         print("Model Number: {0}".format("".join(map(chr, model_number))))

# asyncio.run(main(address))