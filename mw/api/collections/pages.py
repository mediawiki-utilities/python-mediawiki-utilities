import logging

from ...util import none_or
from .collection import Collection

logger = logging.getLogger("mw.api.collections.pages")


class Pages(Collection):
    """
    TODO
    """

    def _edit(self, title=None, pageid=None, section=None, sectiontitle=None,
              text=None, token=None, summary=None, minor=None,
              notminor=None, bot=None, basetimestamp=None,
              starttimestamp=None, recreate=None, createonly=None,
              nocreate=None, watch=None, unwatch=None, watchlist=None,
              md5=None, prependtext=None, appendtext=None, undo=None,
              undoafter=None, redirect=None, contentformat=None,
              contentmodel=None, assert_=None, nassert=None,
              captchaword=None, captchaid=None):
        params = {
            'action': "edit"
        }
        params['title'] = none_or(title, str)
        params['pageid'] = none_or(pageid, int)
        params['section'] = none_or(section, int, levels={'new'})
        params['sectiontitle'] = none_or(sectiontitle, str)
        params['text'] = none_or(text, str)
        params['token'] = none_or(token, str)
        params['summary'] = none_or(summary, str)
        params['minor'] = none_or(minor, bool)
        params['notminor'] = none_or(notminor, bool)
        params['bot'] = none_or(bot, bool)
        params['basetimestamp'] = self._check_timestamp(basetimestamp)
        params['starttimestamp'] = self._check_timestamp(starttimestamp)
        params['recreate'] = none_or(recreate, bool)
        params['createonly'] = none_or(createonly, bool)
        params['nocreate'] = none_or(nocreate, bool)
        params['watch'] = none_or(watch, bool)
        params['unwatch'] = none_or(unwatch, bool)
        params['watchlist'] = none_or(watchlist, bool)
        params['md5'] = none_or(md5, str)
        params['prependtext'] = none_or(prependtext, str)
        params['appendtext'] = none_or(appendtext, str)
        params['undo'] = none_or(undo, int)
        params['undoafter'] = none_or(undoafter, int)

        # TODO finish this
