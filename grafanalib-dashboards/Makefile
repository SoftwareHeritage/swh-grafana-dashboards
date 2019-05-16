# Generate json dashboards

TARGETS= \
	 grafanalib.cpu.usage.json		\
	 grafanalib.disk.iops.json		\
	 grafanalib.disk.latency.json		\
	 grafanalib.disk.throughput.json	\
	 grafanalib.filesystem.sizes.json	\
	 grafanalib.loadavg.json		\
	 grafanalib.memory.usage.json		\
	 grafanalib.network.traffic.json	\
	 grafanalib.swap.json			\
	 grafanalib.uptime.json

default: $(TARGETS)

%.json:	%.py
	generate-dashboard -o $@ $<

clean:
	rm $(TARGETS)
