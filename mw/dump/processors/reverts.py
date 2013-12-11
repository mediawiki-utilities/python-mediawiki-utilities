import sys, subprocess, os, errno, re, argparse, logging, hashlib, types
from itertools import repeat, takewhile
from collections import deque
import wmf

class cirquelar(list):
	"""
	Circular queue use for tracking the most recent N things appended to it.
	
	Specifically used by dequedict below.
	"""
	def __init__(self, iterable=[], maxlen=None):
		if maxlen != None: self.maxlen = int(maxlen)
		else:              self.maxlen = len(iterable)
			
		
		list.__init__(self, repeat(None, self.maxlen))
		self.count = 0
		for item in iterable:
			self.append(item)
		
	def append(self, item):
		currItem = list.__getitem__(self, self._next())
		list.__setitem__(self, self._next(), item)
		self.count += 1
		return currItem
	
	def extend(self, iterable):
		for item in iterable: self.append(item)
	
	def _next(self):
		return self.count % self.maxlen
	
	def __getitem__(self, i):
		if i < 0 or i >= len(self): raise IndexError("%s out of range 0 - %s" % (i, len(self)-1))
		return list.__getitem__(self, self.__internalIndex(i))
	
	def __getslice__(self, start, end):
		for i in range(start, end): yield self.__getitem__(i)
		
	def __setitem__(self, i, item):
		if i < 0 or i >= len(self): raise IndexError("%s out of range 0 - %s" % (i, len(self)-1))
		return list.__setitem__(self, self.__internalIndex(i), item)
	
	def __internalIndex(self, i):
		return (self._next() - len(self)) + i
	
	def __iter__(self):
		for i in range(0, len(self)): yield self.__getitem__(i)
	def __reversed__(self):
		for i in range(len(self)-1, -1, -1): yield self.__getitem__(i)
	
	def __str__(self): return repr(self)
	
	def __repr__(self):
		return "%s(%r)" % (
			self.__class__.__name__,
			list(self)
		)
	
	def __len__(self):
		return min(self.maxlen, self.count)
		
	
class dequedict(dict):
	"""
	Represents a dictionary of maxlen recent items.
	"""
	def __init__(self, pairs=[], maxlen=15):
		dict.__init__(self)
		self.circle = cirquelar(maxlen=maxlen)
		
		for key, value in pairs: self.__setitem__(key, value)
	
	def __setitem__(self, key, value):
		values = dict.get(self, key, deque())
		values.append(value)
		
		dict.__setitem__(self, key, values)
		
		expectorate = self.circle.append((key, value))
		
		if expectorate != None:
			oldKey, oldValue = expectorate
			self.__popKey(oldKey)
			
		return expectorate
	
	def insert(self, key, value):
		return self.__setitem__(key, value)
		
	def __getitem__(self, key):
		if key not in self: raise KeyError(key)
		else: return dict.__getitem__(self, key)[-1]
	
	def __len__(self):
		return len(self.circle)
	
	def __str__(self): return repr(self)
	def __repr__(self):
		return "%s(%s)" % (
			self.__class__.__name__,
			", ".join([
				repr(list(self.circle)),
				repr(self.circle.maxlen)
			])
		)
	
	def __iter__(self):
		return self.circle
	
	def __reversed__(self):
		return reversed(self.circle)
	
	def __popKey(self, key):
		values = dict.__getitem__(self, key)
		values.popleft()
		if len(values) == 0:
			dict.__delitem__(self, key)
		
	

def process(dump, page):
	recentRevs = dequedict(maxlen=15)
	for revision in page.readRevisions():
		checksum = hashlib.md5(revision.getText().encode("utf-8")).hexdigest()
		if checksum in recentRevs:
			#found a revert
			revertedToRev = recentRevs[checksum]
			
			#get the revisions that were reverted
			revertedRevs = list(
				takewhile(
					lambda p: p[0] != checksum,
					reversed(recentRevs)
				)
			)
			
			#noop
			if len(revertedRevs) == 0: continue
			
			isVandalism = wmf.isVandalismByComment(revision.getComment())
			
			#write revert row
			yield (
				'revert',
				revision.getId(), 
				revertedToRev.getId(), 
				isVandalism,
				len(revertedRevs)
			)
			
			for c, rev in revertedRevs:
				yield (
					'reverted',
					rev.getId(),
					revision.getId(),
					revertedToRev.getId(), 
					isVandalism,
					len(revertedRevs)
				)
		else:
			pass
		
		recentRevs.insert(checksum, revision)