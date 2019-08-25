import re

def twos_complement(input_value, num_bits):
	'''Calculates a two's complement integer 
		from the given input value's bits'''
	mask = 2**(num_bits - 1)
	return -(input_value & mask) + (input_value & ~mask)
	
#hex_int = int("FD6F", 16) 
#print(twos_complement(hex_int,16))
'''
def handle_raw(raw):
	if len(raw) <= len("a55a00090000090d0a"):
		return "NULL"
	splited = [ i for i in re.split("a55a|0d0a",raw) if len(i)>0 ]
	print(splited)
	return [ [i[10:-8],twos_complement(int(i[-8:-4],16),16)/10 ] for i in splited ]
'''
def handle_raw(raw):
	if len(raw) <= len("a55a00090000090d0a"):
		return "NULL"
	splited = [ i for i in re.split("a55a|0d0a",raw) if len(i)>0 ]
	#print(splited)
	return [ [i[10:-8],twos_complement(int(i[-8:-4],16),16)/10 ] for i in splited if len(i) == len("0019833400300833b2ddd901400000000000c30190") ]


#raw0 = "a55a0019833000e2003411b802011383258566fd6d02100d0aa55a0019833000e2003411b802011383258566fd6d02100d0a"
#raw1 = "a55a0019813000e28011606000020a92b6457500c9010f0d0a"

#raw = "a55a0019833400300833b2ddd901400000000000c301900d0aa55a0019833400300833b2ddd901400000000000c9019a0d0aa55a0019833400300833b2ddd901400000000000c101920d0aa55a0019833400300833b2ddd901400000000000c301900d0aa55a0019833400300833b2ddd901400000000000c401970d0aa55a00a55a0019833400300833b2ddd901400000000000c501960d0a"
#processed = handle_raw(raw)
#print(processed)

#processed = twos_complement(int("00c9",16),16)
#print(processed)
