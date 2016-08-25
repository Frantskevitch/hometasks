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
decorator = config.getboolean('common', 'state')


def trace(fn):
    def wrapped(*args, **kwargs):
        f = open('decout.txt', 'a')
        f.write("Enter {0} function ".format(fn.__name__) + " with parameters {0}".format([*args])+ '\n')
        f.close()
        print("Enter {0} function ".format(fn.__name__) + " with parameters {0}".format([*args]))
        fn(*args, **kwargs)
        print("Exit {0}".format(fn.__name__))
        f = open('decout.txt', 'a')
        f.write("Exit {0}".format(fn.__name__) + '\n')
        f.close()
    return wrapped if decorator else fn


# get system info
class GatherInfo(object):
    def systeminfo(self):
        cpu = psutil.cpu_percent(interval=1)
        v_mem = (psutil.virtual_memory()[3] / 1024 / 1024).__round__(2)
        mb_send = (psutil.net_io_counters()[0] / 1024 / 1024).__round__(2)
        mem_inf = (psutil.disk_usage('/')[2] / 1024 / 1024 / 1024).__round__(2)
        return cpu, mem_inf, v_mem, mb_send

    # get timestamp
    def timestamp(self):
        tmptime = time.time()
        ts = datetime.datetime.fromtimestamp(tmptime).strftime('%d-%m-%Y %H:%M:%S')
        return " " + ts + ":"

    def get_sn_num(self):
        f = open('stat.txt', 'r')
        try:
            last = f.readlines()[-1]
            split_str = last.split(" ")
            sn = int(split_str[1]) + 1
            return int(sn)
        except IndexError:
            print("TIMESTAMP ERR")
            sn = 1
            return int(sn)


# write to file
class WriteToFile(GatherInfo):
    @trace
    def json_write(self, log, snj):
        info = GatherInfo()
        jsonf = open(log, "a")
        jsonf.write('\n"SNAPSHOT {0}" : "{1}",\n'.format(snj, info.timestamp()))
        jsonf.write('\n"CPU":\n')
        json.dump({"Percent load": info.systeminfo()[0]}, jsonf, indent=1)
        jsonf.write('\n,"Space":\n')
        json.dump({"Avaliable GB": info.systeminfo()[1]}, jsonf, indent=1)
        jsonf.write('\n,"Vmemory": \n')
        json.dump({"Used MB": info.systeminfo()[2]}, jsonf, indent=1)
        jsonf.write('\n,"Network":\n')
        json.dump({"MB send": info.systeminfo()[3]}, jsonf, indent=1)
        jsonf.write(",\n\n")
        jsonf.close()

    @trace
    def txt_write(self, log):
        info = GatherInfo()
        sn = info.get_sn_num()
        f = open(log, 'a')
        f.write("\n" + "SNAPSHOT: " + str(sn) + str(info.timestamp()) +
                "  CPU percent: " + str(info.systeminfo()[0]) +
                "  Space Avaliable GB: " + str(info.systeminfo()[1]) +
                "  Vmemory used MB: " + str(info.systeminfo()[2]) +
                "  MB send: " + str(info.systeminfo()[3])
                )
        f.close()


@trace
def writelog(snj):
    write = WriteToFile()
    if output == "json":
            write.json_write(log='stat.json', snj=snj)
    elif output == "txt":
        write.txt_write(log='stat.txt')

    else:
        print("check config")


snj = 1
while True:
    writelog(snj)
    time.sleep(int(interval))
    snj += 1


