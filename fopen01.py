def fopen(filename, mode="r"):
    import bz2
    import gzip
    from types import StringType
    
    if type(filename) is StringType:
        if filename.endswith(".bz2"):
            f = bz2.BZ2File(filename, mode)
        elif filename.endswith(".gz"):
            f = gzip.open(filename, mode)
        else:
            f = open(filename, mode)
    else: # try to open it, who knows... 
        f = filename
        
    return f


def load(filename, key, sep=None, enc=None):
    ret = dict()

    file = fopen(filename)
    headers = file.readline()

    if not enc is None:
        headers = headers.decode(enc)

    if sep is None:
        headers = headers.split()
    else:
        headers = headers.split(sep)
    
    for line in file:
        if not enc is None:
            line = line.decode(enc)
        if sep is None:
            fline = line.split()
        else:
            fline = line.split(sep)
        if len(fline) != len(headers):
            stderr.write("bad line: "+line+"\n")
        else:
            fline = dict(zip(headers, fline))
            ret[fline[key]] = fline

    return (ret, headers)
