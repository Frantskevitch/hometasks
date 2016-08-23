import psutil
import datetime
import time
import json
import configparser

# reading config
config = configparser.ConfigParser()
config.read('config.ini')
output = config.get('common', 'output')
interval = config.get('common', 'interval')


# get system info
class GatherInfo(object):
    @staticmethod
    def systeminfo():
        cpu = psutil.cpu_percent(interval=1)
        v_mem = (psutil.virtual_memory()[3] / 1024 / 1024)
        mb_send = (psutil.net_io_counters()[0] / 1024 / 1024)
        mem_inf = (psutil.disk_usage('/')[2] / 1024 / 1024 / 1024)
        return cpu, mem_inf, v_mem, mb_send

    # get timestamp
    @staticmethod
    def timestamp():
        tmptime = time.time()
        ts = datetime.datetime.fromtimestamp(tmptime).strftime('%d-%m-%Y %H:%M:%S')
        return " " + ts + ":"

    @staticmethod
    def get_sn_num():
        f = open('stat.txt', 'r')
        try:
            last = f.readlines()[-1].decode()
            split_str = last.split(" ")
            sn = int(split_str[1]) + 1
            return int(sn)
        except IndexError:
            sn = 1
            return int(sn)


# write to file
class WriteToFile(GatherInfo):
    @staticmethod
    def json_write(log):
        sn = 1
        while True:
            jsonf = open(log, "a")
            jsonf.write('\n{ \n')
            jsonf.write('\n"SNAPSHOT {0}" : "{1}",\n'.format(sn, WriteToFile.timestamp()))
            jsonf.write('\n"CPU":\n')
            json.dump({"Percent load": WriteToFile.systeminfo()[0]}, jsonf, indent=1)
            jsonf.write('\n,"Space":\n')
            json.dump({"Avaliable GB": WriteToFile.systeminfo()[1]}, jsonf, indent=1)
            jsonf.write('\n,"Vmemory": \n')
            json.dump({"Used MB": WriteToFile.systeminfo()[2]}, jsonf, indent=1)
            jsonf.write('\n,"Network":\n')
            json.dump({"MB send": WriteToFile.systeminfo()[3]}, jsonf, indent=1)
            jsonf.write("\n\n")
            jsonf.write('\n} \n')
            jsonf.close()
            sn += 1
            time.sleep(int(interval))

    @staticmethod
    def txt_write(log):
        sn = GatherInfo.get_sn_num()
        while True:
            f = open(log, 'a')
            f.write("\n" + "SNAPSHOT: " + str(sn) + str(WriteToFile.timestamp()) +
                    "  CPU percent: " + str(WriteToFile.systeminfo()[0]) +
                    "  Space Avaliable GB: " + str(WriteToFile.systeminfo()[1]) +
                    "  Vmemory used MB: " + str(WriteToFile.systeminfo()[2]) +
                    "  MB send: " + str(WriteToFile.systeminfo()[3])
                    )
            sn += 1
            f.close()
            time.sleep(int(interval))


def writelog():
    if output == "json":
        WriteToFile.json_write('stat.json')
    elif output == "txt":
        WriteToFile.txt_write('stat.txt')
    else:
        print "check config"

try:
    writelog()
except:
    print "something went wrong"
