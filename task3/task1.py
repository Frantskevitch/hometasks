import psutil
import time
import json
import configparser
import datetime

# reading config
config = configparser.ConfigParser()
config.read('config.ini')
output = config.get('common', 'output')
interval = config.get('common', 'interval')


# get system info
def systeminfo():
    cpu = psutil.cpu_percent(interval=1)
    v_mem = (psutil.virtual_memory()[3] / 1024 / 1024)
    mb_send = (psutil.net_io_counters()[0] / 1024 / 1024)
    mem_inf = (psutil.disk_usage('/')[2] / 1024 / 1024 / 1024)
    return cpu, mem_inf, v_mem, mb_send


# get timestamp
def timestamp():
    tmptime = time.time()
    ts = datetime.datetime.fromtimestamp(tmptime).strftime('%d-%m-%Y %H:%M:%S')
    return " " + ts + ":"


# write to txt file
def txt_write():
    # get last snapshot number from txt if empty =1
    def get_sn_num():
        log = open('stat.txt', 'r')
        try:
            last = log.readlines()[-1].decode()
            split_str = last.split(" ")
            snap_num = int(split_str[1]) + 1
        except IndexError:
            snap_num = 1
        return int(snap_num)

    sn = get_sn_num()
    # writing
    while True:
        f = open('stat.txt', 'a')
        f.write("\n" + "SNAPSHOT " + str(sn) + str(timestamp()) +
                "  CPU percent: " + str(systeminfo()[0]) +
                "  Space Avaliable GB: " + str(systeminfo()[1]) +
                "  Vmemory used MB: " + str(systeminfo()[2]) +
                "  MB send: " + str(systeminfo()[3])
                )
        sn += 1
        f.close()
        time.sleep(int(interval))


# write to json file
def json_write():
    sn = 1
    while True:
        jsonf = open('stat.json', "a")
        jsonf.write('\n{ \n')
        jsonf.write('\n"SNAPSHOT {0}" : "{1}",\n'.format(sn, timestamp()))
        jsonf.write('\n"CPU":\n')
        json.dump({"Percent load": systeminfo()[0], }, jsonf, indent=1)
        jsonf.write('\n,"Space":\n')
        json.dump({"Avaliable GB": systeminfo()[1], }, jsonf, indent=1)
        jsonf.write('\n,"Vmemory": \n')
        json.dump({"Used MB": systeminfo()[2], }, jsonf, indent=1)
        jsonf.write('\n,"Network":\n')
        json.dump({"MB send": systeminfo()[3], }, jsonf, indent=1)
        jsonf.write("\n\n")
        jsonf.write('\n} \n')
        jsonf.close()
        sn += 1
        time.sleep(int(interval))


# main
if output == "json":
    json_write()
elif output == "txt":
    txt_write()
else:
    print "check config"
