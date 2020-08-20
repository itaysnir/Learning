import socket
import time

HOST_NAME = 'pwnable.kr'
PORT = 9008
CHUNK = 8192

def receive_parameters (skt):

	data = skt.recv (CHUNK) 
	number = int (data.split() [0][2:])
	count = int (data.split() [1][2:])

	return number, count

def solve_riddle (skt):

	# receive problem parameters
	(number,count) = receive_parameters (skt)
	print (number,count)

	current_index = 0
	result_number = ''
	results_array = []

	while (current_index < count):
		array_to_send = []
		for num in range (number):
			binary_representation = bin (num) [2:]
			binary_representation = '0' * (10-len(binary_representation)) + binary_representation
			if (binary_representation[::-1][current_index] == '0'):
				array_to_send.append (str(num))
	
		data_to_send = ' '.join (array_to_send)
		results_array.append (data_to_send)
		# skt.send (data_to_send)
		# weight_result = int (skt.recv (CHUNK))

		current_index += 1

	data_to_send = '-'.join (results_array) + '\n'
	skt.send (data_to_send)
	weight_result = skt.recv (CHUNK).split('-')

	for num in weight_result:
		if (int(num) % 10 == 9):
			result_number = '0' + result_number
		else:
			result_number = '1' + result_number

	final_result = str(int (result_number,2)) + '\n'
	print (final_result)

	skt.send (final_result)	
	correct_message = skt.recv (CHUNK)
	print (correct_message)



def main():
	
	client_socket = socket.socket()
	client_socket.connect ((HOST_NAME,PORT))

	# receive welcoming message
	data = client_socket.recv (CHUNK) 
	print (data)

	# start solving routine
	solves_counter = 0
	while (solves_counter < 100):
		solve_riddle (client_socket)
		solves_counter += 1

	flag = client_socket.recv (CHUNK) 
	print (flag)

	return

if __name__ == '__main__':
	main()