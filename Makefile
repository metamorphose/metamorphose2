#
# Makefile tested on Linux and FreeBSD.
# May work with other UNIXes.
#
# Authors : Ianaré Sévi, Javier Prats, Pierre-Yves Chibon
# hacked by Gabriel Espinoza to create RPM packages
#

include common.mk

all: options build install

build:
	# make needed directories
	install -d $(DESTDIR)$(PREFIX)/share/$(PACKAGE)/;

remove:
	rm -fR $(DESTDIR)$(PREFIX)/share/$(PACKAGE);
	rm -f $(DESTDIR)$(PREFIX)/bin/$(PACKAGE);
	rm -f $(DESTDIR)$(PREFIX)/share/man/man1/$(PACKAGE).1.gz;

	# delete icon and launcher if folders exist
	if [ -d $(DESTDIR)$(PREFIX)/share/pixmaps ]; then\
		rm -f $(DESTDIR)$(PREFIX)/share/pixmaps/$(PACKAGE).png;\
	fi;
	if [ -d $(DESTDIR)$(PREFIX)/share/applications ] ; then\
		rm -f $(DESTDIR)$(PREFIX)/share/applications/$(PACKAGE).desktop;\
	fi;
	if [ -d $(DESTDIR)$(PREFIX)/share/app-install/icons ] ; then\
		rm -f $(DESTDIR)$(PREFIX)/share/app-install/icons/$(PACKAGE).png;\
	fi;
	if [ -d $(DESTDIR)$(PREFIX)/share/app-install/desktop ] ; then\
		rm -f $(DESTDIR)$(PREFIX)/share/app-install/desktop/$(PACKAGE).desktop;\
	fi;

	# delete translation files
	cd messages && $(MAKE) uninstall

	# delete user files
	if [ ${remusr} = 1 ] ; then\
		find /home/ -depth -name .$(PACKAGE) -exec rm -fR {} \; ;\
		find /root/ -depth -name .$(PACKAGE) -exec rm -fR {} \; ;\
	fi;\

clean:
	find . -type f -regex ".*\\(pyc\|tmp\|~\)$"" -delete;
	find . -depth -name "*.svn" -exec rm -fr {} \;

install: install-doc
	# make sure all permissions are correct
	chmod -R a+r *;
	find . -type d ! -regex '.*/\..*' -exec chmod 755 {} \;
	rm $(PACKAGE).1.gz

	# copy program files and libraries
	mkdir -p $(DESTDIR)$(PREFIX)/share/$(PACKAGE)
	cp -pR src/* $(DESTDIR)$(PREFIX)/share/$(PACKAGE)/;

	# install translation files
	cd messages && $(MAKE) install

	# adjust app.py translations' search-path
	sed -i "s|/usr|$(DESTDIR)$(PREFIX)|g" $(DESTDIR)$(PREFIX)/share/$(PACKAGE)/app.py;

	# install the executables
	install -d $(DESTDIR)$(PREFIX)/bin/;
	install -m 755 $(PACKAGE) $(DESTDIR)$(PREFIX)/bin/;

	# adjust executable' path
	sed -i "s|/usr|$(DESTDIR)$(PREFIX)|g" $(DESTDIR)$(PREFIX)/bin/$(PACKAGE);

	# copy icon and launcher if folders exist
	#must create this folders or rpm won't build
	install -d $(DESTDIR)$(PREFIX)/share/pixmaps
	install -m 644 src/icons/metamorphose64.png $(DESTDIR)$(PREFIX)/share/pixmaps/$(PACKAGE).png;\
	if [ -d $(DESTDIR)$(PREFIX)/share/app-install/icons ]; then\
		ln -s $(DESTDIR)$(PREFIX)/share/pixmaps/$(PACKAGE).png $(DESTDIR)$(PREFIX)/share/app-install/icons/$(PACKAGE).png;\
	fi;
	install -d $(DESTDIR)$(PREFIX)/share/applications
	install -m 644 $(PACKAGE).desktop $(DESTDIR)$(PREFIX)/share/applications/
	# adjust launcher's path
	sed -i "s|/usr|$(DESTDIR)$(PREFIX)|g" $(DESTDIR)$(PREFIX)/share/applications/$(PACKAGE).desktop
	if [ -d $(DESTDIR)$(PREFIX)/share/app-install/desktop ]; then\
		ln -s $(DESTDIR)$(PREFIX)/share/applications/$(PACKAGE).desktop $(DESTDIR)$(PREFIX)/share/app-install/desktop/$(PACKAGE).desktop;\
	fi;

install-doc:
	install -d $(DESTDIR)$(PREFIX)/share/man/man1/
	gzip -c9 manpage.1 > $(PACKAGE).1.gz
	install -m 644 $(PACKAGE).1.gz $(DESTDIR)$(PREFIX)/share/man/man1/

options:
	@echo PACKAGE = $(PACKAGE)
	@echo DESTDIR = $(DESTDIR)
	@echo PREFIX = $(PREFIX)
	@echo remusr = $(remusr)
	@echo msgfmt_location = $(msgfmt_location)
	@echo OS = $(OS)

.PHONY: options all remove

# EOF
