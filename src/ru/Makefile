default: book-html-chunk

include ../tools/Makefile.base

# Makefile.base overrides
BOOK_FO_XSLTPROC_OPTS = --stringparam paper.type A4
L10N_REVISION = в редакции

sync:
	mkdir sync.LOCK
	svn update
	svn status -q
	@echo
	@echo Note local changes and press ENTER...
	@read
	svnversion . > HEADREV
	svn merge -r$$(cat LAST_UPDATED):$$(cat HEADREV) \
			https://svn.red-bean.com/svnbook/trunk/src/en/
	@echo
	mv HEADREV LAST_UPDATED
	rmdir sync.LOCK

dist-html-chunk:
	../tools/book-dist.py --html-chunk --name svnbook-html-chunk-ru
