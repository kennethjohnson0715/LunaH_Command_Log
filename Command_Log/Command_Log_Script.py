from cgi import print_arguments
import csv
from xml.sax import parseString

## PLEASE READ ##
## This python script will take in .bin file from/at the telemetry processor and write it out to a * Command_Log_history.csv * file
## The Command_Log_history.csv will tell you last Command initiated, the following byte values, as well as RADIO_RAW and THRUSTER_DIRECT_CMD sub commands

thisdict =	{}
RADIO_RAW_dict = {}
THRUSTER_DIRECT_dict = {}

cmdlog = open("CLH_bytes.csv", "w") # "w" is for writing to the file [also reads it too]


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






#----------- Read .bin file (example telemetry packet binary file) ------------#
# READ ME
# read at telemetry processor?

with open("debug_pkt.bin", "rb") as file: # replace this .bin file with the telemetry data you want to read 
    
    
    # Read the binary content and create bytearray
    telemetry_packet = file.read()
    telemetry_packet_bytes = bytearray(telemetry_packet)



    # DRVD_LAST_XB1_CMD_EXECUTED is bytes 50-51
    DRVD_LAST_XB1_CMD_EXECUTED = int.from_bytes(telemetry_packet[50:52], "big")

    cmdlog.write(thisdict[str(DRVD_LAST_XB1_CMD_EXECUTED)])
    cmdlog.write(",")
    

    LAST_ACC_CMD_BYTES3 = int.from_bytes(telemetry_packet[52:53], "big")
    LAST_ACC_CMD_BYTES6 = int.from_bytes(telemetry_packet[55:56], "big")
    
    if DRVD_LAST_XB1_CMD_EXECUTED == 7947: #7947 is opcode/APid for RADIO_RAW_LAST_CMD
        
        #print(RADIO_RAW_dict[str(LAST_ACC_CMD_BYTES6)])
        cmdlog.write(RADIO_RAW_dict[str(LAST_ACC_CMD_BYTES6)])
        cmdlog.write(",")
    else:

    
            if DRVD_LAST_XB1_CMD_EXECUTED == 9217: #9217 is opcode/APid THRUSTER_DIRECT_LAST_CMD
                
                #print(THRUSTER_DIRECT_dict[str(LAST_ACC_CMD_BYTES3)])
                cmdlog.write(THRUSTER_DIRECT_dict[str(LAST_ACC_CMD_BYTES3)])
                cmdlog.write(",")
            else:
                cmdlog.write(" ,")


    
    
    
    # LAST_ACC_CMD_BYTES1 is byte 50
    LAST_ACC_CMD_BYTES1 = int.from_bytes(telemetry_packet[50:51], "big")
        
    cmdlog.write(str(LAST_ACC_CMD_BYTES1))
    cmdlog.write(",")
    
    
    # LAST_ACC_CMD_BYTES2 is byte 51
    LAST_ACC_CMD_BYTES2 = int.from_bytes(telemetry_packet[51:52], "big")

    cmdlog.write(str(LAST_ACC_CMD_BYTES2))
    cmdlog.write(",")

   
    # LAST_ACC_CMD_BYTES3 is byte 52
    LAST_ACC_CMD_BYTES3 = int.from_bytes(telemetry_packet[52:53], "big")

    cmdlog.write(str(LAST_ACC_CMD_BYTES3))
    cmdlog.write(",")


    # LAST_ACC_CMD_BYTES4 is byte 53
    LAST_ACC_CMD_BYTES4 = int.from_bytes(telemetry_packet[53:54], "big")

    cmdlog.write(str(LAST_ACC_CMD_BYTES4))
    cmdlog.write(",")


    # LAST_ACC_CMD_BYTES5 is byte 54
    LAST_ACC_CMD_BYTES5 = int.from_bytes(telemetry_packet[54:55], "big")

    cmdlog.write(str(LAST_ACC_CMD_BYTES5))
    cmdlog.write(",")


    # LAST_ACC_CMD_BYTES6 is byte 55
    LAST_ACC_CMD_BYTES6 = int.from_bytes(telemetry_packet[55:56], "big")

    cmdlog.write(str(LAST_ACC_CMD_BYTES6))
    cmdlog.write(",")


    # LAST_ACC_CMD_BYTES7 is byte 56
    LAST_ACC_CMD_BYTES7 = int.from_bytes(telemetry_packet[56:57], "big")

    cmdlog.write(str(LAST_ACC_CMD_BYTES7))
    cmdlog.write(",")


    # LAST_ACC_CMD_BYTES8 is byte 57
    LAST_ACC_CMD_BYTES8 = int.from_bytes(telemetry_packet[57:58], "big")

    cmdlog.write(str(LAST_ACC_CMD_BYTES8))
    cmdlog.write(",")

cmdlog.close()




headers = ["Command Name","Sub Command Name","LAST_ACC_CMD_BYTES1","LAST_ACC_CMD_BYTES2","LAST_ACC_CMD_BYTES3","LAST_ACC_CMD_BYTES4","LAST_ACC_CMD_BYTES5","LAST_ACC_CMD_BYTES6","LAST_ACC_CMD_BYTES7","LAST_ACC_CMD_BYTES8",]

data = open("CLH_bytes.csv", 'r')

f = open("Command_Log_history.csv", "w")

for cell in headers:
    f.write(cell)
    if headers.index(cell) != len(headers) - 1: #Check if we are at end of row
        f.write(',')
f.write('\n') #writes a new line

for row in data: 
    f.write(row)









