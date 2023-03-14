<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">

<xsl:template match="/">
<html>
    <head>
        <title>TuxBox 2.0</title>
        <LINK href="/data/web_interface/user_01/css/menu.css" rel="stylesheet" type="text/css"/>
        <script src="/data/web_interface/user_01/js/common.js" type="text/javascript"/>
        <script src="http://www.google-analytics.com/ga.js" type="text/javascript"/>
        <script language="javascript">
        <![CDATA[
            var uuid = "NULL";

            function showContent()
            {
                var menu = document.getElementById("menu").value;
                var menuLeft = document.getElementById("menuLeft");
                var menuCenter1 = document.getElementById("menuCenter1");
                var menuCenter2 = document.getElementById("menuCenter2");
                var menuCenter3 = document.getElementById("menuCenter3");
                var menuRight = document.getElementById("menuRight");
                menuLeft.className = "menuLeftEnable";
                menuCenter1.className = "menuCenterEnable";
                menuCenter2.className = "menuCenterEnable";
                menuCenter3.className = "menuCenterEnable";
                menuRight.className = "menuRightEnable";
                var frameUrl = "";
                if (menu == "livewithtux")
                {
                    menuLeft.className = "menuLeftActivate";
                    frameUrl = "/wi_user_01/livewithtux?";
                }
                else if (menu == "gadgets")
                {
                    menuCenter1.className = "menuCenterActivate";
                    frameUrl = "/wi_user_01/gadgets?";
                }
                else if (menu == "attitunes")
                {
                    menuCenter2.className = "menuCenterActivate";
                    frameUrl = "/wi_user_01/attitunes?";
                }
                else if (menu == "tools")
                {
                    menuCenter3.className = "menuCenterActivate";
                    frameUrl = "/wi_user_01/tools?";
                }
                else if (menu == "online")
                {
                    menuRight.className = "menuRightActivate";
                    frameUrl = "/wi_user_01/online?";
                }
                else
                {
                    menuLeft.className = "menuLeftActivate";
                    frameUrl = "/wi_user_01/page_livewithtux?";
                }
                frameUrl += "uuid=" + uuid;
                frameUrl += "&language=" + document.getElementById('language').value;
                frameUrl += "&skin='" + document.getElementById('skin').value + "'";
                frameUrl += "&rndParam=" + Math.random();
                var iframe = document.getElementById('ContentIFrame');
                iframe.src = frameUrl;
            }

            function gotoMenu(menuName)
            {
                document.getElementById("menu").value = menuName;
                showContent();
            }

            function gotoGadgetsConfigure(thisUuid)
            {
                uuid = thisUuid;
                gotoMenu("gadgets");
                uuid = "NULL";
            }
        ]]>
        </script>
    </head>
    <body bgcolor="#EFEFEF" onLoad="showContent();">
        <!-- SKIN STORAGE -->
        <xsl:element name="input">
            <xsl:attribute name="type">hidden</xsl:attribute>
            <xsl:attribute name="id">skin</xsl:attribute>
            <xsl:attribute name="value">
                <xsl:value-of select="root/skin"/>
            </xsl:attribute>
        </xsl:element>

        <!-- LANGUAGE STORAGE -->
        <xsl:element name="input">
            <xsl:attribute name="type">hidden</xsl:attribute>
            <xsl:attribute name="id">language</xsl:attribute>
            <xsl:attribute name="value">
                <xsl:value-of select="root/language"/>
            </xsl:attribute>
        </xsl:element>

        <!-- CURRENT MENU STORAGE -->
        <xsl:element name="input">
            <xsl:attribute name="type">hidden</xsl:attribute>
            <xsl:attribute name="id">menu</xsl:attribute>
            <xsl:attribute name="value">
                <xsl:value-of select="root/menu"/>
            </xsl:attribute>
        </xsl:element>

        <!-- MAIN DIV FRAMES -->
        <div style="position:absolute;
                    top:0px;
                    left:50%;
                    height:65px;
                    width:855px;
                    margin-left:-428px;
                    margin-right:50px;">
            <xsl:element name="a">
                <xsl:attribute name="class">menuLeftEnable</xsl:attribute>
                <xsl:attribute name="id">menuLeft</xsl:attribute>
                <xsl:attribute name="onclick">javascript:gotoMenu('livewithtux');return false;</xsl:attribute>
                <xsl:attribute name="href"></xsl:attribute><xsl:value-of select="root/translations/live_with_tux"/>
            </xsl:element>
            <xsl:element name="a">
                <xsl:attribute name="class">menuCenterEnable</xsl:attribute>
                <xsl:attribute name="id">menuCenter1</xsl:attribute>
                <xsl:attribute name="onclick">javascript:gotoMenu('gadgets');return false;</xsl:attribute>
                <xsl:attribute name="href"></xsl:attribute><xsl:value-of select="root/translations/gadgets"/>
            </xsl:element>
            <xsl:element name="a">
                <xsl:attribute name="class">menuCenterEnable</xsl:attribute>
                <xsl:attribute name="id">menuCenter2</xsl:attribute>
                <xsl:attribute name="onclick">javascript:gotoMenu('attitunes');return false;</xsl:attribute>
                <xsl:attribute name="href"></xsl:attribute><xsl:value-of select="root/translations/attitunes"/>
            </xsl:element>
            <xsl:element name="a">
                <xsl:attribute name="class">menuCenterEnable</xsl:attribute>
                <xsl:attribute name="id">menuCenter3</xsl:attribute>
                <xsl:attribute name="onclick">javascript:gotoMenu('tools');return false;</xsl:attribute>
                <xsl:attribute name="href"></xsl:attribute><xsl:value-of select="root/translations/tools"/>
            </xsl:element>
            <xsl:element name="a">
                <xsl:attribute name="class">menuRightEnable</xsl:attribute>
                <xsl:attribute name="id">menuRight</xsl:attribute>
                <xsl:attribute name="onclick">javascript:gotoMenu('online');return false;</xsl:attribute>
                <xsl:attribute name="href"></xsl:attribute><xsl:value-of select="root/translations/online"/>
            </xsl:element>
        </div>
        <div class="ContentView" id="ContentView">
            <iframe class="ContentIFrame"
                    id="ContentIFrame"
                    name="ContentIFrame"
                    frameborder="0"
                    scrolling="no"
                    src="">
            </iframe>
           
        </div>
        <script language="javascript">
        <![CDATA[
            try
            {
                var pageTracker = _gat._getTracker("UA-10113316-1");
                pageTracker._setDomainName("none");
                pageTracker._udn="none";
                pageTracker._trackPageview();
            }
            catch(err) {}
        ]]>
        </script>
        
        <style>
        iframe.ContentIFrame{
            height: 600px;
        }
        </style>
        
    </body>
</html>
</xsl:template>
</xsl:stylesheet>
