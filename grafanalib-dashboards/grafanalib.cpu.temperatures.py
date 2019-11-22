from grafanalib.core import *

def cpu_temperature_graph(target, node=0, time_from=None):
  if time_from is not None:
    timeFrom = "%s" % (time_from,)
  else:
    timeFrom = None
  return Graph(
    title='CPU node %s temperature' % (node,),
    dataSource="Prometheus (Pergamon)",
    timeFrom=timeFrom,
    targets=[
      Target(
        expr='node_hwmon_temp_celsius{chip="platform_coretemp_%s",sensor="temp1",instance="%s"}' % (node, target),
        legendFormat="CPU temperature",
        refId='A',
      ),
    ],
    yAxes=[
      YAxis(format=SHORT_FORMAT),
      YAxis(format=SHORT_FORMAT),
    ],
  )

dashboard = Dashboard(
    title="CPU temperatures auto-generated",
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
            query='node_hwmon_temp_celsius',
            regex='/instance="([^"]*)"/',
            dataSource='Prometheus (Pergamon)',
        ),
        Template(
            name="cpu_node",
            label="",
            query='node_hwmon_temp_celsius{instance="$target"}',
            regex='/chip="platform_coretemp_([0-9]*)"/',
            dataSource='Prometheus (Pergamon)',
            includeAll=True,
            default="All",
            hide = 2,
        ),
    ]),
    rows=[
      Row(
        title = 'CPU node $cpu_node',
        panels=[
            cpu_temperature_graph('$target', '$cpu_node'),
            cpu_temperature_graph('$target', '$cpu_node', "1y"),
        ],
        repeat = 'cpu_node',
      ),
    ],).auto_panel_ids()
