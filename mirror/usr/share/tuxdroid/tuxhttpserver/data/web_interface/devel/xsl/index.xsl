<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">

<xsl:include href="alert.xsl"/>
<xsl:include href="parameter.xsl"/>

<xsl:template match="/">
<html>
    <head>
        <LINK href="/data/web_interface/devel/css/common.css" rel="stylesheet" type="text/css"/>
        <LINK href="/data/web_interface/devel/css/alerts.css" rel="stylesheet" type="text/css"/>
        <LINK href="/data/web_interface/devel/css/main.css" rel="stylesheet" type="text/css"/>
        <script src="/data/web_interface/devel/js/common.js" type="text/javascript"/>
        <script language="javascript">
        <![CDATA[
            function changeContent()
            {
                if (window.frames['elementIFrameContent'].document != null)
                {
                    document.getElementById('elementDivContent').innerHTML = window.frames['elementIFrameContent'].document.getElementsByTagName('html')[0].innerHTML;
                }
            }

            var elementsCount;
            var currentThumb;
            var thumbM1;
            var thumbM2;
            var thumbP1;
            var thumbP2;

            function getNewIdx(idx, rel)
            {
                if (rel == 0)
                {
                    return idx;
                }
                if (rel > 1)
                {
                    loopMax = rel;
                    rel = 1;
                }
                else
                {
                    loopMax = 1;
                }
                for (var i = 0; i < loopMax; i++)
                {
                    idx += rel;
                    if (idx == 0)
                    {
                        idx = elementsCount;
                    }
                    else if (idx > elementsCount)
                    {
                        idx = 1;
                    }
                }
                return idx;
            }

            function showThumbnails(relIdx)
            {
                currentThumb = getNewIdx(currentThumb, relIdx);
                thumbM1 = getNewIdx(thumbM1, relIdx);
                thumbM2 = getNewIdx(thumbM2, relIdx);
                thumbP1 = getNewIdx(thumbP1, relIdx);
                thumbP2 = getNewIdx(thumbP2, relIdx);
                document.getElementById('mainThumbIcon').src = document.getElementById('element_' + currentThumb + '_icon').value;
                setpng(document.getElementById('mainThumbIcon'));
                document.getElementById('mainThumbName').innerHTML = document.getElementById('element_' + currentThumb + '_name').value;
                document.getElementById('m2ThumbIcon').src = document.getElementById('element_' + thumbM2 + '_icon').value;
                setpng(document.getElementById('m2ThumbIcon'));
                document.getElementById('m1ThumbIcon').src = document.getElementById('element_' + thumbM1 + '_icon').value;
                setpng(document.getElementById('m1ThumbIcon'));
                document.getElementById('p2ThumbIcon').src = document.getElementById('element_' + thumbP2 + '_icon').value;
                setpng(document.getElementById('p2ThumbIcon'));
                document.getElementById('p1ThumbIcon').src = document.getElementById('element_' + thumbP1 + '_icon').value;
                setpng(document.getElementById('p1ThumbIcon'));
                var menu = document.getElementById("menu").value;
                var frameUrl = "";
                if (menu == "plugins")
                {
                    frameUrl = "/wi_devel/show_plugin?uuid=";
                }
                else if (menu == "gadgets")
                {
                    frameUrl = "/wi_devel/show_gadget?uuid=";
                }
                else
                {
                    frameUrl = "/wi_devel/show_ugc?uuid=";
                }
                frameUrl += document.getElementById('element_' + currentThumb + '_uuid').value;
                frameUrl += "&language=" + document.getElementById('language').value;
                frameUrl += "&skin='" + document.getElementById('skin').value + "'";
                frameUrl += "&rndParam=" + Math.random();
                var iframe = document.getElementById('elementIFrameContent');
                iframe.src = frameUrl;
            }

            function initThumbnails()
            {
                elementsCount = parseInt(document.getElementById('elementsCount').value);

                currentThumb = 1;
                if (elementsCount == 1)
                {
                    thumbM1 = 1;
                    thumbM2 = 1;
                    thumbP1 = 1;
                    thumbP2 = 1;
                }
                else if (elementsCount == 2)
                {
                    thumbM1 = 2;
                    thumbM2 = 1;
                    thumbP1 = 2;
                    thumbP2 = 1;
                }
                else
                {
                    thumbM1 = elementsCount;
                    thumbM2 = elementsCount - 1;
                    thumbP1 = 2;
                    thumbP2 = 3;
                }

                var firstUuid = document.getElementById('firstUuid').value;
                if (firstUuid != 'NULL')
                {
                    for (var i = 1; i <= elementsCount; i++)
                    {
                        var uuid = document.getElementById('element_' + i + '_uuid').value;
                        if (uuid == firstUuid)
                        {
                            showThumbnails(i - 1);
                            break;
                        }
                    }
                }
                else
                {
                    showThumbnails(0);
                }
            }

            function gotoMenu(menuName)
            {
                var skin = document.getElementById("skin").value;
                var language = document.getElementById("language").value;
                var args = {
                    "menu" : menuName,
                    "skin" : skin,
                    "language" : language,
                    "firstUuid" : "NULL",
                    "frameUrl" : Math.random()
                }
                gotoLocation("/devel/index", args);
            }
        ]]>
        </script>
    </head>
    <body bgcolor="#090909" onLoad="initThumbnails();">
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

        <!-- FAKE IMAGE FOR PLUGIN COMMANDS -->
        <xsl:element name="img">
            <xsl:attribute name="id">fakeImage</xsl:attribute>
            <xsl:attribute name="src"></xsl:attribute>
            <xsl:attribute name="width">0</xsl:attribute>
            <xsl:attribute name="height">0</xsl:attribute>
        </xsl:element>

        <!-- CURRENT MENU STORAGE -->
        <xsl:element name="input">
            <xsl:attribute name="type">hidden</xsl:attribute>
            <xsl:attribute name="id">menu</xsl:attribute>
            <xsl:attribute name="value">
                <xsl:value-of select="root/menu"/>
            </xsl:attribute>
        </xsl:element>

        <!-- FIRST UUID STORAGE -->
        <xsl:element name="input">
            <xsl:attribute name="type">hidden</xsl:attribute>
            <xsl:attribute name="id">firstUuid</xsl:attribute>
            <xsl:attribute name="value">
                <xsl:value-of select="root/firstUuid"/>
            </xsl:attribute>
        </xsl:element>

        <!-- GET ELEMENTS (PLUGIN/GADGET) INFORMATIONS -->
        <!-- ELEMENTS COUNT -->
        <xsl:element name="input">
            <xsl:attribute name="type">hidden</xsl:attribute>
            <xsl:attribute name="id">elementsCount</xsl:attribute>
            <xsl:attribute name="value"><xsl:value-of select="count(root/data/elements/*)"/></xsl:attribute>
        </xsl:element>
        <xsl:for-each select="root/data/elements/*">
            <!-- UUID -->
            <xsl:element name="input">
                <xsl:attribute name="type">hidden</xsl:attribute>
                <xsl:attribute name="id">element_<xsl:value-of select="position()"/>_uuid</xsl:attribute>
                <xsl:attribute name="value"><xsl:value-of select="uuid"/></xsl:attribute>
            </xsl:element>
            <!-- ICON -->
            <xsl:element name="input">
                <xsl:attribute name="type">hidden</xsl:attribute>
                <xsl:attribute name="id">element_<xsl:value-of select="position()"/>_icon</xsl:attribute>
                <xsl:attribute name="value"><xsl:value-of select="iconFile"/></xsl:attribute>
            </xsl:element>
            <!-- NAME -->
            <xsl:element name="input">
                <xsl:attribute name="type">hidden</xsl:attribute>
                <xsl:attribute name="id">element_<xsl:value-of select="position()"/>_name</xsl:attribute>
                <xsl:attribute name="value"><xsl:value-of select="translatedName"/></xsl:attribute>
            </xsl:element>
        </xsl:for-each>

        <!-- MAIN DIV FRAMES -->
        <div style="position:absolute;
                    left:0px;
                    top:10px;
                    height:70px;
                    width:700px;">
            <xsl:element name="a">
                <xsl:attribute name="class">topButton</xsl:attribute>
                <xsl:if test="root/menu = 'plugins'">
                    <xsl:attribute name="class">topButtonActive</xsl:attribute>
                </xsl:if>
                <xsl:attribute name="onclick">javascript:gotoMenu('plugins');return false;</xsl:attribute>
                <xsl:attribute name="href"></xsl:attribute>Plugins
            </xsl:element>
            <xsl:element name="a">
                <xsl:attribute name="class">topButton</xsl:attribute>
                <xsl:if test="root/menu = 'gadgets'">
                    <xsl:attribute name="class">topButtonActive</xsl:attribute>
                </xsl:if>
                <xsl:attribute name="onclick">javascript:gotoMenu('gadgets');return false;</xsl:attribute>
                <xsl:attribute name="href"></xsl:attribute>Gadgets
            </xsl:element>
            <xsl:element name="a">
                <xsl:attribute name="class">topButton</xsl:attribute>
                <xsl:if test="root/menu = 'ugcs'">
                    <xsl:attribute name="class">topButtonActive</xsl:attribute>
                </xsl:if>
                <xsl:attribute name="onclick">javascript:gotoMenu('ugcs');return false;</xsl:attribute>
                <xsl:attribute name="href"></xsl:attribute>UGC
            </xsl:element>
            <xsl:element name="a">
                <xsl:attribute name="class">topButton</xsl:attribute>
                <xsl:attribute name="onclick">javascript:return false;</xsl:attribute>
                <xsl:attribute name="href"></xsl:attribute>Empty
            </xsl:element>
            <xsl:element name="a">
                <xsl:attribute name="class">topButton</xsl:attribute>
                <xsl:attribute name="onclick">javascript:return false;</xsl:attribute>
                <xsl:attribute name="href"></xsl:attribute>Empty
            </xsl:element>
        </div>
        <div style="position:absolute;
                    left:0px;
                    top:100px;">
            <div class="thumbnailsBg">
                <xsl:element name="img">
                    <xsl:attribute name="id">m2ThumbIcon</xsl:attribute>
                    <xsl:attribute name="class">m2ThumbIcon</xsl:attribute>
                    <xsl:attribute name="src"></xsl:attribute>
                    <xsl:attribute name="height">48</xsl:attribute>
                    <xsl:attribute name="width">48</xsl:attribute>
                </xsl:element>
                <xsl:element name="img">
                    <xsl:attribute name="id">m1ThumbIcon</xsl:attribute>
                    <xsl:attribute name="class">m1ThumbIcon</xsl:attribute>
                    <xsl:attribute name="src"></xsl:attribute>
                    <xsl:attribute name="height">48</xsl:attribute>
                    <xsl:attribute name="width">48</xsl:attribute>
                </xsl:element>
                <xsl:element name="img">
                    <xsl:attribute name="id">mainThumbIcon</xsl:attribute>
                    <xsl:attribute name="class">mainThumbIcon</xsl:attribute>
                    <xsl:attribute name="src"></xsl:attribute>
                    <xsl:attribute name="height">48</xsl:attribute>
                    <xsl:attribute name="width">48</xsl:attribute>
                </xsl:element>
                <span class="mainThumbName" id="mainThumbName"></span>
                <xsl:element name="img">
                    <xsl:attribute name="id">p1ThumbIcon</xsl:attribute>
                    <xsl:attribute name="class">p1ThumbIcon</xsl:attribute>
                    <xsl:attribute name="src"></xsl:attribute>
                    <xsl:attribute name="height">48</xsl:attribute>
                    <xsl:attribute name="width">48</xsl:attribute>
                </xsl:element>
                <xsl:element name="img">
                    <xsl:attribute name="id">p2ThumbIcon</xsl:attribute>
                    <xsl:attribute name="class">p2ThumbIcon</xsl:attribute>
                    <xsl:attribute name="src"></xsl:attribute>
                    <xsl:attribute name="height">48</xsl:attribute>
                    <xsl:attribute name="width">48</xsl:attribute>
                </xsl:element>
                <xsl:element name="a">
                    <xsl:attribute name="class">tbButtonPreview</xsl:attribute>
                    <xsl:attribute name="onclick">javascript:showThumbnails(-1);return false;</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute>
                </xsl:element>
                <xsl:element name="a">
                    <xsl:attribute name="class">tbButtonNext</xsl:attribute>
                    <xsl:attribute name="onclick">javascript:showThumbnails(1);return false;</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute>
                </xsl:element>
            </div>
            <div class="tbElementContent" id="elementDivContent">
                <iframe class="tbElementView"
                        id="elementIFrameContent"
                        name="elementIFrameContent"
                        frameborder="0"
                        scrolling="no"
                        width="100%"
                        height="3000"
                        src="">
                </iframe>
            </div>
        </div>
    </body>
</html>
</xsl:template>
</xsl:stylesheet>