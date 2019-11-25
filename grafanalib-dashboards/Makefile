# Generate json dashboards

NAME=swh-grafanalib-dashboards
VERSION=1.0
PKGNAME=$(NAME)-$(VERSION)

STAGEDIR:= $(shell mktemp -d)
DESTDIR=$(STAGEDIR)/usr/local/share/swh-data/swh-grafanalib-dashboards
DOCDIR=$(STAGEDIR)/usr/share/doc/$(NAME)

TARGETS= \
	 grafanalib.cpu.temperatures.json	\
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

package: $(TARGETS)
	cp -a DEBIAN $(STAGEDIR)
	mkdir -p $(DESTDIR)
	cp -a $(TARGETS) $(DESTDIR)
	mkdir -p $(DOCDIR)
	cp -a COPYRIGHT $(DOCDIR)/copyright
	gzip -c -n -9 Changelog > $(DOCDIR)/changelog.gz
	fakeroot dpkg-deb --build $(STAGEDIR)
	mv $(STAGEDIR).deb $(PKGNAME).deb
	@echo "Removing $(STAGEDIR) stage directory"
	@rm -rf $(STAGEDIR)

%.json:	%.py
	generate-dashboard -o $@ $<

clean:
	rm $(TARGETS)
