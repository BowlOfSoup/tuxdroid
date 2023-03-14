<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">

<xsl:include href="plugin_gadget_common.xsl"/>

<xsl:template match="/">
<html>
    <head>
        <link href="/data/web_interface/user_01/css/tools.css" rel="stylesheet" type="text/css"/>
        <!-- CSS HACKS FOR BROWSERS -->
        <xsl:choose>
            <!-- IE -->
            <xsl:when test="system-property('xsl:vendor') = 'Microsoft'">
                <!-- IE <= 7 -->
                <xsl:comment><![CDATA[[if lte IE 7]>
                <link href="/data/web_interface/user_01/css/popup-ie6.css" rel="stylesheet" type="text/css"/>
                <link href="/data/web_interface/user_01/css/window-ie6.css" rel="stylesheet" type="text/css"/>
                <![endif]]]></xsl:comment>
                <!-- IE >= 8 -->
                <xsl:comment><![CDATA[[if gte IE 8]>
                <link href="/data/web_interface/user_01/css/popup.css" rel="stylesheet" type="text/css"/>
                <link href="/data/web_interface/user_01/css/window.css" rel="stylesheet" type="text/css"/>
                <![endif]]]></xsl:comment>
            </xsl:when>
            <!-- FIREFOX ETC... -->
            <xsl:otherwise>
                <link href="/data/web_interface/user_01/css/popup.css" rel="stylesheet" type="text/css"/>
                <link href="/data/web_interface/user_01/css/window.css" rel="stylesheet" type="text/css"/>
            </xsl:otherwise>
        </xsl:choose>
        <script src="/data/web_interface/user_01/js/hashtable.js" type="text/javascript"/>
        <script src="/data/web_interface/user_01/js/common.js" type="text/javascript"/>
        <script type="text/javascript" src="/data/web_interface/user_01/js/prototype.js"></script>
        <script type="text/javascript" src="/data/web_interface/user_01/js/lightbox.js"></script>
        <script language="javascript">
        <![CDATA[
            var icon1AlreadyPng = false;
            var icon2AlreadyPng = false;

            function initialization()
            {
                initializeLightbox();
            }

            function startATool(uuid)
            {
                var language = document.getElementById("language").value;
                var parametersString = "language=" + language;
                var args = {
                    "command" : "run",
                    "uuid" : uuid,
                    "parameters" : parametersString
                }
                getRequest("/plugins_server/start_plugin", args);
            }

            function startAttitunesStudio()
            {
                var language = document.getElementById("language").value;
                var args = {
                    "language" : language
                }
                getRequest("/wi_user_01/start_attitunes_studio", args);
            }

            function updateWindowAbout(uuid)
            {
                if (!icon1AlreadyPng)
                {
                    icon1AlreadyPng = true;
                    setpng(document.getElementById("windowGadgetHelpIcon"));
                }
                var skin = document.getElementById("skin").value;
                var language = document.getElementById("language").value;
                var src = "/wi_user_01/gadget_help?uuid=" + uuid;
                src += "&language=" + language;
                src += "&skin=" + skin;
                src += "&rndParam=" + Math.random();
                document.getElementById("windowAboutContentIFrame").src = src;
            }

            function updateWindowGlobalSettings(uuid)
            {
                if (!icon2AlreadyPng)
                {
                    icon2AlreadyPng = true;
                    setpng(document.getElementById("windowGadgetConfigurationIcon"));
                }
                var skin = document.getElementById("skin").value;
                var language = document.getElementById("language").value;
                var src = "/wi_user_01/global_configuration?";
                src += "language=" + language;
                src += "&skin=" + skin;
                src += "&rndParam=" + Math.random();
                document.getElementById("windowGlobalSettingsContentIFrame").src = src;
            }

            function applyGlobalSettings()
            {
                if (window.frames.windowGlobalSettingsContentIFrame && window.frames.windowGlobalSettingsContentIFrame.applyGlobalConfiguration)
                {
                    window.frames.windowGlobalSettingsContentIFrame.applyGlobalConfiguration();
                }
            }
        ]]>
        </script>
    </head>

    <body bgcolor="#EFEFEF" onLoad="initialization();">
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
        <!-- SOME TRANSLATIONS FOR JS -->
        <xsl:element name="input">
            <xsl:attribute name="type">hidden</xsl:attribute>
            <xsl:attribute name="id">translationStart</xsl:attribute>
            <xsl:attribute name="value">
                <xsl:value-of select="root/translations/start"/>
            </xsl:attribute>
        </xsl:element>
        <xsl:element name="input">
            <xsl:attribute name="type">hidden</xsl:attribute>
            <xsl:attribute name="id">translationStop</xsl:attribute>
            <xsl:attribute name="value">
                <xsl:value-of select="root/translations/stop"/>
            </xsl:attribute>
        </xsl:element>
        <!-- MAIN DIV FRAME -->
        <div style="position:absolute;
                    left:0px;
                    top:0px;">
            <!-- NOTIFICATION VIEW -->
            <div class="frame01TopSpace">
            </div>
            <div class="frame01Middle">
                <!-- ATTITUNE STUDIO -->
                <xsl:if test="root/data/attitunes_studio != ''">
                    <xsl:element name="a">
                        <xsl:attribute name="class">toolsBtnTitle toolsBtnStartEnable</xsl:attribute>
                        <xsl:attribute name="id">toolsStartAttitunesStatudio</xsl:attribute>
                        <xsl:attribute name="onclick">javascript:startAttitunesStudio();return false;</xsl:attribute>
                        <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/start"/>
                    </xsl:element>
                    <span class="toolsRowName"><xsl:value-of select="root/data/attitunes_studio/name"/></span>
                    <div class="frame01Sep"></div>
                </xsl:if>
                <!-- TUX CONTROLLER -->
                <xsl:if test="root/data/tux_controller != ''">
                    <xsl:element name="a">
                        <xsl:attribute name="class">toolsBtnTitle toolsBtnStartEnable</xsl:attribute>
                        <xsl:attribute name="id">toolsStartAttitunesStudio</xsl:attribute>
                        <xsl:attribute name="onclick">javascript:startATool('<xsl:value-of select="root/data/tux_controller/uuid"/>');return false;</xsl:attribute>
                        <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/start"/>
                    </xsl:element>
                    <span class="toolsRowName"><xsl:value-of select="root/data/tux_controller/name"/></span>
                    <div class="frame01Sep"></div>
                </xsl:if>
                <!-- GLOBAL SETTINGS -->
                <xsl:element name="a">
                    <xsl:attribute name="class">toolsBtnTitle toolsBtnShowEnable</xsl:attribute>
                    <xsl:attribute name="id">none</xsl:attribute>
                    <xsl:attribute name="name">lbOn</xsl:attribute>
                    <xsl:attribute name="rel">windowGlobalSettings</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/show"/>
                </xsl:element>
                <span class="toolsRowName"><xsl:value-of select="root/translations/global_settings"/></span>
                <div class="frame01Sep"></div>
                <!-- ONLINE DOCUMENTATION -->
                <xsl:element name="a">
                    <xsl:attribute name="class">toolsBtnTitle toolsBtnShowEnable</xsl:attribute>
                    <xsl:attribute name="target">_blank</xsl:attribute>
                    <xsl:attribute name="href"><xsl:value-of select="root/translations/documentation_url"/></xsl:attribute><xsl:value-of select="root/translations/show"/>
                </xsl:element>
                <span class="toolsRowName"><xsl:value-of select="root/translations/online_documentation"/></span>
                <div class="frame01Sep"></div>
                <!-- ABOUT -->
                <xsl:if test="root/data/about != ''">
                    <xsl:element name="a">
                        <xsl:attribute name="class">toolsBtnTitle toolsBtnShowEnable</xsl:attribute>
                        <xsl:attribute name="id"><xsl:value-of select="root/data/about/uuid"/></xsl:attribute>
                        <xsl:attribute name="name">lbOn</xsl:attribute>
                        <xsl:attribute name="rel">windowAbout</xsl:attribute>
                        <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/show"/>
                    </xsl:element>
                    <span class="toolsRowName"><xsl:value-of select="root/data/about/name"/></span>
                </xsl:if>
            </div>
            <div class="frame01Bottom"></div>
        </div>

        <!-- WINDOW ABOUT -->
        <div id="windowAbout" class="window01Box" onfocus="updateWindowAbout(arguments[0]);" style="height:350px; margin-top:65px;">
            <div class="windowFrame01Top">
                <div class="windowGadgetIcon">
                    <xsl:element name="img">
                        <xsl:attribute name="id">windowGadgetHelpIcon</xsl:attribute>
                        <xsl:attribute name="src"><xsl:value-of select="root/data/about/icon"/></xsl:attribute>
                        <xsl:attribute name="height">33</xsl:attribute>
                        <xsl:attribute name="width">33</xsl:attribute>
                    </xsl:element>
                </div>
                <span class="windowTitle" id="windowGadgetHelpTitle"><xsl:value-of select="root/data/about/name"/></span>
            </div>
            <div class="windowFrame01Middle" style="height:290px;">
                <iframe class="windowContentIFrame"
                    id="windowAboutContentIFrame"
                    name="windowAboutContentIFrame"
                    frameborder="0"
                    scrolling="no"
                    style="height:240px"
                    src="">
                </iframe>
                <div style="display:table;float:left;height:34px;width:370px"></div>
                <xsl:element name="a">
                    <xsl:attribute name="class">windowBtn</xsl:attribute>
                    <xsl:attribute name="name">lbOff</xsl:attribute>
                    <xsl:attribute name="rel">deactivate</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/close"/>
                </xsl:element>
            </div>
            <div class="windowFrame01Bottom"></div>
        </div>
        <!-- GLOBAL SETTINGS -->
        <div id="windowGlobalSettings" class="window01Box" onfocus="updateWindowGlobalSettings();">
            <div class="windowFrame01Top">
                <div class="windowGadgetIcon">
                    <xsl:element name="img">
                        <xsl:attribute name="id">windowGadgetConfigurationIcon</xsl:attribute>
                        <xsl:attribute name="src"><xsl:value-of select="root/data/about/icon"/></xsl:attribute>
                        <xsl:attribute name="height">33</xsl:attribute>
                        <xsl:attribute name="width">33</xsl:attribute>
                    </xsl:element>
                </div>
                <span class="windowTitle" id="windowGadgetConfigurationTitle"><xsl:value-of select="root/translations/global_settings"/></span>
            </div>
            <div class="windowFrame01Middle">
                <iframe class="windowContentIFrame"
                    id="windowGlobalSettingsContentIFrame"
                    name="windowGlobalSettingsContentIFrame"
                    frameborder="0"
                    scrolling="no"
                    src="">
                </iframe>
                <div style="display:table;float:left;height:34px;width:300px"></div>
                <xsl:element name="a">
                    <xsl:attribute name="class">windowBtn</xsl:attribute>
                    <xsl:attribute name="name">lbOff</xsl:attribute>
                    <xsl:attribute name="onclick">javascript:applyGlobalSettings();</xsl:attribute>
                    <xsl:attribute name="rel">deactivate</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/apply"/>
                </xsl:element>
                <xsl:element name="a">
                    <xsl:attribute name="class">windowBtn</xsl:attribute>
                    <xsl:attribute name="name">lbOff</xsl:attribute>
                    <xsl:attribute name="rel">deactivate</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/cancel"/>
                </xsl:element>
            </div>
            <div class="windowFrame01Bottom"></div>
        </div>
    </body>
</html>
</xsl:template>
</xsl:stylesheet>
