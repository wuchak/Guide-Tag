#important
#This program is used to convert the rssi to distance
#But the data of this program is not accurate

def rssi_to_d(X):
	A = 7687368.098564008
	B = -2037808.5734770163
	C = 219518.95272370445
	D = -12197.194027895594
	E = 363.3596882612768
	F = -5.348464229656464
	G = 0.028380651465470648

	distance = round(A + B*X + C*X**2 + D*X**3 + E*X**4 + F*X**5 + G*X**6,2)
	if distance < 0:
		distance = 5
	else:
		distance -= 15
	return distance
