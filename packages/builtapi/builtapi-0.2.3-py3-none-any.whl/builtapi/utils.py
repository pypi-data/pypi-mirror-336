def cleandict(d):
    if not isinstance(d, dict):
        return d
    return dict((k, cleandict(v)) for k, v in d.items() if v is not None)
