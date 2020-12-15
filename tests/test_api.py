'''
Test basic usage of DataThief.
'''

import sciris as sc
import datathief as dt

def test_api(do_plot=False):

    # Read data
    filename = sc.thisdir(__file__, '..', 'examples', 'du_fig1a_annotated.png')
    xlim = [-10, 20]
    ylim = [0, 15]
    data = dt.datathief(filename, xlim=xlim, ylim=ylim, debug=True)

    # Plotting
    if do_plot:
        import pylab as pl
        pl.figure(figsize=(12,4))

        ax1 = pl.subplot(1,2,1)
        ax1.imshow(pl.imread(filename))
        ax1.set_title('Original')

        ax2 = pl.subplot(1,2,2)
        ax2.bar(data.x, data.y)
        ax2.set_title('Extracted')
        ax2.set_xlabel('Serial interval')
        ax2.set_ylabel('Frequency')

        pl.show()

    return data


if __name__ == '__main__':

    do_plot = True

    test_api(do_plot=do_plot)