import psutil, datetime, time, json, configparser

config = configparser.ConfigParser()
config.read('config.ini')
output = config.get('common', 'output')
interval = config.get('common', 'interval')
#get system info
def systeminfo():
   CPU= psutil.cpu_percent(interval=1)
   VMem = (psutil.virtual_memory()[3]/1024/1024)
   MBsend = (psutil.net_io_counters()[0]/1024/1024)
   MemInf = (psutil.disk_usage('/')[2]/1024/1024/1024)
   return CPU, MemInf, VMem, MBsend
  #get timestamp
def timestamp():
    tmptime = time.time()
    TS = datetime.datetime.fromtimestamp(tmptime).strftime('%d-%m-%Y %H:%M:%S')
    return "   "+TS + ": "


def txt_write():
    # get last snapshot number from txt if empty =1
    def getSnNum():
        f = open('stat.txt', 'r')
        try :
            last = f.readlines()[-1].decode()
            str = last.split(" ")
            SN = int(str[1]) +1
        except IndexError:
            SN =1
        return int(SN)
    SN= getSnNum()

    while True:
        f = open('stat.txt', 'a')
        f.write("\n"+ "SNAPSHOT "+str(SN)+ str(timestamp())+ \
                "  CPU percent: " + str(systeminfo()[0])+ \
                "  Space Avaliable GB: " + str(systeminfo()[1]) + \
                "  Vmemory used MB: " + str(systeminfo()[2]) + \
                "  MB send: " + str(systeminfo()[3])
                )
        SN +=1
        f.close()
        time.sleep(int(interval))

def json_write():
       i = 1
       while True:
            jsonf = open('stat.json', "a")
            jsonf.write("\nSNAPSHOT {0} : {1}\n".format(i, timestamp()))
            jsonf.write("\nCPU percent\n")
            json.dump(systeminfo()[0], jsonf, indent=1)
            jsonf.write("\nSpace Avaliable GB\n")
            json.dump(systeminfo()[1], jsonf, indent=1)
            jsonf.write("\nVmemory used MB\n")
            json.dump(systeminfo()[2], jsonf, indent=1)
            jsonf.write("\nMB send\n")
            json.dump(systeminfo()[3], jsonf, indent=1)
            jsonf.write("\n\n")
            jsonf.close()
            i +=1
            time.sleep(int(interval))

if output == "json":
    json_write()
elif output == "txt":
    txt_write()
else:
    print "check config"