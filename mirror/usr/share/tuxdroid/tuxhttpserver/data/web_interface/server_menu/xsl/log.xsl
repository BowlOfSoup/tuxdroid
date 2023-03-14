<?xml version="1.0" encoding="ISO-8859-1"?>
<html xsl:version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">
  <body style="font-family:Arial;font-size:12pt;background-color:#FFFFFF">
  
    <xsl:for-each select="root/data">
    
      <div style="margin-bottom:1em;margin-top:1em;font-size:14pt;font-weight:bold;background-color:#CCCCCC">
        <span style="font-weight:bold"><xsl:value-of select="log_file_path"/></span>
      </div>
        
        <xsl:for-each select="log_text/*">
            <div style="margin-left:60px;font-size:10pt">
                <span style="margin-left:3em;"><xsl:value-of select="."/></span>
            </div>
        </xsl:for-each>
      
    </xsl:for-each>
    
  </body>
</html>