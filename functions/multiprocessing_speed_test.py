from multiprocessing import Process, Queue, Manager
import random
import time

def rand_num(output, x):
	num = random.randint(0, 10)
	output[x] = num



if __name__ == "__main__":
	manager = Manager()
	output = manager.list([0]*100)

	start = time.time()
	processes = [Process(target=rand_num, args=(output, x)) for x in range(100)]

	for p in processes:
		p.start()

	for p in processes:
		p.join()
	print(output)
	print(time.time() - start)