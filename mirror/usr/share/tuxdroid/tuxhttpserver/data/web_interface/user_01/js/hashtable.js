// Code from :
// http://dev-for-fun.blogspot.com/2007/11/javascript-hashtable.html
function Hashtable()
{
    this.clear = hashtable_clear;
    this.containsKey = hashtable_containsKey;
    this.containsValue = hashtable_containsValue;
    this.get = hashtable_get;
    this.isEmpty = hashtable_isEmpty;
    this.keys = hashtable_keys;
    this.put = hashtable_put;
    this.remove = hashtable_remove;
    this.size = hashtable_size;
    this.toString = hashtable_toString;
    this.values = hashtable_values;
    this.hashtable = new Array();
}

function hashtable_clear()
{
    this.hashtable = new Array();
}

function hashtable_containsKey(key)
{
    var exists = false;
    
    for (var i in this.hashtable)
    {
        if (i == key && this.hashtable[i] != null)
        {
            exists = true;
            break;
        }
    }
    
    return exists;
}

function hashtable_containsValue(value)
{
    var contains = false;
    
    if (value != null)
    {
        for (var i in this.hashtable)
        {
            if (this.hashtable[i] == value)
            {
                contains = true;
                break;
            }
        }
    }
    
    return contains;
}

function hashtable_get(key)
{
    return this.hashtable[key];
}

function hashtable_isEmpty()
{
    return (this.size == 0) ? true : false;
}

function hashtable_keys()
{
    var keys = new Array();
    
    for (var i in this.hashtable)
    {
        if (this.hashtable[i] != null)
        {
            keys.push(i);
        }
    }
    
    return keys;
}

function hashtable_put(key, value)
{
    if (key == null || value == null)
    {
        throw 'NullPointerException {' + key + '},{' + value + '}';
    }
    else
    {
        this.hashtable[key] = value;
    }
}

function hashtable_remove(key)
{
    var rtn = this.hashtable[key];
    
    this.hashtable[key] = null;
    
    return rtn;
}

function hashtable_size()
{
    var size = 0;
    
    for (var i in this.hashtable)
    {
        if (this.hashtable[i] != null) 
            size ++;
    }
    
    return size;
}

function hashtable_toString()
{
    var result = '';
    
    for (var i in this.hashtable)
    {      
        if (this.hashtable[i] != null)
        {
            result += '{' + i + '},{' + this.hashtable[i] + '}\n';  
        } 
    }
    return result;
}

function hashtable_values()
{
    var values = new Array();
    
    for (var i in this.hashtable)
    {
        if (this.hashtable[i] != null)
        {
            values.push(this.hashtable[i]);
        }
    }
    
    return values;
}