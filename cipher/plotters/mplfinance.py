from typing import Optional

import mplfinance as mpf

from .base import Plotter


class MPLFinancePlotter(Plotter):
    """https://github.com/matplotlib/mplfinance/blob/master/examples/addplot.ipynb"""

    def run(self, rows: Optional[list] = None):
        apdict = mpf.make_addplot(self.df["sma200"])
        # when dots
        # apd = mpf.make_addplot(df['LowerB'], type='scatter')

        # marker
        # apd = mpf.make_addplot(signal, type='scatter', markersize=200, marker='^')

        # plot multiple
        # tcdf = df[['LowerB','UpperB']]  # DataFrame with two columns
        # apd  = mpf.make_addplot(tcdf)

        # apds = [ mpf.make_addplot(tcdf),
        #          mpf.make_addplot(low_signal,type='scatter',markersize=200,marker='^'),
        #          mpf.make_addplot(high_signal,type='scatter',markersize=200,marker='v'),
        #        ]
        #
        # mpf.plot(df,addplot=apds,figscale=1.25,volume=True)

        # on panel 1 (additional)
        # apds = [ mpf.make_addplot(tcdf),
        #          mpf.make_addplot(low_signal,type='scatter',markersize=200,marker='^'),
        #          mpf.make_addplot(high_signal,type='scatter',markersize=200,marker='v'),
        #          mpf.make_addplot((df['PercentB']),panel=1,color='g')
        #        ]

        # mpf.make_addplot() has a keyword argument called secondary_y which can have three possible values: True, False, and 'auto'

        mpf.plot(self.df, type="candle", volume=True, addplot=apdict)
