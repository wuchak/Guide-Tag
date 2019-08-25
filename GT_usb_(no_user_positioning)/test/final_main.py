import socket
import time
from  threading import Thread
from collections import Counter
from getobjxy import locate_obj #
from data_process import * #
import serial
import os

#101 - A 102 - B 103 - C

mix = [] # data container
ph_msg = [] # message to phone

def my_thread(port,addr):
	check = []
	last_second = int(time.time())
	global mix	
	global ph_msg
	
	reader = serial.Serial('/dev/'+port, 115200)
	cmd = [0XA5,0X5A,0X00,0X0A,0X82,0X00,0X10,0X98,0X0D,0X0A]

	while True:		
		reader.write(cmd)
		raw = reader.readline().hex()
		print("raw: "+raw)
		try:
			if len(raw) > 10 and raw[0:2] == 'a5':
				msg = handle_raw(raw)  # convert the raw message to RSSI & tag id
			else:
				msg = ''
			print("msg: " + repr(msg) )
			now = int(time.time())
			if last_second == now:
				if (type(msg) == list):
					for i in msg:
						check.append(i)  # append all messages which are in same second

			else:
				last_second = now
				if len(check) != 0: #????????
					tag_id = [ i[0] for i in check]
					tag_id = Counter(tag_id)
                    #    print('tag_id ' + repr(tag_id))
						#mix = []
					for id_ in tag_id:
						avg = 0	
						for i,check_id in enumerate(check): # i = index
							if check_id[0] == id_:
								avg += check_id[1]
						avg /= tag_id[id_]
                        #print("avg:" + repr(avg))
					mix.append([ last_second,addr[-3:],avg,id_]) # id_ = tag_id
					#print("mix: " + repr(mix))
					check = [] # clean
				
		except Exception as e:
			print(e)
			print('thread_failed')
			break

		time.sleep(2)


def reader_thread():
	model = ['ttyUSB1']
	for num, reader in enumerate(model):
		num = str(101 + num)
		try:
			Thread(target=my_thread, args=(reader, num)).start() #creat thread
		except Exception as e:
			print("main_failed")
			print(e)	

def socket_thread():
	global ph_msg
	global mix

	bind_ip = "0.0.0.0"
	bind_port = 8081
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((bind_ip,bind_port))
	server.listen(5)
	while True:
		client, addr = server.accept()
		try:	
			raw = client.recv(4096).decode()				
			if raw == 'app':
				if ph_msg != 'None':
					for m in ph_msg:
						respond = '{0},{1},{2}'.format(m[0],m[1],m[2])
						client.send(bytes(respond.encode()))
						time.sleep(10)

		except Exception as e:
			print("main_failed")
			print(e)	
	server.close()

def mix_up():
	global mix
	global ph_msg
	while True:
		if len(mix) >= 5:
			ph_msg = locate_obj(mix)
			print('ph_msg' + repr(ph_msg))
			mix = []

def main():
	try:
		Thread(target=socket_thread).start()
		Thread(target=reader_thread).start()
		Thread(target=mix_up).start()
	except Exception as e:
		print(e)
		print('main failed')

if __name__  == "__main__":
	main() 