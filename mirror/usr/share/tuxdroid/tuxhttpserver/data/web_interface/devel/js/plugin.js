/**
 *
 */
function startPlugin(command)
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
    getRequest("/plugins_server/start_plugin", args);
}

/**
 *
 */
function stopPlugin()
{
    var uuid = document.getElementById("uuid").value;
    var args = {
        "uuid" : uuid
    }
    getRequest("/plugins_server/stop_plugin", args);
}

/**
 *
 */
function makeNewGadget()
{
    var uuid = document.getElementById("uuid").value;
    var skin = document.getElementById("skin").value;
    var language = document.getElementById("language").value;
    var args = {
        "uuid" : uuid,
        "skin" : skin,
        "language" : language
    }
    gotoLocation("/wi_devel/plugin_to_gadget", args);
}
