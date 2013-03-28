import re


def sel(x, cls=None):
    """
    Give cls, a digit, and it will select that class with all subclasses.

    Parameters
        x: passed via the apply on the dataframe.
        cls: a digit you want to match on.

    returns
        Bool

    Example:
        inds[inds.naics.apply(sel, cls='1')]
    """
    try:
        r = re.compile(cls + r'\w')
        m = re.match(r, x)
        if m is None:
            return False
        else:
            return True
    except:
        return False
