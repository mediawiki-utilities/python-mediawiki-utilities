class DummyChecksum():
    """
    Used in when checking for reverts when the checksum of the revision of interest
    is unknown.  DummyChecksums won't match eachother or anything else, but they
    will match themselves and they are hashable.

    >>> dummy1 = DummyChecksum()
    >>> dummy1
    <#140687347334280>
    >>> dummy1 == dummy1
    True
    >>>
    >>> dummy2 = DummyChecksum()
    >>> dummy2
    <#140687347334504>
    >>> dummy1 == dummy2
    False
    >>>
    >>> {"foo", "bar", dummy1, dummy1, dummy2}
    {<#140687347334280>, 'foo', <#140687347334504>, 'bar'}
    """
    
    def __str__(self): repr(self)
    def __repr__(self): return "<#" + str(id(self)) + ">"
