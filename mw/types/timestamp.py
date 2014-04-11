import time, datetime, calendar

from . import serializable

LONG_MW_TIME_STRING = '%Y-%m-%dT%H:%M:%SZ'
"""
The longhand version of MediaWiki time strings.
"""

SHORT_MW_TIME_STRING = '%Y%m%d%H%M%S'
"""
The shorthand version of MediaWiki time strings.
"""

class Timestamp(serializable.Type):
	
	def __new__(cls, time_thing):
		if isinstance(time_thing, cls):
			return time_thing
		elif isinstance(time_thing, time.struct_time):
			return cls.from_time_struct(time_thing)
		elif isinstance(time_thing, datetime.datetime):
			return cls.from_datetime(time_thing)
		elif type(time_thing) in (int, float):
			return cls.from_unix(time_thing)
		else:
			return cls.from_string(time_thing)
		
	def __init__(self, *args, **kwargs): 
		# Important that this does nothing
		pass
	
	def initialize(self, time_struct):
		self.__time = time_struct
	
	@classmethod
	def from_time_struct(cls, struct):
		instance = super().__new__(cls)
		instance.initialize(struct)
		return instance
	
	@classmethod
	def from_datetime(cls, dt):
		time_struct = dt.timetuple()
		return cls.from_time_struct(time_struct)
		
	@classmethod
	def from_unix(cls, seconds):
		time_struct = datetime.datetime.utcfromtimestamp(seconds).timetuple()
		return cls.from_time_struct(time_struct)
	
	@classmethod
	def from_string(cls, string):
		if type(string) == bytes:
			string = str(string, 'utf8')
		else:
			string = str(string)
		
		try:
			return cls.strptime(string, SHORT_MW_TIME_STRING)
		except ValueError as e:
			try:
				return cls.strptime(string, LONG_MW_TIME_STRING)
			except ValueError as e:
				raise ValueError(
					"{0} is not a valid Wikipedia date format".format(
						repr(time_string)
					)
				)
			
		return cls.from_time_struct(time_struct)
		
	@classmethod
	def strptime(cls, string, format):
		return cls.from_time_struct(time.strptime(string, format))
	
	def strftime(self, format): return self.__format__(format)
	def __format__(self, format):
		return time.strftime(format, self.__time)
	
	def __str__(self): return self.short_format()
	
	def short_format(self):
		return self.strftime(SHORT_MW_TIME_STRING)
	
	def long_format(self):
		return self.strftime(LONG_MW_TIME_STRING)
	
	def serialize(self):
		return self.unix()
		
	@classmethod
	def deserialize(cls, time_thing):
		return Timestamp(time_thing)
	
	def __repr__(self):
		return "{0}({1})".format(
			self.__class__.__name__,
			repr(self.long_format())
		)
	
	def __int__(self): return self.unix()
	def __float__(self): return float(self.unix())
	
	def unix(self):
		return int(calendar.timegm(self.__time))
		
	def __sub__(self, other):
		return self.unix() - other.unix()
		
	def __add__(self, seconds):
		return Timestamp(self.unix() + seconds)
	
	def __eq__(self, other):
		try:
			return self.__time == other.__time
		except AttributeError:
			return False
	
	def __lt__(self, other):
		try:
			return self.__time < other.__time
		except AttributeError:
			return NotImplemented
	
	def __gt__(self, other):
		try:
			return self.__time > other.__time
		except AttributeError:
			return NotImplemented
	
	def __lte__(self, other):
		try:
			return self.__time <= other.__time
		except AttributeError:
			return NotImplemented
	
	def __gte__(self, other):
		try:
			return self.__time <= other.__time
		except AttributeError:
			return NotImplemented
	
	def __ne__(self, other):
		try:
			return not self.__time == other.__time
		except AttributeError:
			return NotImplemented
	
