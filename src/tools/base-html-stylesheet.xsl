<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version='1.0'>

  <xsl:param name="html.stylesheet">styles.css</xsl:param>
  <xsl:param name="toc.section.depth">3</xsl:param>
  <xsl:param name="annotate.toc">0</xsl:param>

  <xsl:template match="sect1" mode="toc">
    <xsl:param name="toc-context" select="."/>
    <xsl:call-template name="subtoc">
      <xsl:with-param name="toc-context" select="$toc-context"/>
      <xsl:with-param name="nodes" 
        select="sect2|refentry|bridgehead[$bridgehead.in.toc != 0]"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="sect2" mode="toc">
    <xsl:param name="toc-context" select="."/>

    <xsl:call-template name="subtoc">
      <xsl:with-param name="toc-context" select="$toc-context"/>
      <xsl:with-param name="nodes" 
        select="sect3|refentry|bridgehead[$bridgehead.in.toc != 0]"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template name="user.footer.navigation">
    <hr/>
    <div id="svn-footer">
    <p>You are reading <em>Version Control with Subversion</em>, by Ben Collins-Sussman, Brian W. Fitpatrick, and C. Michael Pilato.<br/>
       This work is licensed under the <a href="http://creativecommons.org/licenses/by/2.0/">Creative Commons Attribution License</a>.<br/>
       To submit comments, corrections, or other contributions to the text, please visit <a href="http://www.svnbook.com/">http://www.svnbook.com/</a>.</p>
    </div>
  </xsl:template>

</xsl:stylesheet>
