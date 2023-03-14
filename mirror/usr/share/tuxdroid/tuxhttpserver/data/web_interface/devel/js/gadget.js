/**
 *
 */
function showPreview()
{
    var uuid = document.getElementById("uuid").value;
    var skin = '"' + document.getElementById("skin").value + '"';
    var language = document.getElementById("language").value;
    var args = {
        "uuid" : uuid,
        "language" : language,
        "parameters" : computeParameters()
    }
    res = postRequest("/wi_devel/post_preview_gadget", args);
    args = {
        "language" : language,
        "skin" : skin,
        "rndTag" : Math.random()
    }
    if (res[0])
    {
        showPopup("/wi_devel/show_preview_gadget", args);
    }
}

/**
 *
 */
function startGadget(command)
{
    var parametersString = "";
    var uuid = document.getElementById("uuid").value;

    var parameters = document.getElementsByTagName("input");

    for (var i = 0; i < parameters.length; i++)
    {
        var param = parameters[i];
        if (param.id == 'unvisible')
        {
            parametersString += param.name + '=' + param.value.replace('&', '&&') + '|';
        }
    }

    for (var i = 0; i < parameters.length; i++)
    {
        var param = parameters[i];
        if ((param.type != 'button') && (param.id != 'unvisible') && (param.name != ''))
        {
            if (param.type == 'checkbox')
            {
                parametersString += param.name + '=' + param.checked + '|';
            }
            else if (param.type == 'radio')
            {
                if (param.checked)
                {
                    parametersString += param.name + '=' + param.value.replace('&', '&&') + '|';
                }
            }
            else
            {
                parametersString += param.name + '=' + param.value.replace('&', '&&') + '|';
            }
        }
    }

    parameters = document.getElementsByTagName("select");
    for (var i = 0; i < parameters.length; i++)
    {
        var param = parameters[i];
        parametersString += param.name + '=' + param.value.replace('&', '&&') + '|';
    }
    var args = {
        "command" : command,
        "uuid" : uuid,
        "parameters" : parametersString
    }
    getRequest("/gadgets_server/start_gadget", args);
}

/**
 *
 */
function stopGadget()
{
    var uuid = document.getElementById("uuid").value;
    var args = {
        "uuid" : uuid
    }
    getRequest("/gadgets_server/stop_gadget", args);
}

/**
 *
 */
function editGadget()
{
    var uuid = document.getElementById("uuid").value;
    var skin = document.getElementById("skin").value;
    var language = document.getElementById("language").value;
    var args = {
        "uuid" : uuid,
        "skin" : skin,
        "language" : language
    }
    gotoLocation("/wi_devel/gadget_edit", args);
}

/**
 *
 */
function deleteGadget()
{
    var answer = confirm("This operation will deleting this gadget. Continue?");
    if (answer)
    {
        var uuid = document.getElementById("uuid").value;
        var args = {
            "uuid" : uuid
        }
        getRequest("/gadgets_server/remove_gadget", args);
        var skin = document.getElementById("skin").value;
        var language = document.getElementById("language").value;
        var url2 = "/devel/index?menu=gadgets&firstUuid=NULL";
        url2 += '&skin="' + skin + '"';
        url2 += "&language=" + language;
        window.top.location = url2;
    }
}

/**
 *
 */
function generateGadget()
{
    var answer = confirm("This will generate a new gadget in the system. Continue?");
    if (answer)
    {
        var uuid = document.getElementById("uuid").value;
        var skin = '"' + document.getElementById("skin").value + '"';
        var language = document.getElementById("language").value;
        var args = {
            "uuid" : uuid,
            "o_uuid" : "NULL",
            "language" : language,
            "parameters" : computeParameters()
        }
        res = postRequest("/wi_devel/generate_gadget", args);
        var url = "/devel/index?menu=gadgets";
        url += "&firstUuid=NULL";
        url += '&skin="' + skin + '"';
        url += "&language=" + language;
        window.top.location = url;
    }
}

/**
 *
 */
function applyGadget()
{
    var answer = confirm("This will update the gadget in the system. Continue?");
    if (answer)
    {
        var uuid = document.getElementById("uuid").value;
        var o_uuid = document.getElementById("o_uuid").value;
        var skin = '"' + document.getElementById("skin").value + '"';
        var language = document.getElementById("language").value;
        var args = {
            "uuid" : uuid,
            "o_uuid" : o_uuid,
            "language" : language,
            "parameters" : computeParameters()
        }
        res = postRequest("/wi_devel/generate_gadget", args);
        var url = "/devel/index?menu=gadgets";
        url += "&firstUuid=" + o_uuid;
        url += '&skin="' + skin + '"';
        url += "&language=" + language;
        window.top.location = url;
    }
}

/**
 *
 */
function duplicateGadget()
{
    var answer = confirm("This operation will duplicate the gadget in the system. Continue?");
    if (answer)
    {
        var uuid = document.getElementById("uuid").value;
        var skin = document.getElementById("skin").value;
        var language = document.getElementById("language").value;
        var args = {
            "uuid" : uuid,
            "language" : language
        }
        getRequest("/wi_devel/gadget_duplicate", args);
        var url2 = "/devel/index?menu=gadgets";
        url2 += "&firstUuid=NULL";
        url2 += '&skin="' + skin + '"';
        url2 += "&language=" + language;
        window.top.location = url2;
    }
}
