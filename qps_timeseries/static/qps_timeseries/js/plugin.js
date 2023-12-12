(function() {

  const { Plugin, PluginService } = g3wsdk.core.plugin;
  const { GUI }                   = g3wsdk.gui;
  const { G3W_FID }               = g3wsdk.constant;

  if (!globalThis.Plotly) {
    $script('https://cdn.plot.ly/plotly-1.52.2.min.js');
  }

  /**
   * Match strings with the following pattern:
   * - starts with the letter "D"
   * - followed by 8 digits representing the date in the format "YYYYMMDD"
   */
  const DATE_REGEX = /^D\d{8}$/;

  /**
   * Chart component
   */
  const Chart = {
    template: `
      <section class="qps-timeseries">
        <bar-loader :loading="loading"/>
        <div ref="chart" style="margin-top: 10px;"></div>
      </section>
    `,

    data() {
      return {
        loading: true, // show loading bar while getting data from server
      }
    },

  };

  class Service extends PluginService {

    init(config = {}) {

      /**
       * @FIXME add description
       */
      this.config = config;

      /**
       * Store key and setter name method to eventually remove when plugin is removed
       * 
       * @type {{}}
       */
      this.keySetters = {};

      /**
       * Query result service
       */
      this.queryresultsService = GUI.getService('queryresults');

      const keyOnAfteraddActionsForLayers = this.queryresultsService.onafter('addActionsForLayers', (actions, layers) => {
        layers.forEach(layer => {
          if (!layer.attributes.filter(attr => DATE_REGEX.test(attr.name)).length) {
            return;
          }
          actions[layer.id].push({
            id: 'qps-timeseries',
            class: GUI.getFontClass('chart-line'),
            hint: 'PS Time Series',
            cbk: (layer, feature) => {
              const fid   = feature.attributes[G3W_FID];
              const chart = new (Vue.extend(Chart))();
              GUI
                .showModalDialog({
                  message: chart.$mount().$el,
                  size: 'large',
                })
                .on("shown.bs.modal", async function() {
                  const { data, layout, config } = await (await fetch(initConfig.baseurl + 'qps_timeseries/api/some-protected-view/' + fid)).json();
                  Plotly.newPlot(chart.$refs.chart, data, layout, config);
                  chart.loading = false;
                });
            }
          });
        });
      });

      this.keySetters[keyOnAfteraddActionsForLayers] = 'addActionsForLayers';
    }

    /**
     * Unlisten to setters events
     */
    clear() {
      Object
        .enties(this.keySetters)
        .forEach(([key, setter]) => this.queryresultsService.un(setter, key));
    }

  }

  new (class extends Plugin {
    constructor() {
      super({
        name: 'qps_timeseries',
        i18n: {},
        service: new Service,
      });
      if (this.registerPlugin(this.config.gid)) {
        this.service.init(this.config);
      }
      // hide loading icon on map
      this.setReady(true);
    }
  })();
  
})();