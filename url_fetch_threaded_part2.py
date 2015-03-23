import Queue
import threading 
import urllib2
import time
from BeautifulSoup import BeautifulSoup


hosts = ["http://yahoo.com","http://google.com","http://amazon.com", "http://ibm.com","http://apple.com"]

queue = Queue.Queue()
out_queue = Queue.Queue()

class ThreadUrl(threading.Thread):
	""" Threaded URL grab """
	def __init__( self, queue, out_queue ):
		threading.Thread.__init__(self)
		self.queue = queue
		self.out_queue = out_queue

	def run(self):
		while True:
			# grabs host from Queue
			host = self.queue.get()

			# grabs urls of hosts and prints first 2024 bytes of page
			url = urllib2.urlopen(host)
			chunk =  url.read()

			# place the chunk into the out queue
			self.out_queue.put(chunk)

			# signals to queue job is done
			self.queue.task_done()

class DatamineThread(threading.Thread):
	""" Threading Url Grab """
	def __init__( self, out_queue):
		threading.Thread.__init__(self)
		self.out_queue = out_queue

	def run(self):
		while True:
			# grabs host from queue
			chunk = self.out_queue.get()

			# parse the chunk
			soup = BeautifulSoup(chunk)
			print soup.findAll(['title'])

			# signals to queue job is done
			self.out_queue.task_done()


start = time.time()

def main():
	# spawn a pool of threads, and pass them a queue instance
	for i in range(5):
		t = ThreadUrl(queue, out_queue)
		t.setDaemon(True)
		t.start()

	# populate the queue with data
	for host in hosts:
		queue.put(host)

	for i in range(5):
		dt = DatamineThread(out_queue)
		dt.setDaemon(True)
		dt.start()

	# wait on the queue until everything has been processed
	queue.join()
	out_queue.join()

main()
print "Elapsed Time: %s" % ( time.time() - start )