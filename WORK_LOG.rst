
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
