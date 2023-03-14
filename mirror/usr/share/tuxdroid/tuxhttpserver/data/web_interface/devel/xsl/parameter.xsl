<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">

    <!-- SHOW PARAMETER -->
    <xsl:template name="showParameter">
        <!-- Parameter is "string" then show it as "text" -->
        <xsl:if test="type = 'string'">
            <xsl:element name="input">
                <xsl:attribute name="class">text</xsl:attribute>
                <xsl:attribute name="type">text</xsl:attribute>
                <xsl:attribute name="id">req_param_<xsl:value-of select="name"/>_value</xsl:attribute>
                <xsl:attribute name="name">
                    <xsl:value-of select="name"/>
                </xsl:attribute>
                <xsl:attribute name="value">
                    <xsl:value-of select="defaultValue"/>
                </xsl:attribute>
                <xsl:attribute name="size">20</xsl:attribute>
            </xsl:element>
        </xsl:if>
        <!-- Parameter is "file" then show it as "text" -->
        <xsl:if test="type = 'file'">
            <xsl:element name="input">
                <xsl:attribute name="class">text</xsl:attribute>
                <xsl:attribute name="type">text</xsl:attribute>
                <xsl:attribute name="id">req_param_<xsl:value-of select="name"/>_value</xsl:attribute>
                <xsl:attribute name="name">
                    <xsl:value-of select="name"/>
                </xsl:attribute>
                <xsl:attribute name="value">
                    <xsl:value-of select="defaultValue"/>
                </xsl:attribute>
                <xsl:attribute name="size">20</xsl:attribute>
            </xsl:element>
        </xsl:if>
        <!-- Parameter is "directory" then show it as "text" -->
        <xsl:if test="type = 'directory'">
            <xsl:element name="input">
                <xsl:attribute name="class">text</xsl:attribute>
                <xsl:attribute name="type">text</xsl:attribute>
                <xsl:attribute name="id">req_param_<xsl:value-of select="name"/>_value</xsl:attribute>
                <xsl:attribute name="name">
                    <xsl:value-of select="name"/>
                </xsl:attribute>
                <xsl:attribute name="value">
                    <xsl:value-of select="defaultValue"/>
                </xsl:attribute>
                <xsl:attribute name="size">20</xsl:attribute>
            </xsl:element>
        </xsl:if>
        <!-- Parameter is "increment" then show it as "text" -->
        <xsl:if test="type = 'increment'">
            <xsl:element name="input">
                <xsl:attribute name="class">text</xsl:attribute>
                <xsl:attribute name="type">text</xsl:attribute>
                <xsl:attribute name="id">req_param_<xsl:value-of select="name"/>_value</xsl:attribute>
                <xsl:attribute name="name">
                    <xsl:value-of select="name"/>
                </xsl:attribute>
                <xsl:attribute name="value">
                    <xsl:value-of select="defaultValue"/>
                </xsl:attribute>
                <xsl:attribute name="size">20</xsl:attribute>
            </xsl:element>
        </xsl:if>
        <!-- Parameter is "booleans" then show it as "radio buttons" -->
        <xsl:if test="type = 'booleans'">
            <xsl:for-each select="enum_values/*">
                <xsl:element name="input">
                    <xsl:attribute name="type">radio</xsl:attribute>
                    <xsl:attribute name="class">checkbox</xsl:attribute>
                    <xsl:attribute name="id">req_param_<xsl:value-of select="name"/>_value</xsl:attribute>
                    <xsl:attribute name="name">
                        <xsl:value-of select="../../name"/>
                    </xsl:attribute>
                    <xsl:attribute name="value">
                        <xsl:value-of select="."/>
                    </xsl:attribute>
                    <xsl:if test=". = ../../defaultValue">
                        <xsl:attribute name="checked">true</xsl:attribute>
                    </xsl:if>
                </xsl:element>
                <xsl:value-of select="."/><xsl:element name="br"/>
            </xsl:for-each>
        </xsl:if>
        <!-- Parameter is "integer" then show it as "input" -->
        <xsl:if test="type = 'integer'">
            <xsl:element name="input">
                <xsl:attribute name="class">text</xsl:attribute>
                <xsl:attribute name="type">text</xsl:attribute>
                <xsl:attribute name="id">req_param_<xsl:value-of select="name"/>_value</xsl:attribute>
                <xsl:attribute name="name">
                    <xsl:value-of select="name"/>
                </xsl:attribute>
                <xsl:attribute name="value">
                    <xsl:value-of select="defaultValue"/>
                </xsl:attribute>
                <xsl:attribute name="size">20</xsl:attribute>
            </xsl:element>
        </xsl:if>
        <!-- Parameter is "password" then show it as "input" -->
        <xsl:if test="type = 'password'">
            <xsl:element name="input">
                <xsl:attribute name="class">text</xsl:attribute>
                <xsl:attribute name="type">password</xsl:attribute>
                <xsl:attribute name="id">req_param_<xsl:value-of select="name"/>_value</xsl:attribute>
                <xsl:attribute name="name">
                    <xsl:value-of select="name"/>
                </xsl:attribute>
                <xsl:attribute name="value">
                    <xsl:value-of select="defaultValue"/>
                </xsl:attribute>
                <xsl:attribute name="size">20</xsl:attribute>
            </xsl:element>
        </xsl:if>
        <!-- Parameter is "boolean" then show it as "checkbox" -->
        <xsl:if test="type = 'boolean'">
            <xsl:element name="input">
                <xsl:attribute name="class">checkbox</xsl:attribute>
                <xsl:attribute name="type">checkbox</xsl:attribute>
                <xsl:attribute name="id">req_param_<xsl:value-of select="name"/>_value</xsl:attribute>
                <xsl:attribute name="name">
                    <xsl:value-of select="name"/>
                </xsl:attribute>
                <xsl:if test="defaultValue = 'true'">
                    <xsl:attribute name="checked">
                        true
                    </xsl:attribute>
                </xsl:if>
            </xsl:element>
        </xsl:if>
        <!-- Parameter is "enum" then show it as "combobox" -->
        <xsl:if test="type = 'enum'">
            <xsl:element name="select">
                <xsl:attribute name="class">select</xsl:attribute>
                <xsl:attribute name="id">req_param_<xsl:value-of select="name"/>_value</xsl:attribute>
                <xsl:attribute name="name">
                    <xsl:value-of select="name"/>
                </xsl:attribute>
                <xsl:if test="count(enumValues/*) &lt; 2">
                    <xsl:attribute name="disabled">disabled</xsl:attribute>
                </xsl:if>
                <xsl:for-each select="enumValues/*">
                    <xsl:element name="option">
                        <xsl:attribute name="value">
                            <xsl:value-of select="."/>
                        </xsl:attribute>
                        <xsl:if test=". = ../../defaultValue">
                            <xsl:attribute name="selected">true</xsl:attribute>
                        </xsl:if>
                        <xsl:value-of select="."/>
                    </xsl:element>
                </xsl:for-each>
            </xsl:element>
        </xsl:if>
    </xsl:template>

</xsl:stylesheet>