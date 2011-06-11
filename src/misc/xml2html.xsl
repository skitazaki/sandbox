<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:template match="/">
  <html>
  <head>
    <meta charset="UTF-8" />
    <link rel="stylesheet" href="d45.css" />
    <title>XSL テスト</title>
  </head>
  <body>
    <div id="wrapper">
      <div id="header"><h1>XSL テスト</h1>メニュー</div>
      <div id="contents"><xsl:apply-templates /></div>
      <div id="footer">フッター</div>
    </div>
  </body>
  </html>
</xsl:template>
<xsl:template match="document">
  <div class="document">
  <h2><xsl:value-of select="@title" /></h2>
    <xsl:apply-templates />
  </div>
</xsl:template>
<xsl:template match="section">
  <div class="section">
  <h3><xsl:value-of select="@title" /></h3>
    <xsl:apply-templates />
  </div>
</xsl:template>
<xsl:template match="table">
  <table>
  <thead>
    <caption><xsl:value-of select="@title" /></caption>
  </thead>
  <tbody>
    <xsl:for-each select="row">
    <tr>
      <xsl:for-each select="cell">
        <td><xsl:value-of select="normalize-space(text())" /></td>
      </xsl:for-each>
    </tr>
    </xsl:for-each>
  </tbody>
  </table>
</xsl:template>
<xsl:template match="para">
  <p><xsl:value-of select="normalize-space(text())" /></p>
</xsl:template>
<xsl:template match="code">
  <pre>
    <xsl:if test="@language">
      <xsl:attribute name="class">
        <xsl:value-of select="@language" />
      </xsl:attribute>
    </xsl:if>
    <xsl:value-of select="text()" />
  </pre>
</xsl:template>
</xsl:stylesheet>

