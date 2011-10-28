<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version='1.0'>

  <!-- Here live locale-specific customizations to the FO base stylesheet -->

  <xsl:param name="draft.mode">yes</xsl:param>
  <xsl:param name="draft.watermark.image">./book/images/draft.png</xsl:param>
  <xsl:param name="body.font.family">PMincho</xsl:param>
  <xsl:param name="monospace.font.family">Gothic</xsl:param>
  <xsl:param name="title.font.family">PGothic</xsl:param>
  <xsl:param name="paper.type">A4</xsl:param>
  <xsl:param name="img.src.path">./book/</xsl:param>
  <xsl:param name="admon.graphics.path">./book/images/</xsl:param>

</xsl:stylesheet>
