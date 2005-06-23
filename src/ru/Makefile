default: book-html-chunk

include ../tools/Makefile.base

# Makefile.base overrides
BOOK_FO_XSLTPROC_OPTS = --stringparam paper.type A4
L10N_REVISION = в редакции

$(BOOK_VERSION_SOURCE): book-last-updated

book-last-updated:
	@if $(SVNVERSION) . > /dev/null; then \
	  echo '<!ENTITY svn.version "$(L10N_REVISION) '`cat LAST_UPDATED`'">' \
	    > $(BOOK_VERSION_SOURCE); \
	else \
	  echo '<!ENTITY svn.version "">' > $(BOOK_VERSION_SOURCE); \
	fi

dist-html-chunk: book-last-updated
	../tools/book-dist.py --html-chunk --name svnbook-html-chunk-ru
