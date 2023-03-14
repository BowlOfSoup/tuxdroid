<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">

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
            function applyGlobalConfiguration()
            {
                var language = document.getElementById("language").value;
                var locutor = document.getElementById("voiceValue").value;
                var pitch = document.getElementById("pitchValue").value;
                var args = {
                    "language" : language,
                    "locutor" : locutor,
                    "pitch" : pitch
                }
                res = postRequest("/wi_user_01/apply_global_configuration", args);
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
                <span class="gadgetConfTitleBarLabel"><xsl:value-of select="root/translations/voice_settings"/></span>
            </div>
            <div class="gadgetConfTitleBarBottom1"></div>
            <!-- VOICE -->
            <div class="gadgetConfContentFrameMiddle">
                <div class="gadgetConfContentFrameSep"></div>
                <span class="gadgetConfParamName">
                    <xsl:value-of select="root/translations/voice_param_title"/>
                </span>
                <span class="gadgetConfParamValue">
                    <xsl:element name="select">
                        <xsl:attribute name="class">select</xsl:attribute>
                        <xsl:attribute name="id">voiceValue</xsl:attribute>
                        <xsl:attribute name="name">voiceValue</xsl:attribute>
                        <xsl:for-each select="root/data/availableLocutors/*">
                            <xsl:element name="option">
                                <xsl:attribute name="value">
                                    <xsl:value-of select="."/>
                                </xsl:attribute>
                                <xsl:if test=". = ../../defaultLocutor">
                                    <xsl:attribute name="selected">true</xsl:attribute>
                                </xsl:if>
                                <xsl:value-of select="."/>
                            </xsl:element>
                        </xsl:for-each>
                    </xsl:element>
                </span>
            </div>
            <!-- PITCH -->
            <div class="gadgetConfContentFrameMiddle">
                <div class="gadgetConfContentFrameSep"></div>
                <span class="gadgetConfParamName">
                    <xsl:value-of select="root/translations/pitch_param_title"/>
                </span>
                <span class="gadgetConfParamValue">
                    <xsl:element name="select">
                        <xsl:attribute name="class">select</xsl:attribute>
                        <xsl:attribute name="id">pitchValue</xsl:attribute>
                        <xsl:attribute name="name">pitchValue</xsl:attribute>
                        <xsl:element name="option">
                            <xsl:attribute name="value">120</xsl:attribute>
                            <xsl:if test="root/data/defaultPitch = '120'">
                                <xsl:attribute name="selected">true</xsl:attribute>
                            </xsl:if>
                            <xsl:value-of select="root/translations/pitch_tux_voice"/>
                        </xsl:element>
                        <xsl:element name="option">
                            <xsl:attribute name="value">100</xsl:attribute>
                            <xsl:if test="root/data/defaultPitch = '100'">
                                <xsl:attribute name="selected">true</xsl:attribute>
                            </xsl:if>
                            <xsl:value-of select="root/translations/pitch_normal"/>
                        </xsl:element>
                        <xsl:element name="option">
                            <xsl:attribute name="value">85</xsl:attribute>
                            <xsl:if test="root/data/defaultPitch = '85'">
                                <xsl:attribute name="selected">true</xsl:attribute>
                            </xsl:if>
                            <xsl:value-of select="root/translations/pitch_low"/>
                        </xsl:element>
                    </xsl:element>
                </span>
            </div>
            <div class="gadgetConfContentFrameBottom"></div>
        </div>
    </body>
</html>
</xsl:template>
</xsl:stylesheet>
