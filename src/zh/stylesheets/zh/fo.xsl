<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:fo="http://www.w3.org/1999/XSL/Format"
                version='1.0'>

  <xsl:import href="../fo.xsl"/>

  <xsl:param name="l10n.gentext.language" select="'zh'"/>

  <!-- Chinese font related settings -->
  <xsl:param name="body.font.master">12</xsl:param>

  <xsl:attribute-set name="standard.para.spacing" use-attribute-sets="normal.para.spacing">
    <xsl:attribute name="text-indent">24pt</xsl:attribute>
  </xsl:attribute-set>

  <xsl:template match="abstract/para|appendix/para|chapter/para|colophon/para|legalnotice/para|preface/para|section/para|sect1/para|sect2/para">
    <fo:block xsl:use-attribute-sets="standard.para.spacing">
      <xsl:call-template name="anchor"/>
      <xsl:apply-templates/>
    </fo:block>
  </xsl:template>

  <xsl:template match="section/para/*">
    <fo:wrapper text-indent="0pt">
      <xsl:apply-imports/>
    </fo:wrapper>
  </xsl:template>

</xsl:stylesheet>
