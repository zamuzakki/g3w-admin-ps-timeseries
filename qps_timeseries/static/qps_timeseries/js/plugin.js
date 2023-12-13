(function() {

  const { Plugin }  = g3wsdk.core.plugin;
  const { GUI }     = g3wsdk.gui;
  const { G3W_FID } = g3wsdk.constant;

  if (!globalThis.Plotly) {
    $script('https://cdn.plot.ly/plotly-1.52.2.min.js');
  }

  document.head.insertAdjacentHTML(
    'beforeend',
    `<style>
      .js-plotly-plot .modebar-container                                   { top: unset !important; bottom: 0; left: 0; text-align: center; }
      .js-plotly-plot a.modebar-btn                                        { font-size: 30px !important; }
      .js-plotly-plot .plotly .modebar                                     { left: 0; }
      .js-plotly-plot .modebar-container > div                             { display: flex; }
      .js-plotly-plot .plotly .modebar .modebar-group:first-of-type        { order: 2; }
      .js-plotly-plot .plotly .modebar .modebar-group:nth-last-child(-n+2) { order: 1; margin-left: auto;}
      .js-plotly-plot .plotly .modebar .modebar-group:last-of-type         { position: fixed; left: 0; top: 8px; }
    </style>`,
  );

  /**
   * Custom modebar button
   * 
   * @see https://plotly.com/javascript/configuration-options/#add-buttons-to-modebar
   */
  const btn = (name, color, data, ids) => ids.length ? ({
    name,
    icon: {
      svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -4 39 9" style="fill:${ color }; stroke:${ color }; stroke-width: 2; opacity:${ 'markers' == data[ids[0]].mode ? 0.5 : 1 }"><path d="M5,0h30M24,4h-8v-8h8v8Z"/></svg>`
    },
    click(p, e) {
      const btn = e.target.closest('.modebar-btn svg');
      const off = btn.style.opacity < 1;
      Plotly.restyle(p, { mode: off ? 'scatter' : 'markers' }, ids);
      btn.style.opacity = off ? 1 : .5;
    }
  }) : undefined;

  /**
   * Match strings with the following pattern:
   * - starts with the letter "D"
   * - followed by 8 digits representing the date in the format "YYYYMMDD"
   */
  const DATE_REGEX = /^D\d{8}$/;

  new (class extends Plugin {
    constructor() {
      super({
        name: 'qps_timeseries',
        i18n: {},
      });
      if (this.registerPlugin(this.config.gid)) {
        GUI
          .getService('queryresults')
          .onafter('addActionsForLayers', (actions, layers) => {
            layers.forEach(layer => {
              if (!layer.attributes.some(attr => DATE_REGEX.test(attr.name))) {
                return;
              }
              actions[layer.id].push({
                id: 'qps-timeseries',
                class: GUI.getFontClass('chart-line'),
                hint: 'PS Time Series',
                cbk: (layer, feature) => {
                  const chart = new (Vue.extend({
                    template: `<section class="qps-timeseries"><bar-loader :loading="loading"/><div ref="chart" style="margin: 10px auto 30px auto;"></div></section>`,
                    data:     () => ({ loading: true }), // show loading bar while getting data from server
                  }))();
                  GUI
                    .showModalDialog({
                      message: chart.$mount().$el,
                      size: 'large',
                    })
                    .on("shown.bs.modal", async function() {
                      const { data, layout, config } = await (await fetch(initConfig.baseurl + 'qps_timeseries/api/plot/' + layer.id + '/' + feature.attributes[G3W_FID])).json();
                      Plotly.newPlot(chart.$refs.chart, data, layout, {...config, modeBarButtonsToAdd: [[
                          initConfig?.user?.admin_url && {
                            name: 'Edit in admin',
                            icon: Plotly.Icons.pencil,
                            direction: 'up',
                            click(gd) {
                              window.open(initConfig.user.admin_url, '_blank');
                            },
                          },
                        ], [
                          btn('Toggle scatter lines', 'black', data, [0]),
                          btn('Toggle replica lines', 'blue', data, data.flatMap((d, i) => (i && 'lines' !== d.mode) ? i : [])), // ie. 'scatter' or 'markers' mode
                        ], [{
                          name: 'Download plot as svg',
                          icon: {
                            width: 70,
                            height: 70,
                            path: 'M60.64,62.3a11.29,11.29,0,0,0,6.09-6.72l6.35-17.72L60.54,25.31l-17.82,6.4c-2.36.86-5.57,3.41-6.6,6L24.48,65.5l8.42,8.42ZM40.79,39.63a7.89,7.89,0,0,1,3.65-3.17l14.79-5.31,8,8L61.94,54l-.06.19a6.44,6.44,0,0,1-3,3.43L34.07,68l-3.62-3.63Zm16.57,7.81a6.9,6.9,0,1,0-6.89,6.9A6.9,6.9,0,0,0,57.36,47.44Zm-4,0a2.86,2.86,0,1,1-2.85-2.85A2.86,2.86,0,0,1,53.32,47.44Zm-4.13,5.22L46.33,49.8,30.08,66.05l2.86,2.86ZM83.65,29,70,15.34,61.4,23.9,75.09,37.59ZM70,21.06l8,8-2.84,2.85-8-8ZM87,80.49H10.67V87H87Z',
                            transform: 'matrix(1 0 0 1 -15 -15)'
                        },
                          click(gd) {
                            Plotly.downloadImage(gd, { format: 'svg' })
                          }
                        }]
                        ].filter(Boolean),
                      });
                      chart.loading = false;
                    });
                }
              });
            });
          });
      }
      // hide loading icon on map
      this.setReady(true);
    }
  })();
  
})();