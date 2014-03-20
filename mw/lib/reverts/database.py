from itertools import chain

from ...types import Timestamp
from ...util import none_or

from .functions import detect

def check(db, rev_id, radius=15, sha1=None, page_id=None, check_archive=False, before=None):
	
	if not hasattr(db, "revisions") and hasattr(db, "all_revisions"):
		raise TypeError("db wrong type.  Expected a mw.database.DB.")
	
	rev_id = int(rev_id)
	radius = int(radius)
	sha1 = none_or(sha1, str)
	page_id = none_or(page_id, int)
	check_archive = bool(check_archive)
	before = none_or(before, Timestamp)
	
	if check_archive: dbrevs = db.all_revisions
	else: dbrevs = db.revisions
	
	if sha1 == None or page_id == None:
		row = dbrevs.get(id=rev_id)
		sha1 = row['sha1']
		page_id = row['rev_page']
		
	# Load history
	past_revs = reversed(list(dbrevs.query(
		page_id=page_id,
		limit=radius,
		before_id=rev_id,
		direction="older"
	)))
	future_revs = dbrevs.query(
		page_id=page_id,
		limit=radius,
		after_id=rev_id,
		before=before,
		direction="newer"
	)
	checksum_revisions = chain(
		((rev['rev_sha1'], rev) for rev in past_revs),
		[(sha1, {'rev_id': rev_id})],
		((rev['rev_sha1'], rev) for rev in future_revs)
	)
	
	for reverting, reverteds, reverted_to in detect(checksum_revisions, radius=radius):
		if len(reverteds) <= 15 and rev_id in {rev['rev_id'] for rev in reverteds}:
			return (reverting, reverteds, reverted_to)
		
	return None
