<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">

    <!-- OPTIONS LOOP -->
    <xsl:template name="optionsLoop">
        <xsl:param name="value"/>
        <xsl:param name="counter"/>
        <xsl:param name="max"/>
        <xsl:element name="option">
            <xsl:attribute name="value">
                <xsl:value-of select="$counter"/>
            </xsl:attribute>
            <xsl:if test="$counter = $value">
                <xsl:attribute name="selected">true</xsl:attribute>
            </xsl:if>
            <xsl:value-of select="$counter"/>
        </xsl:element>
        <xsl:if test="$counter &lt; $max">
            <xsl:call-template name="optionsLoop">
                <xsl:with-param name="value" select="$value"/>
                <xsl:with-param name="counter" select="$counter + 1"/>
                <xsl:with-param name="max" select="$max"/>
            </xsl:call-template>
        </xsl:if>
    </xsl:template>

<!-- TIME RULES -->

    <!-- HOUR SELECTER -->
    <xsl:template name="hourSelecter">
        <xsl:param name="time"/>
        <xsl:param name="mask"/>
        <xsl:if test="$mask/hour = 'True'">
            <xsl:element name="select">
                <xsl:attribute name="class">selectTime</xsl:attribute>
                <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_<xsl:value-of select="name($time)"/>_hour</xsl:attribute>
                <xsl:call-template name="optionsLoop">
                    <xsl:with-param name="value" select="$time/hour"/>
                    <xsl:with-param name="counter" select="0"/>
                    <xsl:with-param name="max" select="23"/>
                </xsl:call-template>
            </xsl:element> H
        </xsl:if>
    </xsl:template>

    <!-- MINUTE SELECTER -->
    <xsl:template name="minuteSelecter">
        <xsl:param name="time"/>
        <xsl:param name="mask"/>
        <xsl:if test="$mask/minute = 'True'">
            <xsl:element name="select">
                <xsl:attribute name="class">selectTime</xsl:attribute>
                <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_<xsl:value-of select="name($time)"/>_minute</xsl:attribute>
                <xsl:call-template name="optionsLoop">
                    <xsl:with-param name="value" select="$time/minute"/>
                    <xsl:with-param name="counter" select="0"/>
                    <xsl:with-param name="max" select="59"/>
                </xsl:call-template>
            </xsl:element> M
        </xsl:if>
    </xsl:template>

    <!-- SECOND SELECTER -->
    <xsl:template name="secondSelecter">
        <xsl:param name="time"/>
        <xsl:param name="mask"/>
        <xsl:if test="$mask/second = 'True'">
            <xsl:element name="select">
                <xsl:attribute name="class">selectTime</xsl:attribute>
                <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_<xsl:value-of select="name($time)"/>_second</xsl:attribute>
                <xsl:call-template name="optionsLoop">
                    <xsl:with-param name="value" select="$time/second"/>
                    <xsl:with-param name="counter" select="0"/>
                    <xsl:with-param name="max" select="59"/>
                </xsl:call-template>
            </xsl:element> S
        </xsl:if>
    </xsl:template>

    <!-- QUARTERS (15/30/60) SELECTER -->
    <xsl:template name="quartersSelecter">
        <xsl:param name="time"/>
        <xsl:element name="select">
            <xsl:attribute name="class">select</xsl:attribute>
            <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_<xsl:value-of select="name($time)"/>_minute</xsl:attribute>
            <xsl:element name="option">
                <xsl:attribute name="value">15</xsl:attribute>
                <xsl:if test="$time/minute = '15'">
                    <xsl:attribute name="selected">true</xsl:attribute>
                </xsl:if><xsl:value-of select="../../../translations/quart_hours"/>
            </xsl:element>
            <xsl:element name="option">
                <xsl:attribute name="value">30</xsl:attribute>
                <xsl:if test="$time/minute = '30'">
                    <xsl:attribute name="selected">true</xsl:attribute>
                </xsl:if><xsl:value-of select="../../../translations/half_hours"/>
            </xsl:element>
            <xsl:element name="option">
                <xsl:attribute name="value">60</xsl:attribute>
                <xsl:if test="$time/minute = '0'">
                    <xsl:if test="$time/hour = '1'">
                        <xsl:attribute name="selected">true</xsl:attribute>
                    </xsl:if>
                </xsl:if><xsl:value-of select="../../../translations/full_hours"/>
            </xsl:element>
        </xsl:element>
    </xsl:template>

    <!-- FREQUENCY (CRAZY/OFTEN/NORMAL/RARELY) SELECTER -->
    <xsl:template name="frequencySelecter">
        <xsl:param name="time"/>
        <xsl:element name="select">
            <xsl:attribute name="class">select</xsl:attribute>
            <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_<xsl:value-of select="name($time)"/>_minute</xsl:attribute>
            <xsl:element name="option">
                <xsl:attribute name="value">1</xsl:attribute>
                <xsl:if test="$time/minute = '1'">
                    <xsl:attribute name="selected">true</xsl:attribute>
                </xsl:if><xsl:value-of select="../../../translations/crazy"/>
            </xsl:element>
            <xsl:element name="option">
                <xsl:attribute name="value">5</xsl:attribute>
                <xsl:if test="$time/minute = '5'">
                    <xsl:attribute name="selected">true</xsl:attribute>
                </xsl:if><xsl:value-of select="../../../translations/often"/>
            </xsl:element>
            <xsl:element name="option">
                <xsl:attribute name="value">15</xsl:attribute>
                <xsl:if test="$time/minute = '15'">
                    <xsl:attribute name="selected">true</xsl:attribute>
                </xsl:if><xsl:value-of select="../../../translations/normal"/>
            </xsl:element>
            <xsl:element name="option">
                <xsl:attribute name="value">60</xsl:attribute>
                <xsl:if test="$time/minute = '0'">
                    <xsl:if test="$time/hour = '1'">
                        <xsl:attribute name="selected">true</xsl:attribute>
                    </xsl:if>
                </xsl:if><xsl:value-of select="../../../translations/rarely"/>
            </xsl:element>
        </xsl:element>
    </xsl:template>

    <!-- TIME SELECTER -->
    <xsl:template name="timeSelecter">
        <xsl:param name="time"/>
        <xsl:param name="mask"/>
        <xsl:call-template name="hourSelecter">
            <xsl:with-param name="time" select='$time' />
            <xsl:with-param name="mask" select='$mask' />
        </xsl:call-template>
        <xsl:call-template name="minuteSelecter">
            <xsl:with-param name="time" select='$time' />
            <xsl:with-param name="mask" select='$mask' />
        </xsl:call-template>
        <xsl:call-template name="secondSelecter">
            <xsl:with-param name="time" select='$time' />
            <xsl:with-param name="mask" select='$mask' />
        </xsl:call-template>
    </xsl:template>

<!-- DATE RULES -->

    <!-- YEAR SELECTER -->
    <xsl:template name="yearSelecter">
        <xsl:param name="date"/>
        <xsl:element name="select">
            <xsl:attribute name="class">selectYear</xsl:attribute>
            <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_date_year</xsl:attribute>
            <xsl:call-template name="optionsLoop">
                <xsl:with-param name="value" select="date/year"/>
                <xsl:with-param name="counter" select="2009"/>
                <xsl:with-param name="max" select="2050"/>
            </xsl:call-template>
        </xsl:element> /
    </xsl:template>

    <!-- MONTH SELECTER -->
    <xsl:template name="monthSelecter">
        <xsl:param name="date"/>
        <xsl:element name="select">
            <xsl:attribute name="class">selectTime</xsl:attribute>
            <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_date_month</xsl:attribute>
            <xsl:call-template name="optionsLoop">
                <xsl:with-param name="value" select="date/month"/>
                <xsl:with-param name="counter" select="1"/>
                <xsl:with-param name="max" select="12"/>
            </xsl:call-template>
        </xsl:element> /
    </xsl:template>

    <!-- DAY SELECTER -->
    <xsl:template name="daySelecter">
        <xsl:param name="date"/>
        <xsl:element name="select">
            <xsl:attribute name="class">selectTime</xsl:attribute>
            <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_date_day</xsl:attribute>
            <xsl:call-template name="optionsLoop">
                <xsl:with-param name="value" select="date/day"/>
                <xsl:with-param name="counter" select="1"/>
                <xsl:with-param name="max" select="31"/>
            </xsl:call-template>
        </xsl:element>
    </xsl:template>

    <!-- DATE SELECTER -->
    <xsl:template name="dateSelecter">
        <xsl:param name="date"/>
        <xsl:call-template name="yearSelecter">
            <xsl:with-param name="date" select='$date' />
        </xsl:call-template>
        <xsl:call-template name="monthSelecter">
            <xsl:with-param name="date" select='$date' />
        </xsl:call-template>
        <xsl:call-template name="daySelecter">
            <xsl:with-param name="date" select='$date' />
        </xsl:call-template>
    </xsl:template>

<!-- WEEK RULES -->
    <xsl:template name="weekMask">
        <xsl:param name="week_mask"/>
        <xsl:param name="type"/>
        <!-- Week mask type is 'flat' show radio buttons -->
        <xsl:if test="$type = 'flat'">
            <!-- Monday -->
            <xsl:element name="input">
                <xsl:attribute name="class">checkbox</xsl:attribute>
                <xsl:attribute name="type">checkbox</xsl:attribute>
                <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_weekMask_day_0</xsl:attribute>
                <xsl:if test="$week_mask/day_0 = 'True'">
                    <xsl:attribute name="checked">true</xsl:attribute>
                </xsl:if>
            </xsl:element> <xsl:value-of select="../../../translations/monday"/>
            <xsl:element name="br"></xsl:element>
            <!-- Tuesday -->
            <xsl:element name="input">
                <xsl:attribute name="class">checkbox</xsl:attribute>
                <xsl:attribute name="type">checkbox</xsl:attribute>
                <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_weekMask_day_1</xsl:attribute>
                <xsl:if test="$week_mask/day_1 = 'True'">
                    <xsl:attribute name="checked">true</xsl:attribute>
                </xsl:if>
            </xsl:element> <xsl:value-of select="../../../translations/tuesday"/>
            <xsl:element name="br"></xsl:element>
            <!-- Wednesday -->
            <xsl:element name="input">
                <xsl:attribute name="class">checkbox</xsl:attribute>
                <xsl:attribute name="type">checkbox</xsl:attribute>
                <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_weekMask_day_2</xsl:attribute>
                <xsl:if test="$week_mask/day_2 = 'True'">
                    <xsl:attribute name="checked">true</xsl:attribute>
                </xsl:if>
            </xsl:element> <xsl:value-of select="../../../translations/wednesday"/>
            <xsl:element name="br"></xsl:element>
            <!-- Thursday -->
            <xsl:element name="input">
                <xsl:attribute name="class">checkbox</xsl:attribute>
                <xsl:attribute name="type">checkbox</xsl:attribute>
                <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_weekMask_day_3</xsl:attribute>
                <xsl:if test="$week_mask/day_3 = 'True'">
                    <xsl:attribute name="checked">true</xsl:attribute>
                </xsl:if>
            </xsl:element> <xsl:value-of select="../../../translations/thursday"/>
            <xsl:element name="br"></xsl:element>
            <!-- Friday -->
            <xsl:element name="input">
                <xsl:attribute name="class">checkbox</xsl:attribute>
                <xsl:attribute name="type">checkbox</xsl:attribute>
                <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_weekMask_day_4</xsl:attribute>
                <xsl:if test="$week_mask/day_4 = 'True'">
                    <xsl:attribute name="checked">true</xsl:attribute>
                </xsl:if>
            </xsl:element> <xsl:value-of select="../../../translations/friday"/>
            <xsl:element name="br"></xsl:element>
            <!-- Saturday -->
            <xsl:element name="input">
                <xsl:attribute name="class">checkbox</xsl:attribute>
                <xsl:attribute name="type">checkbox</xsl:attribute>
                <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_weekMask_day_5</xsl:attribute>
                <xsl:if test="$week_mask/day_5 = 'True'">
                    <xsl:attribute name="checked">true</xsl:attribute>
                </xsl:if>
            </xsl:element> <xsl:value-of select="../../../translations/saturday"/>
            <xsl:element name="br"></xsl:element>
            <!-- Sunday -->
            <xsl:element name="input">
                <xsl:attribute name="class">checkbox</xsl:attribute>
                <xsl:attribute name="type">checkbox</xsl:attribute>
                <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_weekMask_day_6</xsl:attribute>
                <xsl:if test="$week_mask/day_6 = 'True'">
                    <xsl:attribute name="checked">true</xsl:attribute>
                </xsl:if>
            </xsl:element> <xsl:value-of select="../../../translations/sunday"/>
        </xsl:if>
        <!-- Week mask type is 'weekpart' show checkbox -->
        <xsl:if test="$type = 'weekpart'">
            <xsl:element name="input">
                <xsl:attribute name="type">radio</xsl:attribute>
                <xsl:attribute name="class">checkbox</xsl:attribute>
                <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_weekMask_weekpart</xsl:attribute>
                <xsl:attribute name="name">week_<xsl:value-of select="name"/></xsl:attribute>
                <xsl:attribute name="value">0</xsl:attribute>
                <xsl:attribute name="checked">true</xsl:attribute>
                <xsl:if test="$week_mask/day_0 = 'True' and $week_mask/day_1 = 'True' and $week_mask/day_2 = 'True' and $week_mask/day_3 = 'True' and $week_mask/day_4 = 'True' and $week_mask/day_5 = 'True' and $week_mask/day_6 = 'True'">
                    <xsl:attribute name="checked">true</xsl:attribute>
                </xsl:if>
            </xsl:element> <xsl:value-of select="../../../translations/all_days"/>
            <xsl:element name="br"></xsl:element>
            <xsl:element name="input">
                <xsl:attribute name="type">radio</xsl:attribute>
                <xsl:attribute name="class">checkbox</xsl:attribute>
                <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_weekMask_weekpart</xsl:attribute>
                <xsl:attribute name="name">week_<xsl:value-of select="name"/></xsl:attribute>
                <xsl:attribute name="value">1</xsl:attribute>
                <xsl:if test="$week_mask/day_0 = 'True' and $week_mask/day_1 = 'True' and $week_mask/day_2 = 'True' and $week_mask/day_3 = 'True' and $week_mask/day_4 = 'True' and $week_mask/day_5 = 'False' and $week_mask/day_6 = 'False'">
                    <xsl:attribute name="checked">true</xsl:attribute>
                </xsl:if>
            </xsl:element> <xsl:value-of select="../../../translations/working_days"/>
            <xsl:element name="br"></xsl:element>
            <xsl:element name="input">
                <xsl:attribute name="type">radio</xsl:attribute>
                <xsl:attribute name="class">checkbox</xsl:attribute>
                <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_weekMask_weekpart</xsl:attribute>
                <xsl:attribute name="name">week_<xsl:value-of select="name"/></xsl:attribute>
                <xsl:attribute name="value">2</xsl:attribute>
                <xsl:if test="$week_mask/day_0 = 'False' and $week_mask/day_1 = 'False' and $week_mask/day_2 = 'False' and $week_mask/day_3 = 'False' and $week_mask/day_4 = 'False' and $week_mask/day_5 = 'True' and $week_mask/day_6 = 'True'">
                    <xsl:attribute name="checked">true</xsl:attribute>
                </xsl:if>
            </xsl:element> <xsl:value-of select="../../../translations/weekend"/>
        </xsl:if>
        <!-- Week mask type is 'exclusive' show selecter -->
        <xsl:if test="$type = 'exclusive'">
            <xsl:element name="select">
                <xsl:attribute name="class">select</xsl:attribute>
                <xsl:attribute name="id">req_task_<xsl:value-of select="name"/>_weekMask_exclusive</xsl:attribute>
                <xsl:element name="option">
                    <xsl:attribute name="value">0</xsl:attribute>
                    <xsl:attribute name="selected">true</xsl:attribute>
                    <xsl:value-of select="../../../translations/monday"/>
                </xsl:element>
                <xsl:element name="option">
                    <xsl:attribute name="value">1</xsl:attribute>
                    <xsl:value-of select="../../../translations/tuesday"/>
                </xsl:element>
                <xsl:element name="option">
                    <xsl:attribute name="value">2</xsl:attribute>
                    <xsl:value-of select="../../../translations/wednesday"/>
                </xsl:element>
                <xsl:element name="option">
                    <xsl:attribute name="value">3</xsl:attribute>
                    <xsl:value-of select="../../../translations/thursday"/>
                </xsl:element>
                <xsl:element name="option">
                    <xsl:attribute name="value">4</xsl:attribute>
                    <xsl:value-of select="../../../translations/friday"/>
                </xsl:element>
                <xsl:element name="option">
                    <xsl:attribute name="value">5</xsl:attribute>
                    <xsl:value-of select="../../../translations/saturday"/>
                </xsl:element>
                <xsl:element name="option">
                    <xsl:attribute name="value">6</xsl:attribute>
                    <xsl:value-of select="../../../translations/sunday"/>
                </xsl:element>
            </xsl:element>
        </xsl:if>
    </xsl:template>

</xsl:stylesheet>