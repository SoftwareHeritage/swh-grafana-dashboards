from grafanalib.core import *

def filesystem_graph(target, mountpoint, time_from=None):
  if time_from is not None:
    timeFrom = "%s" % (time_from,)
  else:
    timeFrom = None
  return Graph(
    title='Size of %s' % (mountpoint,),
    dataSource="Prometheus (Pergamon)",
    timeFrom=timeFrom,
    targets=[
      Target(
        expr='node_filesystem_size_bytes{instance="%s",mountpoint="%s"}' % (target, mountpoint),
        legendFormat="Filesystem size",
        refId='A',
      ),
      Target(
        expr='node_filesystem_size_bytes{instance="%s",mountpoint="%s"} - ' \
             'node_filesystem_avail_bytes{instance="%s",mountpoint="%s"}' \
             % (target, mountpoint, target, mountpoint),
        legendFormat="Used space",
        refId='B',
      ),
    ],
    yAxes=[
      YAxis(format='bytes'),
      YAxis(format=SHORT_FORMAT),
    ],
  )

dashboard = Dashboard(
    title="Filesystem sizes auto-generated",
    templating=Templating(list=[
	Template(
            name="host",
            label="",
            query='node_uname_info{instance="$target"}',
            regex='/nodename="([^"]*)"/',
            dataSource='Prometheus (Pergamon)',
	),
        Template(
            name="target",
            label="",
            query='node_filesystem_size_bytes',
            regex='/instance="([^"]*)"/',
            dataSource='Prometheus (Pergamon)',
        ),
        Template(
            name="filesystem",
            label="",
            query='node_filesystem_size_bytes{instance="$target"}',
            regex='/mountpoint="([^"]*)"/',
            dataSource='Prometheus (Pergamon)',
            includeAll=True,
            default="All",
            hide = 2,
        ),
    ]),
    rows=[
      Row(
        title = '$filesystem',
        panels=[
          filesystem_graph('$target', '$filesystem'),
          filesystem_graph('$target', '$filesystem', "1y"),
        ],
        repeat = 'filesystem',
      ),
    ],).auto_panel_ids()

