<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">

<xsl:include href="plugin_gadget_common.xsl"/>

<xsl:template match="/">
<html>
    <head>
        <link href="/data/web_interface/user_01/css/attitunes.css" rel="stylesheet" type="text/css"/>
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
            var knowedAttitunesFilter = "all_attitunes";
            var knowedAttitunesDict = null;
            var knowedPlayingAttituneName = "0";
            var lastAttituneNameInAction = "0";
            var lastAttituneIconInAction = "0";
            var translationStart = "";
            var translationStop = ""
            var translationDelete = "";

            function initialization()
            {
                translationStart = document.getElementById("translationStart").value;
                translationStop = document.getElementById("translationStop").value;
                translationDelete = document.getElementById("translationDelete").value;
                fillAttituneRows("all_attitunes");
                updatePlayingAttituneName();
            }

            function updatePlayingAttituneName()
            {
                var result = requestData("/attitune_manager/get_current_playing_attitune",{});
                if (result != null)
                {
                    if (!result.containsKey("name"))
                    {
                        setTimeout("updatePlayingAttituneName()", 500);
                        return;
                    }
                }
                else
                {
                    setTimeout("updatePlayingAttituneName()", 500);
                    return;
                }
                var name = result.get("name");
                if (name == "1")
                {
                    fillAttituneRows(knowedAttitunesFilter);
                }
                else if (name != knowedPlayingAttituneName)
                {
                    knowedPlayingAttituneName = name;
                    if (knowedAttitunesDict != null)
                    {
                        var attitunes = knowedAttitunesDict;
                        var attitunesCount = parseInt(attitunes.get("data0").get("count"));
                        for (i = 0; i < attitunesCount; i++)
                        {
                            name = attitunes.get("data0").get("attitune_" + i + "_name");
                            if (thisAttituneIsPlaying(name))
                            {
                                setStartedAttituneButtons(name);
                                disableEditAttituneButtons(name);
                            }
                            else
                            {
                                if (anAttituneIsPlaying())
                                {
                                    disableStartStopAttituneButtons(name);
                                    enableEditAttituneButtons(name);
                                }
                                else
                                {
                                    enableStartStopAttituneButtons(name);
                                    enableEditAttituneButtons(name);
                                }
                            }
                        }
                    }
                }
                setTimeout("updatePlayingAttituneName()", 500);
            }

            function fillAttituneRows(filter)
            {
                var attitunes = requestData("/attitune_manager/get_attitunes_data",{'filter' : filter});
                if (attitunes != null)
                {
                    if (!attitunes.containsKey("data0"))
                    {
                        return;
                    }
                    else
                    {
                        if (attitunes.get("data0").get("count") == '0')
                        {
                            return;
                        }
                    }
                }
                else
                {
                    return;
                }
                knowedAttitunesDict = attitunes;
                knowedPlayingAttituneName = "0";
                var htmlContent = "";
                var attitunesCount = parseInt(attitunes.get("data0").get("count"));
                for (i = 0; i < attitunesCount; i++)
                {
                    name = attitunes.get("data0").get("attitune_" + i + "_name");
                    icon = attitunes.get("data0").get("attitune_" + i + "_icon");
                    htmlContent += addAttituneRow(name, icon);
                }
                document.getElementById("attitunesListScrollbox").innerHTML = htmlContent;
                // Set png effet for IE6
                for (i = 0; i < attitunesCount; i++)
                {
                    var iconId = "attitunesRowIcon_" + attitunes.get("data0").get("attitune_" + i + "_name");
                    setpng(document.getElementById(iconId));
                }
                // Show correct filter radio button
                if (filter == 'all_attitunes')
                {
                    document.getElementById("attitunesFilterRadioAll").className = "attitunesFilterRadio attitunesFilterRadioActivate";
                }
                knowedAttitunesFilter = filter;
                initializeLightbox();
                // Scroll up
                var objDiv = document.getElementById("attitunesListScrollbox");
                objDiv.scrollTop = 0;
            }

            function addAttituneRow(name, icon)
            {
                var htmlContent = "";
                var iconId = "attitunesRowIcon_" + name;
                htmlContent += '<div class="attitunesVSpacer" style="width:10px;"></div>';
                htmlContent += '<div class="attitunesRowIcon"><img src="' + icon + '" height="34" width="34" id="' + iconId + '"></img></div>';
                htmlContent += '<div class="attitunesVSpacer" style="width:10px;"></div>';
                htmlContent += '<span class="attitunesRowName">' + name + '</span>';
                htmlContent += '<div class="attitunesVSpacer" style="width:26px;"></div>';
                htmlContent += '<a class="attitunesBtnTitle attitunesBtnStartEnable" id="startId_' + name + '" onclick="javascript:startAttitune(\''+name+'\');return false;" href="#">' + translationStart + '</a>';
                htmlContent += '<div class="attitunesVSpacer" style="width:8px;"></div>';
                htmlContent += '<a class="attitunesBtnTitle attitunesBtnStopEnable" id="stopId_' + name + '" onclick="javascript:stopAttitune(\''+name+'\');return false;" href="#">' + translationStop + '</a>';
                htmlContent += '<div class="attitunesVSpacer" style="width:18px;"></div>';
                htmlContent += '<a class="attitunesBtnNoTitle attitunesBtnEdit" id="editId_' + name + '" onclick="javascript:setLastAttituneInAction(\''+name+'\');editAttitune();return false;" href="#"></a>';
                htmlContent += '<div class="attitunesVSpacer" style="width:18px;"></div>';
                htmlContent += '<a class="attitunesBtnNoTitle attitunesBtnDelete" id="deleteId_' + name + '" onclick="" href="#" name="lbOn" rel="popupConfirmDelete"></a>';
                htmlContent += '<div class="frame01Sep2"></div>';
                return htmlContent;
            }

            function getAttituneIconFromName(name)
            {
                if (knowedAttitunesDict != null)
                {
                    var attitunes = knowedAttitunesDict;
                    var attitunesCount = parseInt(attitunes.get("data0").get("count"));
                    for (i = 0; i < attitunesCount; i++)
                    {
                        gName = attitunes.get("data0").get("attitune_" + i + "_name");
                        if (gName == name)
                        {
                            return attitunes.get("data0").get("attitune_" + i + "_icon");
                        }
                    }
                }
                return "";
            }

            function disableAllAttituneButtons(name)
            {
                disableStartStopAttituneButtons(name);
                disableEditAttituneButtons(name);
            }

            function enableAllAttituneButtons(name)
            {
                enableStartStopAttituneButtons(name);
                enableEditAttituneButtons(name);
            }

            function disableStartStopAttituneButtons(name)
            {
                document.getElementById("startId_" + name).className = "attitunesBtnTitle attitunesBtnStartDisable";
                document.getElementById("stopId_" + name).className = "attitunesBtnTitle attitunesBtnStopDisable";
            }

            function enableStartStopAttituneButtons(name)
            {
                document.getElementById("startId_" + name).className = "attitunesBtnTitle attitunesBtnStartEnable";
                document.getElementById("stopId_" + name).className = "attitunesBtnTitle attitunesBtnStopEnable";
            }

            function setStartedAttituneButtons(name)
            {
                document.getElementById("startId_" + name).className = "attitunesBtnTitle attitunesBtnStartActivate";
                document.getElementById("stopId_" + name).className = "attitunesBtnTitle attitunesBtnStopEnable";
            }

            function disableEditAttituneButtons(name)
            {
                document.getElementById("editId_" + name).className = "attitunesBtnNoTitle attitunesBtnEditDisable";
                document.getElementById("deleteId_" + name).className = "attitunesBtnNoTitle attitunesBtnDeleteDisable";
            }

            function enableEditAttituneButtons(name)
            {
                document.getElementById("editId_" + name).className = "attitunesBtnNoTitle attitunesBtnEdit";
                document.getElementById("deleteId_" + name).className = "attitunesBtnNoTitle attitunesBtnDelete";
            }

            function thisAttituneIsPlaying(name)
            {
                if (name == knowedPlayingAttituneName)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }

            function anAttituneIsPlaying()
            {
                if (knowedPlayingAttituneName != "0")
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }

            function startAttitune(name)
            {
                if (anAttituneIsPlaying())
                {
                    return;
                }
                getRequest("/attitune_manager/start_attitune_by_name",
                    {'name' : name, 'begin' : '0.0'});
            }

            function stopAttitune(name)
            {
                if (anAttituneIsPlaying())
                {
                    if (!thisAttituneIsPlaying(name))
                    {
                        return;
                    }
                }
                else
                {
                    return;
                }
                getRequest("/attitune_manager/stop_attitune", {});
            }

            function setLastAttituneInAction(name)
            {
                var idx = name.indexOf("_", 0) + 1;
                name = name.slice(idx, name.length);
                if (anAttituneIsPlaying())
                {
                    if (thisAttituneIsPlaying(name))
                    {
                        lastAttituneNameInAction = "0";
                        lastAttituneIconInAction = "0";
                        return false;
                    }
                }
                lastAttituneNameInAction = name;
                lastAttituneIconInAction = getAttituneIconFromName(name);
                return true;
            }

            function updatePopupAttituneDeleteContent(name)
            {
                if (!setLastAttituneInAction(name))
                {
                    abortNextLightbox();
                    return;
                }
                document.getElementById("popup01AttituneDeleteIcon").src = lastAttituneIconInAction;
                setpng(document.getElementById("popup01AttituneDeleteIcon"));
            }

            function deleteAttitune()
            {
                if (lastAttituneNameInAction == "0")
                {
                    return;
                }
                var args = {
                    "name" : lastAttituneNameInAction
                }
                getRequest("/attitune_manager/remove_attitune", args);
                lastAttituneNameInAction = "0";
                fillAttituneRows(knowedAttitunesFilter);
            }

            function editAttitune()
            {
                if (lastAttituneNameInAction == "0")
                {
                    return;
                }
                var language = document.getElementById("language").value;
                var args = {
                    "name" : lastAttituneNameInAction,
                    "language" : language
                }
                getRequest("/wi_user_01/edit_attitune", args);
                lastAttituneNameInAction = "0";
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
            <!-- FILTER BAR VIEW -->
            <div class="frame01TopSpace">
                <div class="attitunesVSpacer" style="width:35px;height:40px;"></div>
                <xsl:element name="a">
                    <xsl:attribute name="class">attitunesFilterRadio attitunesFilterRadioActivate</xsl:attribute>
                    <xsl:attribute name="id">attitunesFilterRadioAll</xsl:attribute>
                    <xsl:attribute name="onclick">javascript:fillAttituneRows('all_attitunes'); return false;</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/all"/>
                </xsl:element>
            </div>
            <div class="frame01Middle" style="height:465px;">
                <div class="attitunesListScrollbox" id="attitunesListScrollbox"></div>
            </div>
            <div class="frame01Bottom"></div>
        </div>
        <!-- POPUP CONFIRM DELETE -->
        <div id="popupConfirmDelete" class="popup01Box" onfocus="updatePopupAttituneDeleteContent(arguments[0]);">
            <div class="popupFrame01Top"></div>
            <div class="popupFrame01Middle">
                <div class="popup01GadgetIcon">
                    <xsl:element name="img">
                        <xsl:attribute name="id">popup01AttituneDeleteIcon</xsl:attribute>
                        <xsl:attribute name="src">/data/web_interface/user_01/img/empty.png</xsl:attribute>
                        <xsl:attribute name="height">34</xsl:attribute>
                        <xsl:attribute name="width">34</xsl:attribute>
                    </xsl:element>
                </div>
                <span class="popup01Message"><xsl:value-of select="root/translations/popup_confirm_delete_attitune"/></span>
                <xsl:element name="a">
                    <xsl:attribute name="class">popupBtn</xsl:attribute>
                    <xsl:attribute name="name">lbOff</xsl:attribute>
                    <xsl:attribute name="rel">deactivate</xsl:attribute>
                    <xsl:attribute name="onclick">javascript:deleteAttitune();return false;</xsl:attribute>
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
    </body>
</html>
</xsl:template>
</xsl:stylesheet>
