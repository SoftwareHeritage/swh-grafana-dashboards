from grafanalib.core import *

def loadavg_graph(target, time_from=None):
  if time_from is not None:
    timeFrom = "%s" % (time_from,)
  else:
    timeFrom = None
  return Graph(
    title='Load average',
    dataSource="Prometheus (Pergamon)",
    timeFrom=timeFrom,
    targets=[
      Target(
        expr='node_load5{instance="%s"}' % (target),
        legendFormat="5m load average",
        refId='A',
      ),
    ],
    yAxes=[
      YAxis(format=SHORT_FORMAT),
      YAxis(format=SHORT_FORMAT),
    ],
  )

dashboard = Dashboard(
    title="Loadavg auto-generated",
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
            query='node_load5',
            regex='/instance="([^"]*)"/',
            dataSource='Prometheus (Pergamon)',
        ),
    ]),
    rows=[
      Row(
        title = 'Load average',
        panels=[
            loadavg_graph('$target'),
            loadavg_graph('$target', "1y"),
        ],
      ),
    ],).auto_panel_ids()
