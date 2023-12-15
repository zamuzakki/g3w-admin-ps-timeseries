from django.shortcuts import render

from django.views.generic import View
from django.http.response import JsonResponse

class QPSTimeseriesPlot(View):

    def get(self, *args, **kwargs):

        DELTA = 5
        TITLE = 'PS Time Series Viewer<br><sub>coher.: <pid> vel.: <pid> v_stdev.: <pid></sub>'
        X = ['2013-08-04 22:23:00', '2013-09-04 22:23:00', '2013-10-04 22:23:00', '2013-11-04 22:23:00', '2013-12-04 22:23:00']
        Y = [4, 1, 7, 1, 4]

        ## WebGL optimization
        ## https://plotly.com/javascript/webgl-vs-svg/
        TYPE = 'scattergl'

        ## Fake Data
        ## https://plotly.com/javascript/
        return JsonResponse({
            'data':  [
              ## TRACE0 = scatter
              {
                'x': X,
                'y': Y,
                'mode': 'markers',
                'type': TYPE,
                'name': 'Scatter',
                'marker': {
                  'size': 8,
                  'color': 'black',
                  'symbol': 'square',
                },
              },
              ## TRACE1 = replica + delta
              {
                'visible': False if 0 == DELTA else True,
                'x': [] if 0 == DELTA else X,
                'y': [] if 0 == DELTA else [y + DELTA for y in Y],
                'mode': 'scatter',
                'type': TYPE,
                'name': 'Replica +' + str(DELTA),
                'marker': {
                  'size': 8,
                  'color': 'blue',
                  'symbol': 'square',
                },
              },
              ## TRACE2 = replica - delta
              {
                'visible': False if 0 == DELTA else True,
                'x': [] if 0 == DELTA else X,
                'y': [] if 0 == DELTA else [y - DELTA for y in Y],
                'mode': 'scatter',
                'type': TYPE,
                'name': 'Replica -' + str(DELTA),
                'marker': {
                  'size': 8,
                  'color': 'blue',
                  'symbol': 'square',
                },
              },
              ## TRACE3 = trend line
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
                'type': TYPE,
                'name': 'Lin Trend',
                'line': {
                  'color': 'red',
                },
              },
              ## TRACE5 = trend poly 
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
                'type': 'scatter',
                'name': 'Poly Trend',
                # https://plotly.com/javascript/reference/scatter/#scatter-line-shape
                # https://plotly.com/javascript/reference/scattergl/#scattergl-line-shape
                'line': {
                  'shape': 'spline',
                  'smoothing': 1.3,
                  'color': 'green'
                },
              },
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