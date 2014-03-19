from distutils.core import setup

setup(
	name='Mediawiki Utilities',
	version='0.2.0',
	author='Aaron Halfaker',
	author_email='aaron.halfaker@gmail.com',
	packages=['mw', 
	          'mw.api', 
	          'mw.database', 
	          'mw.xml_dump', 
	          'mw.xml_dump.iteration', 
	          'mw.lib', 
	          'mw.lib.persistence', 
	          'mw.lib.reverts', 
	          'mw.lib.sessions',
	          'mw.lib.title',
	          'mw.types',
	          'mw.util',
	          'mw.util.iteration'],
	scripts=[],
	url='http://pypi.python.org/pypi/mediawiki-utilities',
	license='LICENSE',
	description='A set of utilities for working with MediaWiki data.',
	long_description=open('README.rst').read(),
	install_requires=[
	    "argparse >= 1.1",
	    "requests >= 2.0.1"],
	test_suite = 'nose.collector'
)
