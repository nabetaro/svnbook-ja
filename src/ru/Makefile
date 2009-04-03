default: html-chunk

include ../tools/Makefile.base

# Makefile.base overrides
FO_XSLTPROC_OPTS = --param fop.extensions 1 --stringparam paper.type A4
L10N_REVISION = редакции

dist-html-chunk:
	../tools/book-dist.py --html-chunk

dist-glossary: check-glossary ruGlossary.html

check-glossary: ruGlossary.xml
	xmllint --noout --nonet --postvalid --dtdvalid ../tools/dtd/docbook-4.4/docbookx.dtd $<

ruGlossary.html: ruGlossary.xml
	xsltproc --output $@ `[ -d stylesheets ] && echo stylesheets || echo ../tools`/html-stylesheet.xsl $<
