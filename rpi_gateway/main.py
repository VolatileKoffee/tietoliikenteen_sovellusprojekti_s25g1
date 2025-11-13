# This is BLE GATT Client application for Raspberry Pi -server. 
# Python-client works as central device (Central/Client): 
#   It scans devices, connects to Nordic MCU and subscribes BLE (datastream) notifications.

import asyncio
import logging                  # https://docs.python.org/3/library/logging.html
logger = logging.getLogger(__name__)
from bleak import BleakScanner  # https://github.com/hbldh/bleak
from bleak import BleakClient
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

localhost = os.getenv("LOCALHOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")


MODEL_NBR_UUID = "2A00"
TARGET_DEVICE_NAME = "Nordic_VK"
CHAR_UUID = "00001526-1212-efde-1523-785feabcd123"          # named in nRF Connect app as "Unknown characteristic"
TEMP_DATA = []
SENSOR_DATA = []

class BLEGateway:                                           # class for modular approach
    def __init__(self, device_name = TARGET_DEVICE_NAME):
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
    

    def export_to_db(self, data):
        mydb = mysql.connector.connect(
        host=localhost,
        user= db_user,
        password= db_password,
        database=db_name
        )

        print(f"DEBUG: {data}")

        mycursor = mydb.cursor()        
        query = "INSERT INTO rawdata (sensorvalue_x, sensorvalue_y, sensorvalue_z, sensor_orientation) VALUES (%s,%s,%s,%s);"

        mycursor.executemany(query, data)
        mydb.commit() # added row. For error checking add "mydb.rollback()"?
        mycursor.close()

### END OF CLASS ###


### NEW NOTIFY_HANDLER ###

def notify_handler(sender,data): # func to receive data
    int_result = int.from_bytes(data,"little") # data is bytearray, little for 'Little Endian'
    print(f"Received from {sender}: bytearray {data}: int {int_result}") 
    TEMP_DATA.append(int_result)

    if len(TEMP_DATA) == 4:
        SENSOR_DATA.append(tuple(TEMP_DATA)) # list -> tuple  +  appending tuple to a list
        print(f"DEBUG {SENSOR_DATA}")
        TEMP_DATA.clear()
    
    
# ### NEW MAIN ###

async def main():
    logging.basicConfig(level=logging.INFO) # Learning logging-library. No separate log file!
    ble = BLEGateway()
    try:
        address = await ble.device_scanner()
        await ble.connection(address)
        await ble.device_model_number()
        await ble.start_notifications(CHAR_UUID,notify_handler)
        await asyncio.sleep(30)   # keep receiving for 30s
        # Tällä hetkellä datan keruu aloitetaan, odotetaan 30s ja lopetetaan. Millä tavalla jatkuu? Painike, komentorivin komento.. tms.
        # While True:
        #     await ble.start_notifications(CHAR_UUID,notify_handler)
        #     await asyncio.sleep(30)
        #     await ble.stop_notifications(CHAR_UUID)
        #     lähetys tietokantaan
        #     sleep(60) ? ja loop alusta...
    except Exception as e: # from Raise Exception doc
        pass # logging error
    finally:
        ble.stop_notifications(CHAR_UUID)
        await ble.disconnect()
        ble.export_to_db(SENSOR_DATA)

# ### END OF CHANGES ###


# async def scanner():
#     # logger.debug("scanner test")
#     print(f"Scanning devices..")
#     devices = await BleakScanner.discover(timeout=5.0)
#     return devices

# def connected(): # func if connection is established
#     pass


# def notify_handler(sender, data): # func to receive data
#     int_result = int.from_bytes(data,"little") # data is bytearray, little for 'Little Endian'
#     print(f"Received from {sender}: bytearray {data}: int {int_result}")

#     TEMP_DATA.append(int_result)

#     if len(TEMP_DATA) == 4:
#         SENSOR_DATA.append(tuple(TEMP_DATA)) # list -> tuple  +  appending tuple to a list
#         print(f"DEBUG {SENSOR_DATA}")
#         TEMP_DATA.clear()


# def export_to_db(data):

#     mydb = mysql.connector.connect(
#     host=localhost,
#     user= db_user,
#     password= db_password,
#     database=db_name
#     )

#     print(f"DEBUG data: {data}")

#     mycursor = mydb.cursor()
    
#     """
#     sensor_data_dict = {"x": [],"y":[],"z":[],"orientation":[]}

#     integer = 0

#     for x in data:
#         match integer:
#             case 0:
#                 sensor_data_dict["x"].append(x)
#             case 1:
#                 sensor_data_dict["y"].append(x)
#             case 2:
#                 sensor_data_dict["z"].append(x)
#             case 3:
#                 sensor_data_dict["orientation"].append(x)
    
#         integer+=1        
#         if integer == 4:
#             integer = 0
        
#     print(sensor_data_dict)
#     print(sensor_data_dict["x"])

    
#     data_tuples = list(zip(
#         sensor_data_dict["x"],
#         sensor_data_dict["y"],
#         sensor_data_dict["z"],
#         sensor_data_dict["orientation"]
#     ))
#     """
#     # values_to_send = 
#     query = "INSERT INTO rawdata (sensorvalue_x, sensorvalue_y, sensorvalue_z, sensor_orientation) VALUES (%s,%s,%s,%s);" # removed "table" and added ";"
#     # query = "INSERT INTO table rawdata(sensorvalue_x,sensorvalue_y,sensorvalue_z,sensor_orientation) VALUES(%s,%s,%s,%s)"

#     mycursor.executemany(query, data)
#     mydb.commit() # added row. for error checking a "mydb.rollback()"?
#     mycursor.close()



# async def main():
#     # logging.basicConfig(level=logging.DEBUG)
#     print(f"main starting")  

#     found_devices = await scanner()
#     device_address = None

#     for dev in found_devices:
#         print(f"address: {dev.address},  name: {dev.name}")
#         if dev.name == TARGET_DEVICE_NAME:
#             device_address = dev.address
#             print("Success: Device found")
#             exit  # exit or exit() ?
    
#     if device_address == None:
#         print("Device not found.")
#         exit  # exit or exit() ?

#     client = BleakClient(device_address)


#     (await client.connect())
#     model_number = await client.read_gatt_char(MODEL_NBR_UUID)
#     print("Model Number: {0}".format("".join(map(chr, model_number))))

#     if BleakClient.is_connected == 0:
#         print("Client connected")
#     print(model_number)

#     await client.start_notify(CHAR_UUID,notify_handler)
#     # await client.start_notify("00001526-1212-efde-1523-785feabcd123",notify_handler)
#     await asyncio.sleep(30)   # keep receiving for 30s
#     await client.stop_notify(CHAR_UUID)
#     client.disconnect() # frequent error: "RuntimeWarning: coroutine 'BleakClient.disconnect' was never awaited" 
#     export_to_db(SENSOR_DATA)

#     return 1


# if __name__ == "__main__":
#     try:
#         if 1 == asyncio.run(main()):
#             print("Working")
#         else:
#             print("Not working")
#     except KeyboardInterrupt:
#         print("Stopped.")


if __name__ == "__main__":
    asyncio.run(main())