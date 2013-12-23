import re

from ..util import none_or

from . import defaults
from .timestamp import Timestamp

class Protection:
	
	ACTIONS = {'edit', 'move', 'upload', 'create'}
	
	GROUPS = {'sysop', 'autoconfirmed'}
	
	PARAMS_RE = re.compile(
		r"\[" +
			r"({0})".format(r"|".join(ACTIONS)) + 
			r"=" + 
			r"({0})".format(r"|".join(GROUPS)) + 
		r"\]" +
		r" " +
		r"\(([^\]]+)\)([\ \n]|$)"
	)
	
	def __init__(self, action=None, group=None, expiration=None):
		self.action = none_or(action, levels=self.ACTIONS)
		self.group = none_or(group, levels=self.GROUPS)
		self.expiration = none_or(expiration, Timestamp)
		
	def __str__(self): return self.__repr__()
	
	def __repr__(self):
		return "{0}({1})".format(
			self.__class__.__name__,
			", ".join(repr(v) for v in [self.action, self.group, 
			                            self.expiration])
		)
		
	def __eq__(self, other):
		try:
			return (
				self.action == other.action and
				self.group == other.group and
				self.expiration == other.expiration
			)
		except AttributeError:
			return False
	
	@classmethod
	def from_params(cls, params, indefinite=defaults.PARAMS_INDEFINITE, 
	                    time_format=defaults.PARAMS_TIME_FORMAT):
	
		for match in cls.PARAMS_RE.finditer(params):
			action, group, expiration, _ = match.groups()
			
			if expiration == indefinite:
				expiration = None
			else:
				expiration = Timestamp.strptime(expiration, time_format)
			
			yield cls(action, group, expiration)
