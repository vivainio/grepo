import pickleshare
import args
import os
from subprocess import *

db = pickleshare.PickleShareDB("~/.grepo")

root = db.get('root', None)

def here_c(args):
	db['root'] = os.getcwd()

def runpeco(input):
	p = Popen('peco', stdin = PIPE, stdout = PIPE)
	fin, fout = p.stdin, p.stdout
	fin.write(input)
	fin.close()
	out = fout.read()
	return out


def peco_and_edit(input):
	lines = runpeco(input).splitlines()
	for l in lines:
		fname, line, text = l.split(':', 2)
		print "pick:", fname
		call(['subl',fname + ':' + line])




def grep_c(args):
	os.chdir(root)
	out = os.popen('git grep -n ' + args.pattern).read()
	#print out
	db['grepoutput'] = out
	peco_and_edit(out)



def pick_c(args):
	os.chdir(root)
	peco_and_edit(db['grepoutput'])
			

def main():
	args.init()

	args.sub('here', here_c, help = 'Set current dir as prjroot')
	s = args.sub('g', grep_c, help = 'Grep the project')
	s.arg("pattern", type=str)
	args.sub('p', pick_c, help = 'Use peco to quick pick one of the earlier choices')
	args.parse()

if __name__ == "__main__":
	main()
