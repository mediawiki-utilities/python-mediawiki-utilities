def none_or(val, func=None, levels=None):
    if val is None:
        return None
    else:
        if levels is not None:
            if val not in set(levels):
                raise KeyError(val)

            return val
        else:
            return func(val)


def try_keys(dictionary, keys):
    attempted_keys = []
    for key in keys:
        if key in dictionary:
            return dictionary[key]
        attempted_keys.append(key)

    raise KeyError("|".join(str(k) for k in attempted_keys))
