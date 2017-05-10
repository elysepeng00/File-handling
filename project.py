#!/usr/bin/python

import sys, getopt
import re
import os

class DesignData:
	def __init__(self, datafile):
		myDataFile =  "/home/yujie/CS385/DesignData"
                if (datafile):
                        myDataFile = datafile
                dDesignData = {}
                with open(myDataFile) as f:
                        for line in f:
                                if (not line):
                                        continue
                                (key, val) = line.split(":")
                                key = key.strip()
                                #import pdb
                                #pdb.set_trace()
                                val = re.sub('\([^)]+\)', '', val)
                                val = val.strip()
                                dDesignData[key] = val
		self.g = dDesignData["GDS"]
                self.s = dDesignData["Schematic Netlist"]
                self.n = dDesignData["Top cell name"]
                self.r = dDesignData["RTL verilog"]
                self.d = dDesignData["DEF"]
                self.v = dDesignData["Power value"]

class FileGenerator:
	def __init__(self, t, p, objDesignData):
		self.t = t;
                self.p = p;
		self.g = objDesignData.g
		self.s = objDesignData.s
		self.n = objDesignData.n
		self.r = objDesignData.r
		self.d = objDesignData.d
		self.v = objDesignData.v

def main(argv):
	try:
	   opts, args = getopt.getopt(argv, "ht:p:",["technology=","process="])
	except gettop.GetoptError:
	   print 'project.py -t Technology(ex:tsmc65 or umc45) -p Process(ex:6ml)'
	   sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print '.py -t Technology(ex:tsmc65 or umc45) -p Process(ex:6m)'
			sys.exit()
		elif opt in("-t", "--technology"):
			t = arg
		elif opt in("-p", "--process"):
                        p = arg
	
	objDesignData = DesignData("/home/yujie/CS385/DesignData")	
	fileGenerator = FileGenerator(t, p, objDesignData)	
		
	cmd = "./code.py"
	for key, val in fileGenerator.__dict__.iteritems():
		cmd += " -" + key + " " + val
	#project step A) excute your code
	os.system(cmd)

if __name__ == "__main__":
	main(sys.argv[1:])
