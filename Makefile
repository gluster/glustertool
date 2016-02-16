.PHONY: build dist install develop rpm

VERSION := 0.1.1
RPMBUILD := $(HOME)/rpmbuild

build:
	@echo "Doing $@"
	@python setup.py build

dist:
	@echo "Doing $@"
	@python setup.py sdist

install:
	@echo "Doing $@"
	@python setup.py install

develop:
	@echo "Doing $@"
	@python setup.py develop

rpm: dist
	@echo "Doing $@"
	rm -rf $(RPMBUILD)/SOURCES/glustertool*
	rm -rf $(RPMBUILD)/BUILD/glustertool*
	mkdir -p $(RPMBUILD)/SOURCES
	cp ./dist/glustertool-$(VERSION).tar.gz $(RPMBUILD)/SOURCES; \
	rpmbuild -ba glustertool.spec
