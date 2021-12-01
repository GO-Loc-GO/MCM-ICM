<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                version="1.0">

<xsl:output method="html"/>

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--                 Variable Definitions                   -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->

<xsl:variable name="BackgroundColor">#E6EBF5</xsl:variable><!--ButtonFace-->
<xsl:variable name="BackgroundImage">url(<xsl:value-of select="MdElementDialogInfo/CommonPath"/>/esri.gif)</xsl:variable>
<xsl:variable name="BackgroundPosition">bottom right</xsl:variable>
<xsl:variable name="BackgroundRepeat">no-repeat</xsl:variable>

<xsl:variable name="ButtonHeight">20px</xsl:variable>
<xsl:variable name="ButtonFont">Arial</xsl:variable>
<xsl:variable name="ButtonFontSize">8pt</xsl:variable>
<xsl:variable name="ButtonColor">#E6EBF5</xsl:variable><!--buttontext-->
<xsl:variable name="ButtonBackgroundColor">#E6EBF5</xsl:variable><!--ButtonFace-->
<xsl:variable name="ButtonBorderColorTop">threedshadow</xsl:variable>
<xsl:variable name="ButtonBorderColorLeft">threedhighlight</xsl:variable>
<xsl:variable name="ButtonBorderColorBottom">threedshadow</xsl:variable>
<xsl:variable name="ButtonBorderColorRight">threedshadow</xsl:variable>
<xsl:variable name="ButtonBorderStyleTop">ridge</xsl:variable>
<xsl:variable name="ButtonBorderStyleLeft">ridge</xsl:variable>
<xsl:variable name="ButtonBorderStyleBottom">groove</xsl:variable>
<xsl:variable name="ButtonBorderStyleRight">groove</xsl:variable>
<xsl:variable name="ButtonBorderWidth">2px</xsl:variable>

<xsl:variable name="CaptionFont">verdana,arial</xsl:variable>
<xsl:variable name="CaptionSize">8pt</xsl:variable>
<xsl:variable name="CaptionColor">Black</xsl:variable>
<xsl:variable name="CaptionWeight">Normal</xsl:variable>
<xsl:variable name="CaptionStyle">Normal</xsl:variable>

<xsl:variable name="GroupHeadingFont">verdana,arial</xsl:variable>
<xsl:variable name="GroupHeadingSize">8pt</xsl:variable>
<xsl:variable name="GroupHeadingColor">Black</xsl:variable>
<xsl:variable name="GroupHeadingWeight">Bold</xsl:variable>
<xsl:variable name="GroupHeadingStyle">Normal</xsl:variable>

<xsl:variable name="SDMHeadingWeight">Bold</xsl:variable>
<xsl:variable name="SDMHeadingUnderline">underline</xsl:variable>
<xsl:variable name="SDMHeadingIndent">5px</xsl:variable>
<xsl:variable name="SDMHeadingWeight2">Normal</xsl:variable>
<xsl:variable name="SDMHeadingSize">9pt</xsl:variable>

<xsl:variable name="SDMStepPadLeft">20px</xsl:variable>
<xsl:variable name="SDMStepPadLeft2">40px</xsl:variable>
<xsl:variable name="SDMStepPadLeft3">600px</xsl:variable>
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--              MdElementDialogInfo Template              -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<xsl:template match="MdElementDialogInfo">
<HTML> 
  <xsl:attribute name="DIR">
    <xsl:value-of select="Direction" />
  </xsl:attribute>
<xsl:text xml:space="preserve">&#x0D;&#x0A;</xsl:text>
<xsl:comment>&#x20;saved from url=(0016)http://localhost&#x20;</xsl:comment><xsl:text xml:space="preserve">&#x0D;&#x0A;</xsl:text>
<HEAD>
  <TITLE>Content</TITLE>
  <STYLE TYPE="text/css">
  BODY {
    background-color :    <xsl:value-of select="$BackgroundColor" />;
    <!-- background-image :    <xsl:value-of select="$BackgroundImage" />; -->
    background-position : <xsl:value-of select="$BackgroundPosition" />;
    background-repeat :   <xsl:value-of select="$BackgroundRepeat" />;
  }
  .button {   height:               <xsl:value-of select="$ButtonHeight" />; 
              font-family:          <xsl:value-of select="$ButtonFont" />; 
              font-size:            <xsl:value-of select="$ButtonFontSize" />; 
              color:                <xsl:value-of select="$ButtonColor" />; 
              background-color:     <xsl:value-of select="$ButtonBackgroundColor" />; 
              border-top-color:     <xsl:value-of select="$ButtonBorderColorTop" />; 
              border-left-color:    <xsl:value-of select="$ButtonBorderColorLeft" />; 
              border-bottom-color:  <xsl:value-of select="$ButtonBorderColorBottom" />; 
              border-right-color:   <xsl:value-of select="$ButtonBorderColorRight" />; 
              border-top-style:     <xsl:value-of select="$ButtonBorderStyleTop" />; 
              border-left-style:    <xsl:value-of select="$ButtonBorderStyleLeft" />; 
              border-bottom-style:  <xsl:value-of select="$ButtonBorderStyleBottom" />; 
              border-right-style:   <xsl:value-of select="$ButtonBorderStyleRight" />; 
              border-width:         <xsl:value-of select="$ButtonBorderWidth" />; } 
  .caption {  font-family:          <xsl:value-of select="$CaptionFont"/>; 
              font-size:            <xsl:value-of select="$CaptionSize"/>; 
              color:                <xsl:value-of select="$CaptionColor"/>; 
              font-weight:          <xsl:value-of select="$CaptionWeight"/>; 
              font-style:           <xsl:value-of select="$CaptionStyle"/>;}
  .groupheading {  font-family:          <xsl:value-of select="$GroupHeadingFont"/>; 
                   font-size:            <xsl:value-of select="$GroupHeadingSize"/>; 
                   color:                <xsl:value-of select="$GroupHeadingColor"/>; 
                   font-weight:          <xsl:value-of select="$GroupHeadingWeight"/>; 
                   font-style:           <xsl:value-of select="$GroupHeadingStyle"/>;}
  .small { font-family: verdana,arial; font-size: 7pt; }
  .sdmgrouping { font-weight:                 <xsl:value-of select="$GroupHeadingWeight"/>;
                text-decoration:             <xsl:value-of select="$SDMHeadingUnderline"/>;
                text-indent:                 <xsl:value-of select="$SDMHeadingIndent"/>;}    
  .sdmgrouping2 { font-weight:                 <xsl:value-of select="$SDMHeadingWeight"/>;
                font-size:            <xsl:value-of select="$SDMHeadingSize"/>; 
                text-indent:                 <xsl:value-of select="$SDMHeadingIndent"/>;}    
  .sdmsteppad {padding-left:                  <xsl:value-of select="$SDMStepPadLeft"/>;}
  .sdmsteppad2 {padding-left:                 <xsl:value-of select="$SDMStepPadLeft2"/>;}
  .sdmsteppad3 {padding-left:                 <xsl:value-of select="$SDMStepPadLeft3"/>;}
  </STYLE><xsl:text>&#10;</xsl:text>

<xsl:comment> ================ Scripts ================ </xsl:comment>
<xsl:text>&#10;</xsl:text>

<SCRIPT language="JavaScript"><xsl:text>&#10;</xsl:text>
<xsl:comment>
<![CDATA[
function InitForm()
{ ]]>
  // Register each control...
  //
<xsl:for-each select="Properties/PropertyGroup">
<xsl:for-each select="Property">  
   window.external.RegisterControl(<xsl:value-of select="CtrlName"/>, &quot;<xsl:value-of select="PropertyName"/>&quot;, &quot;<xsl:value-of select="Dependency"/>&quot;);
   <xsl:choose> 
     <xsl:when test="CtrlPlacement = 'below'">
       window.external.RegisterControl(<xsl:value-of select="CtrlLabel"/>, &quot;<xsl:value-of select="PropertyName"/>&quot;, &quot;<xsl:value-of select="Dependency"/>&quot;);
     </xsl:when>
  </xsl:choose>
</xsl:for-each>
</xsl:for-each><![CDATA[
  // Update the property image
  //
  var msg;]]>
<xsl:for-each select="Properties/PropertyGroup">
<xsl:for-each select="Property">  
  msg = window.external.GetMessage(&quot;<xsl:value-of select="PropertyName"/>&quot;);
  UpdatePropertyIcon(&quot;<xsl:value-of select="PropertyName"/>Img&quot;, msg);
</xsl:for-each>
</xsl:for-each><![CDATA[
  Window_onresize();
}

var g_showOnce = false;

function Window_onresize()
{ ]]>
  // Resize each control...
  //
  if ((window.document.body.clientWidth - 70) > 0)
  {
    <xsl:for-each select="Properties/PropertyGroup">
    <xsl:for-each select="Property">  <xsl:value-of select="CtrlName"/>.width = window.document.body.clientWidth - 30;
      <xsl:choose> 
        <xsl:when test="CtrlCLSID = 'C2BC7F14-19A1-480F-9B53-B21B1EBA8FA6'">
          <xsl:value-of select="CtrlName"/>.height = window.document.body.clientHeight - 30;
        </xsl:when>
      </xsl:choose>
     
    </xsl:for-each>
    </xsl:for-each><![CDATA[
  }
}

function UpdatePropertyIcon(img, msg)
{
  if (!msg)
    return;
    
  var imgSource;
  var description = msg.Description;
  var path = ]]>&quot;<xsl:value-of select='CommonPath'/>&quot;<![CDATA[
  if (msg.IsError())
  {
    if (msg.Type == 101) 
      imgSource = path + "/msgarrow.gif";
    else 
      imgSource = path + "/msgerror.gif";    
  }
  else if (msg.IsWarning())
    imgSource = path + "/msgwarning.gif";
  else
    imgSource = path +"/msgempty.gif";

  var e = document.getElementById(img);
  
  if (description)
  {
    var index = description.indexOf(":");
    var ErrorCode = -1;
    if (index > 0)
    {
      ErrorCode = description.substring(index - 6, index);
      if (!isNaN(ErrorCode))
        description = description.substring(description.search(":") + 1);
      else
        ErrorCode = "";
    }
    
    if (msg.Type != 101)
    {
      if (g_showOnce == false)
      {
        var elm = document.getElementById("bannerMessage");
        elm.style.visibility = "visible";
        elm.style.display = "block";
        g_showOnce = true;
      }
      e.alt = description + "\nClick for more detailed information.";    
    }
    else
      e.alt = "Click for more detailed information.";

    e.setAttribute('errText', description);
    e.setAttribute('errName', msg.IsError() ? "ERROR" : "WARNING");
    e.setAttribute('errCode', ErrorCode);
  }
  else
  {
    e.setAttribute('errText', "");
    e.setAttribute('errName', "");
    e.setAttribute('errCode', "");
    e.alt = "";
  }
  
  e.src = imgSource;
}

function displaymessage(icon_clicked) 
{
	if (!icon_clicked.firstChild.errText)
		return;
	var elm = document.getElementById("message_window");
	elm.style.visibility = "hidden";
	//var txt = icon_clicked.firstChild.errText;
	var props = icon_clicked.firstChild;
	document.getElementById('errText').innerHTML = props.errText;
	document.getElementById('errName').innerHTML = props.errName;
	document.getElementById('errCode').innerHTML = props.errCode;
	// gets the top and left coordinates we need to position the widdow
	if (icon_clicked.offsetParent)
  {
    curleft = icon_clicked.offsetLeft;
    curtop = icon_clicked.offsetTop;

    while (icon_clicked = icon_clicked.offsetParent)
    {
          curleft += icon_clicked.offsetLeft;
          curtop += icon_clicked.offsetTop;
    }
  }
  
  var theframe = document.getElementById("iframe");
	theframe.style.top = (curtop+15);
  theframe.style.left = (curleft+40);
  theframe.style.width = elm.offsetWidth;
  theframe.style.height = elm.offsetHeight;
  theframe.style.zIndex = 1;
  theframe.style.display = "block";
  
	//elm.innerHTML = "<b>" + txt + "</b>";
	elm.style.top = (curtop+15);
	elm.style.left = (curleft+40);
	elm.style.visibility = "visible";
}
		
// HIDES THE MESSAGE WINDOW
function hidemessage(e)
{
  e.parentNode.style.visibility = "hidden"
  var theframe = document.getElementById("iframe");
  theframe.style.display = "none"
}

// HIDES THE BANNER MESSAGE WINDOW
function hideBannerMessage()
{
  var e = document.getElementById("bannerMessage");
  e.style.display = "none";
  e.style.visibility = "hidden";
}

function UpdatePropertyIcons()
{
  // Update the warning/error icon for each property
  var hasError = false;
  ]]>
  var msg;
<xsl:for-each select="Properties/PropertyGroup">
  <xsl:for-each select="Property">  
  msg = window.external.GetMessage(&quot;<xsl:value-of select="PropertyName"/>&quot;);
  UpdatePropertyIcon(&quot;<xsl:value-of select="PropertyName"/>Img&quot;, msg);
  if (msg)
  {
    if (msg.IsError())
      if (msg.Type != 101)
        hasError = true;
  }
  </xsl:for-each>
</xsl:for-each><![CDATA[ 
if (!hasError)
  hideBannerMessage();
}

//
// HELP TOPIC NOTES: 
//
// Originally we had onClick() handlers for the BODY, DIV, and (property) SPAN 
// elements that would display the corresponding help topic. When clicking on 
// the SPAN element ShowHelpTopic() was being called correctly, however, the 
// onClick() handler for the BODY/DIV element was immediately called, causing 
// the currently displayed help topic to change to the 'Intro' topic. 
//
// To correct this, I've changed the onClick() handler for the SPAN elements
// to set a global 'current-topic' variable (g_currentHelpTopic), and rely on 
// the onClick() handlers for the BODY/DIV elements to call ShowCurrentHelpTopic() 
// to actually display the current topic. ShowCurrentHelpTopic() clears the 
// g_currentHelpTopic variable before returning, and displays the 'Intro' 
// topic.
//
var message="Function Disabled!";

function clickIE() {
	if (document.all) {
		//alert(message);
		return false;
	}
}
function clickNS(e) {
	if (document.layers||(document.getElementById&&!document.all)) {
		if (e.which==2||e.which==3) {
			//alert(message);
			return false;
		}
	}
}
if (document.layers) {
	document.captureEvents(Event.MOUSEDOWN);
	document.onmousedown=clickNS;
} else {
	document.onmouseup=clickNS;
	document.oncontextmenu=clickIE;
}

document.oncontextmenu=new Function("return false")

g_currentHelpTopic = '';

function ShowHelpTopic(topic)
{
  SetCurrentHelpTopic(topic);
  ShowCurrentHelpTopic();
}

function ShowErrorHelp(element)
{
  window.external.ShowErrorHelp(element.innerHTML);
}

function SetCurrentHelpTopic(topic)
{
  g_currentHelpTopic = topic;
}

function ShowCurrentHelpTopic()
{
  window.external.ShowHelpTopic(g_currentHelpTopic);
  g_currentHelpTopic = '';
}

function clicker(a,b) 
{
  if (a.style.display =='') 
  {
    a.style.display = 'none';
]]>    b.src='<xsl:value-of select="CommonPath"/>/triangle.gif'; <![CDATA[
  }
  else 
  {
    a.style.display='';
]]>    b.src='<xsl:value-of select="CommonPath"/>/triangle2.gif'; <![CDATA[
    window.external.UpdateCtrlTabOrder();
  }
}

]]>
</xsl:comment><xsl:text>&#10;</xsl:text>
</SCRIPT><xsl:text>&#10;</xsl:text>

<xsl:text>&#10;</xsl:text>
<SCRIPT language="JavaScript" FOR='window' EVENT='onunload'><xsl:text>&#10;</xsl:text>
<xsl:comment>
<![CDATA[
  window.external.UnRegisterControls();
]]>
</xsl:comment><xsl:text>&#10;</xsl:text>
</SCRIPT><xsl:text>&#10;</xsl:text>
<xsl:text>&#10;</xsl:text>

</HEAD><xsl:text>&#10;</xsl:text>

<BODY style="margin: 0; padding:0" width="100%" onload="InitForm()" TEXT="windowtext" onresize="Window_onresize()" onclick="ShowCurrentHelpTopic();"><xsl:text>&#10;</xsl:text>
<xsl:text>&#10;</xsl:text>
<IFRAME id="iframe" style="DISPLAY: none; LEFT:0px; POSITION: absolute;TOP:0px;" src="javascript:false;" frameBorder="0" scrolling="no"></IFRAME>
  <div id="message_window" 
	  style="visibility: hidden; 
	          border: 1px solid #999; 
	          border-bottom: 2px solid #666; 
	          border-right: 2px solid #666;
	          background: #FFFFCC; 
	          padding: 10px 10px 10px 20px; 
	          width: 250px; 
	          position: absolute; 
	          top: 100px; 
	          left: 100px;
	          font:  12px/16px arial;
	          z-index: 2;
	          ">
    <a href="#" onclick="hidemessage(this);hideBannerMessage();" style="float: right;">
      <img src="{CommonPath}/hidehelp.gif" alt="close window" title="Click to close this window" border="0"/>
    </a>  
     
    <strong><span id='errName'></span>&#32;<a id='errCode' onclick="hidemessage(this.parentNode);hideBannerMessage();ShowErrorHelp(this)" href="#"></a> </strong>
    <div id='errText'></div>

  </div>

<DIV STYLE="margin: 0; ">
  <div id="bannerMessage" width="100%" style="display:'none'; visibility:'hidden'">
	  <table width="100%" style="border-bottom:1px solid black"> 
      <tr style="background:#FFFFCC">
      <td style="font-size:70%;font-family:tahoma; padding-left:17px">Click error and warning icons for more information</td>
      <td width="10px" align="right"> <a href="#" onclick="document.getElementById('bannerMessage').style.visibility = 'hidden';document.getElementById('bannerMessage').style.display = 'none';">
        <img src="{CommonPath}/hidehelp.gif" alt="close window" title="Click to close this window" border="0"/></a></td>
      </tr>
    </table>
  </div>    
  <div style="padding-top:5px">
<xsl:apply-templates select="Intro" />
<xsl:for-each select="Properties">
    <xsl:apply-templates/>
</xsl:for-each>
</div>
</DIV>

</BODY>
</HTML>

</xsl:template>

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--                 Property Group Template                -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<xsl:template match="PropertyGroup">
<div style="padding-top:5px"/>
  <xsl:choose> 
    <xsl:when test="PropertyGroupLabelVisibility = 'show'">
      <TR valign="top">
        <TD colspan="2">
          <DIV ID="GEN" STYLE="cursor: hand;">
            <TABLE onclick="clicker({PropertyGroupName},{PropertyGroupName}Image);" STYLE="cursor:hand;" border="1" bordercolor="#E6EBF5" cellspacing="0" cellpadding="0" width="100%"><!--button-->
              <TR valign="top" bgcolor="#E6EBF5"> <!--menu-->
                <TD colspan="2">
                  <TABLE border="0" cellpadding="0" cellspacing="0" width="100%" >
                    <TR bgcolor="#E6EBF5"><!--buttontext-->
                      <xsl:choose>
                        <xsl:when test="../../Direction = 'ltr' ">
                          <TH align="left">
                          <IMG ID="{PropertyGroupName}Image" SRC="{../../CommonPath}/triangle.gif" ALT="*" ALIGN="LEFT" BORDER="0" WIDTH="11" HEIGHT="11"/>
                          <SPAN class="sdmgrouping" STYLE="color:menutext;"><xsl:value-of select="PropertyGroupLabel"/></SPAN>
                          </TH>
                        </xsl:when>
                        
                        <xsl:otherwise>
                          <TH align="right">
                          <IMG ID="{PropertyGroupName}Image" SRC="{../../CommonPath}/triangle.gif" ALT="*" ALIGN="RIGHT" BORDER="0" WIDTH="11" HEIGHT="11"/>
                          <SPAN class="sdmgroupheading" STYLE="color:menutext;"><xsl:value-of select="PropertyGroupLabel"/></SPAN>
                          </TH>
                        </xsl:otherwise>
                      </xsl:choose>
                      
                    </TR>
                  </TABLE>
                </TD>
              </TR>

              <TR valign="top">
                <TD colspan="2">
                  <DIV ID="{PropertyGroupName}" STYLE="display:'none';" onclick="window.event.cancelBubble = true;">
                    <xsl:for-each select="Property"> 
                      <xsl:apply-templates select="." />
                    </xsl:for-each> 
                  </DIV>
                </TD>
              </TR>

            </TABLE>
          </DIV>
        </TD>
      </TR>
    </xsl:when>

    <xsl:otherwise>
      <TR valign="top">
        <TD colspan="2">
        <TABLE border="0" cellspacing="0" cellpadding="0" width="100%">
        <xsl:for-each select="Property"> 
          <xsl:apply-templates select="." />
        </xsl:for-each> 
        </TABLE>
        </TD>
      </TR>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--                 Property Template                      -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<xsl:template match="Property">
  <TABLE BORDER="0" CELLSPACING="0" CELLPADDING="0" WIDTH="100%">
   <TR class="sdmgrouping"> 
    <xsl:choose>
      <xsl:when test='PropertyName="Param1"'>
                <TD style="padding-bottom=5">
                    Inputs
                </TD>
      </xsl:when>
      <xsl:when test='PropertyName="Param10"'>         
                <!-- <TD style="padding-top=15"> -->
                <TD style="padding-bottom=5">
                    Outputs
                </TD>            
      </xsl:when>
      <xsl:when test='PropertyName="Param13"'>         
                <!-- <TD style="padding-top=15"> -->
                <TD style="padding-bottom=5">
                     MaxEnt Settings
                </TD>            
      </xsl:when>
      <xsl:when test='PropertyName="Param25"'>         
                <!-- <TD style="padding-top=15"> -->
                <TD style="padding-bottom=5">
                    Spatial Jackknifing
                </TD>            
      </xsl:when>
      <xsl:when test='PropertyName="Param35"'>         
                <!-- <TD style="padding-top=15"> -->
                <TD style="padding-bottom=5">
                    For Standard MaxEnt Runs 
                </TD>            
      </xsl:when>
      </xsl:choose>
    </TR>
    <TR class="sdmgrouping2"> 
    <xsl:choose>
      <xsl:when test='PropertyName="Param1"'>         
                <!-- <TD style="padding-top=15"> -->
                <TD style="padding-bottom=5">
                   MaxEnt Program
                </TD>            
      </xsl:when>
    </xsl:choose>
    <xsl:choose>
      <xsl:when test='PropertyName="Param2"'>         
                <!-- <TD style="padding-top=15"> -->
                <TD style="padding-bottom=5">
                    Occurrence Data
                </TD>            
      </xsl:when>
    </xsl:choose>
    <xsl:choose>
      <xsl:when test='PropertyName="Param6"'>         
                <!-- <TD style="padding-top=15"> -->
                <TD style="padding-bottom=5">
                    Environmental Layers
                </TD>            
      </xsl:when>
    </xsl:choose>
    <xsl:choose>
      <xsl:when test='PropertyName="Param9"'>         
                <!-- <TD style="padding-top=15"> -->
                <TD style="padding-bottom=5">
                    Include Bias Files
                </TD>            
      </xsl:when>
    </xsl:choose>
    <xsl:choose>
      <xsl:when test='PropertyName="Param13"'>         
                <!-- <TD style="padding-top=15"> -->
                <TD style="padding-bottom=5">
                   Basic Settings
                </TD>            
      </xsl:when>
    </xsl:choose>
    <xsl:choose>
      <xsl:when test='PropertyName="Param18"'>         
                <!-- <TD style="padding-top=15"> -->
                <TD style="padding-bottom=5">
                   Main Model Parameters
                </TD>            
      </xsl:when>
    </xsl:choose>
    <xsl:choose>
      <xsl:when test='PropertyName="Param20"'>         
                <!-- <TD style="padding-top=15"> -->
                <TD style="padding-bottom=5">
                    Model Projection Settings
                </TD>            
      </xsl:when>
    </xsl:choose>
    <xsl:choose>
      <xsl:when test='PropertyName="Param23"'>         
                <!-- <TD style="padding-top=15"> -->
                <TD style="padding-bottom=5">
                   CPU Settings
                </TD>            
      </xsl:when>
    </xsl:choose>
    <xsl:choose>
      <xsl:when test='PropertyName="Param32"'>         
                <!-- <TD style="padding-top=15"> -->
                <TD style="padding-bottom=5">
                   Model Parameters for Species Not Spatially Jackknifed 
                </TD>            
      </xsl:when>
    </xsl:choose>    <xsl:choose>
      <xsl:when test='PropertyName="Param35"'>         
                <!-- <TD style="padding-top=15"> -->
                <TD style="padding-bottom=5">
                   Auto-Feature Classes 
                </TD>            
      </xsl:when>
    </xsl:choose>
    <xsl:choose>
      <xsl:when test='PropertyName="Param36"'>         
                <!-- <TD style="padding-top=15"> -->
                <TD style="padding-bottom=5">
                    Manual Feature Classes 
                </TD>            
      </xsl:when>
    </xsl:choose>
    </TR>
  </TABLE> 
    <TABLE BORDER="0" CELLSPACING="0" CELLPADDING="0" WIDTH="100%">
     <TR valign="top">
      <TD WIDTH='17' onclick="displaymessage(this)">
        <IMG ID='{PropertyName}Img' src="{../../../CommonPath}/msgempty.gif" />
      </TD>
        <xsl:choose>                   
          <xsl:when test='PropertyName="Param13" or PropertyName="Param14" or PropertyName="Param15" or PropertyName="Param16" or PropertyName="Param17" or PropertyName="Param21" or PropertyName="Param22" or PropertyName="Param24" or PropertyName="Param25" or PropertyName="Param26" or PropertyName="Param31" or PropertyName="Param35" or PropertyName="Param40" or PropertyName="Param36" or PropertyName="Param37" or PropertyName="Param38"  or PropertyName="Param39"'> 
             <TD class="sdmsteppad2">                    
                 
                 <OBJECT width="100%" style="z-index: -1" classid="CLSID:{CtrlCLSID}" id="{CtrlName}" onfocus="ShowHelpTopic('{PropertyName}Topic');"/>                    
             </TD>
          </xsl:when>  		  
          <xsl:otherwise>
             <TD>
                 <OBJECT width="100%" style="z-index: -1" classid="CLSID:9FA602C6-85AF-40E2-A64A-E938C70C67B9" id="{CtrlLabel}" onfocus="ShowHelpTopic('{PropertyName}Topic');" />
                 <OBJECT width="100%" style="z-index: -1" classid="CLSID:{CtrlCLSID}" id="{CtrlName}" onfocus="ShowHelpTopic('{PropertyName}Topic');" />
             </TD>
          </xsl:otherwise>              
        </xsl:choose>             
        
    </TR>
  </TABLE>
</xsl:template>
<!-- Overwrite Select Templates -->
<xsl:template match="PropertyGroup">
    <TR valign="top"><TD>
        <DIV ID="GEN" STYLE="cursor: hand;">
            <!-- Process required parameters -->
            <xsl:for-each select="Property"> 
                <xsl:choose>
                    <!--xsl:when test='not(contains(PropertyLabel,"(optional)"))'-->
                    <xsl:when test='not(PropertyName="Param42" or PropertyName="Param43" or PropertyName="Param35" or PropertyName="Param36" or PropertyName="Param37"  or PropertyName="Param38" or PropertyName="Param39" or PropertyName="Param40"  or PropertyName="Param41")'>                    
					      <xsl:apply-templates select="." />
                    </xsl:when>
                </xsl:choose>
            </xsl:for-each>
            <!-- Add expanding section for optional parameters -->
            <TABLE onclick="parent.clicker({PropertyGroupName},{PropertyGroupName}Image);" STYLE="cursor:hand;" border="0" cellspacing="0" cellpadding="0" width="94%">                
                <TR valign="top" bgcolor="#E6EBF5"><!--menu-->
                    <TD colspan="2">
                        <TABLE border="0" width="100%" cellpadding="0" cellspacing="0">
                            <TR bgcolor="#E6EBF5"><!--menu-->
                                <TH align="left">
                                   <IMG ID="{PropertyGroupName}Image" SRC="{../../CommonPath}/triangle.gif" ALT="*" ALIGN="MIDDLE" BORDER="0" WIDTH="11" HEIGHT="11"/>
									<SPAN class="sdmgrouping" STYLE="padding-bottom=5">Additional Parameters</SPAN>
                                </TH>
                            </TR>
                        </TABLE>
                    </TD>
                </TR>
                <TR valign="top">
                    <TD colspan="2">
                        <DIV ID="{PropertyGroupName}" STYLE="display:'none';" onclick="window.event.cancelBubble = true;">
                            <TABLE border="0" cellspacing="1" cellpadding="4" width="90%">
                                <xsl:for-each select="Property"> 
                                    <xsl:choose>                               
                                        <!--xsl:when test='contains(PropertyLabel,"(optional)")'-->
										<xsl:when test='PropertyName="Param42" or PropertyName="Param43" or PropertyName="Param35" or PropertyName="Param36" or PropertyName="Param37" or PropertyName="Param38" or PropertyName="Param39" or PropertyName="Param40"  or PropertyName="Param41"'> 
                                            <xsl:apply-templates select="." />
										</xsl:when>
                                    </xsl:choose>
                                </xsl:for-each> 
                            </TABLE>
                        </DIV>
                    </TD>
                </TR>
            </TABLE>
        </DIV>
    </TD></TR>
</xsl:template>

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--                   Intro Template                       -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<xsl:template match="Intro">
  <div align="center">
  <b>
  <br/>
  <xsl:value-of select="." />
  </b>
  </div>
</xsl:template>

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--                   Root Template                        -->
<!--                                                        -->
<!-- Matches the whole document, where processing begins    -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<xsl:template match="/">
  <xsl:apply-templates />
</xsl:template>

</xsl:stylesheet>


