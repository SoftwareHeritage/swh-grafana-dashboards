from grafanalib.core import *

def device_iops_graph(target, device, time_from=None):
  if time_from is not None:
    timeFrom = "%s" % (time_from,)
  else:
    timeFrom = None
  return Graph(
    title='IOs for %s' % (device,),
    dataSource="Prometheus (Pergamon)",
    timeFrom=timeFrom,
    targets=[
      Target(
        expr='rate(node_disk_reads_completed_total{instance="%s",device="%s"}[5m])' % (target, device),
        legendFormat="reads per second",
        refId='A',
      ),
      Target(
        expr='rate(node_disk_writes_completed_total{instance="%s",device="%s"}[5m])' % (target, device),
        legendFormat="writes per second",
        refId='B',
      ),
    ],
    yAxes=[
      YAxis(format=SHORT_FORMAT),
      YAxis(format=SHORT_FORMAT),
    ],
    legend=Legend(max=True, min=True, avg=True, current=True),
  )

dashboard = Dashboard(
    title="Diskstat iops auto-generated",
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
            query='node_disk_io_now',
            regex='/instance="([^"]*)"/',
            dataSource='Prometheus (Pergamon)',
        ),
        Template(
            name="device",
            label="",
            query='node_disk_io_now{instance="$target"}',
            regex='/device="([sd|vd|dm|md][a-z0-9-]*)/',
            dataSource='Prometheus (Pergamon)',
            includeAll=True,
            default="All",
            hide = 2,
        ),
    ]),
    rows=[
      Row(
        title = '$device device',
        panels=[
          device_iops_graph('$target', '$device'),
          device_iops_graph('$target', '$device', "1y"),
        ],
        repeat = 'device',
      ),
    ],).auto_panel_ids()
