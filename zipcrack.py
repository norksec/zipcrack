import os
import sys
import zipfile
import time
import atexit
from progressbar import Bar, AnimatedMarker, ProgressBar, Percentage, RotatingMarker, ETA
from optparse import OptionParser
from threading import Thread
from pyfiglet import Figlet

def cls():
	os.system('cls' if os.name=='nt' else 'clear')

def exit_handler():
	print '\n[\033[1;31;40m~\033[1;37;40m] Exiting...\n'

def intro():
	cls()
	f = Figlet(font='graffiti')
	print f.renderText('NoRKSEC')
	print '\033[1;32;40mzipCrack.py - (c) 2016 NORKSEC - No rights reserved\033[1;37;40m'+'\n'
	
def extractFile(zFile, password):
	try:
		zFile.extractall(pwd=password)
		print '\n\n[\033[1;31;40m+\033[1;37;40m] Found password: [\033[1;31;40m' + password + '\033[1;37;40m]'
		exit_handler()
		os._exit(0)
	except:
		pass

def fileLen(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1

def main():
	atexit.register(exit_handler)
	parser = OptionParser(usage="usage: %prog -f <zipfile> -d <dictionary>", version="%prog 1.0")
	parser.add_option('-f', dest='zname', type='string', help='specify zip file')
	parser.add_option('-d', dest='dname', type='string', help='specify dictionary file')
	(options, args) = parser.parse_args()
	if (options.zname == None) | (options.dname == None):
		print parser.error("Invalid arguments.")
		exit(0)
	else:
		zname = options.zname
		dname = options.dname
	if not os.path.isfile(zname):
		print '[\033[1;31;40m-\033[1;37;40m] Zip file \033[1;31;40m' + zname + '\033[1;37;40m does not exist.'
		exit(0)
	if not os.path.isfile(dname):
		print '[\033[1;31;40m-\033[1;37;40m] Dictionary file \033[1;31;40m' + dname + '\033[1;37;40m does not exist.'
		exit(0)
	print '[\033[1;31;40m+\033[1;37;40m] Cracking zip file \033[1;31;40m' + zname + '\033[1;37;40m using dictionary file \033[1;31;40m' + dname + '\033[1;37;40m.\n'
	zFile = zipfile.ZipFile(zname)
	passFile = open(dname)
	lineMax = fileLen(dname)
	pbar = ProgressBar(widgets=['\033[1;32;40mCracking:\033[1;37;40m  ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA()], maxval=lineMax)
	print '[\033[1;31;40m+\033[1;37;40m] Testing \033[1;31;40m' + str(lineMax) + '\033[1;37;40m passwords from dictionary file.\n'
	i = 0
	pbar.start()
	for line in passFile.readlines():
		password = line.strip('\n')
		t = Thread(target=extractFile, args=(zFile, password))
		pbar.update(i+1)
		i = i+1
		try:
			t.start()
		except (KeyboardInterrupt, SystemExit):
			os._exit(1)
	pbar.finish()
	time.sleep(2)
	print '\n[\033[1;31;40m-\033[1;37;40m] Password not found in \033[1;31;40m' + dname + '\033[1;37;40m.\n'
	sys.exit(1)

if __name__ == '__main__':
	intro()
	main()

