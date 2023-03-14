<?xml version="1.0" encoding="ISO-8859-1"?>
<html xsl:version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">
    <body style="font-family:Arial;font-size:12pt;background-color:#FFFFFF">
        <div style="margin-bottom:1em;margin-top:1em;font-size:14pt;font-weight:bold;background-color:#CCCCCC">
            <span style="font-weight:bold"><xsl:value-of select="root/title"/></span>
        </div>
        
        <div style="margin-left:0px;margin-bottom:1em;margin-top:1em;font-size:12pt;background-color:#EEEEEE">
            <span style="font-weight:bold">
                <xsl:value-of select="root/section"/>
            </span>
        </div>
        
        <div style="margin-left:20px;margin-bottom:1em;margin-top:1em;font-size:12pt;background-color:#FFFFFF;font-weight:bold">
            About this resource :
        </div>

        <div style="margin-left:20px;margin-bottom:1em;margin-top:1em;font-size:10pt;background-color:#FFFFFF">
            <xsl:value-of select="root/comment"/>
        </div>
        
        <xsl:if test="count(root/shared_methods/*)>0">
            <div style="margin-left:20px;margin-bottom:1em;margin-top:1em;font-size:12pt;background-color:#FFFFFF;font-weight:bold">
                Provided functionalities :
            </div>
        </xsl:if>
        
        <xsl:for-each select="root/shared_methods/*">
            <div style="margin-left:30px;margin-bottom:1em;margin-top:1em;font-size:10pt;background-color:#FFFFFF">
                <span style="font-weight:bold;text-decoration:underline">
                    <xsl:value-of select="position()"/>) <xsl:value-of select="name"/>
                </span>
            </div>
            <xsl:for-each select="doc/*">
                <xsl:if test="position()=1">
                    <div style="margin-left:40px;margin-bottom:1em;margin-top:1em;font-size:10pt;background-color:#FFFFFF">
                        <xsl:value-of select="."/>
                    </div>
                </xsl:if>
                <xsl:if test="position()>1">
                    <div style="margin-left:45px;margin-right:45px;font-size:10pt;background-color:#EEEEEE">
                        <xsl:value-of select="."/>
                    </div>
                </xsl:if>
            </xsl:for-each>
        </xsl:for-each>
        
        <xsl:if test="count(root/services/*)>0">
            <div style="margin-left:20px;margin-bottom:1em;margin-top:1em;font-size:12pt;background-color:#FFFFFF;font-weight:bold">
                REST Services List :
            </div>
        </xsl:if>
        
        <xsl:for-each select="root/services/*">
            <div style="margin-left:30px;margin-bottom:1em;margin-top:1em;font-size:10pt;background-color:#FFFFFF">
                <span style="font-weight:bold;text-decoration:underline">
                    <xsl:value-of select="position()"/>) <xsl:value-of select="name()"/>
                </span>
            </div>
            <div style="margin-left:40px;margin-bottom:1em;margin-top:1em;font-size:10pt;background-color:#FFFFFF">
                <xsl:value-of select="comment"/>
            </div>
            <div style="margin-left:45px;margin-right:45px;font-size:10pt;background-color:#EEEEEE">
                - Service access is exclusive : <xsl:value-of select="exclusiveExecution"/>
            </div>
            <div style="margin-left:45px;margin-right:45px;font-size:10pt;background-color:#EEEEEE">
                - Minimal client level to use this service : <xsl:value-of select="minimalUserLevel"/>
            </div>
            <div style="margin-left:45px;margin-right:45px;font-size:10pt;background-color:#EEEEEE">
                - Command prototype :
            </div>
            <div style="margin-left:45px;margin-right:45px;margin-top:1em;font-size:10pt;font-style:italic;background-color:#DDDDDD">
                <xsl:value-of select="commandPrototype"/>
            </div>
        </xsl:for-each>
        
    </body>
</html>