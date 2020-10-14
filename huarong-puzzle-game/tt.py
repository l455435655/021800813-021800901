import time

st = time.time()

time.sleep(1)
et = time.time()
print((time.localtime(et)))

print(time.strftime("%H:%M:%S",time.localtime(et-st) ))
