'''
Process data from figures
'''

import numpy as np
import sciris as sc
import matplotlib as mpl


def findpixels(image, color):
    '''
    Find coordinates of pixels in an image matching a certain color.

    Args:
        image: image data (as returned by mpl.image.imread())
        color: color to find (as RGB triplet)

    Returns:
        Tuple of arrays of coordinates of matching pixels
    '''
    img = np.array(image)
    c = np.array(color)
    r_match = img[:,:,0] == c[0]
    g_match = img[:,:,1] == c[1]
    b_match = img[:,:,2] == c[2]
    match = r_match * g_match * b_match
    y,x = np.where(match)
    return x,y


def datathief(filename, xlim=None, ylim=None, xcol=None, ycol=None, dcol=None, debug=False):
    '''
    Extract data from a figure. To use, add a single pixel at the start and end
    of the x-axis (default color: pure blue) and the y-axis (default color: pure
    red), and then one pixel for each data point (default color: pure green). This
    function will then return the x and y coordinates of each data point.

    Args:
        filename (str): the filename of the image to load
        xlim (list): a list of 2 floats defining the start and end values of the x-axis
        ylim (list): likewise, for the y-axis
        xcol (str, list): a hex string or list of 3 floats defining the RGB color for the x-axis pixels
        ycol (str, list): likewise, for the y-axis pixels
        dcol (str, list): likewise, for the data points
        debug (bool): whether to print extra information about the data transformations

    Returns:
        Dict with keys x and y corresponding to the data points

    **Examples**::

        import datathief as dt
        import pylab as pl

        data1 = dt.datathief('my-data-fig.png', xlim=[0,20], ylim=[0,30])
        data2 = dt.datathief('my-other-fig.png', xlim=[0,1], ylim=[0,1], xcol='#f00', ycol='#f0f', dcol='#face00')

        pl.scatter(data2.x, data2.y)

    Inspired by the DataThief Java tool.
    '''

    if xlim is None: xlim = [0,1]
    if ylim is None: ylim = [0,1]
    if xcol is None: xcol = [0,0,1]
    if ycol is None: ycol = [1,0,0]
    if dcol is None: dcol = [0,1,0]

    if sc.isstring(xcol): xcol = sc.hex2rgb(xcol)
    if sc.isstring(ycol): xcol = sc.hex2rgb(ycol)
    if sc.isstring(dcol): xcol = sc.hex2rgb(dcol)

    # Read image data
    lim = sc.objdict(x=xlim, y=ylim)
    perpix = sc.objdict()
    ref = sc.objdict()
    d = sc.objdict()
    img = mpl.image.imread(filename)
    ref.x, tmp_xy = findpixels(img, xcol)
    tmp_yx, ref.y = findpixels(img, ycol)
    d.x, d.y = findpixels(img, dcol)
    ref.y = np.sort(img.shape[0] - ref.y) # Flip y-axis
    d.y = img.shape[0] - d.y # Flip y-axis
    assert len(ref.x) == 2, f'Wrong number of x coordinates found ({len(ref.x)}): please ensure exactly 2 pixels have color {xcol}'
    assert len(ref.y) == 2, f'Wrong number of y coordinates found ({len(ref.y)}): please ensure exactly 2 pixels have color {ycol}'

    if debug:
        print(f'Image shape: {img.shape}')
        print(f'Reference pixels: {ref}')
        print(f'Data pixels: {d}')

    # Process data
    data = sc.objdict()
    order = np.argsort(d.x)
    d.x = d.x[order]
    d.y = d.y[order]
    for k in ['x','y']:
        perpix = (np.diff(lim[k])/np.diff(ref[k]))[0]
        orig   = np.array(d[k], dtype=float)
        rmref  = orig - ref[k][0]
        bypix  = rmref*perpix
        data[k]   = bypix + lim[k][0]

        if debug:
            print('\n\nFor variable:\n ', k)
            print(f'Pixels-per-value: {1.0/perpix}; pixel ratio: {perpix}')
            print(f'Original:\n orig={orig}')
            print(f'Removing reference:\n rmref={rmref}')
            print(f'By pixel:\n bypix={bypix}')
            print(f'Adding limit:\n data={data[k]}')

    return data