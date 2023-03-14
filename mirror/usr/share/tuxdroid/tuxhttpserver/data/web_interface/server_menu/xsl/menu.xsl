<?xml version="1.0" encoding="ISO-8859-1"?>
<html xsl:version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">
    <body style="font-family:Arial;font-size:12pt;background-color:#FFFFFF">
        <div style="margin-bottom:1em;margin-top:1em;font-size:14pt;font-weight:bold;background-color:#CCCCCC">
            <span style="font-weight:bold"><xsl:value-of select="root/title"/></span>
        </div>
        <div style="margin-left:10px;margin-bottom:1em;font-size:12pt">
            <span style="font-weight:bold;font-style:italic">
                <xsl:value-of select="root/section"/> :
            </span>
        </div>
        <xsl:for-each select="root/items/*">
        <div style="margin-left:20px;margin-bottom:1em;margin-top:1em;font-size:10pt;background-color:#FFFFFF">
            <xsl:value-of select="position()"/>)  
            <xsl:element name="a">
                <xsl:attribute name="href">
                    <xsl:value-of select="."/>
                </xsl:attribute>
                <xsl:value-of select="name()"/>
            </xsl:element>
        </div>
        </xsl:for-each>
    </body>
</html>