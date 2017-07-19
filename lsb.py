from PIL import Image
import binascii
import optparse
import sys

def encode(binary,digit):
	binary = binary[:-1] + digit
	return int(binary,2)

def str2bin(message):
	binary = bin(int(binascii.hexlify(message),16))
	binary = binary[0] + binary[2:] 
	return binary

def decode(binary):
	binary = bin(binary)
	return binary[-1]

def bin2str(binary):
	message = binascii.unhexlify('%x' % (int('0b'+binary,2)))
	return message

def hide(filename,message):
	img = Image.open(filename)
	binary = str2bin(message)

	if img.mode in ('RGBA'):
		img = img.convert('RGB')
		datas = img.getdata()
		newData = []
		digit = 0
		if len(binary) > (len(datas)*3-1):
			print "Mess too big !"
			return
		for item in datas:
			if (digit < len(binary)) :
				if((len(binary)-digit) >= 3 ):
					r = encode(bin(item[0]),binary[digit])
					g = encode(bin(item[1]),binary[digit+1])
					b = encode(bin(item[2]),binary[digit+2])
					item = (r,g,b)
				if((len(binary)-digit) == 2 ):
					r = encode(bin(item[0]),binary[digit])
					g = encode(bin(item[1]),binary[digit+1])
					b = item[2]
					item = (r,g,b)
				if((len(binary)-digit) == 1):
					r = encode(bin(item[0]),binary[digit])
					g = item[1]
					b = item[2]
					item = (r,g,b)
				digit += 3
				#print (r,g,b,len(binary),digit)
			newData.append(item)
		img.putdata(newData)
		img.save("lsb-"+filename,"PNG")
		return "Completed!"
	return datas

def read(filename):
	character = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPWRSTUVWXYZ0123456789 /=>?@#$%^&*()_+-~`,.:;"
	img = Image.open(filename)
	if img.mode in ('RGBA'):
		img = img.convert('RGB')
		datas = img.getdata()
		mess = ''
		data = ''
		for item in datas:
			for i in item :
				data += decode(i)
				if len(data) == 8 :
					print data
					print bin2str(data)
					if bin2str(data) in character:
						mess += bin2str(data)
						data = ''
					else:
						return mess

def Main():
	parser = optparse.OptionParser('usage %prog <name file image>\n -e : to hide message\n -d : to read message hide')
	parser.add_option('-e', dest='hide', type='string', \
		help='target picture path to hide text')
	parser.add_option('-d', dest='retr', type='string', \
		help='target picture path to retrieve text')
	
	(options, args) = parser.parse_args()
	if (options.hide != None):
		text = raw_input("Enter a message to hide: ")
		print hide(options.hide, text)
	elif (options.retr != None):
                print read(options.retr)
	else:
		print parser.usage
		exit(0)

if __name__ == '__main__':
	Main()