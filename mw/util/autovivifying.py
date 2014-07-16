class Dict(dict):
    def __init__(self, *args, vivifier=lambda k: None, **kwargs):
        self.vivifier = vivifier

        dict.__init__(self, *args, **kwargs)

    def __getitem__(self, key):
        if key not in self:
            dict.__setitem__(self, key, self.vivifier(key))

        return dict.__getitem__(self, key)
