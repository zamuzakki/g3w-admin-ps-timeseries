from sitetree.utils import item
from core.utils.tree import G3Wtree

# Be sure you defined `sitetrees` in your module.
sitetrees = (
  # Define a tree with `tree` function.
  G3Wtree(
        'qps_timeseries',
        title='PS TIMESERIES',
        module='qps_timeseries',
        items=[
            # Then define items and their children with `item` function.
            item(
                'PS TIMESERIES',
                '#',
                type_header=True,
            ),
            item(
                'Projects',
                '#',
                icon_css_class='fa fa-users',
                children=[
                    item(
                        'Aggiungi progetto',
                        'qpstimeseries-project-add',
                        url_as_pattern=True,
                        icon_css_class='fa fa-plus',
                        access_by_perms=['qps_timeseries.add_qpstimeseriesproject'],
                    ),
                    item(
                        'Lista progetti',
                        'qpstimeseries-project-list',
                        url_as_pattern=True,
                        icon_css_class='fa fa-list',
                    ),
                    item(
                        'Agg. progetto {{ object.project.title }}',
                        'qpstimeseries-project-update object.pk',
                        url_as_pattern=True,
                        icon_css_class='fa fa-edit',
                        in_menu=False,
                        alias='qpstimeseries-project-update',
                    ),
                ]
            ),
        ]
    ),

  G3Wtree('qps_timeseries_en', title='PS TIMSERIES', module='qps_timeseries', items=[
      # Then define items and their children with `item` function.
      item('PS TIMESERIES', '#', type_header=True),
      item('Projects', '#', icon_css_class='fa fa-users', children=[
          item('Add project', 'qpstimeseries-project-add', url_as_pattern=True, icon_css_class='fa fa-plus',
               access_by_perms=['qps_timeseries.add_qpstimeseriesproject']),
          item('Projects list', 'qpstimeseries-project-list', url_as_pattern=True, icon_css_class='fa fa-list'),
          item('Update project {{ object.project.title }}', 'qpstimeseries-project-update object.pk', url_as_pattern=True,
               icon_css_class='fa fa-edit', in_menu=False, alias='qpstimeseries-project-update'),
      ]),
  ]),
)