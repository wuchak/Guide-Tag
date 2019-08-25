import socket
import time
from  threading import Thread
from collections import Counter
from getobjxy import locate_obj #
from data_process import * #

#101 - A 102 - B 103 - C

mix = [] # data container
ph_msg = [] # message to phone

def my_thread(client,addr):
	check = []
	last_second = int(time.time())
	last_msg = [[50, 50, 'id_001',60]]
	global mix	
	global ph_msg

	while True:
		raw = client.recv(4096).decode()  #decode the raw message from wifi module
		#print(raw)
		if raw == "app":
			print(raw)
			
			if type(ph_msg) == list:
				last_msg = ph_msg
			print("msg " + repr(last_msg))
			try:
				for m in last_msg:
					respond = '{0},{1},{2},{3}'.format(m[0],m[1],m[2],m[3])
					client.send(bytes(respond.encode()))
					time.sleep(10)
			except Exception as e:
				print(e)

#		elif type(ph_msg) == list:
#			last_msg = ph_msg
#			print("change!")
		else:
			try:
				if len(raw) > 10:
					msg = handle_raw(raw)  # convert the raw message to RSSI & tag id
				else:
					msg = ''

				now = int(time.time())
				#print("now: " + str(now))
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
						for id_ in tag_id:
							avg = 0	
							for i,check_id in enumerate(check): # i = index
								if check_id[0] == id_:
									avg += check_id[1]
							avg /= tag_id[id_]
                        #print("avg:" + repr(avg))
						mix.append([ last_second,addr[-3:],avg,id_]) # id_ = tag_id
#					print("mix: " + repr(mix))
					check = [] # clean
				
			except Exception as e:
				print(e)
				print('thread_failed')
				break

			if not raw:
				break		
	client.close()

def server_main(height):
		global mix
		global ph_msg	
	
		bind_ip = "0.0.0.0"
		bind_port = 8081
		connected_ip = []
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind((bind_ip,bind_port))
		server.listen(5)
		print("server started... share....")
		
		while True:
			client, addr = server.accept()
			try:
				Thread(target=my_thread, args=(client, addr[0])).start() #creat thread
				#ph_msg = locate_obj(mix,height)
				#if type(ph_msg) == list or (len(mix) >= 40) :
			#		print('ph_msg' + repr(ph_msg))
				#	mix = []

			except Exception as e:
				print("main_failed")
				print(e)	
		server.close()

def check_main(height):
	global mix
	global ph_msg
	while True:
		ph_msg = locate_obj(mix,height)
		if (type(ph_msg) == list) or (len(mix) >= 40) :
			print("ph_msg " + repr(ph_msg) )
			mix = []
		time.sleep(1)

if __name__  == "__main__":
	height = 60
	Thread(target=server_main,args=(height,)).start()
	Thread(target=check_main, args=(height,)).start()
	#server_main(height)