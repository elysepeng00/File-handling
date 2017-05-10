#!/usr/bin/python

import sys, getopt
import os
import re
from collections import OrderedDict

def main(argv):
        technology = ''
	process = ''
	GDS_full_path = ''
	schematic_netlist_full_path = ''
	top_cell_name = ''
	RTL_verilog_full_path = ''
	DEF_full_path = ''
	power_value = ''
        try:
           opts, args = getopt.getopt(argv, "ht:p:g:s:n:r:d:v:",["technology=","process=","GDS_full_path=", "schematic_netlist_full_path=", "top_cell_name=", "RTL_verilog_full_path=", "DEF_full_path=", "power_value="])
        except gettop.GetoptError:
           print 'copy.py -t Technology(ex:tsmc65 or umc45) -p Process(ex:6m) -g layout_full_path(GDS full path) -s sch_full_path(schematic netlist full path) -n top_cell_name -r RTL_verilog_full_path -d DEF_full_path -v power_value'
           sys.exit(2)
        for opt, arg in opts:
                if opt == '-h':
                        print 'copy.py -t Technology(ex:tsmc65 or umc45) -p Process(ex:6m) -g layout_full_path(GDS full path) -s sch_full_path(schematic netlist full path) -n top_cell_name -r RTL_verilog_full_path -d DEF_full_path -v power_value'
                        sys.exit()
                elif opt in("-t", "--technology"):
                        technology = arg
                elif opt in("-p", "--process"):
                        process = arg
                elif opt in("-g", "--GDS_full_path"):
                        GDS_full_path = arg
                elif opt in("-s", "--schematic_netlist_full_path"):
                        schematic_netlist_full_path = arg
                elif opt in("-n", "--top_cell_name"):
                        top_cell_name = arg
                elif opt in("-r", "--RTL_verilog_full_path"):
                        RTL_verilog_full_path = arg
                elif opt in("-d", "--DEF_full_path"):
                        DEF_full_path = arg
                elif opt in("-v", "--power_value"):
                        power_value = arg
    currentTechProcess = technology + ', ' + process
	dPower = OrderedDict()
    dDRC = OrderedDict()
	dFoundry = {}
	dTechDetail = {}
	keyFoundry = ""
	key = ""
	val = ""
	with open("TechnologyFile", 'r') as f:
		for line in f:
			if not line:
				continue
			if (line.find(':') == -1):
				dTechDetail[key.strip()] += '\n' + line
			else:
				(key, val) = line.split(":")
				key = key.strip()
                val = val.strip()

				if (not key):
					continue
				if (not val):
					if (dTechDetail):
						dFoundry[keyFoundry] = dTechDetail
					dTechDetail = {}
					keyFoundry = key
				else:
					dTechDetail[key] = val
		if (dTechDetail):
			dFoundry[keyFoundry] = dTechDetail
	
	#output Power file
	filename = "/home/yujie/CS385/pwr/PowerFile"
        if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
        with open("PowerFile", 'r') as f, open("TechnologyFile", 'r') as f1, open(filename, 'w') as f2:
                read_data = f.read()
		#split file content to key val pairs
		elements = re.split('[ \n\r\t]+-', read_data)
		for element in elements:
			if (element.find(' ') == -1):
				dPower[element] = ""
				key = ""
				val = ""
			else:
				(key, val) = element.split(' ', 1)
				key = key.strip()
				val = val.strip()
				dPower[key] = val
			#grep and replace value from Foundry and Design data
			if (key in dFoundry[currentTechProcess]):
				dPower[key] = dFoundry[currentTechProcess][key]
			else:
				if (key == 'dotlib'):
					dPower[key] = dFoundry[currentTechProcess]['lib']
			
		dPower['gds'] = GDS_full_path
		dPower['sch'] = schematic_netlist_full_path
                dPower['def'] = DEF_full_path
                dPower['vdd'] = power_value
 
                #write dPower key vals to powerFile in the order they were inserted
		spam = OrderedDict(dPower)
		for key, val in spam.iteritems():
			if (val):
				f2.write('-')
			f2.write(key+' ')
			if (val):
				f2.write(val+' ')
		f2.write('\n')

        #output Synthesis file
	filename = "/home/yujie/CS385/syn/Logic_Synthesis_file"
        if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
        with open("Logic_Synthesis_file", 'r') as f, open(filename, 'w') as f1:
                read_data = f.read()
                new_data = re.sub('read -f verilog [^\s]+', 'read -f verilog ' + RTL_verilog_full_path, read_data)
                f1.write(new_data)
	
	
	#output DRC run file
	filename = "/home/yujie/CS385/drc/DRC_run_file"        
	if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
        with open("DRC_run_file", 'r') as f, open(filename, 'w') as f1:
                read_data = f.read()
		new_data = re.sub('-top_cell [^\s]+', '-top_cell ' + top_cell_name, read_data)
		new_data = re.sub('-gds [^\s]+', '-gds ' + GDS_full_path, new_data)
		new_data = re.sub('-deck [^\s]+', '-deck ' + dFoundry[currentTechProcess]['drc'], new_data)
                f1.write(new_data)

	
	#output LVS run file	
	filename = "/home/yujie/CS385/lvs/LVS_run_file"
        if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
        with open("LVS_run_file", 'r') as f, open(filename, 'w') as f1:
                read_data = f.read()
		new_data = re.sub('-top [^\s]+', '-top ' + top_cell_name, read_data)
                new_data = re.sub('-gds [^\s]+', '-gds ' + GDS_full_path, new_data)
		new_data = re.sub('-sch [^\s]+', '-sch ' + schematic_netlist_full_path, new_data)
                new_data = re.sub('-deck [^\s]+', '-deck ' + dFoundry[currentTechProcess]['lvs'], new_data)
                f1.write(new_data)


	#output dtmf.conf file	
	filename = "/home/yujie/CS385/pnr/dtmf.conf"
        if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
        with open("dtmf.conf", 'r') as f, open(filename, 'w') as f1:
                read_data = f.read()
                new_data = re.sub('"[^"]+\.sdc"', '"' + dFoundry[currentTechProcess]['sdc'] + '"', read_data)
                new_data = re.sub('"[^"]+\.lib"', '"' + dFoundry[currentTechProcess]['lib'] + '"', new_data)
		new_data = re.sub('"[^"]+\.lef"', '"' + dFoundry[currentTechProcess]['lef'] + '"', new_data)
                f1.write(new_data)


if __name__ == "__main__":
	main(sys.argv[1:])
