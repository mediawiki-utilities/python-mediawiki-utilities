import logging
from multiprocessing import Process
from queue import Empty

from .iteration import Iterator
from .functions import open_file

logger = logging.getLogger("mw.dump.processor")

class Processor(Process):
	
	
	def __init__(self, pathq, outputq, process_dump, callback=lambda:None, logger=logger):
		self.pathq        = pathq
		self.outputq      = outputq
		self.process_dump = process_dump
		self.callback     = callback
		self.logger       = logger
		Process.__init__(self)
	
	def run(self):
		try:
			while True:
				
				foo = self.pathq.qsize() # This is done to force the queue to 
				                         # reset and behave reasonably.  
				path = self.pathq.get(block=False)
				dump = Iterator.from_file(open_file(path))
				logger.info("Beginning to process {0}.".format(repr(path)))
				try:
					for out in self.process_dump(dump, path):
						self.outputq.put(out)
				except Exception as e:
					logger.error(
						"Failed while processing dump {0}: {1}".format(
							repr(path), e)
					)
					
				
			
			
		except Empty:
			self.logger.info("Nothing left to do.  Shutting down thread.")
		finally:
			self.callback()
