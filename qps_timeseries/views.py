from django.shortcuts import render

from django.views.generic import View
from django.http.response import JsonResponse

class QPSTimeseriesPlot(View):

    def get(self, *args, **kwargs):
        DELTA = 5
        TITLE = 'PS Time Series Viewer<br><sub>coher.: <pid> vel.: <pid> v_stdev.: <pid></sub>'
        X = [
            '2013-08-04 22:23:00',
            '2013-09-04 22:23:00',
            '2013-10-04 22:23:00',
            '2013-11-04 22:23:00',
            '2013-12-04 22:23:00',
        ]
        Y = [4, 1, 7, 1, 4]
        ## Fake Data
        ## https://plotly.com/javascript/
        return JsonResponse({
            'data':  [
              ## SCATTER
              {
                'x': X,
                'y': Y,
                'mode': 'markers',
                'type': 'scatter',
                'name': 'Scatter',
                'marker': {
                  'size': 8,
                  'color': 'black',
                  'symbol': 'square',
                },
              },
              ## REPLICA (+ DELTA)
              {
                'visible': False if 0 == DELTA else True,
                'x': [] if 0 == DELTA else X,
                'y': [] if 0 == DELTA else [y + DELTA for y in Y],
                'mode': 'scatter',
                'type': 'scatter',
                'name': 'Replica +' + str(DELTA),
                'marker': {
                  'size': 8,
                  'color': 'blue',
                  'symbol': 'square',
                },
              },
              ## REPLICA (- DELTA)
              {
                'visible': False if 0 == DELTA else True,
                'x': [] if 0 == DELTA else X,
                'y': [] if 0 == DELTA else [y - DELTA for y in Y],
                'mode': 'scatter',
                'type': 'scatter',
                'name': 'Replica -' + str(DELTA),
                'marker': {
                  'size': 8,
                  'color': 'blue',
                  'symbol': 'square',
                },
              },
              ## TREND LINE
              {
                'x': [
                  '2013-08-04 22:23:00',
                  '2013-09-04 22:23:00',
                  '2013-10-04 22:23:00',
                  '2013-11-04 22:23:00',
                  '2013-12-04 22:23:00',
                ],
                'y': [3, 2, 1.5, 2, 4],
                'mode': 'lines',
                'name': 'Lin Trend',
                'marker': {
                  'color': 'red'
                }
              }
            ],
            'layout': {
              'xaxis': {
                'title': '[Date]',
                'autorange': True,
                'linecolor': 'black',
                'mirror': True,
                'ticks': 'outside',
                'tickcolor': '#000',
                'zeroline': False,
                'rangeslider': {
                    # 'range': [ '2013-07-04 22:23:00', '2014-01-04 22:23:00' ],
                    # 'range': [ '2013', '2014' ],
                    # 'range': [ ],
                  'thickness': 0.1,
                },
                'type': 'date'
              },
              'yaxis': {
                'title': '[mm]',
                'autorange': True,
                # 'range': [0 - DELTA, 8 + DELTA],
                'linecolor': 'black',
                'mirror': True,
                'ticks': 'outside',
                'tickcolor': '#000',
                'zeroline': False,
                'rangeslider': { },
                'type': 'linear',
              },
              'title': {
                "font": {
                  "size": 20,
                  "color": "blue",
                  "family": "monospace",
                },
                'text': TITLE,
              },
              'hovermode': 'closest',
            },
            'config': {
              'displayModeBar': True,
              'modeBarButtonsToRemove': ['select2d', 'lasso2d', 'resetScale2d'],
              'editable': True,
              'responsive': True,
              'scrollZoom': True,
              'toImageButtonOptions': { 'filename': 'qps-timeseries' },
            },
        })