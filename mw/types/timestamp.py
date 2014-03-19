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

def Timestamp(time_thing):
	if isinstance(time_thing, TimestampType):
		return time_thing
	else:
		return TimestampType(time_thing)
	
class TimestampType(serializable.Type):
	
	def __init__(self, time_thing):
		if isinstance(time_thing, time.struct_time):
			self.__time = time_thing
		elif type(time_thing) in (int, float):
			self.__time = datetime.datetime.utcfromtimestamp(time_thing).timetuple()
		else:
			if type(time_thing) == bytes:
				time_string = str(time_thing, 'utf8')
			else:
				time_string = str(time_thing)
			
			try:
				self.__time = time.strptime(time_string, LONG_MW_TIME_STRING)
			except ValueError as e:
				try:
					self.__time = time.strptime(time_string, SHORT_MW_TIME_STRING)
				except ValueError as e:
					raise ValueError("'%s' is not a valid Wikipedia date format" % time_string)
			
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
		if isinstance(time_thing, cls):
			return time_thing
		else:
			return TimestampType(time_thing)
	
	def __repr__(self):
		return "{0}({1})".format(
			self.__class__.__name__,
			repr(self.long_format())
		)
	
	def __int__(self): return self.unix()
	
	def unix(self):
		return int(calendar.timegm(self.__time))
		
	def __sub__(self, other):
		return self.unix() - other.unix()
	
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
	



Timestamp.strptime = lambda string, format: \
	TimestampType(time.strptime(string, format))

Timestamp.serialize = TimestampType.serialize
Timestamp.deserialize = TimestampType.deserialize
