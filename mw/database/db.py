import getpass
import logging
import os

import pymysql
import pymysql.cursors

from .collections import AllRevisions, Archives, Pages, Revisions, Users

logger = logging.getLogger("mw.database.db")


class DB:
    """
    Represents a connection to a MySQL database.

    :Parameters:
        connection = :class:`oursql.Connection`
            A connection to a MediaWiki database
    """

    def __init__(self, connection):
        self.shared_connection = connection
        self.shared_connection.cursorclass = pymysql.cursors.DictCursor

        self.revisions = Revisions(self)
        """
        An instance of :class:`mw.database.Revisions`.
        """

        self.archives = Archives(self)
        """
        An instance of :class:`mw.database.Archives`.
        """

        self.all_revisions = AllRevisions(self)
        """
        An instance of :class:`mw.database.AllRevisions`.
        """

        self.pages = Pages(self)
        """
        An instance of :class:`mw.database.Pages`.
        """

        self.users = Users(self)
        """
        An instance of :class:`mw.database.Users`.
        """

    def __repr__(self):
        return "%s(%s)" % (
            self.__class__.__name__,
            ", ".join(
                [repr(arg) for arg in self.args] +
                ["%s=%r" % (k, v) for k, v in self.kwargs.items()]
            )
        )

    def __str__(self):
        return self.__repr__()

    @classmethod
    def add_arguments(cls, parser, defaults=None):
        """
        Adds the arguments to an :class:`argparse.ArgumentParser` in order to
        create a database connection.
        """
        defaults = defaults if defaults is not None else defaults

        default_host = defaults.get('host', "localhost")
        parser.add_argument(
            '--host', '-h',
            help="MySQL database host to connect to (defaults to {0})".format(default_host),
            default=default_host
        )

        default_database = defaults.get('database', getpass.getuser())
        parser.add_argument(
            '--database', '-d',
            help="MySQL database name to connect to (defaults to  {0})".format(default_database),
            default=default_database
        )

        default_defaults_file = defaults.get('defaults-file', os.path.expanduser("~/.my.cnf"))
        parser.add_argument(
            '--defaults-file',
            help="MySQL defaults file (defaults to {0})".format(default_defaults_file),
            default=default_defaults_file
        )

        default_user = defaults.get('user', getpass.getuser())
        parser.add_argument(
            '--user', '-u',
            help="MySQL user (defaults to %s)".format(default_user),
            default=default_user
        )
        return parser

    @classmethod
    def from_arguments(cls, args):
        """
        Constructs a :class:`~mw.database.DB`.
        Consumes :class:`argparse.ArgumentParser` arguments given by
        :meth:`add_arguments` in order to create a :class:`DB`.

        :Parameters:
            args : :class:`argparse.Namespace`
                A collection of argument values returned by :class:`argparse.ArgumentParser`'s :meth:`parse_args()`
        """
        connection = pymysql.connect(
            args.host,
            args.user,
            database=args.database,
            read_default_file=args.defaults_file
        )
        return cls(connection)

    @classmethod
    def from_params(cls, *args, **kwargs):
        """
        Constructs a :class:`~mw.database.DB`.  Passes `*args` and `**kwargs`
        to :meth:`oursql.connect` and configures the connection.

        :Parameters:
            args : :class:`argparse.Namespace`
                A collection of argument values returned by :class:`argparse.ArgumentParser`'s :meth:`parse_args()`
        """
        kwargs['cursorclass'] = pymysql.cursors.DictCursor
        if kwargs['db']:
            kwargs['database'] = kwargs['db']
            del kwargs['db']
        connection = pymysql.connect(*args, **kwargs)
        return cls(connection)
