<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">

<xsl:include href="plugin_gadget_common.xsl"/>

<xsl:template match="/">
<html>
    <head>
        <LINK href="/data/web_interface/devel/css/common.css" rel="stylesheet" type="text/css"/>
        <LINK href="/data/web_interface/devel/css/alerts.css" rel="stylesheet" type="text/css"/>
        <LINK href="/data/web_interface/devel/css/pg_infos.css" rel="stylesheet" type="text/css"/>
        <script src="/data/web_interface/common/wiky/wiky.js" type="text/javascript"/>
        <script src="/data/web_interface/devel/js/common.js" type="text/javascript"/>
        <script src="/data/web_interface/devel/js/gadget.js" type="text/javascript"/>
        <script language="javascript"><![CDATA[]]></script>
    </head>

    <body bgcolor="#090909" onload="javascript:fillHelpBox();">
        <xsl:for-each select="root/data">
            <!-- HTML PARAM STORAGE -->
            <xsl:call-template name="htmlParamStorage"/>
            <!-- MAIN DIV FRAME -->
            <div style="position:absolute;
                        left:0px;
                        top:0px;">
                <!-- SHOW GADGET TOOL BOX -->
                <xsl:call-template name="showGadgetToolBox">
                    <xsl:with-param name="title" select="'Gadget tool box'"/>
                    <xsl:with-param name="showApply" select="'false'"/>
                    <xsl:with-param name="showGenerate" select="'true'"/>
                    <xsl:with-param name="noTitle" select="'true'"/>
                </xsl:call-template>
                <!-- SHOW DESCRIPTION -->
                <xsl:call-template name="showDescription"/>
                <!-- EDIT DESCRIPTION -->
                <xsl:call-template name="editDescription">
                    <xsl:with-param name="title" select="'Description'"/>
                </xsl:call-template>
                <!-- SELECT PARAMETERS -->
                <xsl:call-template name="selectParameters">
                    <xsl:with-param name="title" select="'Parameters'"/>
                </xsl:call-template>
                <!-- SHOW ALERTS -->
                <xsl:call-template name="svaAlerts">
                    <xsl:with-param name="title" select="'Live with Tux Droid'"/>
                    <xsl:with-param name="onlyShow" select="'false'"/>
                    <xsl:with-param name="selectVisible" select="'true'"/>
                    <xsl:with-param name="selectActivated" select="'false'"/>
                </xsl:call-template>
                <!-- SELECT ON DEMAND -->
                <xsl:call-template name="selectOnDemand">
                    <xsl:with-param name="title" select="'On demand'"/>
                    <xsl:with-param name="description" select="'This gadget will be accessible with the remote control.'"/>
                </xsl:call-template>
                <!-- EDIT HELP -->
                <xsl:call-template name="editHelp">
                    <xsl:with-param name="title" select="'Help'"/>
                </xsl:call-template>
            </div>
        </xsl:for-each>
    </body>
</html>
</xsl:template>
</xsl:stylesheet>
