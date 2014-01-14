import logging
from multiprocessing import Queue, cpu_count, Value
from queue import Empty

from .processor import Processor
from .functions import file

logger = logging.getLogger("mw.dump.map")

def map(paths, process_dump, threads=cpu_count(), output_buffer=100):
	"""
	Maps a function across all of the pages in a set of dump files and returns
	an (order not guaranteed) iterator over the output.  Increasing the 
	`output_buffer` size will allow more mapplications to happen before the 
	output is read, but will consume memory to do so.  Big output buffers 
	are benefitial when the resulting iterator from this map will be read in
	bursts.
	
	The `process_dump` function must return an iterable object (such as a 
	generator).  If your process_dump function does not need to produce 
	output, make it return an empty iterable upon completion (like an empty
	list).
	
	:Parameters:
		dumps : `list`
			a list of paths to dump files to process
		process_dump : `function`
			a function to run on every 'dump.Iterator'
		threads : `int`
			the number of individual processing threads to spool up
		output_buffer : `int`
			the maximum number of output values to buffer. 
	"""
	pathsq  = queue_files(paths)
	outputq = Queue(maxsize=output_buffer)
	running = Value('i', 0)
	threads = max(1, min(int(threads), pathsq.qsize()))
	
	def dec(): running.value -= 1
	
	for i in range(0, threads):
		running.value += 1
		Processor(
			pathsq,
			outputq,
			process_dump,
			callback=dec
		).start()
	
	#output while processes are running
	while running.value > 0:
		try:          yield outputq.get(timeout=.25)
		except Empty: pass
	
	#finish yielding output buffer
	try:
		while True: yield outputq.get(block=False) 
	except Empty: 
		pass

def queue_files(paths):
	"""
	Produces a `multiprocessing.Queue` containing path for each value in
	`paths` to be used by the `Processor`s.
	
	:Parameters:
		paths : iterable
			the paths to add to the processing queue
	"""
	q = Queue()
	for path in paths: q.put(file(path))
	return q
