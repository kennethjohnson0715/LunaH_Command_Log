from asyncore import read
import csv
from xml.sax import parseString
import ast
import pandas as pd

## PLEASE READ ##
## This python script is to be used for the influxdb query results in a csv format
## it will write the resulting Command History into a Command_Log.txt file



opcode = open("opcode.csv", "w")
cmdlog = open("Command_Log.txt", "w")


#---------using panda data tool- to do this use -pip install panda or -import pandas as pd---------#

rt = pd.read_csv("03_03_2022_cmd_history_v1.csv") # insert influxdb command history csv here

byte_1 = rt['LAST_ACC_CMD_BYTES1'] #apid byte
byte_2 = rt['LAST_ACC_CMD_BYTES2'] #opcode byte
byte_3 = rt['LAST_ACC_CMD_BYTES3'] 
byte_4 = rt['LAST_ACC_CMD_BYTES4']
byte_5 = rt['LAST_ACC_CMD_BYTES5']
byte_6 = rt['LAST_ACC_CMD_BYTES6'] 

for index in range(0, len(rt)):    

    a = int(byte_1[index])
    b = int(byte_2[index]) 

    hex_apid_op = hex(a) + "0" + f'{b:x}' + "\n" #ask about opcode formatting, ie when we concatonate apid and opcode then add the zero

    apid_opcode = int(hex_apid_op,0) # removes the hex prefix 0x from hex_apid_op
        
    opcode.write(('{},{},{},{},{},{},{},{},{}\n'.format(rt['time'][index],rt['TAI_SECONDS'][index], apid_opcode, rt['LAST_ACC_CMD_BYTES3'][index], rt['LAST_ACC_CMD_BYTES4'][index], rt['LAST_ACC_CMD_BYTES5'][index], rt['LAST_ACC_CMD_BYTES6'][index], rt['LAST_ACC_CMD_BYTES1'][index], rt['LAST_ACC_CMD_BYTES2'][index])))

    #RADIO_RAW and THRUSTER_D sub commands as well as byte values after commands, TAI seconds


file = pd.read_csv("opcode.csv")

# adding header
headerList = ["time","DRVD_TAI_SECONDS","line[2]","LAST_ACC_CMD_BYTES3","LAST_ACC_CMD_BYTES4","LAST_ACC_CMD_BYTES5","LAST_ACC_CMD_BYTES6","LAST_ACC_CMD_BYTES1","LAST_ACC_CMD_BYTES2"]

# converting data frame to csv
file.to_csv("influxdb.csv", header=headerList, index=False)




thisdict =	{}
RADIO_RAW_dict = {}
THRUSTER_DIRECT_dict = {}

with open("Command Dictionary.csv", "r") as cd:
   reader = csv.reader(cd)
   for line in reader:
        
        thisdict[(line[0])]=line[1]

with open("RADIO_RAW_dictionary.csv", "r") as rr: # "r" is only for reading file
     reader = csv.reader(rr)
     for line in reader:
    
        RADIO_RAW_dict[(line[0])]=line[1]

with open("THRUSTER_DIRECT_CMD_dictionary.csv", "r") as td:
     reader = csv.reader(td)
     for line in reader:
    
        THRUSTER_DIRECT_dict[(line[0])]=line[1]


with open("influxdb.csv", "r") as d:
                
    reader = csv.reader(d)

    lastcmd = ""

    
    for i, line in enumerate(reader): 

        if i==0:
            pass
        if line[2] == str(7947): #7947 is opcode/APid for RADIO_RAW_LAST_CMD

            if lastcmd != thisdict.get(line[2]):       
                   
                lastcmd = thisdict.get(line[2])
            
                print('{} {} {} {} {} {} {} {} {} {}'.format(line[0], line[1], thisdict.get(line[2]), RADIO_RAW_dict[line[6]], line[7], line[8], line[3], line[4], line[5], line[6])) 
                cmdlog.write('{} {} {} {} {} {} {} {} {} {}\n '.format(line[0], line[1], thisdict.get(line[2]), RADIO_RAW_dict[line[6]], line[7], line[8], line[3], line[4], line[5], line[6])) 

        
        elif line[2] == str(9217): #9217 is opcode/APid THRUSTER_DIRECT_LAST_CMD
            if lastcmd != thisdict.get(line[2]):       
                   
                lastcmd = thisdict.get(line[2])
            
                print('{} {} {} {} {} {} {} {} {} {}'.format(line[0], line[1], thisdict.get(line[2]), THRUSTER_DIRECT_dict[line[3]], line[7], line[8], line[3], line[4], line[5], line[6])) 
                cmdlog.write('{} {} {} {} {} {} {} {} {} {}\n '.format(line[0], line[1], thisdict.get(line[2]), THRUSTER_DIRECT_dict[line[3]], line[7], line[8], line[3], line[4], line[5], line[6]))          
                   
        else:
            if lastcmd != thisdict.get(line[2]):       
                   
                lastcmd = thisdict.get(line[2])
            
                print('{} {} {} {} {} {} {} {} {}'.format(line[0], line[1], thisdict.get(line[2]), line[7], line[8], line[3], line[4], line[5], line[6])) 
                cmdlog.write('{} {} {} {} {} {} {} {} {}\n '.format(line[0], line[1], thisdict.get(line[2]), line[7], line[8], line[3], line[4], line[5], line[6])) 
            
      
        



