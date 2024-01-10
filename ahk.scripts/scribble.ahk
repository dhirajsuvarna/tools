#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

^y::
Run, www.youtube.com
return

^g::
clipboard= ;empty clipboard
send, {ctrl down}c{ctrl up}
ClipWait, 2
if(clipboard="")
{
	Run, www.google.co.in
}
else
{
	Run, www.google.co.in/#q=%clipboard%
}
	
return

#n::
IfWinExist, ahk_class Notepad++
{
	WinActivate, ahk_class Notepad++
	;WinSet, Top
}
else
{
	Run, "C:\Program Files (x86)\Notepad++\notepad++.exe"
}
return

^h::
send, my name is dhiraj
return 

::btw::by the way
return

#o::
SendMessage 0x112, 0xF170, 2,,Program Manager
return 

#NumpadAdd::
Send {Volume_Up 2}
return 

#NumpadSub::
Send {Volume_Down 2}
return 

#NumpadEnter::
Send {Volume_Mute}
return 


#c::
Run, "C:\Program Files (x86)\Cisco Systems\VPN Client\vpngui.exe"
WinWait, ahk_exe vpngui.exe
IfWinExist, ahk_exe vpngui.exe
{
	WinActivate
	;MsgBox, dhiraj
	ControlClick, x170 y158, ahk_exe vpngui.exe
	ControlClick, QWidget85, ahk_exe vpngui.exe
	WinWaitActive, VPN Client  |  User Authentication for "TSG", , 10
	ControlSendRaw, QWidget4, nsdl@890, VPN Client  |  User Authentication for "TSG"
	ControlClick, QWidget2, VPN Client  |  User Authentication for "TSG"
	
	WinWaitActive, VPN Client  |  Banner, , 10
	ControlClick, QWidget1, VPN Client  |  Banner
	if !ErrorLevel
	{
		Run, "C:\Windows\System32\mstsc.exe"
		WinWaitActive, Remote Desktop Connection, , 10
		if !ErrorLevel
		{
			ControlClick, Button5, Remote Desktop Connection
		}
	}
}
return 

#^i::
Run, "C:\Program Files (x86)\TP-LINK\TP-LINK Wireless Configuration Utility\TWCU.exe"
WinWait, ahk_exe TWCU.exe
IfWinExist, ahk_exe TWCU.exe
{
	ControlClick, Static16, ahk_exe TWCU.exe
	ControlGetText, textOnButton, Button24, ahk_exe TWCU.exe
	if(%textOnButton% == "Disconnect")
		MsgBox, Text is Disconnect
	else
		MsgBox, Text is Connect
}
return
