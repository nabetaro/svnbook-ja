include ../tools/Makefile.base

# Makefile.base overrides
BOOK_FO_XSLTPROC_OPTS = --stringparam paper.type A4
L10N_REVISION = revisjon

# Stuff below here is added for building the Norwegian version.

COLLAB=http://svn.red-bean.com/svnbook

BUILDTMP_DIR = build.tmp
BOOKFILES = appa.xml appb.xml appc.xml appd.xml book.xml ch00.xml \
            ch01.xml ch02.xml ch03.xml ch04.xml ch05.xml ch06.xml \
            ch07.xml ch08.xml ch09.xml colo.xml copyright.xml \
            foreword.xml glossary.xml

BDTMP = bd.tmp
BDFILES = book.xml foreword.xml ch00.xml ch01.xml ch02.xml ch03.xml \
          ch04.xml appa.xml ch05.xml ch06.xml ch07.xml ch08.xml \
          ch09.xml appb.xml appc.xml appd.xml copyright.xml colo.xml \
          glossary.xml

build: dircheck htmlbook copytobuild

dircheck:
	mkdir $(BUILDTMP_DIR)
	rmdir $(BUILDTMP_DIR)

htmlbook:
	$(MAKE) clean && $(MAKE) all-html

copytobuild:
	svn co http://svn.sunbase.org/repos/svnbook_nb/build $(BUILDTMP_DIR)
	find $(BUILDTMP_DIR) -type f | grep -v '/\.svn/' | xargs rm
	cp -a $(BOOK_HTML_CHUNK_DIR) $(BUILDTMP_DIR)/
	cp -a $(BOOK_HTML_TARGET) $(BUILDTMP_DIR)/
	cp -a $(BOOK_IMAGES) $(BUILDTMP_DIR)/images/
	cp -a $(BOOK_DIR)/styles.css $(BUILDTMP_DIR)/

editmode:
	$(MAKE) convfiles CONV_PARAM=-e

commitmode:
	$(MAKE) convfiles CONV_PARAM=

convfiles:
	@for _prc in $(BOOKFILES); do \
		echo -n "$$_prc: convert..."; \
		dest=book/$$_prc; \
		swp=book/.$$_prc.swp; \
		if [ -e $$swp ]; then \
			echo "$$swp: Swap file found. Is the file being edited?" >&2; \
			exit 1; \
		fi; \
		bin/clean_files $(CONV_PARAM) $$dest >$$dest.tmp || exit 1; \
		echo -n "move..."; \
		mv $$dest.tmp $$dest; \
		echo "OK."; \
	done

bookdiff:
	mkdir $(BDTMP)
	svn co -N -r`cat LAST_UPDATED` $(COLLAB)/trunk/src/en/book $(BDTMP)/eng
	for _ptd in $(BDFILES); do \
		cat $(BDTMP)/eng/$$_ptd | bin/clean_files -e >>$(BDTMP)/eng.txt; \
		cat book/$$_ptd | bin/clean_files -e >>$(BDTMP)/norw.txt; \
	done
	vimdiff $(BDTMP)/norw.txt $(BDTMP)/eng.txt
	@echo The temporary files are still in $(BDTMP)/ for you to play with.

sync:
	mkdir sync.LOCK
	svn update
	@echo ======= START svn status =======
	@svn status -q
	@echo ======== END svn status ========
	@echo If there are no local changes, press ENTER...
	@read
	svnversion . >HEADREV
	$(MAKE) editmode
	svn merge -r$$(cat LAST_UPDATED):$$(cat HEADREV) $(COLLAB)/trunk/src/en .
	mv HEADREV LAST_UPDATED
	$(MAKE) commitmode
	rmdir sync.LOCK

# $Id$
# vim: set ts=4 sw=4 sts=4 noet :
