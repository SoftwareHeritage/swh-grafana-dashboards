from grafanalib.core import *

def network_graph(target, device, time_from=None):
  if time_from is not None:
    timeFrom = "%s" % (time_from,)
  else:
    timeFrom = None
  return Graph(
    title='Network traffic',
    dataSource="Prometheus (Pergamon)",
    timeFrom=timeFrom,
    stack=True,
    tooltip=Tooltip(valueType=INDIVIDUAL),
    targets=[
      Target(
        expr='irate(node_network_receive_bytes_total{instance="%s",device="%s"}[5m]) * 8' % (target, device),
        legendFormat="bytes per second in",
        refId='A',
      ),
      Target(
        expr='irate(node_network_transmit_bytes_total{instance="%s",device="%s"}[5m]) * 8' % (target, device),
        legendFormat="bytes per second out",
        refId='B',
      ),
    ],
    yAxes=[
      YAxis(format='bits'),
      YAxis(format=SHORT_FORMAT),
    ],
    legend=Legend(max=True, min=True, avg=True, current=True),
  )

dashboard = Dashboard(
    title="Network traffic auto-generated",
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
            query='node_network_receive_bytes_total',
            regex='/instance="([^"]*)"/',
            dataSource='Prometheus (Pergamon)',
        ),
        Template(
            name="interface",
            label="",
            query='node_network_receive_bytes_total{instance="$target"}',
            regex='/device="([^"]*)/',
            dataSource='Prometheus (Pergamon)',
            includeAll=True,
            default="All",
            hide = 2,
        ),
    ]),
    rows=[
      Row(
        title = '$interface traffic',
        panels=[
          network_graph('$target', "$interface"),
          network_graph('$target', "$interface", "1y"),
        ],
	repeat = 'interface',
      ),
    ],).auto_panel_ids()
