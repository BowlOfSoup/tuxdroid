/**
 *
 */
function fillHelpBox()
{
    document.getElementById("helpBox").innerHTML = Wiky.toHtml(document.getElementById("req_helpContent").value);
}

/**
 *
 */
function setpng(img)
{
    if (document.all && (IEver=parseFloat(navigator.appVersion.split("MSIE")[1])) && (IEver>=5.5) && (IEver<=8) && document.body.filters && img)
    {
        var imgName = img.src.toUpperCase();
        if (imgName.substring(imgName.length-3,imgName.length) == "PNG")
        {
            img.outerHTML= "<span "+(img.id?"id='"+img.id+"' ":"")+(img.className?"class='"+img.className+"' ":"")+(img.title?"title=\""+img.title+"\" ":"")
            +"style=\"width:"+img.width+"px;height:"+img.height+"px;"+(img.align=="left"?"float:left;":(img.align=="right"?"float:right;":""))
            +(img.parentElement.href?"cursor:hand;":"")+"display:inline-block;"+img.style.cssText+";"
            +"filter:progid:DXImageTransform.Microsoft.AlphaImageLoader(src='"+img.src+"',sizingMethod='scale');\"></span>";
        }
    }
}

/**
 *
 */
function formatValue(value)
{
    value = value.replace(/(\r?\n)/g, '[RETURN]');
    value = value.replace('/\&/g', '&&');
    value = value.replace(/\|/g, '[PIPE]');
    value = value.replace(/\=/g, '[EQUAL]');
    value = value.replace(/\&/g, '[AMP]');
    value = value.replace(/\+/g, '[PLUS]');
    return value;
}

/**
 *
 */
function computeParameters()
{
    var result = '';
    var elements = document.getElementsByTagName('input');
    for (var i = 0; i < elements.length; i++)
    {
        var element = elements[i];
        if (element.id.indexOf('req_', 0) == 0)
        {
            if (element.type == 'checkbox')
            {
                result += element.id + '=' + element.checked + '|';
            }
            else if (element.type == 'radio')
            {
                if (element.checked)
                {
                    result += element.id + '=' + formatValue(element.value) + '|';
                }
            }
            else
            {
                result += element.id + '=' + formatValue(element.value) + '|';
            }
        }
    }
    var elements = document.getElementsByTagName('select');
    for (var i = 0; i < elements.length; i++)
    {
        var element = elements[i];
        if (element.id.indexOf('req_', 0) == 0)
        {
            result += element.id + '=' + formatValue(element.value) + '|';
        }
    }
    var helptext = "";
    if (document.getElementById("req_helpContent") != null)
    {
        helptext = document.getElementById("req_helpContent").value;
    }
    result += 'req_helpContent=' + formatValue(helptext) + '|';
    return result;
}

/**
 *
 */
function postRequest(url, values)
{
    var httpRequest = false;
    var isIe = false;
    var result = new Array(false, "");
    if (window.XMLHttpRequest)
    {   // Mozilla, Safari,...
        httpRequest = new XMLHttpRequest();
        if (httpRequest.overrideMimeType)
        {
            httpRequest.overrideMimeType('text/xml');
        }
    }
    else
    {
        isIe = true;
        if (window.ActiveXObject)
        {   // IE
            try
            {
                httpRequest = new ActiveXObject("Msxml2.XMLHTTP");
            }
            catch (e)
            {
                try
                {
                    httpRequest = new ActiveXObject("Microsoft.XMLHTTP");
                }
                catch (e){}
            }
        }
    }
    if (!httpRequest)
    {
        alert('Cannot create XMLHTTP instance');
        return result;
    }
    var data = "";
    for (var property in values)
    {
        if (values.hasOwnProperty(property))
        {
            if (data.length > 0)
            {
                data += "&";
            }
            data += property + "=" + values[property];
        }
    }
    httpRequest.open('POST', url, false);
    var stateChangeFunction = function() {
        if(httpRequest.readyState == 4)
        {
            if (httpRequest.status == 200)
            {
                result[0] = true;
                result[1] = httpRequest.responseText;
            }
        }
    }
    if (isIe)
    {
        httpRequest.onreadystatechange = stateChangeFunction;
    }
    else
    {
        httpRequest.onload = stateChangeFunction;
    }

    try
    {
        httpRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        httpRequest.send(data);
    }
    catch (e)
    {
        return result;
    }
    return result;
}

/**
 *
 */
function getRequest(url, values)
{
    var httpRequest = false;
    var isIe = false;
    var result = false;
    if (window.XMLHttpRequest)
    {   // Mozilla, Safari,...
        httpRequest = new XMLHttpRequest();
        if (httpRequest.overrideMimeType)
        {
            httpRequest.overrideMimeType('text/xml');
        }
    }
    else
    {
        isIe = true;
        if (window.ActiveXObject)
        {   // IE
            try
            {
                httpRequest = new ActiveXObject("Msxml2.XMLHTTP");
            }
            catch (e)
            {
                try
                {
                    httpRequest = new ActiveXObject("Microsoft.XMLHTTP");
                }
                catch (e){}
            }
        }
    }
    if (!httpRequest)
    {
        alert('Cannot create XMLHTTP instance');
        return result;
    }
    url += "?rndTag=" + Math.random() ;
    for (var property in values)
    {
        if (values.hasOwnProperty(property))
        {
            url += "&" + property + "=" + values[property];
        }
    }
    httpRequest.open('GET', url, false);
    var stateChangeFunction = function() {
        if(httpRequest.readyState == 4)
        {
            if (httpRequest.status == 200)
            {
                result = true;
            }
        }
    }
    if (isIe)
    {
        httpRequest.onreadystatechange = stateChangeFunction;
    }
    else
    {
        httpRequest.onload = stateChangeFunction;
    }
    try
    {
        httpRequest.send(null);
    }
    catch (e)
    {
        return result;
    }
    return result;
}

/**
 *
 */
var httpRequester = false;
var flag01 = false;
function requestData(url, values)
{
    var result = new Hashtable();
    if (!httpRequester)
    {
        if (window.XMLHttpRequest)
        {   // Mozilla, Safari,...
            httpRequester = new XMLHttpRequest();
            if (httpRequester.overrideMimeType)
            {
                httpRequester.overrideMimeType('text/xml');
            }
        }
        else
        {
            flag01 = true;
            if (window.ActiveXObject)
            {   // IE
                try
                {
                    httpRequester = new ActiveXObject("Msxml2.XMLHTTP");
                }
                catch (e)
                {
                    try
                    {
                        httpRequester = new ActiveXObject("Microsoft.XMLHTTP");
                    }
                    catch (e)
                    {
                        httpRequester = false;
                    }
                }
            }
        }
        if (!httpRequester)
        {
            return null;
        }
    }
    var data = "";
    for (var property in values)
    {
        if (values.hasOwnProperty(property))
        {
            if (data.length > 0)
            {
                data += "&";
            }
            data += property + "=" + values[property];
        }
    }
    httpRequester.open('POST', url, false);
    var stateChangeFunction = function() {
        if(httpRequester.readyState == 4)
        {
            if (httpRequester.status == 200)
            {
                try
                {
                    var xmldoc = httpRequester.responseXML;
                    var root = xmldoc.getElementsByTagName('root').item(0);
                    var dataCount = 0;
                    var dataNodeName = "";
                    for (var iNode = 0; iNode < root.childNodes.length; iNode++)
                    {
                        var node = root.childNodes.item(iNode);
                        if (node.firstChild.nodeValue != null)
                        {
                            result.put(node.nodeName, node.firstChild.data);
                        }
                        else
                        {
                            var subDict = new Hashtable();
                            for (var jNode = 0; jNode < node.childNodes.length; jNode++)
                            {
                                var node1 = node.childNodes.item(jNode);
                                subDict.put(node1.nodeName, node1.firstChild.data);
                            }
                            if (node.nodeName == "data")
                            {
                                dataNodeName = "data" + dataCount;
                                dataCount++;
                            }
                            else
                            {
                                dataNodeName = node.nodeName;
                            }
                            result.put(dataNodeName, subDict);
                        }
                    }
                    result.put("dataCount", dataCount);
                }
                catch (e)
                {
                    result = null;
                }
            }
            else
            {
                result = null;
            }
        }
    }
    if (flag01)
    {
        httpRequester.onreadystatechange = stateChangeFunction;
    }
    else
    {
        httpRequester.onreadystatechange = stateChangeFunction;
        httpRequester.onload = stateChangeFunction;
    }
    try
    {
        httpRequester.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        httpRequester.send(data);
    }
    catch (e)
    {
        return null;
    }
    return result;
}

/**
 *
 */
function gotoLocation(url, values)
{
    url += "?";
    for (var property in values)
    {
        if (values.hasOwnProperty(property))
        {
            url += property + "=" + values[property] + "&";
        }
    }
    window.location = url;
}

/**
 *
 */
function showPopup(url, values)
{
    url += "?";
    for (var property in values)
    {
        if (values.hasOwnProperty(property))
        {
            url += property + "=" + values[property] + "&";
        }
    }
    window.open(url);
}

/**
 *
 */
function clickMe(element)
{
    try
    {
        document.getElementById(element).click();
    } catch(e)
    {
        var evt = document.createEvent("MouseEvents");
        evt.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
        var cb = document.getElementById(element);
        cb.dispatchEvent(evt);
    }
}
