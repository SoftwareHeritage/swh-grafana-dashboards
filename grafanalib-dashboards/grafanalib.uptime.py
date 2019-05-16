from grafanalib.core import *

def uptime_graph(target, time_from=None):
  if time_from is not None:
    timeFrom = "%s" % (time_from,)
  else:
    timeFrom = None
  return Graph(
    title='Uptime',
    dataSource="Prometheus (Pergamon)",
    timeFrom=timeFrom,
    targets=[
      Target(
        expr='time() - node_boot_time_seconds{instance="%s"}' % (target),
        legendFormat="uptime",
        refId='A',
      ),
    ],
    yAxes=[
      YAxis(format=SECONDS_FORMAT),
      YAxis(format=SHORT_FORMAT),
    ],
  )

dashboard = Dashboard(
    title="Uptime auto-generated",
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
            query='node_boot_time_seconds',
            regex='/instance="([^"]*)"/',
            dataSource='Prometheus (Pergamon)',
        ),
    ]),
    rows=[
      Row(
        title = 'Uptime',
        panels=[
          uptime_graph('$target'),
          uptime_graph('$target', "1y"),
        ],
      ),
    ],).auto_panel_ids()
