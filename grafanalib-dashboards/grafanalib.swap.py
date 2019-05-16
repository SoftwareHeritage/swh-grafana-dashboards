from grafanalib.core import *

def swap_activity_graph(target, time_from=None):
  if time_from is not None:
    timeFrom = "%s" % (time_from,)
  else:
    timeFrom = None
  return Graph(
    title='Swap activity',
    dataSource="Prometheus (Pergamon)",
    timeFrom=timeFrom,
    targets=[
      Target(
        expr='irate(node_vmstat_pswpin{instance="%s"}[5m])' % (target),
        legendFormat="pages per second in",
        refId='A',
      ),
      Target(
        expr='irate(node_vmstat_pswpout{instance="%s"}[5m])' % (target),
        legendFormat="pages per second out",
        refId='B',
      ),
    ],
    yAxes=[
      YAxis(format=SHORT_FORMAT),
      YAxis(format=SHORT_FORMAT),
    ],
  )

dashboard = Dashboard(
    title="Swap usage auto-generated",
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
            query='node_memory_SwapTotal_bytes',
            regex='/instance="([^"]*)"/',
            dataSource='Prometheus (Pergamon)',
        ),
    ]),
    rows=[
      Row(
        title = 'Swap',
        panels=[
          swap_activity_graph('$target'),
          swap_activity_graph('$target', "1y"),
        ],
      ),
    ],).auto_panel_ids()
