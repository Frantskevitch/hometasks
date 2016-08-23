stat = dict()
f = open("./access_log")
for line in f:
    split_str = line.split(" ")
    stat[split_str[0]] = stat.get(split_str[0], 0) + 1
c = (sorted(stat, key=stat.get, reverse=True))
print c[:10]
