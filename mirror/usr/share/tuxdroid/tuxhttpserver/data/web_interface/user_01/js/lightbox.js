/*
Created By: Chris Campbell
Website: http://particletree.com
Date: 2/1/2006

Adapted By: Simon de Haan
Website: http://blog.eight.nl
Date: 21/2/2006

Inspired by the lightbox implementation found at http://www.huddletogether.com/projects/lightbox/
And the lightbox gone wild by ParticleTree at http://particletree.com/features/lightbox-gone-wild/

*/

/*-------------------------------GLOBAL VARIABLES------------------------------------*/

var detect = navigator.userAgent.toLowerCase();
var OS,browser,version,total,thestring;
var _abortNext = false;

/*-----------------------------------------------------------------------------------------------*/

//Browser detect script origionally created by Peter Paul Koch at http://www.quirksmode.org/

function getBrowserInfo() {
	if (checkIt('konqueror')) {
		browser = "Konqueror";
		OS = "Linux";
	}
	else if (checkIt('safari')) browser 	= "Safari"
	else if (checkIt('omniweb')) browser 	= "OmniWeb"
	else if (checkIt('opera')) browser 		= "Opera"
	else if (checkIt('webtv')) browser 		= "WebTV";
	else if (checkIt('icab')) browser 		= "iCab"
	else if (checkIt('msie')) browser 		= "Internet Explorer"
	else if (!checkIt('compatible')) {
		browser = "Netscape Navigator"
		version = detect.charAt(8);
	}
	else browser = "An unknown browser";

	if (!version) version = detect.charAt(place + thestring.length);

	if (!OS) {
		if (checkIt('linux')) OS 		= "Linux";
		else if (checkIt('x11')) OS 	= "Unix";
		else if (checkIt('mac')) OS 	= "Mac"
		else if (checkIt('win')) OS 	= "Windows"
		else OS 								= "an unknown operating system";
	}
}

function checkIt(string) {
	place = detect.indexOf(string) + 1;
	thestring = string;
	return place;
}

/*-----------------------------------------------------------------------------------------------*/

function abortNextLightbox()
{
    _abortNext = true;
}

Event.observe(window, 'load', getBrowserInfo, false);
Event.observe(window, 'unload', Event.unloadCache, false);

var lightbox = Class.create();

lightbox.prototype = {

	yPos : 0,
	xPos : 0,

	initialize: function(ctrl) {
		this.content = ctrl.rel;
        this.elementId = ctrl.id;
		Event.observe(ctrl, 'click', this.activate.bindAsEventListener(this), false);
		ctrl.onclick = function(){return false;};
	},

	// Turn everything on - mainly the IE fixes
	activate: function(){
        this.displayLightbox("block");
	},

	displayLightbox: function(display){
		$('overlay').style.display = display;
        parent.top.document.getElementById('overlay').style.display = display;
		$(this.content).style.display = display;
		if (display != 'none')
        {
            this.actions();
            $(this.content).onfocus(this.elementId);
            if (_abortNext)
            {
                _abortNext = false;
                this.displayLightbox("none");
            }
        }
	},

	// Search through new links within the lightbox, and attach click event
	actions: function(){
        lbActions = document.getElementsByTagName('a');
        for(i = 0; i < lbActions.length; i++)
        {
            if (lbActions[i].name == 'lbOff')
            {
                Event.observe(lbActions[i], 'click', this[lbActions[i].rel].bindAsEventListener(this), false);
            }
        }
	},

	// Example of creating your own functionality once lightbox is initiated
	deactivate: function(){
		this.displayLightbox("none");
	}
}

/*-----------------------------------------------------------------------------------------------*/

// Onload, make all links that need to trigger a lightbox active
function initializeLightbox(){
	addLightboxMarkup();
    lbox = document.getElementsByTagName('a');
    for(i = 0; i < lbox.length; i++)
    {
        if (lbox[i].name == 'lbOn')
        {
            valid = new lightbox(lbox[i]);
        }
    }
}

// Add in markup necessary to make this work. Basically two divs:
// Overlay holds the shadow
// Lightbox is the centered square that the content is put into.
function addLightboxMarkup() {

	bod 				= document.getElementsByTagName('body')[0];

	overlay 			= document.createElement('div');
	overlay.id			= 'overlay';

	bod.appendChild(overlay);

    bodParent 			= window.top.document.getElementsByTagName('body')[0];
	overlay 		    = window.top.document.createElement('div');
	overlay.id	        = 'overlay';

	bodParent.appendChild(overlay);
}