<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">

<xsl:include href="plugin_gadget_common.xsl"/>

<xsl:template match="/">
<html>
    <head>
        <link href="/data/web_interface/user_01/css/online.css" rel="stylesheet" type="text/css"/>
        <link href="/data/web_interface/user_01/css/gadgets.css" rel="stylesheet" type="text/css"/>
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
            var lastGadgetSymbolicNameInAction = "0";
            var lastGadgetNameInAction = "0";
            var lastGadgetIconInAction = "0";
            var knowedGadgetsDict = null;
            var knowedGadgetsFilter = "all_gadgets";

            function initialization()
            {
                fillGadgetRows("all_gadgets");
            }

            function fillGadgetRows(filter)
            {
                var language = document.getElementById("language").value;
                var gadgets = requestData("/gadgets_server/get_online_gadgets_data",
                    {
                        'filter' : filter,
                        'language' : language
                    });
                if (gadgets != null)
                {
                    if (!gadgets.containsKey("data0"))
                    {
                        return;
                    }
                }
                else
                {
                    return;
                }
                knowedGadgetsDict = gadgets;
                var htmlContent = "";
                var gadgetsCount = parseInt(gadgets.get("data0").get("gadgets_count"));
                for (i = 0; i < gadgetsCount; i++)
                {
                    symbolicName = gadgets.get("data0").get("gadget_" + i + "_symbolicName");
                    name = gadgets.get("data0").get("gadget_" + i + "_name");
                    icon = gadgets.get("data0").get("gadget_" + i + "_iconFile");
                    isAnUpdate = gadgets.get("data0").get("gadget_" + i + "_isAnUpdate");
                    htmlContent += addGadgetRow(symbolicName, name, icon, isAnUpdate);
                }
                document.getElementById("gadgetsListScrollbox").innerHTML = htmlContent;
                // Set png effet for IE6
                for (i = 0; i < gadgetsCount; i++)
                {
                    var iconId = "gadgetsRowIcon_" + gadgets.get("data0").get("gadget_" + i + "_symbolicName");
                    setpng(document.getElementById(iconId));
                }
                // Show correct filter radio button
                if (filter == 'all_gadgets')
                {
                    document.getElementById("gadgetsFilterRadioAll").className = "gadgetsFilterRadio gadgetsFilterRadioActivate";
                }
                else
                {
                    document.getElementById("gadgetsFilterRadioAll").className = "gadgetsFilterRadio gadgetsFilterRadioActivate";
                }
                knowedGadgetsFilter = filter;
                initializeLightbox();
                // Scroll up
                var objDiv = document.getElementById("gadgetsListScrollbox");
                objDiv.scrollTop = 0;
            }

            function addGadgetRow(symbolicName, name, icon, isAnUpdate)
            {
                var htmlContent = "";
                var iconId = "gadgetsRowIcon_" + symbolicName;
                htmlContent += '<div class="gadgetsVSpacer" style="width:10px;"></div>';
                htmlContent += '<div class="gadgetsRowIcon"><img src="' + icon + '" height="34" width="34" id="' + iconId + '"></img></div>';
                htmlContent += '<div class="gadgetsVSpacer" style="width:10px;"></div>';
                htmlContent += '<span class="gadgetsRowName2">' + name + '</span>';
                htmlContent += '<div class="gadgetsVSpacer" style="width:18px;"></div>';
                htmlContent += '<a class="gadgetsBtnNoTitle gadgetsBtnHelp" id="helpId_' + symbolicName + '" onclick="" href="#" name="lbOn" rel="windowGadgetHelp"></a>';
                htmlContent += '<div class="gadgetsVSpacer" style="width:8px;"></div>';
                if (isAnUpdate == "True")
                {
                    htmlContent += '<a class="gadgetsBtnNoTitle gadgetsBtnUpdate" id="downloadId_' + symbolicName + '" onclick="" href="#" name="lbOn" rel="popupConfirmUpdate"></a>';
                }
                else
                {
                    htmlContent += '<a class="gadgetsBtnNoTitle gadgetsBtnDownload" id="downloadId_' + symbolicName + '" onclick="" href="#" name="lbOn" rel="popupConfirmDownload"></a>';
                }
                htmlContent += '<div class="frame01Sep2"></div>';
                return htmlContent;
            }

            function getGadgetNameFromSymbolicName(symbolicName)
            {
                if (knowedGadgetsDict != null)
                {
                    var gadgets = knowedGadgetsDict;
                    var gadgetsCount = parseInt(gadgets.get("data0").get("gadgets_count"));
                    for (i = 0; i < gadgetsCount; i++)
                    {
                        gSymbolicName = gadgets.get("data0").get("gadget_" + i + "_symbolicName");
                        if (gSymbolicName == symbolicName)
                        {
                            return gadgets.get("data0").get("gadget_" + i + "_name");
                        }
                    }
                }
                return "";
            }

            function getGadgetIconFromSymbolicName(symbolicName)
            {
                if (knowedGadgetsDict != null)
                {
                    var gadgets = knowedGadgetsDict;
                    var gadgetsCount = parseInt(gadgets.get("data0").get("gadgets_count"));
                    for (i = 0; i < gadgetsCount; i++)
                    {
                        gSymbolicName = gadgets.get("data0").get("gadget_" + i + "_symbolicName");
                        if (gSymbolicName == symbolicName)
                        {
                            return gadgets.get("data0").get("gadget_" + i + "_iconFile");
                        }
                    }
                }
                return "";
            }

            function getGadgetScgFromSymbolicName(symbolicName)
            {
                if (knowedGadgetsDict != null)
                {
                    var gadgets = knowedGadgetsDict;
                    var gadgetsCount = parseInt(gadgets.get("data0").get("gadgets_count"));
                    for (i = 0; i < gadgetsCount; i++)
                    {
                        gSymbolicName = gadgets.get("data0").get("gadget_" + i + "_symbolicName");
                        if (gSymbolicName == symbolicName)
                        {
                            return gadgets.get("data0").get("gadget_" + i + "_scgFile");
                        }
                    }
                }
                return "";
            }

            function setLastGadgetInAction(symbolicName)
            {
                var idx = symbolicName.indexOf("_", 0) + 1;
                symbolicName = symbolicName.slice(idx, symbolicName.length);
                lastGadgetSymbolicNameInAction = symbolicName;
                lastGadgetNameInAction = getGadgetNameFromSymbolicName(symbolicName);
                lastGadgetIconInAction = getGadgetIconFromSymbolicName(symbolicName);
                return true;
            }

            function updateWindowGadgetHelpContent(symbolicName)
            {
                if (!setLastGadgetInAction(symbolicName))
                {
                    abortNextLightbox();
                    return;
                }
                document.getElementById("windowGadgetHelpIcon").src = lastGadgetIconInAction;
                setpng(document.getElementById("windowGadgetHelpIcon"));
                document.getElementById("windowGadgetHelpTitle").firstChild.nodeValue = lastGadgetNameInAction;
                var skin = document.getElementById("skin").value;
                var language = document.getElementById("language").value;
                var src = "/wi_user_01/online_gadget_help?symbolic_name=" + lastGadgetSymbolicNameInAction;
                src += "&language=" + language;
                src += "&skin=" + skin;
                src += "&rndParam=" + Math.random();
                document.getElementById("windowGadgetHelpContentIFrame").src = src;
            }

            function updatePopupGadgetDownloadContent(symbolicName)
            {
                if (!setLastGadgetInAction(symbolicName))
                {
                    abortNextLightbox();
                    return;
                }
                document.getElementById("popup01GadgetDownloadIcon").src = lastGadgetIconInAction;
                setpng(document.getElementById("popup01GadgetDownloadIcon"));
            }

            function updatePopupGadgetUpdateContent(symbolicName)
            {
                if (!setLastGadgetInAction(symbolicName))
                {
                    abortNextLightbox();
                    return;
                }
                document.getElementById("popup01GadgetUpdateIcon").src = lastGadgetIconInAction;
                setpng(document.getElementById("popup01GadgetUpdateIcon"));
            }

            function downloadGadget()
            {
                if (lastGadgetSymbolicNameInAction == "0")
                {
                    return;
                }
                var scgFile = getGadgetScgFromSymbolicName(lastGadgetSymbolicNameInAction);
                var args = {
                    "path" : scgFile
                }
                getRequest("/gadgets_server/insert_gadget", args);
                symbolicName = lastGadgetSymbolicNameInAction;
                lastGadgetSymbolicNameInAction = "0";
                var idx = symbolicName.indexOf("_", 0) + 1;
                symbolicName = symbolicName.slice(idx, symbolicName.length);
                if (window.top.gotoGadgetsConfigure)
                {
                    window.top.gotoGadgetsConfigure(symbolicName);
                }
            }

            function updateGadget()
            {
                if (lastGadgetSymbolicNameInAction == "0")
                {
                    return;
                }
                var scgFile = getGadgetScgFromSymbolicName(lastGadgetSymbolicNameInAction);
                var args = {
                    "path" : scgFile
                }
                getRequest("/gadgets_server/insert_gadget", args);
                lastGadgetSymbolicNameInAction = "0";
                fillGadgetRows(knowedGadgetsFilter);
                setTimeout('clickMe("popupUpdatedShow")', 500);
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
                <div class="gadgetsVSpacer" style="width:35px;height:40px;"></div>
                <xsl:element name="a">
                    <xsl:attribute name="class">gadgetsFilterRadio gadgetsFilterRadioActivate</xsl:attribute>
                    <xsl:attribute name="id">gadgetsFilterRadioAll</xsl:attribute>
                    <xsl:attribute name="onclick">javascript:fillGadgetRows('all_gadgets'); return false;</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/all"/>
                </xsl:element>
            </div>
            <div class="frame01Middle" style="height:465px;">
                <div class="gadgetsListScrollbox2" id="gadgetsListScrollbox"></div>
            </div>
            <div class="frame01Bottom2"></div>
        </div>
        <!-- POPUP CONFIRM DOWNLOAD -->
        <div id="popupConfirmDownload" class="popup01Box" onfocus="updatePopupGadgetDownloadContent(arguments[0]);">
            <div class="popupFrame01Top"></div>
            <div class="popupFrame01Middle">
                <div class="popup01GadgetIcon">
                    <xsl:element name="img">
                        <xsl:attribute name="id">popup01GadgetDownloadIcon</xsl:attribute>
                        <xsl:attribute name="src">/data/web_interface/user_01/img/empty.png</xsl:attribute>
                        <xsl:attribute name="height">34</xsl:attribute>
                        <xsl:attribute name="width">34</xsl:attribute>
                    </xsl:element>
                </div>
                <span class="popup01Message"><xsl:value-of select="root/translations/popup_confirm_download_gadget"/></span>
                <xsl:element name="a">
                    <xsl:attribute name="class">popupBtn</xsl:attribute>
                    <xsl:attribute name="name">lbOff</xsl:attribute>
                    <xsl:attribute name="rel">deactivate</xsl:attribute>
                    <xsl:attribute name="onclick">javascript:downloadGadget();return false;</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/yes"/>
                </xsl:element>
                <xsl:element name="a">
                    <xsl:attribute name="class">popupBtn</xsl:attribute>
                    <xsl:attribute name="name">lbOff</xsl:attribute>
                    <xsl:attribute name="id">closeLightbox</xsl:attribute>
                    <xsl:attribute name="rel">deactivate</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/no"/>
                </xsl:element>
            </div>
            <div class="popupFrame01Bottom"></div>
        </div>
        <!-- POPUP CONFIRM UPDATE -->
        <div id="popupConfirmUpdate" class="popup01Box" onfocus="updatePopupGadgetUpdateContent(arguments[0]);">
            <div class="popupFrame01Top"></div>
            <div class="popupFrame01Middle">
                <div class="popup01GadgetIcon">
                    <xsl:element name="img">
                        <xsl:attribute name="id">popup01GadgetUpdateIcon</xsl:attribute>
                        <xsl:attribute name="src">/data/web_interface/user_01/img/empty.png</xsl:attribute>
                        <xsl:attribute name="height">34</xsl:attribute>
                        <xsl:attribute name="width">34</xsl:attribute>
                    </xsl:element>
                </div>
                <span class="popup01Message"><xsl:value-of select="root/translations/popup_confirm_update_gadget"/></span>
                <xsl:element name="a">
                    <xsl:attribute name="class">popupBtn</xsl:attribute>
                    <xsl:attribute name="name">lbOff</xsl:attribute>
                    <xsl:attribute name="rel">deactivate</xsl:attribute>
                    <xsl:attribute name="onclick">javascript:updateGadget();return false;</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/yes"/>
                </xsl:element>
                <xsl:element name="a">
                    <xsl:attribute name="class">popupBtn</xsl:attribute>
                    <xsl:attribute name="name">lbOff</xsl:attribute>
                    <xsl:attribute name="id">closeLightbox</xsl:attribute>
                    <xsl:attribute name="rel">deactivate</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/no"/>
                </xsl:element>
            </div>
            <div class="popupFrame01Bottom"></div>
        </div>
        <!-- POPUP GADGET IS UP TO DATE -->
        <div id="popupGadgetUpToDate" class="popup01Box" onfocus="return true;">
            <div class="popupFrame01Top"></div>
            <div class="popupFrame01Middle">
                <span class="popup01Message" style="width:409px;text-align:center;"><xsl:value-of select="root/translations/popup_gadget_has_been_updated"/></span>
                <xsl:element name="a">
                    <xsl:attribute name="class">popupBtn</xsl:attribute>
                    <xsl:attribute name="name">lbOff</xsl:attribute>
                    <xsl:attribute name="rel">deactivate</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/close"/>
                </xsl:element>
                <xsl:element name="a">
                    <xsl:attribute name="id">popupUpdatedShow</xsl:attribute>
                    <xsl:attribute name="name">lbOn</xsl:attribute>
                    <xsl:attribute name="rel">popupGadgetUpToDate</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute>
                </xsl:element>
            </div>
            <div class="popupFrame01Bottom"></div>
        </div>
        <!-- WINDOW GADGET HELP -->
        <div id="windowGadgetHelp" class="window01Box" onfocus="updateWindowGadgetHelpContent(arguments[0]);" style="height:350px; margin-top:65px;">
            <div class="windowFrame01Top">
                <div class="windowGadgetIcon">
                    <xsl:element name="img">
                        <xsl:attribute name="id">windowGadgetHelpIcon</xsl:attribute>
                        <xsl:attribute name="src">/data/web_interface/user_01/img/empty.png</xsl:attribute>
                        <xsl:attribute name="height">33</xsl:attribute>
                        <xsl:attribute name="width">33</xsl:attribute>
                    </xsl:element>
                </div>
                <span class="windowTitle" id="windowGadgetHelpTitle"> . </span>
            </div>
            <div class="windowFrame01Middle" style="height:290px;">
                <iframe class="windowContentIFrame"
                    id="windowGadgetHelpContentIFrame"
                    name="windowGadgetHelpContentIFrame"
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
    </body>
</html>
</xsl:template>
</xsl:stylesheet>
