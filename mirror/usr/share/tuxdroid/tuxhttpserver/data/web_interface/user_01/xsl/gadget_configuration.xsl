<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">

<xsl:include href="plugin_gadget_common.xsl"/>

<xsl:template match="/">
<html>
    <head>
        <LINK href="/data/web_interface/user_01/css/gadget-configuration.css" rel="stylesheet" type="text/css"/>
        <script src="/data/web_interface/user_01/js/hashtable.js" type="text/javascript"/>
        <script src="/data/web_interface/user_01/js/common.js" type="text/javascript"/>
        <script language="javascript">
        <![CDATA[
            function initialization()
            {
            }

            /**
             *
             */
            function applyGadgetConfiguration()
            {
                var uuid = document.getElementById("uuid").value;
                var language = document.getElementById("language").value;
                var args = {
                    "uuid" : uuid,
                    "language" : language,
                    "parameters" : computeParameters()
                }
                res = postRequest("/wi_user_01/apply_gadget", args);
            }
        ]]>
        </script>
    </head>

    <body bgcolor="#dcdadb" onLoad="initialization();">
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
            <xsl:attribute name="id">uuid</xsl:attribute>
            <xsl:attribute name="value">
                <xsl:value-of select="root/data/description/uuid"/>
            </xsl:attribute>
        </xsl:element>
        <!-- MAIN DIV FRAME -->
        <div style="position:absolute;
                    left:0px;
                    top:0px;
                    width:423px;
                    height:388px;
                    overflow-y:scroll;
                    overflow-x:hidden;">
            <!-- SETTINGS BAR -->
            <div class="gadgetConfTitleBarSettings">
                <span class="gadgetConfTitleBarLabel"><xsl:value-of select="root/translations/gadget_settings"/></span>
            </div>
            <div class="gadgetConfTitleBarBottom1"></div>
            <!-- SETTINGS CONTENT -->
            <!-- GADGET NAME -->
            <div class="gadgetConfContentFrameMiddle" style="height:4px;"></div>
            <div class="gadgetConfContentFrameMiddle">
                <span class="gadgetConfParamName"><xsl:value-of select="root/translations/gadget_name"/></span>
                <span class="gadgetConfParamValue">
                    <xsl:element name="input">
                        <xsl:attribute name="class">text</xsl:attribute>
                        <xsl:attribute name="type">text</xsl:attribute>
                        <xsl:attribute name="id">req_gadget_name</xsl:attribute>
                        <xsl:attribute name="value">
                            <xsl:value-of select="root/data/description/name"/>
                        </xsl:attribute>
                    </xsl:element>
                </span>
            </div>
            <!-- GADGET PARAMETERS -->
            <xsl:for-each select="root/data/parameters/*">
                <xsl:if test="visible = 'True'">
                    <div class="gadgetConfContentFrameMiddle">
                        <div class="gadgetConfContentFrameSep"></div>
                        <xsl:element name="input">
                            <xsl:attribute name="class">text</xsl:attribute>
                            <xsl:attribute name="type">hidden</xsl:attribute>
                            <xsl:attribute name="id">req_param_<xsl:value-of select="name"/>_visible</xsl:attribute>
                            <xsl:attribute name="value">true</xsl:attribute>
                        </xsl:element>
                        <span class="gadgetConfParamName"><xsl:value-of select="description"/></span>
                        <span class="gadgetConfParamValue">
                            <xsl:call-template name="showParameter"/>
                        </span>
                    </div>
                </xsl:if>
            </xsl:for-each>
            <div class="gadgetConfContentFrameBottom"></div>
            <!-- ON DEMAND -->
            <xsl:choose>
            <xsl:when test="root/data/description/onDemandIsAble = 'true'">
                <!-- BAR -->
                <div class="gadgetConfTitleBarOnDemand">
                    <span class="gadgetConfTitleBarLabel"><xsl:value-of select="root/translations/on_demand"/></span>
                </div>
                <div class="gadgetConfTitleBarBottom2"></div>
                <!-- Content -->
                <xsl:element name="input">
                    <xsl:attribute name="class">checkbox</xsl:attribute>
                    <xsl:attribute name="type">checkbox</xsl:attribute>
                    <xsl:attribute name="id">req_gadget_onDemandIsActivated</xsl:attribute>
                    <xsl:if test="root/data/description/onDemandIsActivated = 'true'">
                        <xsl:attribute name="checked">true</xsl:attribute>
                    </xsl:if>
                </xsl:element>
                <span class="gadgetConfMyUseDescription"><xsl:value-of select="root/translations/on_demand_description"/></span>
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="input">
                    <xsl:attribute name="class">text</xsl:attribute>
                    <xsl:attribute name="type">hidden</xsl:attribute>
                    <xsl:attribute name="id">req_gadget_onDemandIsActivated</xsl:attribute>
                    <xsl:attribute name="value">false</xsl:attribute>
                </xsl:element>
            </xsl:otherwise>
            </xsl:choose>
            <!-- ALERTS -->
            <xsl:for-each select="root/data/tasks/*">
                <xsl:element name="input">
                    <xsl:attribute name="class">text</xsl:attribute>
                    <xsl:attribute name="type">hidden</xsl:attribute>
                    <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_visible</xsl:attribute>
                    <xsl:attribute name="value">true</xsl:attribute>
                </xsl:element>
                <!-- BAR -->
                <div class="gadgetConfTitleBarAlert">
                    <span class="gadgetConfTitleBarLabel"><xsl:value-of select="../../../translations/alerts"/></span>
                </div>
                <div class="gadgetConfTitleBarBottom2"></div>
                <!-- CONTENT -->
                <xsl:element name="input">
                    <xsl:attribute name="class">checkbox</xsl:attribute>
                    <xsl:attribute name="type">checkbox</xsl:attribute>
                    <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_activated</xsl:attribute>
                    <xsl:if test="activated = 'True'">
                        <xsl:attribute name="checked">true</xsl:attribute>
                    </xsl:if>
                </xsl:element>
                <span class="gadgetConfMyUseDescription">
                    <xsl:value-of select="description"/>
                </span>
                <xsl:if test="dateVisible='True' or hoursBeginVisible='True' or hoursEndVisible='True' or delayVisible='True' or weekMaskVisible='True' or ../../showAlertAttitune='True' or count(parameters/*[visible='True']) > 0">
                    <div class="gadgetConfContentFrameTop"></div>
                    <!-- GADGET ALERT ATTITUNE -->
                    <xsl:if test="../../showAlertAttitune = 'True'">
                        <div class="gadgetConfContentFrameMiddle">
                            <span class="gadgetConfParamName">
                                <xsl:value-of select="../../../translations/introduction_alerts"/>
                            </span>
                            <span class="gadgetConfParamValue">
                                <xsl:element name="select">
                                    <xsl:attribute name="class">select</xsl:attribute>
                                    <xsl:attribute name="id">req_alertAttitune</xsl:attribute>
                                    <xsl:attribute name="name">AlertAttitune</xsl:attribute>
                                    <xsl:for-each select="../../availableAttitunes/*">
                                        <xsl:element name="option">
                                            <xsl:attribute name="value">
                                                <xsl:value-of select="."/>
                                            </xsl:attribute>
                                            <xsl:if test=". = ../../alertAttitune">
                                                <xsl:attribute name="selected">true</xsl:attribute>
                                            </xsl:if>
                                            <xsl:value-of select="."/>
                                        </xsl:element>
                                    </xsl:for-each>
                                </xsl:element>
                            </span>
                            <xsl:if test="dateVisible='True' or hoursBeginVisible='True' or hoursEndVisible='True' or delayVisible='True' or weekMaskVisible='True' or count(parameters/*[visible='True']) > 0">
                                <div class="gadgetConfContentFrameSep"></div>
                            </xsl:if>
                        </div>
                    </xsl:if>
                    <!-- ALERT PARAMETERS -->
                    <xsl:for-each select="parameters/*">
                        <xsl:if test="visible = 'True'">
                            <div class="gadgetConfContentFrameMiddle">
                                <xsl:element name="input">
                                    <xsl:attribute name="class">text</xsl:attribute>
                                    <xsl:attribute name="type">hidden</xsl:attribute>
                                    <xsl:attribute name="id">req_param_<xsl:value-of select="name"/>_visible</xsl:attribute>
                                    <xsl:attribute name="value">true</xsl:attribute>
                                </xsl:element>
                                <span class="gadgetConfParamName"><xsl:value-of select="description"/></span>
                                <span class="gadgetConfParamValue">
                                    <xsl:call-template name="showParameter"/>
                                </span>
                                <div class="gadgetConfContentFrameSep"></div>
                            </div>
                        </xsl:if>
                    </xsl:for-each>
                    <xsl:if test="dateVisible = 'True'">
                        <div class="gadgetConfContentFrameMiddle">
                            <span class="gadgetConfParamName">
                                <xsl:value-of select="../../../translations/date"/>
                            </span>
                            <span class="gadgetConfParamValue">
                                <xsl:call-template name="dateSelecter">
                                    <xsl:with-param name="date" select='date' />
                                </xsl:call-template>
                            </span>
                            <xsl:if test="hoursBeginVisible='True' or hoursEndVisible='True' or delayVisible='True' or weekMaskVisible='True'">
                                <div class="gadgetConfContentFrameSep"></div>
                            </xsl:if>
                        </div>
                    </xsl:if>
                    <xsl:if test="hoursBeginVisible = 'True'">
                        <div class="gadgetConfContentFrameMiddle">
                            <span class="gadgetConfParamName">
                                 <xsl:value-of select="../../../translations/starting_at"/>
                            </span>
                            <span class="gadgetConfParamValue">
                                <xsl:call-template name="timeSelecter">
                                    <xsl:with-param name="time" select='hoursBegin' />
                                    <xsl:with-param name="mask" select='hoursBeginMask' />
                                </xsl:call-template>
                            </span>
                            <xsl:if test="hoursEndVisible='True' or delayVisible='True' or weekMaskVisible='True'">
                                <div class="gadgetConfContentFrameSep"></div>
                            </xsl:if>
                        </div>
                    </xsl:if>
                    <xsl:if test="hoursEndVisible = 'True'">
                        <div class="gadgetConfContentFrameMiddle">
                            <span class="gadgetConfParamName">
                                <xsl:value-of select="../../../translations/stopping_at"/>
                            </span>
                            <span class="gadgetConfParamValue">
                                <xsl:call-template name="timeSelecter">
                                    <xsl:with-param name="time" select='hoursEnd' />
                                    <xsl:with-param name="mask" select='hoursEndMask' />
                                </xsl:call-template>
                            </span>
                            <xsl:if test="delayVisible='True' or weekMaskVisible='True'">
                                <div class="gadgetConfContentFrameSep"></div>
                            </xsl:if>
                        </div>
                    </xsl:if>
                    <xsl:if test="delayVisible = 'True'">
                        <div class="gadgetConfContentFrameMiddle">
                            <span class="gadgetConfParamName">
                                <xsl:value-of select="../../../translations/delay"/>
                            </span>
                            <span class="gadgetConfParamValue">
                                <xsl:if test="delayType = 'hms'">
                                    <xsl:call-template name="timeSelecter">
                                        <xsl:with-param name="time" select='delay' />
                                        <xsl:with-param name="mask" select='delayMask' />
                                    </xsl:call-template>
                                </xsl:if>
                                <xsl:if test="delayType = 'quarters'">
                                    <xsl:call-template name="quartersSelecter">
                                        <xsl:with-param name="time" select='delay' />
                                    </xsl:call-template>
                                </xsl:if>
                                <xsl:if test="delayType = 'frequency'">
                                    <xsl:call-template name="frequencySelecter">
                                        <xsl:with-param name="time" select='delay' />
                                    </xsl:call-template>
                                </xsl:if>
                            </span>
                            <xsl:if test="weekMaskVisible='True'">
                                <div class="gadgetConfContentFrameSep"></div>
                            </xsl:if>
                        </div>
                    </xsl:if>
                    <xsl:if test="weekMaskVisible = 'True'">
                        <div class="gadgetConfContentFrameMiddle">
                            <span class="gadgetConfParamName">
                                <xsl:value-of select="../../../translations/my_week"/>
                            </span>
                            <span class="gadgetConfParamValue" style="height:0px;">
                                <xsl:call-template name="weekMask">
                                    <xsl:with-param name="week_mask" select='weekMask' />
                                    <xsl:with-param name="type" select='weekMaskType' />
                                </xsl:call-template>
                            </span>
                        </div>
                    </xsl:if>
                    <div class="gadgetConfContentFrameBottom"></div>
                </xsl:if>
            </xsl:for-each>
            <xsl:element name="br"></xsl:element>
        </div>
    </body>
</html>
</xsl:template>
</xsl:stylesheet>
