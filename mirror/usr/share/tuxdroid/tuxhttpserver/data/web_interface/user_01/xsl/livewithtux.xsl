<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">

<xsl:include href="plugin_gadget_common.xsl"/>

<xsl:template match="/">
<html>
    <head>
        <LINK href="/data/web_interface/user_01/css/livewithtux.css" rel="stylesheet" type="text/css"/>
        <script src="/data/web_interface/user_01/js/hashtable.js" type="text/javascript"/>
        <script src="/data/web_interface/user_01/js/common.js" type="text/javascript"/>
        <script type="text/javascript" src="/data/web_interface/user_01/js/prototype.js"></script>
        <script type="text/javascript" src="/data/web_interface/user_01/js/lightbox.js"></script>
        <script language="javascript">
        <![CDATA[
            var knowedDongleState = "off";
            var knowedRadioState = "off";
            var knowedBatteryState = "nodongle";
            var knowedSoundState = "off";
            var knowedGadget01Name = null;
            var knowedGadget01Icon = null;
            var knowedGadget01Uuid = null;
            var knowedGadget02Name = null;
            var knowedGadget02Icon = null;
            var knowedGadget02Uuid = null;
            var knowedGadget03Name = null;
            var knowedGadget03Icon = null;
            var knowedGadget03Uuid = null;
            var knowedGadget04Name = null;
            var knowedGadget04Icon = null;
            var knowedGadget04Uuid = null;
            var knowedGadget04Description = null;
            var knowedGadget05Name = null;
            var knowedGadget05Icon = null;
            var knowedGadget05Uuid = null;
            var knowedGadget06Name = null;
            var knowedGadget06Icon = null;
            var knowedGadget06Uuid = null;
            var knowedGadget07Name = null;
            var knowedGadget07Icon = null;
            var knowedGadget07Uuid = null;
            var knowedAlertGadgetName = null;
            var knowedAlertGadgetIcon = null;
            var knowedAlertGadgetUuid = null;
            var emptyGadgetIcon = "/data/web_interface/user_01/img/empty.png";
            var emptyGadgetName = " ";
            var knowedGadgetMessagesDict = null;

            function updateStates()
            {
                var dongleState = "off";
                var radioState = "off";
                var batteryState = "0";
                var soundState = "off";

                var states = requestData("/wi_user_01/get_states", {});
                if (states != null)
                {
                    if (!states.containsKey("data0"))
                    {
                        setTimeout("updateStates();", 500);
                        return;
                    }
                    dongleState = states.get("data0").get("dongleState");
                    radioState = states.get("data0").get("radioState");
                    batteryState = states.get("data0").get("batteryState");
                    soundState = states.get("data0").get("soundState");
                    var gadgets = null;
                    try
                    {
                        gadgets = states.get("gadgets");
                    }
                    catch (e)
                    {
                        gadgets = null;
                    }
                    if (gadgets != null)
                    {
                        if (gadgets.containsKey("gadget_04_uuid"))
                        {
                            updateCurrentGadget(gadgets.get("gadget_04_uuid"),
                                gadgets.get("gadget_04_name"),
                                gadgets.get("gadget_04_icon"),
                                gadgets.get("gadget_04_description"));
                            updateGadgetThumb01(gadgets.get("gadget_01_uuid"),
                                gadgets.get("gadget_01_name"),
                                gadgets.get("gadget_01_icon"));
                            updateGadgetThumb02(gadgets.get("gadget_02_uuid"),
                                gadgets.get("gadget_02_name"),
                                gadgets.get("gadget_02_icon"));
                            updateGadgetThumb03(gadgets.get("gadget_03_uuid"),
                                gadgets.get("gadget_03_name"),
                                gadgets.get("gadget_03_icon"));
                            updateGadgetThumb05(gadgets.get("gadget_05_uuid"),
                                gadgets.get("gadget_05_name"),
                                gadgets.get("gadget_05_icon"));
                            updateGadgetThumb06(gadgets.get("gadget_06_uuid"),
                                gadgets.get("gadget_06_name"),
                                gadgets.get("gadget_06_icon"));
                            updateGadgetThumb07(gadgets.get("gadget_07_uuid"),
                                gadgets.get("gadget_07_name"),
                                gadgets.get("gadget_07_icon"));
                        }
                        else
                        {
                            updateCurrentGadget("0", emptyGadgetName, emptyGadgetIcon);
                            updateGadgetThumb01("0", emptyGadgetName, emptyGadgetIcon);
                            updateGadgetThumb02("0", emptyGadgetName, emptyGadgetIcon);
                            updateGadgetThumb03("0", emptyGadgetName, emptyGadgetIcon);
                            updateGadgetThumb05("0", emptyGadgetName, emptyGadgetIcon);
                            updateGadgetThumb06("0", emptyGadgetName, emptyGadgetIcon);
                            updateGadgetThumb07("0", emptyGadgetName, emptyGadgetIcon);
                        }
                    }
                    else
                    {
                        updateCurrentGadget("0", emptyGadgetName, emptyGadgetIcon);
                        updateGadgetThumb01("0", emptyGadgetName, emptyGadgetIcon);
                        updateGadgetThumb02("0", emptyGadgetName, emptyGadgetIcon);
                        updateGadgetThumb03("0", emptyGadgetName, emptyGadgetIcon);
                        updateGadgetThumb05("0", emptyGadgetName, emptyGadgetIcon);
                        updateGadgetThumb06("0", emptyGadgetName, emptyGadgetIcon);
                        updateGadgetThumb07("0", emptyGadgetName, emptyGadgetIcon);
                    }
                    var alertGadget = null;
                    try
                    {
                        alertGadget = states.get("alert");
                    }
                    catch (e)
                    {
                        alertGadget = null;
                    }
                    if (alertGadget != null)
                    {
                        updateCurrentAlertGadget(alertGadget.get("uuid"),
                                alertGadget.get("name"),
                                alertGadget.get("icon"));
                    }
                    else
                    {
                        updateCurrentAlertGadget("0", emptyGadgetName, emptyGadgetIcon);
                    }
                    var gadgetMessagesDict = null;
                    try
                    {
                        gadgetMessagesDict = states.get("gadget_messages");
                    }
                    catch (e)
                    {
                        gadgetMessagesDict = null;
                    }
                    if (gadgetMessagesDict != null)
                    {
                        updateMessagesBox(gadgetMessagesDict);
                    }
                }
                if (batteryState != knowedBatteryState)
                {
                    knowedBatteryState = batteryState;
                    showBatteryState(batteryState);
                }
                if (soundState != knowedSoundState)
                {
                    knowedSoundState = soundState;
                    if (soundState == "off")
                    {
                        showSoundOff();
                    }
                    else
                    {
                        showSoundOn();
                    }
                }
                if (radioState != knowedRadioState)
                {
                    knowedRadioState = radioState;
                    if (radioState == "off")
                    {
                        showRadioOff();
                    }
                    else
                    {
                        showRadioOn();
                    }
                }
                if (dongleState != knowedDongleState)
                {
                    knowedDongleState = dongleState;
                    if (dongleState == "off")
                    {
                        showDongleOff();
                    }
                    else
                    {
                        showDongleOn();
                    }
                }
                setTimeout("updateStates();", 500);
            }

            function initialization()
            {
                setpng(document.getElementById('thumbnailBarTooltip'));
                updateCurrentAlertGadget("0", "0", "0");
                updateStates();
            }

            function showSoundOn()
            {
                document.getElementById("statusBtnSoundOn").className = "statusBtnSoundOnActivate";
                document.getElementById("statusBtnSoundOff").className = "statusBtnSoundOffEnable";
            }

            function setSoundOn()
            {
                getRequest("/robot_content_interactions/unmute", {});
            }

            function showSoundOff()
            {
                document.getElementById("statusBtnSoundOn").className = "statusBtnSoundOnEnable";
                document.getElementById("statusBtnSoundOff").className = "statusBtnSoundOffActivate";
            }

            function setSoundOff()
            {
                getRequest("/robot_content_interactions/mute", {});
            }

            function showBatteryState(state)
            {
                if (state == 'nodongle')
                {
                    document.getElementById("statusPicBattery").src = "/data/web_interface/user_01/img/status_battery_nodongle.png";
                }
                else if (state == 'charge')
                {
                    document.getElementById("statusPicBattery").src = "/data/web_interface/user_01/img/status_battery_oncharge.png";
                }
                else if (state == 'empty')
                {
                    document.getElementById("statusPicBattery").src = "/data/web_interface/user_01/img/status_battery_empty.gif";
                }
                else if (state == 'low')
                {
                    document.getElementById("statusPicBattery").src = "/data/web_interface/user_01/img/status_battery_low.png";
                }
                else if (state == 'middle')
                {
                    document.getElementById("statusPicBattery").src = "/data/web_interface/user_01/img/status_battery_middle.png";
                }
                else
                {
                    document.getElementById("statusPicBattery").src = "/data/web_interface/user_01/img/status_battery_high.png";
                }
            }

            function showRadioOn()
            {
                document.getElementById("statusRadioOnOff").src = "/data/web_interface/user_01/img/status_active_on.png";
            }

            function showRadioOff()
            {
                document.getElementById("statusRadioOnOff").src = "/data/web_interface/user_01/img/status_active_off.png";
            }

            function showDongleOn()
            {
                document.getElementById("statusDongleOnOff").src = "/data/web_interface/user_01/img/status_active_on.png";
            }

            function showDongleOff()
            {
                document.getElementById("statusDongleOnOff").src = "/data/web_interface/user_01/img/status_active_off.png";
            }

            function previousGadget()
            {
                getRequest("/robot_content_interactions/previous_gadget", {});
            }

            function nextGadget()
            {
                getRequest("/robot_content_interactions/next_gadget", {});
            }

            function startGadget()
            {
                getRequest("/robot_content_interactions/start_gadget", {});
            }

            function startStopGadget()
            {
                getRequest("/robot_content_interactions/start_stop_gadget", {});
            }

            function stopGadget()
            {
                getRequest("/robot_content_interactions/stop_gadget", {});
            }

            function updateCurrentGadget(uuid, name, icon, description)
            {
                if ((knowedGadget04Name != name) || (knowedGadget04Uuid != uuid))
                {
                    knowedGadget04Name = name;
                    knowedGadget04Uuid = uuid;
                    knowedGadget04Icon = icon;
                    knowedGadget04Description = description;
                    document.getElementById("thumbnailBarGadgetIcon04").src = icon;
                    setpng(document.getElementById('thumbnailBarGadgetIcon04'));
                    document.getElementById('thumbnailBarGadgetIcon04').onclick = function() {
                        startStopGadget();
                    }
                    if (name.length > 20) {name = name.slice(0, 18) + "...";}
                    document.getElementById("thumbnailBarGadgetName04").firstChild.nodeValue = name;
                    document.getElementById("notifyHintGadgetIcon").src = icon;
                    setpng(document.getElementById('notifyHintGadgetIcon'));
                    document.getElementById("notifyHintGadgetName").firstChild.nodeValue = name;
                    document.getElementById("notifyHintGadgetDescription").firstChild.nodeValue = description;
                    clearMessagesBox();
                }
            }

            function updateMessagesBox(gadgetMessagesDict)
            {
                if (gadgetMessagesDict.get("count") == "0")
                {
                    return;
                }
                knowedCount = 0;
                if (knowedGadgetMessagesDict != null)
                {
                    knowedCount = parseInt(knowedGadgetMessagesDict.get("count"));
                }
                currentCount = parseInt(gadgetMessagesDict.get("count"));
                if (knowedCount == currentCount)
                {
                    return;
                }
                knowedGadgetMessagesDict = gadgetMessagesDict;
                var divContent = '<span class="notifyHintGadgetMessage">';
                for (i = 0; i < currentCount; i++)
                {
                    message = gadgetMessagesDict.get("msg_" + i);
                    divContent += message + "<br>";
                }
                divContent += "</span>";
                document.getElementById("notifyHintGadgetMessages").innerHTML = divContent;
                // Scroll down
                var objDiv = document.getElementById("notifyHintGadgetMessages");
                objDiv.scrollTop = objDiv.scrollHeight;
            }

            function clearMessagesBox()
            {
                document.getElementById("notifyHintGadgetMessages").innerHTML = "<span></span>";
                knowedGadgetMessagesDict = null;
            }

            function updateGadgetThumb01(uuid, name, icon)
            {
                if ((knowedGadget01Name != name) || (knowedGadget01Uuid != uuid))
                {
                    knowedGadget01Name = name;
                    knowedGadget01Uuid = uuid;
                    knowedGadget01Icon = icon;
                    document.getElementById("thumbnailBarGadgetIcon01").src = icon;
                    setpng(document.getElementById('thumbnailBarGadgetIcon01'));
                    if (name.length > 10) {name = name.slice(0, 8) + "...";}
                    document.getElementById("thumbnailBarGadgetName01").firstChild.nodeValue = name;
                }
            }

            function updateGadgetThumb02(uuid, name, icon)
            {
                if ((knowedGadget02Name != name) || (knowedGadget02Uuid != uuid))
                {
                    knowedGadget02Name = name;
                    knowedGadget02Uuid = uuid;
                    knowedGadget02Icon = icon;
                    document.getElementById("thumbnailBarGadgetIcon02").src = icon;
                    setpng(document.getElementById('thumbnailBarGadgetIcon02'));
                    if (name.length > 10) {name = name.slice(0, 8) + "...";}
                    document.getElementById("thumbnailBarGadgetName02").firstChild.nodeValue = name;
                }
            }

            function updateGadgetThumb03(uuid, name, icon)
            {
                if ((knowedGadget03Name != name) || (knowedGadget03Uuid != uuid))
                {
                    knowedGadget03Name = name;
                    knowedGadget03Uuid = uuid;
                    knowedGadget03Icon = icon;
                    document.getElementById("thumbnailBarGadgetIcon03").src = icon;
                    setpng(document.getElementById('thumbnailBarGadgetIcon03'));
                    if (name.length > 10) {name = name.slice(0, 8) + "...";}
                    document.getElementById("thumbnailBarGadgetName03").firstChild.nodeValue = name;
                }
            }

            function updateGadgetThumb05(uuid, name, icon)
            {
                if ((knowedGadget05Name != name) || (knowedGadget05Uuid != uuid))
                {
                    knowedGadget05Name = name;
                    knowedGadget05Uuid = uuid;
                    knowedGadget05Icon = icon;
                    document.getElementById("thumbnailBarGadgetIcon05").src = icon;
                    setpng(document.getElementById('thumbnailBarGadgetIcon05'));
                    if (name.length > 10) {name = name.slice(0, 8) + "...";}
                    document.getElementById("thumbnailBarGadgetName05").firstChild.nodeValue = name;
                }
            }

            function updateGadgetThumb06(uuid, name, icon)
            {
                if ((knowedGadget06Name != name) || (knowedGadget06Uuid != uuid))
                {
                    knowedGadget06Name = name;
                    knowedGadget06Uuid = uuid;
                    knowedGadget06Icon = icon;
                    document.getElementById("thumbnailBarGadgetIcon06").src = icon;
                    setpng(document.getElementById('thumbnailBarGadgetIcon06'));
                    if (name.length > 10) {name = name.slice(0, 8) + "...";}
                    document.getElementById("thumbnailBarGadgetName06").firstChild.nodeValue = name;
                }
            }

            function updateGadgetThumb07(uuid, name, icon)
            {
                if ((knowedGadget07Name != name) || (knowedGadget07Uuid != uuid))
                {
                    knowedGadget07Name = name;
                    knowedGadget07Uuid = uuid;
                    knowedGadget07Icon = icon;
                    document.getElementById("thumbnailBarGadgetIcon07").src = icon;
                    setpng(document.getElementById('thumbnailBarGadgetIcon07'));
                    if (name.length > 10) {name = name.slice(0, 8) + "...";}
                    document.getElementById("thumbnailBarGadgetName07").firstChild.nodeValue = name;
                }
            }

            function updateCurrentAlertGadget(uuid, name, icon)
            {
                if ((knowedAlertGadgetName != name) || (knowedAlertGadgetUuid != uuid))
                {
                    knowedAlertGadgetName = name;
                    knowedAlertGadgetUuid = uuid;
                    knowedAlertGadgetIcon = icon;
                    if (uuid == "0")
                    {
                        document.getElementById("notifyHintAlert").style.display = 'none';
                    }
                    else
                    {
                        document.getElementById("notifyAlertGadgetIcon").src = icon;
                        setpng(document.getElementById('notifyAlertGadgetIcon'));
                        document.getElementById("notifyHintAlert").style.display = '';
                    }
                }
            }
        ]]>
        </script>
    </head>

    <body bgcolor="#EFEFEF" onLoad="initialization();">
        <!-- MAIN DIV FRAME -->
        <div style="position:absolute;
                    left:0px;
                    top:0px;">
            <!-- THUMBNAIL VIEW -->
            <div class="frame01TopSpace"></div>
            <div class="frame01Middle">
                <!-- PREVIOUS BUTTON -->
                <xsl:element name="a">
                    <xsl:attribute name="class">thumbnailBarBtnPrevious</xsl:attribute>
                    <xsl:attribute name="onclick">javascript:previousGadget();return false;</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute>
                </xsl:element>
                <!-- THUMBNAIL BAR -->
                <div class="thumbnailBarView">
                    <!-- THUMBNAIL 01 -->
                    <div class="thumbnailBarGadgetFirstDiv">
                        <xsl:element name="img">
                            <xsl:attribute name="id">thumbnailBarGadgetIcon01</xsl:attribute>
                            <xsl:attribute name="src">/data/web_interface/user_01/img/empty.png</xsl:attribute>
                            <xsl:attribute name="height">44</xsl:attribute>
                            <xsl:attribute name="width">44</xsl:attribute>
                        </xsl:element>
                    </div>
                    <!-- THUMBNAIL 02 -->
                    <div class="thumbnailBarGadgetDiv">
                        <xsl:element name="img">
                            <xsl:attribute name="id">thumbnailBarGadgetIcon02</xsl:attribute>
                            <xsl:attribute name="src">/data/web_interface/user_01/img/empty.png</xsl:attribute>
                            <xsl:attribute name="height">44</xsl:attribute>
                            <xsl:attribute name="width">44</xsl:attribute>
                        </xsl:element>
                    </div>
                    <!-- THUMBNAIL 03 -->
                    <div class="thumbnailBarGadgetDiv">
                        <xsl:element name="img">
                            <xsl:attribute name="id">thumbnailBarGadgetIcon03</xsl:attribute>
                            <xsl:attribute name="src">/data/web_interface/user_01/img/empty.png</xsl:attribute>
                            <xsl:attribute name="height">44</xsl:attribute>
                            <xsl:attribute name="width">44</xsl:attribute>
                        </xsl:element>
                    </div>
                    <!-- THUMBNAIL 04 -->
                    <div class="thumbnailBarGadgetDivCenter">
                        <xsl:element name="img">
                            <xsl:attribute name="id">thumbnailBarGadgetIcon04</xsl:attribute>
                            <xsl:attribute name="src">/data/web_interface/user_01/img/empty.png</xsl:attribute>
                            <xsl:attribute name="onclick">javascript:startStopGadget();return false;</xsl:attribute>
                            <xsl:attribute name="height">70</xsl:attribute>
                            <xsl:attribute name="width">70</xsl:attribute>
                        </xsl:element>
                    </div>
                    <!-- THUMBNAIL 05 -->
                    <div class="thumbnailBarGadgetDivFift">
                        <xsl:element name="img">
                            <xsl:attribute name="id">thumbnailBarGadgetIcon05</xsl:attribute>
                            <xsl:attribute name="src">/data/web_interface/user_01/img/empty.png</xsl:attribute>
                            <xsl:attribute name="height">44</xsl:attribute>
                            <xsl:attribute name="width">44</xsl:attribute>
                        </xsl:element>
                    </div>
                    <!-- THUMBNAIL 06 -->
                    <div class="thumbnailBarGadgetDiv">
                        <xsl:element name="img">
                            <xsl:attribute name="id">thumbnailBarGadgetIcon06</xsl:attribute>
                            <xsl:attribute name="src">/data/web_interface/user_01/img/empty.png</xsl:attribute>
                            <xsl:attribute name="height">44</xsl:attribute>
                            <xsl:attribute name="width">44</xsl:attribute>
                        </xsl:element>
                    </div>
                    <!-- THUMBNAIL 07 -->
                    <div class="thumbnailBarGadgetDiv">
                        <xsl:element name="img">
                            <xsl:attribute name="id">thumbnailBarGadgetIcon07</xsl:attribute>
                            <xsl:attribute name="src">/data/web_interface/user_01/img/empty.png</xsl:attribute>
                            <xsl:attribute name="height">44</xsl:attribute>
                            <xsl:attribute name="width">44</xsl:attribute>
                        </xsl:element>
                    </div>
                    <span class="thumbnailBarGadget01Name" id="thumbnailBarGadgetName01"> . </span>
                    <span class="thumbnailBarGadget02Name" id="thumbnailBarGadgetName02"> . </span>
                    <span class="thumbnailBarGadget03Name" id="thumbnailBarGadgetName03"> . </span>
                    <span class="thumbnailBarGadget05Name" id="thumbnailBarGadgetName05"> . </span>
                    <span class="thumbnailBarGadget06Name" id="thumbnailBarGadgetName06"> . </span>
                    <span class="thumbnailBarGadget07Name" id="thumbnailBarGadgetName07"> . </span>
                </div>
                <!-- NEXT BUTTON -->
                <xsl:element name="a">
                    <xsl:attribute name="class">thumbnailBarBtnNext</xsl:attribute>
                    <xsl:attribute name="onclick">javascript:nextGadget();return false;</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute>
                </xsl:element>
            </div>
            <div class="frame01Bottom"></div>
            <!-- THUMBNAILBAR TOOLTIP -->
            <div class="thumbnailBarTooltip">
                <xsl:element name="img">
                    <xsl:attribute name="id">thumbnailBarTooltip</xsl:attribute>
                    <xsl:attribute name="src">/data/web_interface/user_01/img/thumbnailbar_tooltip.png</xsl:attribute>
                    <xsl:attribute name="height">50</xsl:attribute>
                    <xsl:attribute name="width">172</xsl:attribute>
                </xsl:element>
            </div>
            <span class="thumbnailBarGadget04Name" id="thumbnailBarGadgetName04"> . </span>
            <!-- NOTIFICATION VIEW -->
            <div class="frame01Top"></div>
            <div class="frame01MiddleNotify">
                <!-- TUX DROID PICTURE -->
                <xsl:element name="img">
                    <xsl:attribute name="class">notifyTuxIdle</xsl:attribute>
                    <xsl:attribute name="src">/data/web_interface/user_01/img/notify_pic_tux_idle.png</xsl:attribute>
                </xsl:element>
                <!-- NOTIFIER HINT FRAME -->
                <div class="notifyHintFrame">
                    <div class="notifyHintGadgetIcon">
                        <xsl:element name="img">
                            <xsl:attribute name="id">notifyHintGadgetIcon</xsl:attribute>
                            <xsl:attribute name="src">/data/web_interface/user_01/img/empty.png</xsl:attribute>
                            <xsl:attribute name="height">30</xsl:attribute>
                            <xsl:attribute name="width">30</xsl:attribute>
                        </xsl:element>
                    </div>
                    <span class="notifyHintGadgetName" id="notifyHintGadgetName"> . </span>
                    <span class="notifyHintGadgetDescription" id="notifyHintGadgetDescription"> . </span>
                    <div class="notifyHintGadgetMessages" id="notifyHintGadgetMessages">
                    </div>
                </div>
            </div>
            <div class="frame01Bottom"></div>
            <!-- NOTIFIER HINT ALERT -->
            <div class="notifyHintAlert" id="notifyHintAlert">
                <div class="notifyAlertGadgetIcon">
                    <xsl:element name="img">
                        <xsl:attribute name="id">notifyAlertGadgetIcon</xsl:attribute>
                        <xsl:attribute name="src">/data/web_interface/user_01/img/empty.png</xsl:attribute>
                        <xsl:attribute name="height">22</xsl:attribute>
                        <xsl:attribute name="width">22</xsl:attribute>
                    </xsl:element>
                </div>
            </div>
            <!-- STATUS VIEW -->
            <div class="statusFrame">
                <!-- STATUS VIEW TITLE -->
                <span class="statusViewTitle"><xsl:value-of select="root/translations/status"/></span>
                <!-- STATUS PIC RADIO -->
                <xsl:element name="img">
                    <xsl:attribute name="class">statusPicRadio</xsl:attribute>
                    <xsl:attribute name="src">/data/web_interface/user_01/img/status_pic_radio.png</xsl:attribute>
                </xsl:element>
                <!-- STATUS RADIO ON/OFF -->
                <xsl:element name="img">
                    <xsl:attribute name="class">statusActiveOnOff</xsl:attribute>
                    <xsl:attribute name="id">statusRadioOnOff</xsl:attribute>
                    <xsl:attribute name="src">/data/web_interface/user_01/img/status_active_off.png</xsl:attribute>
                </xsl:element>
                <!-- STATUS PIC DONGLE -->
                <xsl:element name="img">
                    <xsl:attribute name="class">statusPicDongle</xsl:attribute>
                    <xsl:attribute name="src">/data/web_interface/user_01/img/status_pic_dongle.png</xsl:attribute>
                </xsl:element>
                <!-- STATUS DONGLE ON/OFF -->
                <xsl:element name="img">
                    <xsl:attribute name="class">statusActiveOnOff</xsl:attribute>
                    <xsl:attribute name="id">statusDongleOnOff</xsl:attribute>
                    <xsl:attribute name="src">/data/web_interface/user_01/img/status_active_off.png</xsl:attribute>
                </xsl:element>
                <!-- STATUS PIC BATTERY -->
                <xsl:element name="img">
                    <xsl:attribute name="class">statusPicBattery</xsl:attribute>
                    <xsl:attribute name="id">statusPicBattery</xsl:attribute>
                    <xsl:attribute name="src">/data/web_interface/user_01/img/status_battery_nodongle.png</xsl:attribute>
                </xsl:element>
                <!-- STATUS BTN SOUND ON -->
                <xsl:element name="a">
                    <xsl:attribute name="class">statusBtnSoundOnEnable</xsl:attribute>
                    <xsl:attribute name="id">statusBtnSoundOn</xsl:attribute>
                    <xsl:attribute name="onclick">javascript:setSoundOn();return false;</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/sound_on"/>
                </xsl:element>
                <!-- STATUS BTN SOUND OFF -->
                <xsl:element name="a">
                    <xsl:attribute name="class">statusBtnSoundOffActivate</xsl:attribute>
                    <xsl:attribute name="id">statusBtnSoundOff</xsl:attribute>
                    <xsl:attribute name="onclick">javascript:setSoundOff();return false;</xsl:attribute>
                    <xsl:attribute name="href">#</xsl:attribute><xsl:value-of select="root/translations/sound_off"/>
                </xsl:element>
                
                <div class="statusFrame" style="position:absolute;
                    left:0px;
                    top:540px;
                    "><a style="width: 100%;
                        text-align: center;
                        display: block;
                        margin-top: 15px;
                        color: red;">                 
                    Please wait 5 minutes and run : sudo tuxhttpserver -u</a>
                </div>   
            </div>
        </div>
        <!-- EXAMPLE OF LIGHTBOX -->
        <div id="ligthboxExample" class="leightbox">
            <h1>A lightbox</h1>
            <p> This is a test</p>
            <p class="footer">
                <a href="#" class="lbAction" rel="deactivate">Close</a>
            </p>
        </div>
    </body>
</html>
</xsl:template>
</xsl:stylesheet>
