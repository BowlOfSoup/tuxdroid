/**
 *
 */
function startUgc(command)
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
    getRequest("/ugc_server/start_ugc", args);
}

/**
 *
 */
function stopUgc()
{
    var uuid = document.getElementById("uuid").value;
    var args = {
        "uuid" : uuid
    }
    getRequest("/ugc_server/stop_ugc", args);
}

/**
 *
 */
function deleteUgc()
{
    var answer = confirm("This operation will deleting this UGC gadget. Continue?");
    if (answer)
    {
        var uuid = document.getElementById("uuid").value;
        var args = {
            "uuid" : uuid
        }
        getRequest("/ugc_server/remove_ugc", args);
        var skin = document.getElementById("skin").value;
        var language = document.getElementById("language").value;
        var url2 = "/devel/index?menu=ugcs&firstUuid=NULL";
        url2 += '&skin="' + skin + '"';
        url2 += "&language=" + language;
        window.top.location = url2;
    }
}

/**
 *
 */
function applyUgcConfiguration()
{
    var answer = confirm("This will update the gadget configuration in the system. Continue?");
    if (answer)
    {
        var uuid = document.getElementById("uuid").value;
        var o_uuid = document.getElementById("o_uuid").value;
        var skin = '"' + document.getElementById("skin").value + '"';
        var language = document.getElementById("language").value;
        var args = {
            "uuid" : uuid,
            "language" : language,
            "parameters" : computeParameters()
        }
        res = postRequest("/wi_devel/apply_ugc", args);
        var url = "/devel/index?menu=ugcs";
        url += "&firstUuid=" + uuid;
        url += '&skin="' + skin + '"';
        url += "&language=" + language;
        window.top.location = url;
    }
}

/**
 *
 */
function duplicateUgc()
{
    var answer = confirm("This operation will duplicate the UGC gadget in the system. Continue?");
    if (answer)
    {
        var uuid = document.getElementById("uuid").value;
        var skin = document.getElementById("skin").value;
        var language = document.getElementById("language").value;
        var args = {
            "uuid" : uuid,
            "language" : language
        }
        getRequest("/wi_devel/ugc_duplicate", args);
        var url2 = "/devel/index?menu=ugcs";
        url2 += "&firstUuid=NULL";
        url2 += '&skin="' + skin + '"';
        url2 += "&language=" + language;
        window.top.location = url2;
    }
}
