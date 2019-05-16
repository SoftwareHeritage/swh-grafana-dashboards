from grafanalib.core import *

def memory_graph(target, time_from=None):
  if time_from is not None:
    timeFrom = "%s" % (time_from,)
  else:
    timeFrom = None
  return Graph(
    title='Memory usage',
    dataSource="Prometheus (Pergamon)",
    timeFrom=timeFrom,
    stack=True,
    tooltip=Tooltip(valueType=INDIVIDUAL),
    targets=[
      Target(
        expr='node_memory_MemTotal_bytes{instance="%s"}' % (target),
        legendFormat="Total memory",
        refId='A',
      ),
      Target(
        expr='node_memory_MemTotal_bytes{instance="%s"} - \
	      node_memory_MemAvailable_bytes{instance="%s"}' % (target, target),
        legendFormat="Used memory",
        refId='B',
      ),
      Target(
        expr='node_memory_Cached_bytes{instance="%s"}' % (target),
        legendFormat="File cache",
        refId='C',
      ),
      Target(
        expr='node_memory_SwapTotal_bytes{instance="%s"} - \
	      node_memory_SwapFree_bytes{instance="%s"}' % (target, target),
        legendFormat="Used swap",
        refId='D',
      ),
    ],
    seriesOverrides = [
	{"alias": "Total memory", "stack": "false"},
	{"alias": "Used swap", "stack": "false", "fill": "10"},
    ],
    yAxes=[
      YAxis(format='bytes'),
      YAxis(format=SHORT_FORMAT),
    ],
    legend=Legend(min=True, max=True, avg=True, current=True),
  )

dashboard = Dashboard(
    title="Memory usage auto-generated",
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
            query='node_uname_info',
            regex='/instance="([^"]*)"/',
            dataSource='Prometheus (Pergamon)',
        ),
    ]),
    rows=[
      Row(
        title = 'Memory',
        panels=[
          memory_graph('$target'),
          memory_graph('$target', "1y"),
        ],
      ),
    ],).auto_panel_ids()
