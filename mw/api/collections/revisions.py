import logging

from ...util import none_or
from ..errors import MalformedResponse
from .collection import Collection

logger = logging.getLogger("mw.api.collections.revisions")


class Revisions(Collection):
    """
    A collection of revisions indexes by title, page_id and user_text.
    Note that revisions of deleted pages are queriable via
    :class:`mw.api.DeletedRevs`.
    """
    
    PROPERTIES = {'ids', 'flags', 'timestamp', 'user', 'userid', 'size',
                  'sha1', 'contentmodel', 'comment', 'parsedcomment',
                  'content', 'tags', 'flagged'}
    
    DIFF_TO = {'prev', 'next', 'cur'}
    
    # This is *not* the right way to do this, but it should work for all queries.
    MAX_REVISIONS = 50
    
    def get(self, rev_id, **kwargs):
        """
        Get a single revision based on it's ID.  Throws a :py:class:`KeyError`
        if the rev_id cannot be found.
        
        :Parameters:
            rev_id : int
                Revision ID
            ``**kwargs``
                Passed to :py:meth:`query`
            
        :Returns:
            A single rev dict
        """
        rev_id = int(rev_id)
        
        revs = list(self.query(revids={rev_id}, **kwargs))
        
        if len(revs) < 1:
            raise KeyError(rev_id)
        else:
            return revs[0]
        
    def query(self, *args, limit=None, **kwargs):
        """
        Get revision information.
        See `<https://www.mediawiki.org/wiki/API:Properties#revisions_.2F_rv>`_
        
        :Parameters:
            properties : set(str)
                Which properties to get for each revision:
                
                * ids            - The ID of the revision
                * flags          - Revision flags (minor)
                * timestamp      - The timestamp of the revision
                * user           - User that made the revision
                * userid         - User id of revision creator
                * size           - Length (bytes) of the revision
                * sha1           - SHA-1 (base 16) of the revision
                * contentmodel   - Content model id
                * comment        - Comment by the user for revision
                * parsedcomment  - Parsed comment by the user for the revision
                * content        - Text of the revision
                * tags           - Tags for the revision
            limit : int
                Limit how many revisions will be returned
                No more than 500 (5000 for bots) allowed
            start_id : int
                From which revision id to start enumeration (enum)
            end_id : int
                Stop revision enumeration on this revid
            start : :class:`mw.Timestamp`
                From which revision timestamp to start enumeration (enum)
            end : :class:`mw.Timestamp`
                Enumerate up to this timestamp
            direction : str
                "newer" or "older"
            user : str
                Only include revisions made by user_text
            excludeuser : bool
                Exclude revisions made by user
            tag : str
                Only list revisions tagged with this tag
            expandtemplates : bool
                Expand templates in revision content (requires "content" propery)
            generatexml : bool
                Generate XML parse tree for revision content (requires "content" propery)
            parse : bool
                Parse revision content (requires "content" propery)
            section : int
                Only retrieve the content of this section number
            token : set(str)
                Which tokens to obtain for each revision
                
                * rollback - See `<https://www.mediawiki.org/wiki/API:Edit_-_Rollback#Token>`_
            rvcontinue : str
                When more results are available, use this to continue
            diffto : int
                Revision ID to diff each revision to. Use "prev", "next" and
                "cur" for the previous, next and current revision respectively
            difftotext : str
                Text to diff each revision to. Only diffs a limited number of
                revisions. Overrides diffto. If section is set, only that
                section will be diffed against this text
            contentformat : str
                Serialization format used for difftotext and expected for output of content
                
                * text/x-wiki
                * text/javascript
                * text/css
                * text/plain
                * application/json
        
        :Returns:
            An iterator of rev dicts returned from the API.
        """
        
        revisions_yielded = 0
        done = False
        while not done:
            if limit == None:
                kwargs['limit'] = self.MAX_REVISIONS
            else:
                kwargs['limit'] = min(limit - revisions_yielded, self.MAX_REVISIONS)
            
            rev_docs, rvcontinue = self._query(*args, **kwargs)
            
            for doc in rev_docs:
                yield doc
                revisions_yielded += 1
                
                if limit != None and revisions_yielded >= limit:
                    done = True
                    break
                
            if rvcontinue != None and len(rev_docs) > 0:
                kwargs['rvcontinue'] = rvcontinue
            else:
                done = True
            
    
    def _query(self, revids=None, titles=None, pageids=None, properties=None,
                     limit=None, start_id=None, end_id=None, start=None,
                     end=None, direction=None, user=None, excludeuser=None,
                     tag=None, expandtemplates=None, generatexml=None,
                     parse=None, section=None, token=None, rvcontinue=None,
                     diffto=None, difftotext=None, contentformat=None):
        
        params = {
            'action': "query",
            'prop': "revisions"
        }
        
        params['revids'] = self._items(revids, type=int)
        params['titles'] = self._items(titles)
        params['pageids'] = self._items(pageids, type=int)
        
        params['rvprop'] = self._items(properties, levels=self.PROPERTIES)
        
        if revids == None: # Can't have a limit unless revids is none
            params['rvlimit'] = none_or(limit, int)
            
        params['rvstartid'] = none_or(start_id, int)
        params['rvendid'] = none_or(end_id, int)
        params['rvstart'] = self._check_timestamp(start)
        params['rvend'] = self._check_timestamp(end)
        
        params['rvdir'] = self._check_direction(direction)
        params['rvuser'] = none_or(user, str)
        params['rvexcludeuser'] = none_or(excludeuser, int)
        params['rvtag'] = none_or(tag, str)
        params['rvexpandtemplates'] = none_or(expandtemplates, bool)
        params['rvgeneratexml'] = none_or(generatexml, bool)
        params['rvparse'] = none_or(parse, bool)
        params['rvsection'] = none_or(section, int)
        params['rvtoken'] = none_or(token, str)
        params['rvcontinue'] = none_or(rvcontinue, int)
        params['rvdiffto'] = self._check_diffto(diffto)
        params['rvdifftotext'] = none_or(difftotext, str)
        params['rvcontentformat'] = none_or(contentformat, str)
        
        doc = self.session.get(params)
        
        try:
            if 'query-continue' in doc:
                rvcontinue = doc['query-continue']['revisions']['rvcontinue']
            else:
                rvcontinue = None
            
            pages = doc['query']['pages'].values()
            rev_docs = []
            
            for page_doc in pages:
                if 'missing' in page_doc: continue
                
                page_rev_docs = page_doc['revisions']
                del page_doc['revisions']
                
                for rev_doc in page_rev_docs:
                    rev_doc['page'] = page_doc
                
                rev_docs.extend(page_rev_docs)
            
            return rev_docs, rvcontinue
            
        except KeyError as e:
            raise MalformedResponse(str(e), doc)
        
    
    def _check_diffto(self, diffto):
        if diffto == None or diffto in self.DIFF_TO:
            return diffto
        else:
            return int(diffto)
