<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">

<xsl:include href="plugin_gadget_common.xsl"/>

<xsl:template match="/">
<html>
    <head>
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
            var knowedGadgetsFilter = "on_demand";
            var knowedGadgetsDict = null;
            var knowedPlayingGadgetUuid1 = "0";
            var knowedPlayingGadgetUuid2 = "0";
            var lastGadgetUuidInAction = "0";
            var lastGadgetNameInAction = "0";
            var lastGadgetIconInAction = "0";
            var newGadgetOnEdit = false;
            var translationStart = "";
            var translationStop = ""
            var translationDelete = "";

            function initialization()
            {
                translationStart = document.getElementById("translationStart").value;
                translationStop = document.getElementById("translationStop").value;
                translationDelete = document.getElementById("translationDelete").value;
                var configureUuid = document.getElementById("configure_uuid").value;
                if (configureUuid != "NULL")
                {
                    fillGadgetRows("all_gadgets");
                    clickMe("configureId_" + configureUuid);
                }
                else
                {
                    fillGadgetRows("on_demand");
                }
                updatePlayingGadgetUuid();
            }

            function updatePlayingGadgetUuid()
            {
                var result = requestData("/robot_content_interactions/get_current_playing_gadgets",{});
                if (result != null)
                {
                    if (!result.containsKey("uuid1"))
                    {
                        setTimeout("updatePlayingGadgetUuid()", 500);
                        return;
                    }
                }
                else
                {
                    setTimeout("updatePlayingGadgetUuid()", 500);
                    return;
                }
                var uuid1 = result.get("uuid1");
                var uuid2 = result.get("uuid2");
                if ((uuid1 != knowedPlayingGadgetUuid1) || (uuid2 != knowedPlayingGadgetUuid2))
                {
                    knowedPlayingGadgetUuid1 = uuid1;
                    knowedPlayingGadgetUuid2 = uuid2;
                    if (knowedGadgetsDict != null)
                    {
                        var gadgets = knowedGadgetsDict;
                        var gadgetsCount = parseInt(gadgets.get("data0").get("count"));
                        for (i = 0; i < gadgetsCount; i++)
                        {
                            gUuid = gadgets.get("data0").get("gadget_" + i + "_uuid");
                            ondemand = gadgets.get("data0").get("gadget_" + i + "_ondemand");
                            if (thisGadgetIsPlaying(gUuid))
                            {
                                if (ondemand == "true")
                                {
                                    setStartedGadgetButtons(gUuid);
                                }
                                else
                                {
                                    disableStartStopGadgetButtons(gUuid);
                                }
                                disableEditGadgetButtons(gUuid);
                            }
                            else
                            {
                                if (aGadgetIsPlaying())
                                {
                                    disableStartStopGadgetButtons(gUuid);
                                    enableEditGadgetButtons(gUuid);
                                }
                                else
                                {
                                    if (ondemand == "true")
                                    {
                                        enableStartStopGadgetButtons(gUuid);
                                    }
                                    else
                                    {
                                        disableStartStopGadgetButtons(gUuid);
                                    }
                                    enableEditGadgetButtons(gUuid);
                                }
                            }
                        }
                    }
                }
                setTimeout("updatePlayingGadgetUuid()", 500);
            }

            function fillGadgetRows(filter)
            {
                var gadgets = requestData("/robot_content_interactions/get_gadgets_data",{'filter' : filter});
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
                knowedPlayingGadgetUuid1 = "0";
                knowedPlayingGadgetUuid2 = "0";
                var htmlContent = "";
                var gadgetsCount = parseInt(gadgets.get("data0").get("count"));
                for (i = 0; i < gadgetsCount; i++)
                {
                    uuid = gadgets.get("data0").get("gadget_" + i + "_uuid");
                    name = gadgets.get("data0").get("gadget_" + i + "_name");
                    icon = gadgets.get("data0").get("gadget_" + i + "_icon");
                    ondemand = gadgets.get("data0").get("gadget_" + i + "_ondemand");
                    htmlContent += addGadgetRow(uuid, name, icon, ondemand);
                }
                document.getElementById("gadgetsListScrollbox").innerHTML = htmlContent;
                // Set png effet for IE6
                for (i = 0; i < gadgetsCount; i++)
                {
                    var iconId = "gadgetsRowIcon_" + gadgets.get("data0").get("gadget_" + i + "_uuid");
                    setpng(document.getElementById(iconId));
                }
                // Show correct filter radio button
                if (filter == 'all_gadgets')
                {
                    document.getElementById("gadgetsFilterRadioAll").className = "gadgetsFilterRadio gadgetsFilterRadioActivate";
                    document.getElementById("gadgetsFilterRadioOnDemand").className = "gadgetsFilterRadio gadgetsFilterRadioEnable";
                    document.getElementById("gadgetsFilterRadioAlerts").className = "gadgetsFilterRadio gadgetsFilterRadioEnable";
                }
                else if (filter == 'on_demand')
                {
                    document.getElementById("gadgetsFilterRadioAll").className = "gadgetsFilterRadio gadgetsFilterRadioEnable";
                    document.getElementById("gadgetsFilterRadioOnDemand").className = "gadgetsFilterRadio gadgetsFilterRadioActivate";
                    document.getElementById("gadgetsFilterRadioAlerts").className = "gadgetsFilterRadio gadgetsFilterRadioEnable";
                }
                else
                {
                    document.getElementById("gadgetsFilterRadioAll").className = "gadgetsFilterRadio gadgetsFilterRadioEnable";
                    document.getElementById("gadgetsFilterRadioOnDemand").className = "gadgetsFilterRadio gadgetsFilterRadioEnable";
                    document.getElementById("gadgetsFilterRadioAlerts").className = "gadgetsFilterRadio gadgetsFilterRadioActivate";
                }
                knowedGadgetsFilter = filter;
                initializeLightbox();
                // Scroll up
                var objDiv = document.getElementById("gadgetsListScrollbox");
                objDiv.scrollTop = 0;
            }

            function addGadgetRow(uuid, name, icon, ondemand)
            {
                var htmlContent = "";
                var iconId = "gadgetsRowIcon_" + uuid;
                htmlContent += '<div class="gadgetsVSpacer" style="width:10px;"></div>';
                htmlContent += '<div class="gadgetsRowIcon"><img src="' + icon + '" height="34" width="34" id="' + iconId + '"></img></div>';
                htmlContent += '<div class="gadgetsVSpacer" style="width:10px;"></div>';
                htmlContent += '<span class="gadgetsRowName">' + name + '</span>';
                htmlContent += '<div class="gadgetsVSpacer" style="width:26px;"></div>';
                if (ondemand == 'true')
                {
                    htmlContent += '<a class="gadgetsBtnTitle gadgetsBtnStartEnable" id="startId_' + uuid + '" onclick="javascript:startGadget(\''+uuid+'\');return false;" href="#">' + translationStart + '</a>';
                }
                else
                {
                    htmlContent += '<a class="gadgetsBtnTitle gadgetsBtnStartDisable" id="startId_' + uuid + '" onclick="return false;" href="#">' + translationStart + '</a>';
                }
                htmlContent += '<div class="gadgetsVSpacer" style="width:8px;"></div>';
                if (ondemand == 'true')
                {
                    htmlContent += '<a class="gadgetsBtnTitle gadgetsBtnStopEnable" id="stopId_' + uuid + '" onclick="javascript:stopGadget(\''+uuid+'\');return false;" href="#">' + translationStop + '</a>';
                }
                else
                {
                    htmlContent += '<a class="gadgetsBtnTitle gadgetsBtnStopDisable" id="stopId_' + uuid + '" onclick="javascript:return false;" href="#">' + translationStop + '</a>';
                }
                htmlContent += '<div class="gadgetsVSpacer" style="width:18px;"></div>';
                htmlContent += '<a class="gadgetsBtnNoTitle gadgetsBtnHelp" id="helpId_' + uuid + '" onclick="" href="#" name="lbOn" rel="windowGadgetHelp"></a>';
                htmlContent += '<div class="gadgetsVSpacer" style="width:8px;"></div>';
                htmlContent += '<a class="gadgetsBtnNoTitle gadgetsBtnConfigure" id="configureId_' + uuid + '" onclick="" href="#" name="lbOn" rel="windowGadgetConfiguration"></a>';
                htmlContent += '<div class="gadgetsVSpacer" style="width:8px;"></div>';
                htmlContent += '<a class="gadgetsBtnNoTitle gadgetsBtnDuplicate" id="duplicateId_' + uuid + '" onclick="javascript:setLastGadgetInAction(\''+uuid+'\');duplicateUgc();return false;" href="#"></a>';
                htmlContent += '<div class="gadgetsVSpacer" style="width:18px;"></div>';
                htmlContent += '<a class="gadgetsBtnNoTitle gadgetsBtnDelete" id="deleteId_' + uuid + '" onclick="" href="#" name="lbOn" rel="popupConfirmDelete"></a>';
                htmlContent += '<div class="frame01Sep2"></div>';
                return htmlContent;
            }

            function getGadgetNameFromUuid(uuid)
            {
                if (knowedGadgetsDict != null)
                {
                    var gadgets = knowedGadgetsDict;
                    var gadgetsCount = parseInt(gadgets.get("data0").get("count"));
                    for (i = 0; i < gadgetsCount; i++)
                    {
                        gUuid = gadgets.get("data0").get("gadget_" + i + "_uuid");
                        if (gUuid == uuid)
                        {
                            return gadgets.get("data0").get("gadget_" + i + "_name");
                        }
                    }
                }
                return "";
            }

            function getGadgetIconFromUuid(uuid)
            {
                if (knowedGadgetsDict != null)
                {
                    var gadgets = knowedGadgetsDict;
                    var gadgetsCount = parseInt(gadgets.get("data0").get("count"));
                    for (i = 0; i < gadgetsCount; i++)
                    {
                        gUuid = gadgets.get("data0").get("gadget_" + i + "_uuid");
                        if (gUuid == uuid)
                        {
                            return gadgets.get("data0").get("gadget_" + i + "_icon");
                        }
                    }
                }
                return "";
            }

            function disableAllGadgetButtons(uuid)
            {
                disableStartStopGadgetButtons(uuid);
                disableEditGadgetButtons(uuid);
            }

            function enableAllGadgetButtons(uuid)
            {
                enableStartStopGadgetButtons(uuid);
                enableEditGadgetButtons(uuid);
            }

            function disableStartStopGadgetButtons(uuid)
            {
                document.getElementById("startId_" + uuid).className = "gadgetsBtnTitle gadgetsBtnStartDisable";
                document.getElementById("stopId_" + uuid).className = "gadgetsBtnTitle gadgetsBtnStopDisable";
            }

            function enableStartStopGadgetButtons(uuid)
            {
                document.getElementById("startId_" + uuid).className = "gadgetsBtnTitle gadgetsBtnStartEnable";
                document.getElementById("stopId_" + uuid).className = "gadgetsBtnTitle gadgetsBtnStopEnable";
            }

            function setStartedGadgetButtons(uuid)
            {
                document.getElementById("startId_" + uuid).className = "gadgetsBtnTitle gadgetsBtnStartActivate";
                document.getElementById("stopId_" + uuid).className = "gadgetsBtnTitle gadgetsBtnStopEnable";
            }

            function disableEditGadgetButtons(uuid)
            {
                document.getElementById("helpId_" + uuid).className = "gadgetsBtnNoTitle gadgetsBtnHelpDisable";
                document.getElementById("configureId_" + uuid).className = "gadgetsBtnNoTitle gadgetsBtnConfigureDisable";
                document.getElementById("duplicateId_" + uuid).className = "gadgetsBtnNoTitle gadgetsBtnDuplicateDisable";
                document.getElementById("deleteId_" + uuid).className = "gadgetsBtnNoTitle gadgetsBtnDeleteDisable";
            }

            function enableEditGadgetButtons(uuid)
            {
                document.getElementById("helpId_" + uuid).className = "gadgetsBtnNoTitle gadgetsBtnHelp";
                document.getElementById("configureId_" + uuid).className = "gadgetsBtnNoTitle gadgetsBtnConfigure";
                document.getElementById("duplicateId_" + uuid).className = "gadgetsBtnNoTitle gadgetsBtnDuplicate";
                document.getElementById("deleteId_" + uuid).className = "gadgetsBtnNoTitle gadgetsBtnDelete";
            }

            function thisGadgetIsPlaying(uuid)
            {
                if ((uuid == knowedPlayingGadgetUuid1) || (uuid == knowedPlayingGadgetUuid2))
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }

            function aGadgetIsPlaying()
            {
                if ((knowedPlayingGadgetUuid1 != "0") || (knowedPlayingGadgetUuid2 != "0"))
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }

            function startGadget(uuid)
            {
                if (aGadgetIsPlaying())
                {
                    return;
                }
                getRequest("/robot_content_interactions/start_gadget_by_uuid", {'uuid' : uuid});
            }

            function stopGadget(uuid)
            {
                if (aGadgetIsPlaying())
                {
                    if (!thisGadgetIsPlaying(uuid))
                    {
                        return;
                    }
                }
                else
                {
                    return;
                }
                getRequest("/robot_content_interactions/stop_gadget", {});
            }

            function setLastGadgetInAction(uuid)
            {
                var idx = uuid.indexOf("_", 0) + 1;
                uuid = uuid.slice(idx, uuid.length);
                if (aGadgetIsPlaying())
                {
                    if (thisGadgetIsPlaying(uuid))
                    {
                        lastGadgetUuidInAction = "0";
                        lastGadgetNameInAction = "0";
                        lastGadgetIconInAction = "0";
                        return false;
                    }
                }
                lastGadgetUuidInAction = uuid;
                lastGadgetNameInAction = getGadgetNameFromUuid(uuid);
                lastGadgetIconInAction = getGadgetIconFromUuid(uuid);
                return true;
            }

            function updateWindowGadgetHelpContent(uuid)
            {
                if (!setLastGadgetInAction(uuid))
                {
                    abortNextLightbox();
                    return;
                }
                document.getElementById("windowGadgetHelpIcon").src = lastGadgetIconInAction;
                setpng(document.getElementById("windowGadgetHelpIcon"));
                document.getElementById("windowGadgetHelpTitle").firstChild.nodeValue = lastGadgetNameInAction;
                var skin = document.getElementById("skin").value;
                var language = document.getElementById("language").value;
                var src = "/wi_user_01/gadget_help?uuid=" + lastGadgetUuidInAction;
                src += "&language=" + language;
                src += "&skin=" + skin;
                src += "&rndParam=" + Math.random();
                document.getElementById("windowGadgetHelpContentIFrame").src = src;
            }

            function updateWindowGadgetConfigurationContent(uuid)
            {
                if (!setLastGadgetInAction(uuid))
                {
                    abortNextLightbox();
                    return;
                }
                document.getElementById("windowGadgetConfigurationIcon").src = lastGadgetIconInAction;
                setpng(document.getElementById("windowGadgetConfigurationIcon"));
                document.getElementById("windowGadgetConfigurationTitle").firstChild.nodeValue = lastGadgetNameInAction;
                var skin = document.getElementById("skin").value;
                var language = document.getElementById("language").value;
                var src = "/wi_user_01/gadget_configuration?uuid=" + lastGadgetUuidInAction;
                src += "&language=" + language;
                src += "&skin=" + skin;
                src += "&rndParam=" + Math.random();
                document.getElementById("windowGadgetConfigurationContentIFrame").src = src;
            }

            function updatePopupGadgetDeleteContent(uuid)
            {
                if (!setLastGadgetInAction(uuid))
                {
                    abortNextLightbox();
                    return;
                }
                document.getElementById("popup01GadgetDeleteIcon").src = lastGadgetIconInAction;
                setpng(document.getElementById("popup01GadgetDeleteIcon"));
            }

            function duplicateUgc()
            {
                if (lastGadgetUuidInAction == "0")
                {
                    return;
                }
                var language = document.getElementById("language").value;
                var args = {
                    "uuid" : lastGadgetUuidInAction,
                    "language" : language
                }
                getRequest("/wi_devel/ugc_duplicate", args);
                lastGadgetUuidInAction = "0";
                fillGadgetRows(knowedGadgetsFilter);
                // Scroll down
                var objDiv = document.getElementById("gadgetsListScrollbox");
                objDiv.scrollTop = objDiv.scrollHeight;
                // Show the configuration of the new gadget.
                if (knowedGadgetsDict != null)
                {
                    var gadgets = knowedGadgetsDict;
                    var gadgetsCount = parseInt(gadgets.get("data0").get("count"));
                    if (gadgetsCount > 0)
                    {
                        lastIdx = gadgetsCount - 1;
                        lastUuid = uuid = gadgets.get("data0").get("gadget_" + lastIdx + "_uuid");
                        newGadgetOnEdit = true;
                        clickMe("configureId_" + lastUuid);
                    }
                }
            }

            function deleteUgc()
            {
                if (lastGadgetUuidInAction == "0")
                {
                    return;
                }
                var args = {
                    "uuid" : lastGadgetUuidInAction
                }
                getRequest("/ugc_server/remove_ugc", args);
                lastGadgetUuidInAction = "0";
                fillGadgetRows(knowedGadgetsFilter);
            }

            function applyUgc()
            {
                if (window.frames.windowGadgetConfigurationContentIFrame && window.frames.windowGadgetConfigurationContentIFrame.applyGadgetConfiguration)
                {
                    window.frames.windowGadgetConfigurationContentIFrame.applyGadgetConfiguration();
                }
                if (newGadgetOnEdit)
                {
                    newGadgetOnEdit = false;
                    fillGadgetRows('all_gadgets');
                }
                else
                {
                    fillGadgetRows(knowedGadgetsFilter);
                }
            }

            function abortApplyUgc()
            {
                if (newGadgetOnEdit)
                {
                    newGadgetOnEdit = false;
                    deleteUgc();
                }
                else
                {
                    newGadgetOnEdit = false;
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
        <!-- UUID STORAGE -->
        <xsl:element name="input">
            <xsl:attribute name="type">hidden</xsl:attribute>
            <xsl:attribute name="id">configure_uuid</xsl:attribute>
            <xsl:attribute name="value">
                <xsl:value-of select="root/uuid"/>
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
        <xsl:element name="input">
            <xsl:attribute name="type">hidden</xsl:attribute>
            <xsl:attribute name="id">translationDelete</xsl:attribute>
            <xsl:attribute name="value">
                <xsl:value-of select="root/translations/delete"/>
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
                    <xsl:attribute name="class">gadgetsFilterRadio gadgetsFilterRadioEnable</xsl:attribute>
                    <xsl:attribute name="id">gadgetsFilterRadioOnDemand</xsl:attribute>
                    <xsl:attribute name="onclick">javascript:fillGadgetRows('on_demand');return false;</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/on_demand"/>
                </xsl:element>
                <div class="gadgetsVSpacer" style="width:5px;height:40px;"></div>
                <xsl:element name="a">
                    <xsl:attribute name="class">gadgetsFilterRadio gadgetsFilterRadioEnable</xsl:attribute>
                    <xsl:attribute name="id">gadgetsFilterRadioAlerts</xsl:attribute>
                    <xsl:attribute name="onclick">javascript:fillGadgetRows('alerts');return false;</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/alerts"/>
                </xsl:element>
                <div class="gadgetsVSpacer" style="width:5px;height:40px;"></div>
                <xsl:element name="a">
                    <xsl:attribute name="class">gadgetsFilterRadio gadgetsFilterRadioActivate</xsl:attribute>
                    <xsl:attribute name="id">gadgetsFilterRadioAll</xsl:attribute>
                    <xsl:attribute name="onclick">javascript:fillGadgetRows('all_gadgets'); return false;</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/all"/>
                </xsl:element>
            </div>
            <div class="frame01Middle" style="height:465px;">
                <div class="gadgetsListScrollbox" id="gadgetsListScrollbox"></div>
            </div>
            <div class="frame01Bottom"></div>
        </div>
        <!-- POPUP CONFIRM DELETE -->
        <div id="popupConfirmDelete" class="popup01Box" onfocus="updatePopupGadgetDeleteContent(arguments[0]);">
            <div class="popupFrame01Top"></div>
            <div class="popupFrame01Middle">
                <div class="popup01GadgetIcon">
                    <xsl:element name="img">
                        <xsl:attribute name="id">popup01GadgetDeleteIcon</xsl:attribute>
                        <xsl:attribute name="src">/data/web_interface/user_01/img/empty.png</xsl:attribute>
                        <xsl:attribute name="height">34</xsl:attribute>
                        <xsl:attribute name="width">34</xsl:attribute>
                    </xsl:element>
                </div>
                <span class="popup01Message"><xsl:value-of select="root/translations/popup_confirm_delete_gadget"/></span>
                <xsl:element name="a">
                    <xsl:attribute name="class">popupBtn</xsl:attribute>
                    <xsl:attribute name="name">lbOff</xsl:attribute>
                    <xsl:attribute name="rel">deactivate</xsl:attribute>
                    <xsl:attribute name="onclick">javascript:deleteUgc();return false;</xsl:attribute>
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
        <!-- POPUP NOT YET IMPLEMENTED -->
        <div id="popupNotYetImplemented" class="popup01Box" onfocus="return true;">
            <div class="popupFrame01Top"></div>
            <div class="popupFrame01Middle">
                <span class="popup01Message" style="width:409px;text-align:center;"><xsl:value-of select="root/translations/popup_not_yet_implemented"/></span>
                <xsl:element name="a">
                    <xsl:attribute name="class">popupBtn</xsl:attribute>
                    <xsl:attribute name="name">lbOff</xsl:attribute>
                    <xsl:attribute name="rel">deactivate</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/close"/>
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
        <!-- WINDOW GADGET CONFIGURATION -->
        <div id="windowGadgetConfiguration" class="window01Box" onfocus="updateWindowGadgetConfigurationContent(arguments[0]);">
            <div class="windowFrame01Top">
                <div class="windowGadgetIcon">
                    <xsl:element name="img">
                        <xsl:attribute name="id">windowGadgetConfigurationIcon</xsl:attribute>
                        <xsl:attribute name="src">/data/web_interface/user_01/img/empty.png</xsl:attribute>
                        <xsl:attribute name="height">33</xsl:attribute>
                        <xsl:attribute name="width">33</xsl:attribute>
                    </xsl:element>
                </div>
                <span class="windowTitle" id="windowGadgetConfigurationTitle"> . </span>
            </div>
            <div class="windowFrame01Middle">
                <iframe class="windowContentIFrame"
                    id="windowGadgetConfigurationContentIFrame"
                    name="windowGadgetConfigurationContentIFrame"
                    frameborder="0"
                    scrolling="no"
                    src="">
                </iframe>
                <div style="display:table;float:left;height:34px;width:300px"></div>
                <xsl:element name="a">
                    <xsl:attribute name="class">windowBtn</xsl:attribute>
                    <xsl:attribute name="name">lbOff</xsl:attribute>
                    <xsl:attribute name="onclick">javascript:applyUgc();</xsl:attribute>
                    <xsl:attribute name="rel">deactivate</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/apply"/>
                </xsl:element>
                <xsl:element name="a">
                    <xsl:attribute name="class">windowBtn</xsl:attribute>
                    <xsl:attribute name="name">lbOff</xsl:attribute>
                    <xsl:attribute name="onclick">javascript:abortApplyUgc();</xsl:attribute>
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
