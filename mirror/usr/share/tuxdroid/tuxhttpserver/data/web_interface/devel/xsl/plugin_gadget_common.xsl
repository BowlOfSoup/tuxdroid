<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">

<xsl:include href="alert.xsl"/>
<xsl:include href="parameter.xsl"/>

<!--
================================================================================
HTML PARAM STORAGE
================================================================================
-->
<xsl:template name="htmlParamStorage">
    <!-- UUID STORAGE -->
    <xsl:element name="input">
        <xsl:attribute name="type">hidden</xsl:attribute>
        <xsl:attribute name="id">uuid</xsl:attribute>
        <xsl:attribute name="value">
            <xsl:value-of select="description/uuid"/>
        </xsl:attribute>
    </xsl:element>

    <!-- ORIGINAL GADGET UUID STORAGE -->
    <xsl:element name="input">
        <xsl:attribute name="type">hidden</xsl:attribute>
        <xsl:attribute name="id">o_uuid</xsl:attribute>
        <xsl:attribute name="value">
            <xsl:value-of select="description/o_uuid"/>
        </xsl:attribute>
    </xsl:element>

    <!-- SKIN STORAGE -->
    <xsl:element name="input">
        <xsl:attribute name="type">hidden</xsl:attribute>
        <xsl:attribute name="id">skin</xsl:attribute>
        <xsl:attribute name="value">
            <xsl:value-of select="../skin"/>
        </xsl:attribute>
    </xsl:element>

    <!-- LANGUAGE STORAGE -->
    <xsl:element name="input">
        <xsl:attribute name="type">hidden</xsl:attribute>
        <xsl:attribute name="id">language</xsl:attribute>
        <xsl:attribute name="value">
            <xsl:value-of select="../language"/>
        </xsl:attribute>
    </xsl:element>
</xsl:template>

<!--
================================================================================
SHOW DESCRIPTION
================================================================================
-->
<xsl:template name="showDescription">
    <div class="descriptionTop">
        <span class="decriptionName">
            <xsl:value-of select="description/translatedName"/>
        </span>
        <xsl:element name="img">
            <xsl:attribute name="class">descriptionIcon</xsl:attribute>
            <xsl:attribute name="src"><xsl:value-of select="description/iconFile"/></xsl:attribute>
            <xsl:attribute name="onload">javascript:setpng(this);</xsl:attribute>
        </xsl:element>
        <div class="descriptionBox">
            <span class="descriptionDescription">
                <xsl:value-of select="description/description"/>
            </span>
            <xsl:element name="br"></xsl:element>
            <span class="descriptionAuthor">
                - by <xsl:value-of select="description/author"/> -
            </span>
        </div>
    </div>
    <div class="descriptionBottom"></div>
</xsl:template>

<!--
================================================================================
EDIT DESCRIPTION
================================================================================
-->

<xsl:template name="editDescription">
    <xsl:param name="title"/>

    <!-- DESCRIPTION SECTION SEPARATOR -->
    <div class="sectionSepHelp">
        <span class="sectionSepTitle"><xsl:value-of select="$title"/></span>
    </div>
    <div class="sectionContentTop2"></div>
    <!-- GADGET NAME -->
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionContentPName">
                Gadget name
            </span>
        </div>
        <div class="sectionContentCol22">
            <span class="sectionContentPName">
            <xsl:element name="input">
                <xsl:attribute name="class">text</xsl:attribute>
                <xsl:attribute name="type">text</xsl:attribute>
                <xsl:attribute name="id">req_gadget_name</xsl:attribute>
                <xsl:attribute name="value">
                    <xsl:value-of select="description/translatedName"/>
                </xsl:attribute>
            </xsl:element>
            </span>
        </div>
    </div>
    <!-- GADGET TTS NAME -->
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionContentPName">
                Gadget TTS sentence
            </span>
        </div>
        <div class="sectionContentCol22">
            <span class="sectionContentPName">
            <xsl:element name="input">
                <xsl:attribute name="class">text</xsl:attribute>
                <xsl:attribute name="type">text</xsl:attribute>
                <xsl:attribute name="id">req_gadget_ttsName</xsl:attribute>
                <xsl:attribute name="value">
                    <xsl:value-of select="description/ttsName"/>
                </xsl:attribute>
            </xsl:element>
            </span>
        </div>
    </div>
    <!-- GADGET DESCRIPTION -->
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionContentPName">
                Gadget description
            </span>
        </div>
        <div class="sectionContentCol22">
            <span class="sectionContentPName">
            <xsl:element name="input">
                <xsl:attribute name="class">text</xsl:attribute>
                <xsl:attribute name="type">text</xsl:attribute>
                <xsl:attribute name="id">req_gadget_description</xsl:attribute>
                <xsl:attribute name="value">
                    <xsl:value-of select="description/description"/>
                </xsl:attribute>
            </xsl:element>
            </span>
        </div>
    </div>
    <!-- GADGET AUTHOR -->
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionContentPName">
                Gadget author
            </span>
        </div>
        <div class="sectionContentCol22">
            <span class="sectionContentPName">
            <xsl:element name="input">
                <xsl:attribute name="class">text</xsl:attribute>
                <xsl:attribute name="type">text</xsl:attribute>
                <xsl:attribute name="id">req_gadget_author</xsl:attribute>
                <xsl:attribute name="value">
                    <xsl:value-of select="description/author"/>
                </xsl:attribute>
            </xsl:element>
            </span>
        </div>
    </div>
    <!-- GADGET VERSION -->
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionContentPName">
                Gadget version
            </span>
        </div>
        <div class="sectionContentCol22">
            <span class="sectionContentPName">
            <xsl:element name="input">
                <xsl:attribute name="class">text</xsl:attribute>
                <xsl:attribute name="type">text</xsl:attribute>
                <xsl:attribute name="id">req_gadget_version</xsl:attribute>
                <xsl:attribute name="value">
                    <xsl:value-of select="description/version"/>
                </xsl:attribute>
            </xsl:element>
            </span>
        </div>
    </div>
    <!-- ICON FILE -->
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionContentPName">
                Icon file
            </span>
        </div>
        <div class="sectionContentCol22">
            <span class="sectionContentPName">
            <xsl:element name="input">
                <xsl:attribute name="class">text</xsl:attribute>
                <xsl:attribute name="type">text</xsl:attribute>
                <xsl:attribute name="id">req_gadget_iconFile</xsl:attribute>
                <xsl:attribute name="value">
                    <xsl:value-of select="description/iconFile"/>
                </xsl:attribute>
            </xsl:element>
            </span>
        </div>
    </div>
    <!-- GADGET CATEGORY -->
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionContentPName">
                Gadget category
            </span>
        </div>
        <div class="sectionContentCol22">
            <span class="sectionContentPName">
            <xsl:element name="input">
                <xsl:attribute name="class">text</xsl:attribute>
                <xsl:attribute name="type">text</xsl:attribute>
                <xsl:attribute name="id">req_gadget_category</xsl:attribute>
                <xsl:attribute name="value">Misc</xsl:attribute>
            </xsl:element>
            </span>
        </div>
    </div>
    <!-- GADGET DEFAULT LANGUAGE -->
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionContentPName">
                Gadget language
            </span>
        </div>
        <div class="sectionContentCol22">
            <span class="sectionContentPName">
            <xsl:element name="select">
                <xsl:attribute name="class">select</xsl:attribute>
                <xsl:attribute name="id">req_gadget_defaultLanguage</xsl:attribute>
                <xsl:attribute name="name">defaultLanguage</xsl:attribute>
                <xsl:element name="option">
                    <xsl:attribute name="value">all</xsl:attribute>
                    <xsl:if test="description/defaultLanguage = 'all'">
                        <xsl:attribute name="selected">true</xsl:attribute>
                    </xsl:if>All
                </xsl:element>
                <xsl:element name="option">
                    <xsl:attribute name="value">en</xsl:attribute>
                    <xsl:if test="description/defaultLanguage = 'en'">
                        <xsl:attribute name="selected">true</xsl:attribute>
                    </xsl:if>English
                </xsl:element>
                <xsl:element name="option">
                    <xsl:attribute name="value">fr</xsl:attribute>
                    <xsl:if test="description/defaultLanguage = 'fr'">
                        <xsl:attribute name="selected">true</xsl:attribute>
                    </xsl:if>French
                </xsl:element>
                <xsl:element name="option">
                    <xsl:attribute name="value">nl</xsl:attribute>
                    <xsl:if test="description/defaultLanguage = 'nl'">
                        <xsl:attribute name="selected">true</xsl:attribute>
                    </xsl:if>Dutch
                </xsl:element>
                <xsl:element name="option">
                    <xsl:attribute name="value">ar</xsl:attribute>
                    <xsl:if test="description/defaultLanguage = 'ar'">
                        <xsl:attribute name="selected">true</xsl:attribute>
                    </xsl:if>Arabic
                </xsl:element>
                <xsl:element name="option">
                    <xsl:attribute name="value">es</xsl:attribute>
                    <xsl:if test="description/defaultLanguage = 'es'">
                        <xsl:attribute name="selected">true</xsl:attribute>
                    </xsl:if>Spanish
                </xsl:element>
                <xsl:element name="option">
                    <xsl:attribute name="value">de</xsl:attribute>
                    <xsl:if test="description/defaultLanguage = 'de'">
                        <xsl:attribute name="selected">true</xsl:attribute>
                    </xsl:if>German
                </xsl:element>
                <xsl:element name="option">
                    <xsl:attribute name="value">it</xsl:attribute>
                    <xsl:if test="description/defaultLanguage = 'it'">
                        <xsl:attribute name="selected">true</xsl:attribute>
                    </xsl:if>Italian
                </xsl:element>
                <xsl:element name="option">
                    <xsl:attribute name="value">pt</xsl:attribute>
                    <xsl:if test="description/defaultLanguage = 'pt'">
                        <xsl:attribute name="selected">true</xsl:attribute>
                    </xsl:if>Portuguese
                </xsl:element>
                <xsl:element name="option">
                    <xsl:attribute name="value">no</xsl:attribute>
                    <xsl:if test="description/defaultLanguage = 'no'">
                        <xsl:attribute name="selected">true</xsl:attribute>
                    </xsl:if>Norwegian
                </xsl:element>
                <xsl:element name="option">
                    <xsl:attribute name="value">sv</xsl:attribute>
                    <xsl:if test="description/defaultLanguage = 'sv'">
                        <xsl:attribute name="selected">true</xsl:attribute>
                    </xsl:if>Swedish
                </xsl:element>
                <xsl:element name="option">
                    <xsl:attribute name="value">da</xsl:attribute>
                    <xsl:if test="description/defaultLanguage = 'da'">
                        <xsl:attribute name="selected">true</xsl:attribute>
                    </xsl:if>Danish
                </xsl:element>
            </xsl:element>
            </span>
        </div>
    </div>
    <div class="sectionContentBottom"></div>
    <xsl:element name="br"></xsl:element>
</xsl:template>

<!--
================================================================================
EDIT UGC NAMES
================================================================================
-->

<xsl:template name="editUgcNames">
    <xsl:param name="title"/>

    <!-- UGC NAMES SECTION SEPARATOR -->
    <div class="sectionSepHelp">
        <span class="sectionSepTitle"><xsl:value-of select="$title"/></span>
    </div>
    <div class="sectionContentTop2"></div>
    <!-- GADGET NAME -->
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionContentPName">
                Name
            </span>
        </div>
        <div class="sectionContentCol22">
            <span class="sectionContentPName">
            <xsl:element name="input">
                <xsl:attribute name="class">text</xsl:attribute>
                <xsl:attribute name="type">text</xsl:attribute>
                <xsl:attribute name="id">req_gadget_name</xsl:attribute>
                <xsl:attribute name="value">
                    <xsl:value-of select="description/name"/>
                </xsl:attribute>
            </xsl:element>
            </span>
        </div>
    </div>
    <!-- GADGET TTS NAME -->
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionContentPName">
                TTS sentence
            </span>
        </div>
        <div class="sectionContentCol22">
            <span class="sectionContentPName">
            <xsl:element name="input">
                <xsl:attribute name="class">text</xsl:attribute>
                <xsl:attribute name="type">text</xsl:attribute>
                <xsl:attribute name="id">req_gadget_ttsName</xsl:attribute>
                <xsl:attribute name="value">
                    <xsl:value-of select="description/ttsName"/>
                </xsl:attribute>
            </xsl:element>
            </span>
        </div>
    </div>
    <div class="sectionContentBottom"></div>
    <xsl:element name="br"></xsl:element>
</xsl:template>

<!--
================================================================================
SHOW PARAMETERS
================================================================================
-->
<xsl:template name="showParameters">
    <xsl:param name="title"/>

    <xsl:if test="count(parameters/*[visible='True']) > 0">
        <!-- PARMETERS SECTION SEPARATOR -->
        <div class="sectionSepParameters">
            <span class="sectionSepTitle"><xsl:value-of select="$title"/></span>
        </div>
        <!-- PARMETERS CONTENT -->
        <div class="sectionContentTop2"></div>
        <xsl:for-each select="parameters/*">
            <xsl:if test="visible = 'True'">
                <div class="sectionContentRowBox">
                    <xsl:element name="input">
                        <xsl:attribute name="class">text</xsl:attribute>
                        <xsl:attribute name="type">hidden</xsl:attribute>
                        <xsl:attribute name="id">req_param_<xsl:value-of select="name"/>_visible</xsl:attribute>
                        <xsl:attribute name="value">true</xsl:attribute>
                    </xsl:element>
                    <div class="sectionContentCol12">
                        <span class="sectionContentPName">
                            <xsl:value-of select="description"/>
                        </span>
                    </div>
                    <div class="sectionContentCol22">
                        <span class="sectionContentPName">
                        <xsl:call-template name="showParameter"/>
                        </span>
                    </div>
                </div>
            </xsl:if>
        </xsl:for-each>
        <div class="sectionContentBottom"></div>
        <xsl:element name="br"></xsl:element>
    </xsl:if>
</xsl:template>

<!--
================================================================================
SELECT PARAMETERS
================================================================================
-->
<xsl:template name="selectParameters">
    <xsl:param name="title"/>

    <xsl:if test="count(parameters/*[visible='True']) > 0">
        <!-- PARMETERS SECTION SEPARATOR -->
        <div class="sectionSepParameters">
            <span class="sectionSepTitle"><xsl:value-of select="$title"/></span>
        </div>
        <!-- PARMETERS CONTENT -->
        <div class="sectionContentTop2"></div>
        <xsl:for-each select="parameters/*">
            <xsl:if test="visible = 'True'">
                <div class="sectionContentRowBox">
                    <div class="sectionContentCol13">
                        <xsl:element name="input">
                            <xsl:attribute name="class">checkbox</xsl:attribute>
                            <xsl:attribute name="type">checkbox</xsl:attribute>
                            <xsl:attribute name="id">req_param_<xsl:value-of select="name"/>_visible</xsl:attribute>
                            <xsl:if test="selected = 'True'">
                                <xsl:attribute name="checked">true</xsl:attribute>
                            </xsl:if>
                        </xsl:element>
                    </div>
                    <div class="sectionContentCol23">
                        <span class="sectionContentPName">
                            <xsl:value-of select="description"/>
                        </span>
                    </div>
                    <div class="sectionContentCol33">
                        <span class="sectionContentPName">
                        <xsl:call-template name="showParameter"/>
                        </span>
                    </div>
                </div>
            </xsl:if>
        </xsl:for-each>
        <div class="sectionContentBottom"></div>
        <xsl:element name="br"></xsl:element>
    </xsl:if>
</xsl:template>

<!--
================================================================================
SHOW, VISIBILITY, ACTIVATE ALERTS
================================================================================
-->
<xsl:template name="svaAlerts">
    <xsl:param name="title"/>
    <xsl:param name="onlyShow"/>
    <xsl:param name="selectVisible"/>
    <xsl:param name="selectActivated"/>

    <!-- SECTION SEPARATOR -->
    <div class="sectionSepAlerts">
        <span class="sectionSepTitle"><xsl:value-of select="$title"/></span>
    </div>
    <!-- ALERTS CONTENT -->
    <xsl:for-each select="tasks/*">
        <div class="sectionElementDescBox">
            <xsl:if test="$onlyShow = 'false'">

                <xsl:if test="$selectVisible = 'true'">
                    <xsl:element name="input">
                        <xsl:attribute name="class">checkbox</xsl:attribute>
                        <xsl:attribute name="type">checkbox</xsl:attribute>
                        <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_visible</xsl:attribute>
                        <xsl:if test="selected = 'True'">
                            <xsl:attribute name="checked">true</xsl:attribute>
                        </xsl:if>
                    </xsl:element>
                    <xsl:element name="input">
                        <xsl:attribute name="class">text</xsl:attribute>
                        <xsl:attribute name="type">hidden</xsl:attribute>
                        <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_activated</xsl:attribute>
                        <xsl:attribute name="value">false</xsl:attribute>
                    </xsl:element>
                </xsl:if>
                <xsl:if test="$selectActivated = 'true'">
                    <xsl:element name="input">
                        <xsl:attribute name="class">checkbox</xsl:attribute>
                        <xsl:attribute name="type">checkbox</xsl:attribute>
                        <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_activated</xsl:attribute>
                        <xsl:if test="activated = 'True'">
                            <xsl:attribute name="checked">true</xsl:attribute>
                        </xsl:if>
                    </xsl:element>
                    <xsl:element name="input">
                        <xsl:attribute name="class">text</xsl:attribute>
                        <xsl:attribute name="type">hidden</xsl:attribute>
                        <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_visible</xsl:attribute>
                        <xsl:attribute name="value">true</xsl:attribute>
                    </xsl:element>
                </xsl:if>
                <span class="sectionElementDescNameCheck">
                    <xsl:value-of select="translatedName"/>
                </span>
            </xsl:if>
            <xsl:if test="$onlyShow = 'true'">
                <span class="sectionElementDescName">
                    <xsl:value-of select="translatedName"/>
                </span>
            </xsl:if>
            <xsl:element name="br"></xsl:element>
            <span class="sectionElementDescDescription">
                <xsl:value-of select="description"/>
            </span>
            <xsl:if test="dateVisible='True' or hoursBeginVisible='True' or hoursEndVisible='True' or delayVisible='True' or weekMaskVisible='True' or count(parameters/*[visible='True']) > 0">
                <div class="sectionContentTop"></div>
                <xsl:for-each select="parameters/*">
                    <xsl:if test="visible = 'True'">
                        <div class="sectionContentRowBox">
                            <xsl:element name="input">
                                <xsl:attribute name="class">text</xsl:attribute>
                                <xsl:attribute name="type">hidden</xsl:attribute>
                                <xsl:attribute name="id">req_param_<xsl:value-of select="name"/>_visible</xsl:attribute>
                                <xsl:attribute name="value">true</xsl:attribute>
                            </xsl:element>

                            <div class="sectionContentCol12">
                                <span class="sectionContentPName">
                                    <xsl:value-of select="description"/>
                                </span>
                            </div>
                            <div class="sectionContentCol22">
                                <span class="sectionContentPName">
                                    <xsl:call-template name="showParameter"/>
                                </span>
                            </div>
                        </div>
                    </xsl:if>
                </xsl:for-each>
                <xsl:if test="dateVisible = 'True'">
                    <div class="sectionContentRowBox">
                        <div class="sectionContentCol12">
                            <span class="sectionContentPName">
                                Date
                            </span>
                        </div>
                        <div class="sectionContentCol22">
                            <span class="sectionContentPName">
                                <xsl:call-template name="dateSelecter">
                                    <xsl:with-param name="date" select='date' />
                                </xsl:call-template>
                            </span>
                        </div>
                    </div>
                </xsl:if>
                <xsl:if test="hoursBeginVisible = 'True'">
                    <div class="sectionContentRowBox">
                        <div class="sectionContentCol12">
                            <span class="sectionContentPName">
                                Starting at
                            </span>
                        </div>
                        <div class="sectionContentCol22">
                            <span class="sectionContentPName">
                                <xsl:call-template name="timeSelecter">
                                    <xsl:with-param name="time" select='hoursBegin' />
                                    <xsl:with-param name="mask" select='hoursBeginMask' />
                                </xsl:call-template>
                            </span>
                        </div>
                    </div>
                </xsl:if>
                <xsl:if test="hoursEndVisible = 'True'">
                    <div class="sectionContentRowBox">
                        <div class="sectionContentCol12">
                            <span class="sectionContentPName">
                                Stopping at
                            </span>
                        </div>
                        <div class="sectionContentCol22">
                            <span class="sectionContentPName">
                                <xsl:call-template name="timeSelecter">
                                    <xsl:with-param name="time" select='hoursEnd' />
                                    <xsl:with-param name="mask" select='hoursEndMask' />
                                </xsl:call-template>
                            </span>
                        </div>
                    </div>
                </xsl:if>
                <xsl:if test="delayVisible = 'True'">
                    <div class="sectionContentRowBox">
                        <div class="sectionContentCol12">
                            <span class="sectionContentPName">
                                Frequency
                            </span>
                        </div>
                        <div class="sectionContentCol22">
                            <span class="sectionContentPName">
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
                        </div>
                    </div>
                </xsl:if>
                <xsl:if test="weekMaskVisible = 'True'">
                    <div class="sectionContentRowBox">
                        <div class="sectionContentCol12">
                            <span class="sectionContentPName">
                                My week
                            </span>
                        </div>
                        <div class="sectionContentCol22">
                            <span class="sectionContentPName">
                                <xsl:call-template name="weekMask">
                                    <xsl:with-param name="week_mask" select='weekMask' />
                                    <xsl:with-param name="type" select='weekMaskType' />
                                </xsl:call-template>
                            </span>
                        </div>
                    </div>
                </xsl:if>
                <div class="sectionContentBottom"></div>
            </xsl:if>
        </div>
    </xsl:for-each>
</xsl:template>

<!--
================================================================================
SHOW ON DEMAND
================================================================================
-->
<xsl:template name="showOnDemand">
    <xsl:param name="title"/>
    <xsl:param name="description"/>

    <xsl:choose>
    <xsl:when test="description/onDemandIsAble = 'true'">
        <div class="sectionElementDescBox">
            <xsl:element name="input">
                <xsl:attribute name="class">checkbox</xsl:attribute>
                <xsl:attribute name="type">checkbox</xsl:attribute>
                <xsl:attribute name="id">req_gadget_onDemandIsActivated</xsl:attribute>
                <xsl:if test="description/onDemandIsActivated = 'true'">
                    <xsl:attribute name="checked">true</xsl:attribute>
                </xsl:if>
            </xsl:element>
            <span class="sectionElementDescNameCheck"><xsl:value-of select="$title"/></span>
            <xsl:element name="br"></xsl:element>
            <span class="sectionElementDescDescription">
                <xsl:value-of select="$description"/>
            </span>
        </div>
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
    <xsl:element name="br"></xsl:element>
</xsl:template>

<!--
================================================================================
SELECT ON DEMAND
================================================================================
-->
<xsl:template name="selectOnDemand">
    <xsl:param name="title"/>
    <xsl:param name="description"/>

    <xsl:choose>
    <xsl:when test="defaultRunCommand = 'run'">
        <div class="sectionElementDescBox">
            <xsl:element name="input">
                <xsl:attribute name="class">checkbox</xsl:attribute>
                <xsl:attribute name="type">checkbox</xsl:attribute>
                <xsl:attribute name="id">req_gadget_onDemandIsAble</xsl:attribute>
                <xsl:if test="description/onDemandIsAble = 'true'">
                    <xsl:attribute name="checked">true</xsl:attribute>
                </xsl:if>
            </xsl:element>
            <span class="sectionElementDescNameCheck"><xsl:value-of select="$title"/></span>
            <xsl:element name="br"></xsl:element>
            <span class="sectionElementDescDescription">
                <xsl:value-of select="$description"/>
            </span>
        </div>
    </xsl:when>
    <xsl:otherwise>
        <xsl:element name="input">
            <xsl:attribute name="class">text</xsl:attribute>
            <xsl:attribute name="type">hidden</xsl:attribute>
            <xsl:attribute name="id">req_gadget_onDemandIsAble</xsl:attribute>
            <xsl:attribute name="value">false</xsl:attribute>
        </xsl:element>
    </xsl:otherwise>
    </xsl:choose>
    <xsl:element name="br"></xsl:element>
</xsl:template>

<!--
================================================================================
SHOW HELP
================================================================================
-->
<xsl:template name="showHelp">
    <xsl:param name="title"/>

    <div class="sectionSepHelp">
        <span class="sectionSepTitle"><xsl:value-of select="$title"/></span>
    </div>
    <!-- HELP BOX -->
    <div class="sectionContentTop2">
        <div id="helpBox" class="descriptionHelpBox">
            <textarea id="req_helpContent" rows="19" cols="43"  style="visibility:hidden;">
                <xsl:value-of select="description/helpFile"/>
            </textarea>
        </div>
    </div>
    <div class="sectionContentBottom"></div>
    <xsl:element name="br"></xsl:element>
</xsl:template>

<!--
================================================================================
EDIT HELP
================================================================================
-->
<xsl:template name="editHelp">
    <xsl:param name="title"/>

    <div class="sectionSepHelp">
        <span class="sectionSepTitle"><xsl:value-of select="$title"/></span>
    </div>
    <!-- HELP BOX -->
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Preview of the help content
        </span>
    </div>
    <div class="sectionContentTop"></div>
    <div class="sectionContentTop2">
        <div id="helpBox" class="descriptionHelpBox">
            <textarea id="req_helpContent" style="visibility:hidden;">
                <xsl:value-of select="description/helpFile"/>
            </textarea>
        </div>
    </div>
    <div class="sectionContentBottom"></div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Edit the help in markup language
        </span>
    </div>
    <div class="sectionContentTop"></div>
    <div class="sectionContentTop2">
        <textarea id="req_helpContent" rows="19" cols="43" onkeyup="javascript:fillHelpBox();" style="margin-left:17px;">
            <xsl:value-of select="description/helpFile"/>
        </textarea>
    </div>
    <div class="sectionContentBottom"></div>
    <xsl:element name="br"></xsl:element>
</xsl:template>

<!--
================================================================================
SHOW COMMANDS
================================================================================
-->
<xsl:template name="showCommands">
    <xsl:param name="title"/>
    <xsl:param name="commandType"/>

    <!-- COMMANDS SECTION SEPARATOR -->
    <div class="sectionSepCommands">
        <span class="sectionSepTitle"><xsl:value-of select="$title"/></span>
    </div>
    <!-- COMMANDS CONTENT -->
    <xsl:for-each select="commands/*">
        <div class="sectionContentRowBox">
            <div class="sectionContentCol12">
                <span class="sectionElementColName">
                    <xsl:value-of select="name"/>
                </span>
                <xsl:element name="br"></xsl:element>
                <span class="sectionElementColDescription">
                    <xsl:value-of select="description"/>
                </span>
            </div>
            <div class="sectionContentCol22">
                <xsl:element name="a">
                    <xsl:attribute name="class">buttonStart</xsl:attribute>
                    <xsl:if test="$commandType = 'plugin'">
                        <xsl:attribute name="onclick">javascript:startPlugin("<xsl:value-of select="name"/>");return false;</xsl:attribute>
                    </xsl:if>
                    <xsl:if test="$commandType = 'gadget'">
                        <xsl:attribute name="onclick">javascript:startGadget("<xsl:value-of select="name"/>");return false;</xsl:attribute>
                    </xsl:if>
                    <xsl:if test="$commandType = 'ugc'">
                        <xsl:attribute name="onclick">javascript:startUgc("<xsl:value-of select="name"/>");return false;</xsl:attribute>
                    </xsl:if>
                    <xsl:attribute name="href"></xsl:attribute>Start
                </xsl:element>
                <xsl:element name="a">
                    <xsl:attribute name="class">buttonStop</xsl:attribute>
                    <xsl:if test="$commandType = 'plugin'">
                        <xsl:attribute name="onclick">javascript:stopPlugin();return false;</xsl:attribute>
                    </xsl:if>
                    <xsl:if test="$commandType = 'gadget'">
                        <xsl:attribute name="onclick">javascript:stopGadget();return false;</xsl:attribute>
                    </xsl:if>
                    <xsl:if test="$commandType = 'ugc'">
                        <xsl:attribute name="onclick">javascript:stopUgc();return false;</xsl:attribute>
                    </xsl:if>
                    <xsl:attribute name="href"></xsl:attribute>Stop
                </xsl:element>
            </div>
        </div>
    </xsl:for-each>
    <div class="sectionContentBottom"></div>
    <xsl:element name="br"></xsl:element>
</xsl:template>

<!--
================================================================================
SHOW MISC PLUGIN
================================================================================
-->
<xsl:template name="showMiscPlugin">
    <xsl:param name="title"/>

    <!-- MISCELLANEOUS SECTION SEPARATOR -->
    <div class="sectionSepHelp">
        <span class="sectionSepTitle"><xsl:value-of select="$title"/></span>
    </div>
    <!-- MISCELLANEOUS INFORMATIONS -->
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Plugin uuid
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/uuid"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Plugin versions
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/version"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Plugin temporary path
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/workingPath"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Plugin SCP file
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/scpFile"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Plugin target platform
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/platform"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Plugin default run command
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="defaultRunCommand"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Plugin default check command
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="defaultCheckCommand"/>
        </span>
    </div>
    <xsl:element name="br"></xsl:element>
</xsl:template>

<!--
================================================================================
SHOW MISC GADGET
================================================================================
-->
<xsl:template name="showMiscGadget">
    <xsl:param name="title"/>

    <!-- MISCELLANEOUS SECTION SEPARATOR -->
    <div class="sectionSepHelp">
        <span class="sectionSepTitle"><xsl:value-of select="$title"/></span>
    </div>
    <!-- MISCELLANEOUS INFORMATIONS -->
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Parent plugin name
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/parentPluginName"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Parent plugin uuid
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/parentPluginUuid"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Gadget uuid
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/uuid"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Gadget versions
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/version"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Gadget temporary path
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/workingPath"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Gadget SCG file
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/scgFile"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Gadget target platform
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/platform"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Gadget category
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/category"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Gadget default language
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/defaultLanguage"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Gadget default run command
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="defaultRunCommand"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Gadget default check command
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="defaultCheckCommand"/>
        </span>
    </div>
    <xsl:element name="br"></xsl:element>
</xsl:template>

<!--
================================================================================
SHOW MISC UGC
================================================================================
-->
<xsl:template name="showMiscUgc">
    <xsl:param name="title"/>

    <!-- MISCELLANEOUS SECTION SEPARATOR -->
    <div class="sectionSepHelp">
        <span class="sectionSepTitle"><xsl:value-of select="$title"/></span>
    </div>
    <!-- MISCELLANEOUS INFORMATIONS -->
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Parent plugin name
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/parentPluginName"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Parent plugin uuid
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/parentPluginUuid"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Parent gadget name
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/parentGadgetName"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Parent gadget uuid
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/parentGadgetUuid"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            UGC uuid
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/uuid"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            UGC file
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/ugcFile"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Category
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/category"/>
        </span>
    </div>
    <div class="sectionElementDescBox">
        <span class="sectionElementDescName">
            Default language
        </span>
        <xsl:element name="br"></xsl:element>
        <span class="sectionElementDescDescription">
            <xsl:value-of select="description/defaultLanguage"/>
        </span>
    </div>
    <xsl:element name="br"></xsl:element>
</xsl:template>

<!--
================================================================================
GADGET TOOL BOX
================================================================================
-->
<xsl:template name="showGadgetToolBox">
    <xsl:param name="title"/>
    <xsl:param name="showApply"/>
    <xsl:param name="showGenerate"/>
    <xsl:param name="noTitle"/>

    <xsl:if test="$noTitle = 'false'">
        <div class="sectionSepCommands">
            <span class="sectionSepTitle"><xsl:value-of select="$title"/></span>
        </div>
    </xsl:if>
    <xsl:if test="$noTitle = 'true'">
        <div class="sectionContentTop"></div>
    </xsl:if>
    <!-- GADGET TOOL BOX CONTENT -->
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionElementColSingle">
                Show the gadget preview
            </span>
        </div>
        <div class="sectionContentCol22">
            <xsl:element name="a">
                <xsl:attribute name="class">button170</xsl:attribute>
                <xsl:attribute name="href">javascript:showPreview()</xsl:attribute>Preview
            </xsl:element>
        </div>
    </div>
    <xsl:if test="$showGenerate = 'true'">
        <div class="sectionContentRowBox">
            <div class="sectionContentCol12">
                <span class="sectionElementColSingle">
                    Generate the gadget
                </span>
            </div>
            <div class="sectionContentCol22">
                <xsl:element name="a">
                    <xsl:attribute name="class">button170</xsl:attribute>
                    <xsl:attribute name="href">javascript:generateGadget()</xsl:attribute>Generate
                </xsl:element>
            </div>
        </div>
    </xsl:if>
    <xsl:if test="$showApply = 'true'">
        <div class="sectionContentRowBox">
            <div class="sectionContentCol12">
                <span class="sectionElementColSingle">
                    Apply the modifications
                </span>
            </div>
            <div class="sectionContentCol22">
                <xsl:element name="a">
                    <xsl:attribute name="class">button170</xsl:attribute>
                    <xsl:attribute name="href">javascript:applyGadget()</xsl:attribute>Apply
                </xsl:element>
            </div>
        </div>
    </xsl:if>
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12"></div>
        <div class="sectionContentCol22">
            <xsl:element name="a">
                <xsl:attribute name="class">button170</xsl:attribute>
                <xsl:attribute name="href">javascript:history.back()</xsl:attribute>Go Back
            </xsl:element>
        </div>
    </div>
    <div class="sectionContentBottom"></div>
    <xsl:element name="br"></xsl:element>
</xsl:template>

<!--
================================================================================
PLUGIN TOOL BOX : MAKE A GADGET
================================================================================
-->
<xsl:template name="showPluginToolBoxMakeGadget">
    <xsl:param name="title"/>
    <xsl:param name="noTitle"/>

    <xsl:if test="$noTitle = 'false'">
        <div class="sectionSepCommands">
            <span class="sectionSepTitle"><xsl:value-of select="$title"/></span>
        </div>
    </xsl:if>
    <xsl:if test="$noTitle = 'true'">
        <div class="sectionContentTop"></div>
    </xsl:if>
    <!-- GADGET TOOL BOX CONTENT -->
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionElementColSingle">
                Download the plugin
            </span>
        </div>
        <div class="sectionContentCol22">
            <xsl:element name="a">
                <xsl:attribute name="class">button170</xsl:attribute>
                <xsl:attribute name="href">
                    <xsl:value-of select="description/scpUrl"/>
                </xsl:attribute>Download
            </xsl:element>
        </div>
    </div>
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionElementColSingle">
                Make a new gadget from<xsl:element name="br"></xsl:element>
                this plugin
            </span>
        </div>
        <div class="sectionContentCol22">
            <xsl:element name="a">
                <xsl:attribute name="class">button170</xsl:attribute>
                <xsl:attribute name="onclick">makeNewGadget();return false;</xsl:attribute>
                <xsl:attribute name="href"></xsl:attribute>New gadget
            </xsl:element>
        </div>
    </div>
    <div class="sectionContentBottom"></div>
    <xsl:element name="br"></xsl:element>
</xsl:template>

<!--
================================================================================
GADGET TOOL BOX : EDITING GADGET
================================================================================
-->
<xsl:template name="showGadgetToolBoxEditingGadget">
    <xsl:param name="title"/>
    <xsl:param name="noTitle"/>

    <xsl:if test="$noTitle = 'false'">
        <div class="sectionSepCommands">
            <span class="sectionSepTitle"><xsl:value-of select="$title"/></span>
        </div>
    </xsl:if>
    <xsl:if test="$noTitle = 'true'">
        <div class="sectionContentTop"></div>
    </xsl:if>
    <!-- GADGET TOOL BOX CONTENT -->
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionElementColSingle">
                Download the gadget
            </span>
        </div>
        <div class="sectionContentCol22">
            <xsl:element name="a">
                <xsl:attribute name="class">button170</xsl:attribute>
                <xsl:attribute name="href">
                    <xsl:value-of select="description/scgUrl"/>
                </xsl:attribute>Download
            </xsl:element>
        </div>
    </div>
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionElementColSingle">
                Duplicate the gadget
            </span>
        </div>
        <div class="sectionContentCol22">
            <xsl:element name="a">
                <xsl:attribute name="class">button170</xsl:attribute>
                <xsl:attribute name="onclick">duplicateGadget();return false;</xsl:attribute>
                <xsl:attribute name="href"></xsl:attribute>Duplicate
            </xsl:element>
        </div>
    </div>
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionElementColSingle">
                Edit the gadget
            </span>
        </div>
        <div class="sectionContentCol22">
            <xsl:element name="a">
                <xsl:attribute name="class">button170</xsl:attribute>
                <xsl:attribute name="onclick">editGadget();return false;</xsl:attribute>
                <xsl:attribute name="href"></xsl:attribute>Edit
            </xsl:element>
        </div>
    </div>
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionElementColSingle">
                Delete the gadget
            </span>
        </div>
        <div class="sectionContentCol22">
            <xsl:element name="a">
                <xsl:attribute name="class">button170</xsl:attribute>
                <xsl:attribute name="onclick">deleteGadget();return false;</xsl:attribute>
                <xsl:attribute name="href"></xsl:attribute>Delete
            </xsl:element>
        </div>
    </div>
    <div class="sectionContentBottom"></div>
    <xsl:element name="br"></xsl:element>
</xsl:template>

<!--
================================================================================
GADGET TOOL BOX : EDITING UGC
================================================================================
-->
<xsl:template name="showGadgetToolBoxEditingUgc">
    <xsl:param name="title"/>
    <xsl:param name="noTitle"/>

    <xsl:if test="$noTitle = 'false'">
        <div class="sectionSepCommands">
            <span class="sectionSepTitle"><xsl:value-of select="$title"/></span>
        </div>
    </xsl:if>
    <xsl:if test="$noTitle = 'true'">
        <div class="sectionContentTop"></div>
    </xsl:if>
    <!-- GADGET TOOL BOX CONTENT -->
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionElementColSingle">
                Download the UGC gadget
            </span>
        </div>
        <div class="sectionContentCol22">
            <xsl:element name="a">
                <xsl:attribute name="class">button170</xsl:attribute>
                <xsl:attribute name="href">
                    <xsl:value-of select="description/ugcUrl"/>
                </xsl:attribute>Download
            </xsl:element>
        </div>
    </div>
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionElementColSingle">
                Duplicate the UGC gadget
            </span>
        </div>
        <div class="sectionContentCol22">
            <xsl:element name="a">
                <xsl:attribute name="class">button170</xsl:attribute>
                <xsl:attribute name="onclick">duplicateUgc();return false;</xsl:attribute>
                <xsl:attribute name="href"></xsl:attribute>Duplicate
            </xsl:element>
        </div>
    </div>
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionElementColSingle">
                Apply configuration
            </span>
        </div>
        <div class="sectionContentCol22">
            <xsl:element name="a">
                <xsl:attribute name="class">button170</xsl:attribute>
                <xsl:attribute name="onclick">applyUgcConfiguration();return false;</xsl:attribute>
                <xsl:attribute name="href"></xsl:attribute>Apply
            </xsl:element>
        </div>
    </div>
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12">
            <span class="sectionElementColSingle">
                Delete the UGC gadget
            </span>
        </div>
        <div class="sectionContentCol22">
            <xsl:element name="a">
                <xsl:attribute name="class">button170</xsl:attribute>
                <xsl:attribute name="onclick">deleteUgc();return false;</xsl:attribute>
                <xsl:attribute name="href"></xsl:attribute>Delete
            </xsl:element>
        </div>
    </div>
    <div class="sectionContentBottom"></div>
    <xsl:element name="br"></xsl:element>
</xsl:template>

<!--
================================================================================
SHOW GO BACK
================================================================================
-->
<xsl:template name="showGoBack">
    <div class="sectionContentTop"></div>
    <div class="sectionContentRowBox">
        <div class="sectionContentCol12"></div>
        <div class="sectionContentCol22">
            <xsl:element name="a">
                <xsl:attribute name="class">button170</xsl:attribute>
                <xsl:attribute name="href">javascript:history.back()</xsl:attribute>Go Back
            </xsl:element>
        </div>
    </div>
    <div class="sectionContentBottom"></div>
    <xsl:element name="br"></xsl:element>
</xsl:template>

</xsl:stylesheet>