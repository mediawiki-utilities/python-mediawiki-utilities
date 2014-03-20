import oursql, os, getpass, time, logging

from .pages import Pages
from .recent_changes import RecentChanges
from .revisions import Revisions, Archives, AllRevisions
from .users import Users

logger = logging.getLogger("mw.database.db")

class DB:
	
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
		self.kwargs['default_cursor'] = oursql.DictCursor
		self.shared_connection = oursql.connect(*args, **kwargs)
		
		self.revisions = Revisions(self)
		self.archives = Archives(self)
		self.all_revisions = AllRevisions(self)
		self.pages = Pages(self)
		
	def __repr__(self):
		return "%s(%s)" % (
			self.__class__.__name__,
			", ".join(
				[repr(arg) for arg in self.args] +
				["%s=%r" % (k,v) for k,v in self.kwargs.items()]
			)
		)
	
	def __str__(self): return self.__repr__()
	
	@classmethod
	def add_args(cls, parser, defaults=None):
		defaults = defaults if defaults != None else defaults
		
		parser.add_argument(
			'--host', '-h',
			help="MySQL database host to connect to (defaults to {0})".format(defaults.get('host', "localhost")),
			default=defaults.get('host', "localhost")
		)
		parser.add_argument(
			'--database', '-d',
			help="MySQL database name to connect to (defaults to  {0})".format(defaults.get('database', getpass.getuser())),
			default=defaults.get('database', getpass.getuser())
		)
		parser.add_argument(
			'--defaults-file',
			help="MySQL defaults file (defaults to {0})".format(defaults.get('defaults-file', os.path.expanduser("~/.my.cnf"))),
			default=defaults.get('defaults-file', os.path.expanduser("~/.my.cnf"))
		)
		parser.add_argument(
			'--user', '-u',
			help="MySQL user (defaults to %s)".format(defaults.get('user', getpass.getuser())),
			default=defaults.get('user', getpass.getuser())
		)
		return parser
	
	@classmethod
	def from_args(cls, args):
		return cls(
			args.host,
			args.user,
			db=args.database,
			read_default_file=args.defaults_file
		)
	

