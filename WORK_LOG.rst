

2013-12-19
	Still working on `mw.lib.changes`.  I like the structure for the most part.  It looks like I'm going to have to join `revision` and `logging` to `recentchanges` in order construct an appropriate `change.Change` from a row.  That means I'm going to need a funny new method on `database.RecentChanges`.  That's going to confuse people.  Boo.
	
	I also need to figure out a way to configure for the lame timestamp format that appears in blocks and page protections.  I think I'm going to extend `types.TimestampType` to have a `strptime` method. 

2013-12-18
	Tests passing.  HistoricalMap was fine.  Will be code-complete once lib.changes is done.  Still need to figure out how I'm going to configure a title parser and pass it into the change constructor.  Also, I rediscovered how stupid the recentchanges table is.
	
	OK.. New lame thing.  So, when you "protect" a page, the log keeps the 
	following type of value in log_params:
	``\u200e[edit=autoconfirmed] (expires 03:20, 21 November 2013 (UTC))``
	
	That date format... It's not the long or short format for `Timestamp`. 
	I think it is a custom format that changes on a wiki-to-wiki basis.
	
	I feel sad.  This made my day worse.  It's important to remind myself of 
	the fact that MediaWiki was not designed to allow me to reverse engineer it.
	-halfak

2013-12-17
	Test on revert detector failing since simplifying restructure.  I'm not sure what the issue is, but I suspect that I broke something in util.ordered.HistoricalMap. -halfak
