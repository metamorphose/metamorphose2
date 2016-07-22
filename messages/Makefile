#
# Makefile
#
# Update or create all translation files.
#

include ../common.mk
msgfmt_location=$(shell which msgfmt)

build:
	@for lang in $$(ls); do\
		if [ -d $$lang ]; then\
			echo building "$$lang/LC_MESSAGES/metamorphose2.mo";\
			mkdir -p $$lang/LC_MESSAGES;\
			$(msgfmt_location) -o $$lang/LC_MESSAGES/metamorphose2.mo $$lang/$$lang.po;\
		fi;\
	done;

clean:
	@for lang in $$(ls); do\
		if [ -d $$lang ]; then\
			echo deleting "$$lang/LC_MESSAGES/metamorphose2.mo";\
			rm $$lang/LC_MESSAGES/metamorphose2.mo;\
			rmdir $$lang/LC_MESSAGES;\
		fi;\
	done;

copy:
	@for lang in $$(ls); do\
		if [ -d $$lang ]; then\
			echo copying to "$(DESTDIR)$(PREFIX)/share/locale/$$lang/LC_MESSAGES/metamorphose2.mo";\
			mkdir -p $(DESTDIR)$(PREFIX)/share/locale/$$lang/LC_MESSAGES;\
			cp $$lang/LC_MESSAGES/*.mo $(DESTDIR)$(PREFIX)/share/locale/$$lang/LC_MESSAGES/;\
		fi;\
	done;

install: build copy clean

uninstall:
	@for lang in $$(ls); do\
		if [ -d $$lang ]; then\
			echo deleting "$(DESTDIR)$(PREFIX)/share/locale/$$lang/LC_MESSAGES/metamorphose2.mo";\
			rm $(DESTDIR)$(PREFIX)/share/locale/$$lang/LC_MESSAGES/*.mo;\
			echo deleting $(DESTDIR)$(PREFIX)/share/locale/$$lang/LC_MESSAGES;\
			rmdir -p $(DESTDIR)$(PREFIX)/share/locale/$$lang/LC_MESSAGES > /dev/null 2>&1;\
		fi;\
	done;

options:
	@echo PACKAGE = $(PACKAGE)
	@echo DESTDIR = $(DESTDIR)
	@echo PREFIX = $(PREFIX)
	@echo remusr = $(remusr)
	@echo msgfmt_location = $(msgfmt_location)
	@echo OS = $(OS)

.PHONY: options install uninstall

# EOF
