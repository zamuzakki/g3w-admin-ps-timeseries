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
      .js-plotly-plot .modebar-container                           { top: unset !important; bottom: 0; left: 0; text-align: center; }
      .js-plotly-plot a.modebar-btn                                { font-size: 30px !important; }
      .js-plotly-plot .plotly .modebar                             { left: 0; }
      .js-plotly-plot .plotly .modebar .modebar-group:last-of-type { position: fixed; left: 0; top: 8px; }
    </style>`,
  );

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
                      Plotly.newPlot(chart.$refs.chart, data, layout, config);
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