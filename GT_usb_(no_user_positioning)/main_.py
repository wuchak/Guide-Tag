import socket
import time
from threading import Thread
from collections import Counter
import numpy as np
from getobjxy import locate_obj #
from data_process import * #
import serial
import serial.tools.list_ports

mix = []
ph_msg = []
'''
def reader(port):
    global mix
    global ph_msg

    check = []
    #mac = [0xA5,0x5A, 0x00, 0x08, 0x04, 0x0C, 0x0D, 0x0A] 
    cmd = [0XA5,0X5A,0X00,0X0A,0X82,0X00,0X10,0X98,0X0D,0X0A]
    with serial.Serial(port, 115200, timeout=1) as ser:
        addr = str(101 + int(port[-1]))
        #print(addr)
        #print(port)
        try:
            while True:
                last_second = int(time.time())
                ser.write(cmd)
                raw = ser.read(1000).hex()    # read up to ten bytes (timeout)
                #print(raw)
                if len(raw) > 10:
                    processed = handle_raw(raw)
                else:
                    processed = ''

                if type(processed) == list:
                    tag_id = Counter([i[0] for i in processed])
                    for id_ in tag_id:
                        avg = 0
                        for i, check_id in enumerate(processed):
                            #print('check_id:' + str(type(check_id[1])))
                            if check_id[0] == id_:
                                avg += check_id[1]
                        #print("num: " + repr(tag_id[id_]))
                        avg /= tag_id[id_]
                        #print("avg: " + str(avg))
                        mix.append([last_second, addr, round(avg,2), id_])
                        #print("mix: " + repr(mix))
                #time.sleep(0.2)

        except Exception as e:
            print(e)
            print("reader failed")
'''

def reader_main():
    global mix
    global ph_msg
    myports = [list(p) for p in list(serial.tools.list_ports.comports())]
    while True:
        try:
            for i in myports:
                if i[1] == 'FT232R USB UART':
                    port = i[0]
                    #Thread(target=reader,args=(i[0],)).start()

                    cmd = [0XA5,0X5A,0X00,0X0A,0X82,0X00,0X10,0X98,0X0D,0X0A]
            
                    with serial.Serial(port, 115200, timeout=1) as ser:
                        addr = str(101 + int(port[-1]))
                       
                        try:
                            last_second = int(time.time())
                            ser.write(cmd)
                            raw = ser.read(1000).hex()    # read up to ten bytes (timeout)
                            if len(raw) > 10:
                                processed = handle_raw(raw)
                            else:
                                processed = ''    
                
                            if type(processed) == list:
                                tag_id = Counter([i[0] for i in processed])
                                for id_ in tag_id:
                                    avg = 0
                                    for i, check_id in enumerate(processed):
                                        if check_id[0] == id_:
                                            avg += check_id[1]
                                    avg /= tag_id[id_]
                                    mix.append([last_second, addr, round(avg,2), id_])
                                   # print("mix: " + repr(mix)) 
                        except Exception as e:
                            print(e)
                            print("reader failed")

        except Exception as e:
            print(e)
            print("reader_thread failed")

#-------------------------------------------------------

def connection(client):
    global ph_msg
    global last_msg
    last_msg = [[34, 10, '300833b2ddd9014000000000',60]]
    while True:
        try:
            raw = client.recv(4096).decode()

            if (type(ph_msg) == list):
                if last_msg != ph_msg:
                    last_msg = ph_msg

            if raw == 'app':
                print(raw)
                # if (type(ph_msg) == list):
                #     last_msg = ph_msg

                for m in last_msg:
                    respond = '{0},{1},{2},{3}'.format(m[0],m[1],m[2],m[3])
                    client.send(bytes(respond.encode()))
                    time.sleep(10)
            
        except Exception as e:
            print(e)
            print("connection failed")
    client.close()
    print("disconect")

def server_main():
    bind_ip = "0.0.0.0"
    bind_port = 8081
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip,bind_port))
    server.listen(5)
    while True:
        client, addr = server.accept()
        try:
            Thread(target=connection,args=(client,)).start()
        except Exception as e:
            print("main_failed")
            print(e)
    server.close()

#-------------------------------------

def mix_data(height):
   # height = 60
    global mix
    global ph_msg
    while True:
        try:
            ph_msg = locate_obj(mix, height)
            #print(mix)
            if (len(mix) >= 50) or (type(ph_msg) is list):
                print(ph_msg)
                mix = []
            time.sleep(1)
        except Exception as e:
            print(e)
            print("mix_data failed")

if __name__ == "__main__":
    height = 60
    Thread(target=reader_main).start()
    Thread(target=server_main).start()
    Thread(target=mix_data, args=(height,)).start()
    