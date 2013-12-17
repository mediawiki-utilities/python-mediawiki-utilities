from hashlib import sha1

from .. import reverts
from .tokens import Tokens, Token
from . import defaults

class Version:
	__slots__ = ('tokens')
	
	def __init__(self, tokens=None):
		self.tokens = tokens if tokens != None else Tokens()

class State:
	"""
	Represents the state of word persistence in a page.
	"""
	def __init__(self, tokenize=defaults.TOKENIZE, diff=defaults.DIFF, 
	                   revert_radius=reverts.defaults.RADIUS, 
	                   revert_detector=None):
		self.tokenize  = tokenize
		self.diff = diff
		
		# Either pass a detector or the revert radius so I can make one
		if revert_detector == None:
			self.revert_detector = reverts.Detector(int(revert_radius))
		else:
			self.revert_detector = revert_detector
		
		# Stores the last tokens
		self.last_tokens = None
	
	def process(self, text, revision=None, checksum=None):
		"""
		Modifies the internal state based a change to the content and returns
		the sets of words added and removed.
		"""
		if checksum == None: checksum = sha1(bytes(text, 'utf8')).hexdigest()
		
		version = Version()
		
		revert = self.revert_detector.process(checksum, version)
		if revert != None: # Revert
			
			# Empty words.
			tokens = version.tokens
			tokens_added = Tokens()
			tokens_removed = Tokens()
			
			# Extract reverted_to revision
			_, _, reverted_to = revert
			tokens.extend(reverted_to.tokens)
			print([t.text for t in reverted_to.tokens])
			
		else:
			
			if self.last_tokens == None: # First version of the page!
				
				tokens = Tokens(Token(t) for t in self.tokenize(text))
				tokens_added = tokens
				tokens_removed = Tokens()
				
			else:
				
				# NOTICE: HEAVY COMPUTATION HERE!!!
				#
				# OK.  It's not that heavy.  It's just performing a diff,
				# but you're still going to spend most of your time here. 
				# Diffs usually run in O(n^2) -- O(n^3) time and most tokenizers
				# produce a lot of tokens.
				tokens, tokens_added, tokens_removed = \
					self.last_tokens.compare(self.tokenize(text), self.diff)
				
				
			
		tokens.persist(revision)
		
		self.last_tokens = tokens
		
		return tokens, tokens_added, tokens_removed
	
	
