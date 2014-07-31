2014-06-02
	After some reading, it looks like py3 will do something reasonable with re-raised errors, so I'm just going to let the error be re-raised and call it good.

2014-05-31
	I figured out that you just plain can't get a stack trace out of a multiprocessing.Process in such a way that you an re-associate it with its exception on the other side.  I'm now working on putting together a picklable container exception that I can use to manage and format the exceptions that come out of a mapping function.  It's not going great.

2014-04-08
	I've been extending the API.  I added list=deletedrevs and tested (fixed) the api.Session.login() method.  It all seems to work now.  I also did some minor cleanup on  lib.title.Parser to make the method names more explicit.
	
	I'd like to start tracking changes so that I can build changelists to go with new versions.  For now, I'll keep track of substantial changes here.
	
	* Released 0.2.1
	* Added list=deletedrevs to api module

2014-03-27
	I just fixed up the structure for lib.reverts.database.check() and check_row().  You can give check_row() a database row or check() a rev_id and page_id.  The functions should then either return None or the first reverting revision they encounter.
	
	I like this pattern.  Lib gets to reference core, but not vice versa.  I need to talk to the Wikimetrics people about implementing some of the metrics within a new lib.  Yet, one of the cool things about libs is that they don't necessarily need to be packaged with core.  So you could write something that makes use of core and other libs as a standalone package first and incorporate it later.  :D

2014-03-20
	Just a quick update today.  I realized that database.DB.add_args was setting
	default values that won't make sense for anyone but me personally.  I cleared that up and added a way to set your own defaults.

2014-03-18
	Refactoring!  I've got a user.  He immediately found problems.  So I'm fixing them aggressively.  I just renamed the library back to "mw".  I also renamed the dump processing module to "xml_dump".  I hope that these name changes will make more sense.
	
	I also moved the revert detection functionality out of the database module and into the lib.reverts module.  I think that this makes more sense.  If it is a core functionality, it should live in code.  If it is a library, it should only have other libraries depend on it.  If I need to write a magical DB abstractor in lib, so be it.

2014-02-08
	It's time to kill `mw.lib.changes`.  I just don't see that working as a core
	part of this library.  It might make sense to return build up another library
	to handle changes.  I'll have to get back to that at some other time.

2013-12-23
	Still hacking on `mw.lib.changes`.  It's the same set of issues described in
	the last log.  I'm making progress building a params parser.  I think that my strategy is going to be to let the user handle params parsing themselves with 	a new `types.Protection` type.
	
	Oh! And I did get `types.TimestampType` extended to have a `strptime` method.
	That's all nice and tested.
	
	Note that I think it might be a good idea to consolidate all defaults for
	better documentation.
	
	Anyway.  All tests are passing.  It's time to work on something else for a
	little while.

2013-12-19
	Still working on `mw.lib.changes`.  I like the structure for the most part.  It looks like I'm going to have to join `revision` and `logging` to `recentchanges` in order construct an appropriate `change.Change` from a row.  That means I'm going to need a funny new method on `database.RecentChanges`.  That's going to confuse people.  Boo.
	
	I also need to figure out a way to configure for the lame timestamp format that appears in blocks and page protections.  I think I'm going to extend `types.TimestampType` to have a `strptime` method.

2013-12-18
	Tests passing.  HistoricalMap was fine.  Will be code-complete once lib.changes is done.  Still need to figure out how I'm going to configure a title parser and pass it into the change constructor.  Also, I rediscovered how stupid the recentchanges table is.
	
	OK.. New lame thing.  So, when you "protect" a page, the log keeps the following type of value in log_params:
	``\u200e[edit=autoconfirmed] (expires 03:20, 21 November 2013 (UTC))``
	
	That date format... It's not the long or short format for `Timestamp`. I think it is a custom format that changes on a wiki-to-wiki basis.
	
	I feel sad.  This made my day worse.  It's important to remind myself of the fact that MediaWiki was not designed to allow me to reverse engineer it.
	
2013-12-17
	Test on revert detector failing since simplifying restructure.  I'm not sure what the issue is, but I suspect that I broke something in util.ordered.HistoricalMap. -halfak
