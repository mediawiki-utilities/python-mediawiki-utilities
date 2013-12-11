import re, sys

from wmf import persistence
from wmf.util import STOP_WORDS, digest

PUNCT = r""".,'"-_+=[]{}!@#$%^&*()\/|?"""
PUNCTUATION = re.compile(r"[%s]" % "".join(r"\%s" % char for char in PUNCT))

def splitter(text):
	tokens = persistence.splitter(text)
	filtered = []
	for token in tokens:
		token = PUNCTUATION.sub(" ", token)
		if (
			token.strip() != "" and 
			token not in STOP_WORDS and
			len(token) > 2
		):
			filtered.append(token)
	
	return filtered

def process(dump, page):
	
	revisions = {}
	
	state = persistence.PersistenceState(
		splitter,
		persistence.differ
	)
	
	for rev in page.readRevisions():
		if rev.getContributor() != None:
			user_name = rev.getContributor().getUsername()
		else:
			user_name = "<deleted>"
		
		p_revision = persistence.Revision(
			rev.getId(),
			page.getId(),
			user_name,
			rev.getTimestamp(),
			rev.getComment(),
			digest(rev.getText())
		)
		added, removed = state.update(p_revision, rev.getText())
		revisions[rev.getId()] = (added, removed)
	
	sys.stderr.write("%s(%s) " % (page.getTitle(), len(revisions)))
	for rev_id in revisions:
		added, removed = revisions[rev_id]
		yield rev_id, sum(w.getVisible() for w in added), len(added)
