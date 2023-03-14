<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">

<xsl:template match="/">
<html>
    <head>
        <LINK href="/data/web_interface/user_01/css/gadget-help.css" rel="stylesheet" type="text/css"/>
        <script src="/data/web_interface/common/wiky/wiky.js" type="text/javascript"/>
        <script src="/data/web_interface/user_01/js/common.js" type="text/javascript"/>
        <script language="javascript">
        <![CDATA[
            function initialization()
            {
                fillHelpBox();
            }
        ]]>
        </script>
    </head>

    <body bgcolor="#dcdadb" onLoad="initialization();">
        <!-- MAIN DIV FRAME -->
        <div id="helpBox"
             style="position:absolute;
                    left:0px;
                    top:0px;
                    width:423px;
                    height:238px;
                    overflow-y:auto;
                    overflow-x:hidden;
                    font-family:Verdana, Bitstream Vera Sans;">
            <textarea id="req_helpContent" rows="0" cols="0"  style="visibility:hidden;">
                <xsl:value-of select="root/data/description/helpFile"/>
            </textarea>
        </div>
        <!-- UNNEEDED CODE TO AVOID BAD ANTIVIRUS DETECTION ... -->
        <!--
        <div id="ligthboxExample" class="leightbox">
            <h1>A lightbox</h1>
            <p> This is a test</p>
            <p class="footer">
                <a href="#" class="lbAction" rel="deactivate">Close</a>
            </p>
        </div>
        -->
    </body>
</html>
</xsl:template>
</xsl:stylesheet>
