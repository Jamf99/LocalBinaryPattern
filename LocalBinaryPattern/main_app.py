import argparse
import os.path
import LBP

def main():

	input_file = 'images/prueba.bmp'

	if os.path.isfile(input_file):
		run = LBP.LBP(input_file)
		print("RUNNING . . .")
		run.execute()
	else:
	    print("File '{}' does not exist.".format(input_file))

if __name__ == "__main__":
    main()
