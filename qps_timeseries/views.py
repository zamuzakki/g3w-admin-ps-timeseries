from django.shortcuts import render

from django.views.generic import View
from django.http.response import JsonResponse

class SomeProtectedView(View):

    def get(self, *args, **kwargs):
        ## Fake Data
        ## https://plotly.com/javascript/
        return JsonResponse({
            'data':  [
              {
                'x': [
                  '2013-08-04 22:23:00',
                  '2013-09-04 22:23:00',
                  '2013-10-04 22:23:00',
                  '2013-11-04 22:23:00',
                  '2013-12-04 22:23:00',
                ],
                'y': [4, 1, 7, 1, 4],
                'mode': 'markers',
                'type': 'scatter',
                'name': 'Scatter',
                'marker': { 'size': 5, 'color': 'black' }
              },
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
                'range': [ '2013-07-04 22:23:00', '2014-01-04 22:23:00' ]
              },
              'yaxis': {
                'title': '[mm]',
                'range': [0, 8]
              },
              'title':'Data Labels Hover'
            },
            'config': {
              'displayModeBar': True,
              'editable': True,
              'responsive': True,
              'scrollZoom': True
            },
        })