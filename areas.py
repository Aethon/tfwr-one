# An area is a tuple (x0: pos int, y0: pos int, cx: pos int, cy: pos int, rel: bool)
# Areas can be relative or absolute

def defaulted(val, default):
    if val == None:
        return default
    return val

def _slice_axis(i0, ci, b0, cb):

    if i0 < b0:
        trunc = b0 - i0
        i0 = b0
        ci = ci - trunc

    if ci < 0:
        return i0, 0

    if cb == None:
        return i0, ci
        
    return i0, min(ci, cb - (i0 - b0))

def _create(x0, y0, cx, cy, rel):

    x0, cx = _slice_axis(x0, cx, 0, None)
    y0, cy = _slice_axis(y0, cy, 0, None)
    rel = rel == True

    return x0, y0, cx, cy, rel

def create_relative(x0, y0, cx, cy):
    return _create(x0, y0, cx, cy, True)

def create_absolute(x0, y0, cx, cy):
    return _create(x0, y0, cx, cy, False)

def get_base_area(base, sub):
    bx0, by0, bcx, bcy, brel = base
    sx0, sy0, scx, scy, srel = sub
    
    if srel:
        x0, cx =_slice_axis(bx0 + sx0, scx, bx0, bcx)
        y0, cy =_slice_axis(by0 + sy0, scy, by0, bcy)
    else:
        x0, cx =_slice_axis(sx0, scx, bx0, bcx)
        y0, cy =_slice_axis(sy0, scy, by0, bcy)

    return _create(x0, y0, cx, cy, brel)

def force_absolute(ctx):
    x0, y0, cx, cy, rel = ctx
    if rel:
        ctx = _create(x0, y0, cx, cy, False)
    return ctx
