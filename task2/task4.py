stat = dict()
f = open("./access_log")
for line in f:
      str = line.split(" ")
      stat[str[0]] = stat.get(str[0],0) +1
c = (sorted(stat, key=stat.get, reverse=True))
print c[:10]
