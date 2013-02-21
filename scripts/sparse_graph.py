import matplotlib.pyplot as plt


def sparse_graph(sp, cmap=plt.cm.binary):
    """Make a graph given some sparse matrix.
    Parameters
    ----------
    * sp: A sparse matrix, which is able to be converted to an array.
    * cmap: matplotlib colormap.

    Returns
    -------
    * (fig, ax) tuple.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.matshow(sp.toarray(), cmap=cmap)
    return fig, ax
