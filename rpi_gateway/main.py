# This is BLE GATT Client application for Raspberry Pi -server. 
# Python-client works as central device (Central/Client): 
#   It scans devices, connects to Nordic MCU and subscribes BLE (datastream) notifications.

import asyncio
import logging                  # https://docs.python.org/3/library/logging.html
logger = logging.getLogger(__name__)
from bleak import BleakScanner  # https://github.com/hbldh/bleak
from bleak import BleakClient
# testing mysql-connection with mysql.connector.connect


MODEL_NBR_UUID = "2A00"
TARGET_DEVICE_NAME = "Nordic_VK"
CHAR_UUID = "00001526-1212-efde-1523-785feabcd123" # named in nRF Connect app as "Unknown characteristic"
SENSOR_DATA = []
class BLEGateway: # class for modular approach
    def __init__(self, client, device_name = TARGET_DEVICE_NAME):
        self.client = None
        self.device_name = device_name
    
    async def device_scanner(self, timeout=5):
        logger.info("Scanning ble devices.")
        devices = await BleakScanner.discover(timeout=timeout)

        for dev in devices:
            # print(f"address: {dev.address},  name: {dev.name}") # debug
            if dev.name == self.device_name:
                logger.info(f"Success: target device found {dev.address}")
                return dev.address
        
        raise RuntimeError(f"Target device '{self.device_name}' not found.")


    async def device_model_number(self):
        model_number = await self.client.read_gatt_char(MODEL_NBR_UUID)
        # do we need this
        pass

    async def connection(self, address):
        self.client = BleakClient(address)
        await self.client.connect()
        # if != bleak is_connected
        # raise connection error
        logger.info(f"Connected to {address}.")

    async def start_notifications(self, uuid, handler):
        await self.client.start_notify(uuid,handler)
    
    async def stop_notifications(self, uuid):
        await self.client.stop_notify(uuid)


    async def disconnect(self):
        if self.client:     # checking if self.client is None
            await self.client.disconnect()
        logger.info(f"'{self.client}' disconnected.") # check this!
    
    """def export_to_db(self,data):

        
        pass
"""
### END OF CLASS ###


### NEW NOTIFY_HANDLER ###

# def notify_handler(sender,data): # func to receive data
#     int_result = int.from_bytes(data,"little") # data is bytearray, little for 'Little Endian'
#     print(f"Received from {sender}: bytearray {data}: int {int_result}") 
    
    
    
### NEW MAIN ###

# async def main():
#     logging.basicConfig(level=logging.INFO) # Learning logging-library. No separate log file!
#     ble = BLEGateway()
#     try:
#         address = await ble.device_scanner()
#         await ble.connection(address)
#         await ble.device_model_number()
#         await ble.start_notifications(CHAR_UUID,notify_handler)
#         await asyncio.sleep(30)   # keep receiving for 30s

#         # Mihin ble.stop_notifications(uuid) ? esim tähän vai ennen disconnect()
#         # Tällä hetkellä datan keruu aloitetaan, odotetaan 30s ja lopetetaan. Millä tavalla jatkuu? Painike, komentorivin komento.. tms.

#     except Exception as e: # from Raise Exception doc
#         pass # logging error
#     finally:
#         await ble.disconnect()

### END OF CHANGES ###


async def scanner():
    # logger.debug("scanner test")
    print(f"Scanning devices..")
    devices = await BleakScanner.discover(timeout=5.0)
    return devices

def connected(): # func if connection is established
    pass


def notify_handler(sender,data): # func to receive data
    int_result = int.from_bytes(data,"little") # data is bytearray, little for 'Little Endian'
    print(f"Received from {sender}: bytearray {data}: int {int_result}") 
    SENSOR_DATA.append(data)

def export_to_db(data):

    pass


    

async def main():
    # logging.basicConfig(level=logging.DEBUG)
    print(f"main starting")  

    found_devices = await scanner()
    device_address = None

    for dev in found_devices:
        print(f"address: {dev.address},  name: {dev.name}")
        if dev.name == TARGET_DEVICE_NAME:
            device_address = dev.address
            print("Success: Device found")
            exit  # exit or exit() ?
    
    if device_address == None:
        print("Device not found.")
        exit  # exit or exit() ?

    client = BleakClient(device_address)


    (await client.connect())
    model_number = await client.read_gatt_char(MODEL_NBR_UUID)
    print("Model Number: {0}".format("".join(map(chr, model_number))))

    if BleakClient.is_connected == 0:
        print("Client connected")
    print(model_number)

    await client.start_notify(CHAR_UUID,notify_handler)
    # await client.start_notify("00001526-1212-efde-1523-785feabcd123",notify_handler)
    await asyncio.sleep(30)   # keep receiving for 30s
    await client.stop_notify(CHAR_UUID)
    print(SENSOR_DATA)
    client.disconnect() # frequent error: "RuntimeWarning: coroutine 'BleakClient.disconnect' was never awaited" 

    return 1


if __name__ == "__main__":
    try:
        if 1 == asyncio.run(main()):
            print("Working")
        else:
            print("Not working")
    except KeyboardInterrupt:
        print("Stopped.")