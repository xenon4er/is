# ascii 8

def str_hex_bin(s):
	b = s.encode('hex')
	return bin(int(b, 16))[2:]

def bin_hex_str(h):
	s = hex(h)[2:]
	return s.decode('hex')

def complete_str(s):
	s = str_hex_bin(s)	
	if len(s)%4 != 0:
		s = "0"*(4-len(s)%4) + s			
	return s	

def div_str(s):
	l = len(s)%8 	
	if l != 0:
		s = s + chr(1)*(8-l)
	M = []
	i = 0
	m = ""		
	for x in s:
		m += x
		i += 1
		if i%8 == 0:
			m = complete_str(m)
#			print (i/8,m,len(m))
			M.append(m)
			m = ""
	return M

def make_keys(s="abcdefgh"):
	keys = []
	s = complete_str(s)
#	print ("s",s,len(s))
	for i in range(1,11):
		k = (s[i*3:] + s[:i*3])[:32]
		keys.append(k)
	return keys	
			
def xor(x,y):
	s = str(bin(int(x,2)^int(y,2)))[2:]	
	if len(s) != 32:
		s = (32-len(s))*"0" + s
	return(s)

def f(xl):
	l0 = xl[:16]
	l1 = xl[16:]
	
	tmp = xl[16:]
 
	# <<< 7
	l1 = l0[7:]+l0[:7]

	# ~(>>> 5)	
	l0 = tmp[11:]+tmp[:11]
	
	return l1+l0

def festel(M,keys):
	C = []	
	for m in M:
		xl = m[:32]
		xr = m[32:]		
#		print(xl,xr)	
		for i in range(9):
			tmp = xl[:]
			xl = xor(f(xor(xl,keys[i])),xr)[:]
			xr = xor(tmp,keys[i])[:]
#			print(xl,xr)
		tmp = xl[:]
		xr = xor(f(xor(xl,keys[9])),xr)[:]
		xl = xor(tmp,keys[9])[:]
#		print(xl,xr)
		C.append(xl+xr)
	return C 	

def antifestel(M,keys):
	C = []	
	for m in M:
		xl = m[:32]
		xr = m[32:]		
#		print(xl,xr)	
		for i in range(9):
			tmp = xl[:]
			xl = xor(f(xl),xr)[:]
			xr = xor(tmp,keys[i])[:]
#			print(xl,xr)
		tmp = xl[:]
		xr = xor(f(xl),xr)[:]
		xl = xor(tmp,keys[9])[:]
#		print(xl,xr)
		C.append(xl+xr)
	return C 	

def antif(xl):
	l0 = xl[:16]
	l1 = xl[16:]
	
	# >>> 7
	l1 = l1[9:]+l1[:9]

	# ~(<<< 5)	
	l0 = l0[5:]+l0[:5]
	return l1+l0
	

if __name__=="__main__":
	input_str = "adfghjhgfdsghjuytrfdcvbjkhgfdcgvhbjkhfdvjhbfsadasbjfgdsjfksd668"
	
	M = div_str(input_str)
	print("M:")
	for c in M:
		print c
	print(">>>>>>")

	keys = make_keys("asdfghjk")

	C = festel(M,keys)
	print("C:")
	for c in C:
		print c
	print(">>>>>>")

	keys.reverse()

	Z = antifestel(C,keys)
	print("Z:")
	for c in Z:
		print c

	print ("equal: ",  set(M)==set(Z))

	s = ""
	for c in Z:
		s += bin_hex_str(int(c,2))

	i = s.find(str(chr(1)))		
	s = s[:i]

	print ("input str:  " + input_str,len(input_str))
	print ("output str: " + s,len(s))


