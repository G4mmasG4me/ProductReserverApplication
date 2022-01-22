import random
import time

unordered_list = []
for i in range(10000):
  unordered_list.append(random.randint(0, 10000))

start = time.time()
for i in range(len(unordered_list)):
  for j in range(len(unordered_list)-1):
    if unordered_list[j] > unordered_list[j+1]:
      unordered_list[j], unordered_list[j+1] = unordered_list[j+1], unordered_list[j]
end = time.time()
run_time = end - start
print(run_time)