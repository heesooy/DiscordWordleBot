import operator

stats = {1: (2, 12, 3.3), 2:(11, 9, 2.0)}
most = max(stats.items(), key=lambda elem: elem[1][2])

filtered = filter(lambda elem: elem[1][0] >= 3, stats.copy().items())

for filt in filtered:
  print(filt)