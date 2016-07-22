#
# Makefile tested on Linux and FreeBSD.
# May work with other UNIXes.
#
# Authors : Ianaré Sévi, Javier Prats, Pierre-Yves Chibon
# hacked by Gabriel Espinoza to create RPM packages
#

# Specify an alternate install root
DESTDIR=
PREFIX=/usr

PACKAGE=metamorphose2

# change to 1 to remove all metamorphose user files
remusr=0

OS=`uname -s`

all: build install

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
	if [ -d $(DESTDIR)$(PREFIX)/share/locale ] ; then\
		find $(DESTDIR)$(PREFIX)/share/locale -name $(PACKAGE).mo -delete;\
	fi;\

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
	cp -pR src/* $(DESTDIR)$(PREFIX)/share/$(PACKAGE)/;


	# install translation files
	if [ ${OS} = "Linux" ]; then\
		for lang in `ls -1 messages`; do\
			if [ -d messages/$${lang} ]; then\
				mkdir -p $(DESTDIR)$(PREFIX)/share/locale/$${lang}/LC_MESSAGES;\
				cp -p messages/$${lang}/LC_MESSAGES/$(PACKAGE).mo $(DESTDIR)$(PREFIX)/share/locale/$${lang}/LC_MESSAGES/;\
			fi;\
		done;\
	fi;\
	if [ ${OS} != "Linux" ]; then\
		cp -pR messages $(DESTDIR)$(PREFIX)/share/$(PACKAGE)/;\
	fi;\

	# install the executables
	install -d $(DESTDIR)$(PREFIX)/bin/;
	install -m 755 $(PACKAGE) $(DESTDIR)$(PREFIX)/bin/;

	# copy icon and launcher if folders exist
	#must create this folders or rpm won't build
	install -d $(DESTDIR)$(PREFIX)/share/pixmaps
	install -m 644 src/icons/metamorphose64.png $(DESTDIR)$(PREFIX)/share/pixmaps/$(PACKAGE).png;\
	if [ -d $(DESTDIR)$(PREFIX)/share/app-install/icons ]; then\
		ln -s $(DESTDIR)$(PREFIX)/share/pixmaps/$(PACKAGE).png $(DESTDIR)$(PREFIX)/share/app-install/icons/$(PACKAGE).png;\
	fi;
	install -d $(DESTDIR)$(PREFIX)/share/applications
	install -m 644 $(PACKAGE).desktop $(DESTDIR)$(PREFIX)/share/applications/
	if [ -d $(DESTDIR)$(PREFIX)/share/app-install/desktop ]; then\
		ln -s $(DESTDIR)$(PREFIX)/share/applications/$(PACKAGE).desktop $(DESTDIR)$(PREFIX)/share/app-install/desktop/$(PACKAGE).desktop;\
	fi;

install-doc:
	install -d $(DESTDIR)$(PREFIX)/share/man/man1/
	gzip -c9 manpage.1 > $(PACKAGE).1.gz
	install -m 644 $(PACKAGE).1.gz $(DESTDIR)$(PREFIX)/share/man/man1/

# EOF
