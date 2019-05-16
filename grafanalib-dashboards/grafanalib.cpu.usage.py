from grafanalib.core import *

def cpu_usage_graph(target, cpu=0, time_from=None):
  if time_from is not None:
    timeFrom = "%s" % (time_from,)
  else:
    timeFrom = None
  return Graph(
    title='CPU %s usage' % (cpu,),
    dataSource="Prometheus (Pergamon)",
    timeFrom=timeFrom,
    stack=True,
    percentage=True,
    targets=[
      Target(
        expr='irate(node_cpu_seconds_total{instance="%s",cpu="%s",mode="system"}[5m])' % (target, cpu),
        legendFormat="system time",
        refId='A',
      ),
      Target(
        expr='irate(node_cpu_seconds_total{instance="%s",cpu="%s",mode="irq"}[5m])' % (target, cpu),
        legendFormat="irq",
        refId='B',
      ),
      Target(
        expr='irate(node_cpu_seconds_total{instance="%s",cpu="%s",mode="softirq"}[5m])' % (target, cpu),
        legendFormat="softirq",
        refId='C',
      ),
      Target(
        expr='irate(node_cpu_seconds_total{instance="%s",cpu="%s",mode="user"}[5m])' % (target, cpu),
        legendFormat="user time",
        refId='D',
      ),
      Target(
        expr='irate(node_cpu_seconds_total{instance="%s",cpu="%s",mode="nice"}[5m])' % (target, cpu),
        legendFormat="nice",
        refId='E',
      ),
      Target(
        expr='irate(node_cpu_seconds_total{instance="%s",cpu="%s",mode="idle"}[5m])' % (target, cpu),
        legendFormat="idle",
        refId='F',
      ),
      Target(
        expr='irate(node_cpu_seconds_total{instance="%s",cpu="%s",mode="iowait"}[5m])' % (target, cpu),
        legendFormat="iowait",
        refId='G',
      ),
      Target(
        expr='irate(node_cpu_seconds_total{instance="%s",cpu="%s",mode="steal"}[5m])' % (target, cpu),
        legendFormat="steal",
        refId='H',
      ),
    ],
    yAxes=[
      YAxis(format='percentunit'),
      YAxis(format=SHORT_FORMAT),
    ],
  )

dashboard = Dashboard(
    title="CPU usage auto-generated",
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
        Template(
            name="cpu",
            label="",
            query='node_cpu_seconds_total{instance="$target"}',
            regex='/cpu="([^"]*)"/',
            dataSource='Prometheus (Pergamon)',
            includeAll=True,
            default="All",
            hide = 2,
        ),
    ]),
    rows=[
      Row(
        title = 'CPU $cpu',
        panels=[
            cpu_usage_graph('$target', '$cpu'),
            cpu_usage_graph('$target', '$cpu', "1y"),
        ],
        repeat = 'cpu',
      ),
    ],).auto_panel_ids()
