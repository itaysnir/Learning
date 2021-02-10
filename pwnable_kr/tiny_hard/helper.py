#!/usr/bin/env python
import os
import time

EXECUTABLE_NAME = "./exploit"

def main():

	while(True):
		os.system(EXECUTABLE_NAME)
		time.sleep(0.1)

	return

if __name__ == '__main__':
	main()