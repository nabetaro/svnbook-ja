<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:fo="http://www.w3.org/1999/XSL/Format"
                version='1.0'>

  <xsl:import href="../../tools/fo-stylesheet.xsl"/>

  <xsl:param name="l10n.gentext.language" select="'zh'"/>

  <xsl:param name="hyphenate">false</xsl:param>
  <xsl:param name="section.autolabel" select="1" />
  <xsl:param name="paper.type" select="'A4'"></xsl:param>

  <!-- Chinese font related settings -->
  <xsl:param name="body.font.master">12</xsl:param>
  <xsl:param name="title.font.family">Calibri,sans-serif,SimHei</xsl:param>
  <xsl:param name="body.font.family">Cambria,Cambria Math,serif,SimSun</xsl:param>
  <xsl:param name="sans.font.family">Calibri,sans-serif,SimHei</xsl:param>
  <xsl:param name="dingbat.font.family">Cambria,Cambria Math,serif,SimSun</xsl:param>
  <xsl:param name="monospace.font.family">Courier New,monospace,FangSong</xsl:param>

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
