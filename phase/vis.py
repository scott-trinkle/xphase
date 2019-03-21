import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm


def subplot_colorbar(image, ax, fig, fmt='sci',
                     position='right', size='5%', pad=0.05):
    divider = make_axes_locatable(ax)
    cax = divider.append_axes(position, size, pad)
    if fmt == 'sci':
        fmt = '%.0e'
    fig.colorbar(image, cax=cax, format=fmt)
    return fig, ax


def imshow_clean(data, ax, title=None, log=False):
    norm = LogNorm() if log else None
    im = ax.imshow(data, cmap='gray', norm=norm)
    ax.set_title(title)
    ax.axis('off')
    return im, ax


def show_refindex_slice(data, z=None, log=False,
                        show=True, save=False, fn=None):

    if z is None:
        z = data.shape[-1] // 2

    fmt = None if log else 'sci'

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    delta, ax1 = imshow_clean(1 - data.real[..., z], ax1, title=r'$\delta$',
                              log=log)
    fig, ax1 = subplot_colorbar(delta, ax1, fig, fmt=fmt)

    beta, ax2 = imshow_clean(data.imag[..., z], ax2, title=r'$\beta$',
                             log=log)
    fig, ax1 = subplot_colorbar(beta, ax2, fig, fmt=fmt)

    fig.tight_layout()

    if show:
        plt.show()
    if save:
        fig.savefig(fn)
