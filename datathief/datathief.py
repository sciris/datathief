'''
Process data from figures
'''

import numpy as np
import sciris as sc
import matplotlib as mpl


def findpixels(image, color):
    ''' Find pixels matching a certain color '''
    img = np.array(image)
    c = np.array(color)
    r_match = img[:,:,0] == c[0]
    g_match = img[:,:,1] == c[1]
    b_match = img[:,:,2] == c[2]
    match = r_match * g_match * b_match
    y,x = np.where(match)
    return x,y


def datathief(fn, xlim=None, ylim=None, xcol=None, ycol=None, dcol=None, verbose=True):
    '''
    Extract data from a figure. To use, add a single pixel at the start and end
    of the x-axis (default color: pure blue) and the y-axis (default color: pure
    red), and then one pixel for each data point (default color: pure green). This
    function will then return the x and y coordinates of each data point.

    **Example**::

        import datathief as dt
        data = dt.datathief('my-data-fig.png', xlim=[0,20], ylim=[0,30])

    Inspired by the DataThief Java tool.
    '''

    if xlim is None: xlim = [0,1]
    if ylim is None: ylim = [0,1]
    if xcol is None: xcol = [0,0,1]
    if ycol is None: ycol = [1,0,0]
    if dcol is None: dcol = [0,1,0]

    if sc.isstring(xcol): xcol = sc.hex2(xcol)
    if sc.isstring(ycol): xcol = sc.hex2(ycol)
    if sc.isstring(dcol): xcol = sc.hex2(dcol)

    # Process image
    lim = sc.objdict(x=xlim, y=ylim)
    perpix = sc.objdict()
    ref = sc.objdict()
    d = sc.objdict()
    img = mpl.image.imread(fn)
    ref.x, tmp_xy = findpixels(img, xcol)
    tmp_yx, ref.y = findpixels(img, ycol)
    d.x, d.y = findpixels(img, dcol)
    ref.y = np.sort(img.shape[0] - ref.y) # Flip y-axis
    d.y = img.shape[0] - d.y # Flip y-axis
    assert len(ref.x) == 2, f'Wrong number of x coordinates found (len(ref.x)): please ensure exactly 2 pixels have color {xcol}'
    assert len(ref.y) == 2, f'Wrong number of y coordinates found (len(ref.y)): please ensure exactly 2 pixels have color {ycol}'

    if verbose:
        print(f'{img.shape=}')
        print(f'{ref=}')
        print(f'{d=}')

    order = np.argsort(d.x)
    d.x = d.x[order]
    d.y = d.y[order]

    # Process data
    data = sc.objdict()
    for k in ['x','y']:
        perpix = (np.diff(lim[k])/np.diff(ref[k]))[0]
        orig   = np.array(d[k], dtype=float)
        rmref  = orig - ref[k][0]
        bypix  = rmref*perpix
        data[k]   = bypix + lim[k][0]

        if verbose:
            print('\n\nFor variable:\n ', k)
            print(f'{perpix=}')
            print(f'Original:\n {orig=}')
            print(f'Removing reference:\n {rmref=}')
            print(f'By pixel:\n {bypix=}')
            print(f'Adding limit:\n {data[k]=}')

    return data