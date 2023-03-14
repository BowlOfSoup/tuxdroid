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
        <script src="/data/web_interface/devel/js/ugc.js" type="text/javascript"/>
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
                <!-- SHOW GADGET TOOL BOX : EDIT THIS GADGET -->
                <xsl:call-template name="showGadgetToolBoxEditingUgc">
                    <xsl:with-param name="title" select="'Editing gadget'"/>
                    <xsl:with-param name="noTitle" select="'true'"/>
                </xsl:call-template>
                <!-- SHOW DESCRIPTION -->
                <xsl:call-template name="showDescription"/>
                <!-- EDIT UGC NAMES -->
                <xsl:call-template name="editUgcNames">
                    <xsl:with-param name="title" select="'Description'"/>
                </xsl:call-template>
                <!-- SHOW PARAMETERS -->
                <xsl:call-template name="showParameters">
                    <xsl:with-param name="title" select="'Parameters'"/>
                </xsl:call-template>
                <!-- SHOW ALERTS -->
                <xsl:call-template name="svaAlerts">
                    <xsl:with-param name="title" select="'Live with Tux Droid'"/>
                    <xsl:with-param name="onlyShow" select="'false'"/>
                    <xsl:with-param name="selectVisible" select="'false'"/>
                    <xsl:with-param name="selectActivated" select="'true'"/>
                </xsl:call-template>
                <!-- SHOW ON DEMAND -->
                <xsl:call-template name="showOnDemand">
                    <xsl:with-param name="title" select="'On demand'"/>
                    <xsl:with-param name="description" select="'This gadget will be accessible with the remote control.'"/>
                </xsl:call-template>
                <xsl:element name="br"></xsl:element>
                <!-- SHOW HELP -->
                <xsl:call-template name="showHelp">
                    <xsl:with-param name="title" select="'Help'"/>
                </xsl:call-template>
                <!-- SHOW COMMANDS -->
                <xsl:call-template name="showCommands">
                    <xsl:with-param name="title" select="'Commands'"/>
                    <xsl:with-param name="commandType" select="'ugc'"/>
                </xsl:call-template>
                <!-- SHOW MISC GADGET -->
                <xsl:call-template name="showMiscUgc">
                    <xsl:with-param name="title" select="'Miscellaneous'"/>
                </xsl:call-template>
            </div>
        </xsl:for-each>
    </body>
</html>
</xsl:template>
</xsl:stylesheet>
