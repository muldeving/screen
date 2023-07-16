import psutil
import time
from datetime import datetime
import serial 

arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1)

UPDATE_DELAY = 0.5 # in seconds



sep = "Package id 0', current=" 
sep1 = '.'

def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024
# get the network I/O stats from psutil
io = psutil.net_io_counters()
# extract the total bytes sent and received
bytes_sent, bytes_recv = io.bytes_sent, io.bytes_recv
while True:
    from pySMART import *
    ssd1 = Device('/dev/sdd')
    ssd2 = Device('/dev/sdd')
    ssd3 = Device('/dev/sdd')
    ssd4 = Device('/dev/sdd')
    # get the stats again
    io_2 = psutil.net_io_counters()
    ssd1_temp = ssd1.temperature
    ssd2_temp = ssd2.temperature
    ssd3_temp = ssd3.temperature
    ssd4_temp = ssd4.temperature
    cpu = psutil.cpu_percent(interval=1)
    amount_of_ram = str(psutil.virtual_memory()[2]).split(sep1, 1)[0] # --||--
    ram = 'RAM', str(amount_of_ram)
    cpu_temp = str(psutil.sensors_temperatures(fahrenheit=False)).split(sep)[1]
    now = datetime.now()
    d = now.strftime("%d/%m/%Y")
    h = now.strftime("%H:%M:%S")
    us, ds = io_2.bytes_sent - bytes_sent, io_2.bytes_recv - bytes_recv
    toserial = "<" + d + "," + h + "," + str(cpu) + "%," + str(amount_of_ram) + "%," + str(get_size(ds / UPDATE_DELAY)) + "/s," + str(get_size(us / UPDATE_DELAY)) + "/s," + "eth0" + "," + str(cpu_temp[0:2]) + "," + str(ssd1_temp) + "," + str(ssd2_temp) + "," + str(ssd3_temp) + "," + str(ssd4_temp) + ">"
    print(toserial)
    arduino.write(bytes(toserial, 'utf-8'))
    bytes_sent, bytes_recv = io_2.bytes_sent, io_2.bytes_recv