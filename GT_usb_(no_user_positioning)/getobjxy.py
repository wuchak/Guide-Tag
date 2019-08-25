import positioning as ps
import numpy as np
from collections import Counter, defaultdict

def locate_obj(mix,height):
	#height = 60 # triangle
	d = defaultdict(list)
	for k in mix:  #split data using tag_id
		tag_id = k[-1]
		d[tag_id].append(k[:-1])
	#print(d.items())
	msg = []
	for id_,data in d.items():
		d_ = defaultdict(list)
		for k in data: #count the number of addr
			addr = k[1]
			d_[addr].append(k[-1])
#		print(id_)
#		print(len(d_.items()))
		print("port" + repr(sorted(d_.items())))
#		print(' ')
		data = d_.items()
		#print(data)
		if bool(d_['101']) & bool(d_['102']) & bool(d_['103']): # the number of addr is greater than 3
#			print(len(data))
			map_xy = ps.plan_coor(height ,len(data))
			anchor = []
			#print(map_xy)
			n = 0
			for addr, rssi in sorted(data):
				avg = sum(rssi) / len(rssi)
				#print(repr(addr) + repr(avg))
				distance = ps.rssi_to_d(avg)
				print(addr + ' ' + repr(distance))
				anchor.append([map_xy[n][0], map_xy[n][1], distance])
				n += 1
			#print(anchor)
			obj_xy = ps.obj_coor(anchor).tolist()
			#print(obj_xy[1][0])
			msg.append([ int(obj_xy[0][0]), int(obj_xy[1][0]), id_, height])
			return msg
		else:
			return 'None'
#		print(' ')
	#print(msg)
'''
mix	= [['1231445', '102', 20.0, 'id_1'], ['1231445', '101', 20.5, 'id_1'],['1231445', '103', 20.0, 'id_1'], 
		['1231445', '103', 19.5, 'id_2'],['1231445', '101', 20.5, 'id_2'],['1231445', '102', 20.5, 'id_2'],
		['1231445', '103', 19.4, 'id_2'],['1231445', '103', 19.4, 'id_2'],['1231445', '101',19.5, 'id_2'],
		['1231445', '103', 20.5, 'id_2'],['1231445', '104', 20.5, 'id_2'],['1231445', '101', 20.5, 'id_2']]
'''

#locate_obj(mix)