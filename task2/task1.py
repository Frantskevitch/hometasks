lkeys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
litems = ['a','b','c','d']
dict0= dict(zip(lkeys , litems + [None]*(len(lkeys)-len(litems))))
print dict0