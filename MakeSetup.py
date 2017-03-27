#!/usr/bin/env python
#coding=utf-8

import winreg
import enum
import sys
import os
import platform

def GetPFX86Dir():
    if '64' in platform.machine():
        return r'%programfiles(x86)%'
    else:
        return r'%programfiles%'

## key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r'SYSTEM\CurrentControlSet\Services\Tcpip\Performance')

def getHKLMValue(path,name):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,path)
        value,type = winreg.QueryValueEx(key,name)
        return value
    except WindowsError:
        return None
    return None

#vs2008.WindowsSdkDir->MSDK\v6.0A\
#vs2008.FrameWorkSDKDir->MSDK\v6.0A
#vs2010.WindowsSDK80Path->WindowsKits\8.0
#vs2010.WindowsSdkDir->MSDK\v7.0A
#vs2010.FrameworkSdkDir->MSDK\Windows\v7.0A
#vs2012.windowsSdkDir->WindowsKits\8.0
#vs2012.windowsSdkDir_80->WindowsKits\8.0
#vs2012.windowsSdkDir_80a->MSDK\V8.0A
#vs2012.FrameworkDir-WindowsKits\8.0
#vs2013.windowssdkdir->WindowsKits\8.1
#vs2013.windowssdkdir_80->WindowsKits\8.0
#vs2013.windowssdkdir_81->WindowsKits\8.1
#vs2013.windowssdkdir_81a->MSDK\8.1A
#vs2013.frameworkSdkDir->WindowsKits\8.1
#vs2013_xp.windowssdkdir_71A->MSDK\71A
#vs2013_xp.frameworkSdkDir_71A->MSDK\71A
#vs2015.windowssdkdir->WindowsKits\8.1
#vs2015.windowssdkDir_10->windowsKits\10


#8.0 for vs2012
#KitsRoot->8.0
#KitsRoot10->10
#kitsRoot81->8.1
#%programfiles% win64下有效，win32下有效
#%programfiles(x86)% win64下有效，win32下无效


#        (VSVer,VCVer,VCDirName,MSDKVer, WKVer, WKRegName)
VerList = (
         ('2005', '8.0',  'V80',  '',      '',    '',),
         ('2008', '9.0',  'V90',  'v7.0A', '',    '',),
         ('2010', '10.0', 'V100', 'v7.0A', '',    '',),
         #('2012', '11.0', 'V110', 'v8.0', '8.0',  'KitsRoot',),
         ('2012', '11.0', 'V110', '', '8.0',  'KitsRoot',),
         #('2013', '12.0', 'V120', 'v8.1', '8.1',  'KitsRoot81',),
         ('2013', '12.0', 'V120', '', '8.1',  'KitsRoot81',),
         ('2015', '14.0', 'V140', 'v8.1', '10',   'KitsRoot10',)
         )


def getVCInstallDir(VCVer):
    dir = getHKLMValue(r'SOFTWARE\Microsoft\VisualStudio\{VCV}\Setup\VC'.format(VCV=VCVer),'ProductDir')
    if dir :
        return dir.rstrip('\\')
    dir = getHKLMValue(r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\{VCV}\Setup\VC'.format(VCV=VCVer),'ProductDir')
    if dir :
        return dir.rstrip('\\')
    dir = getHKLMValue(r'SOFTWARE\Microsoft\VCExpress\{VCV}\Setup\VC'.format(VCV=VCVer),'ProductDir')
    if dir :
        return dir.rstrip('\\')
    dir = getHKLMValue(r'SOFTWARE\Wow6432Node\Microsoft\VCExpress\{VCV}\Setup\VC'.format(VCV=VCVer),'ProductDir')
    if dir :
        return dir.rstrip('\\')
    return None

def isInstallVC(VCVer):
    if getVCInstallDir(VCVer):
        return True
    return False

def copyFile(nameFrom,dirTo):
    cmd = r'xcopy "{NF}" "{DT}" /I /Y'.format(NF=nameFrom,DT=dirTo)
    os.system(cmd)

def copyDir(dirFrom,dirTo):
    cmd = r'xcopy "{DF}" "{DT}" /I /E /Y'.format(DF=dirFrom,DT=dirTo)
    print(cmd)
    os.system(cmd)

def copyVC(vcVer,VCDirName):
    vcDir = getVCInstallDir(vcVer)
    if dir :
        dirFrom = r'{VCD}\..\Common7'.format(VCD=vcDir)
        dirTo = r'{CP}\Bin\Compiler\{VCDN}\Common7'.format(CP=sys.path[0],VCDN=VCDirName)
        copyDir(dirFrom,dirTo)
        dirFrom = r'{VCD}\..\VC'.format(VCD=vcDir)
        dirTo = r'{CP}\Bin\Compiler\{VCDN}\VC'.format(CP=sys.path[0],VCDN=VCDirName)
        copyDir(dirFrom,dirTo)


def getMSdkDir(ver):
    msdir = getHKLMValue(r'SOFTWARE\Microsoft\Microsoft SDKs\Windows\{VER}'.format(VER=ver),'InstallationFolder')
    if msdir :
        return msdir.rstrip('\\')
    msdir = getHKLMValue(r'SOFTWARE\Wow6432Node\Microsoft\Microsoft SDKs\Windows\{VER}'.format(VER=ver),'InstallationFolder')
    if msdir :
        return msdir.rstrip('\\')
    return None

def copyMicrosoftSDKs(ver):
    dirFrom = getMSdkDir(ver)
    if dirFrom :
        dirTo = r'{CP}\Bin\MicrosoftSDKs\Windows\{VER}'.format(CP=sys.path[0],VER=ver)
        copyDir(dirFrom,dirTo)

def copyMSBuildV110Down(VCDirName):
    nameFrom = r'{PF}\MSBuild\Microsoft.Cpp\v4.0\*.*'.format(PF=GetPFX86Dir())
    dirTo = r'{CP}\Bin\MSBuild\{VCDN}'.format(CP=sys.path[0],VCDN=VCDirName)
    copyFile(nameFrom,dirTo)
    
    dirFrom = r'{PF}\MSBuild\Microsoft.Cpp\v4.0\1033'.format(PF=GetPFX86Dir())
    dirTo = r'{CP}\Bin\MSBuild\{VCDN}\1033'.format(CP=sys.path[0],VCDN=VCDirName)
    copyDir(dirFrom,dirTo)

    dirFrom = r'{PF}\MSBuild\Microsoft.Cpp\v4.0\2052'.format(PF=GetPFX86Dir())
    dirTo = r'{CP}\Bin\MSBuild\{VCDN}\2052'.format(CP=sys.path[0],VCDN=VCDirName)
    copyDir(dirFrom,dirTo)
    
    dirFrom = r'{PF}\MSBuild\Microsoft.Cpp\v4.0\BuildCustomizations'.format(PF=GetPFX86Dir())
    dirTo = r'{CP}\Bin\MSBuild\{VCDN}\BuildCustomizations'.format(CP=sys.path[0],VCDN=VCDirName)
    copyDir(dirFrom,dirTo)

    dirFrom = r'{PF}\MSBuild\Microsoft.Cpp\v4.0\Platforms\Itanium'.format(PF=GetPFX86Dir())
    dirTo = r'{CP}\Bin\MSBuild\{VCDN}\Platforms\Itanium'.format(CP=sys.path[0],VCDN=VCDirName)
    copyDir(dirFrom,dirTo)

    nameFrom = r'{PF}\MSBuild\Microsoft.Cpp\v4.0\Platforms\Win32\*.*'.format(PF=GetPFX86Dir())
    dirTo = r'{CP}\Bin\MSBuild\{VCDN}\Platforms\Win32'.format(CP=sys.path[0],VCDN=VCDirName)
    copyFile(nameFrom,dirTo)

    dirFrom = r'{PF}\MSBuild\Microsoft.Cpp\v4.0\Platforms\Win32\1033'.format(PF=GetPFX86Dir())
    dirTo = r'{CP}\Bin\MSBuild\{VCDN}\Platforms\Win32\1033'.format(CP=sys.path[0],VCDN=VCDirName)
    copyDir(dirFrom,dirTo)

    dirFrom = r'{PF}\MSBuild\Microsoft.Cpp\v4.0\Platforms\Win32\2052'.format(PF=GetPFX86Dir())
    dirTo = r'{CP}\Bin\MSBuild\{VCDN}\Platforms\Win32\2052'.format(CP=sys.path[0],VCDN=VCDirName)
    copyDir(dirFrom,dirTo)

    dirFrom = r'{PF}\MSBuild\Microsoft.Cpp\v4.0\Platforms\Win32\PlatformToolsets\{VCDN}'.format(PF=GetPFX86Dir(),VCDN=VCDirName)
    dirTo = r'{CP}\Bin\MSBuild\{VCDN}\Platforms\Win32\PlatformToolsets\{VCDN}'.format(CP=sys.path[0],VCDN=VCDirName)
    copyDir(dirFrom,dirTo)

    nameFrom = r'{PF}\MSBuild\Microsoft.Cpp\v4.0\Platforms\x64\*.*'.format(PF=GetPFX86Dir())
    dirTo = r'{CP}\Bin\MSBuild\{VCDN}\Platforms\x64'.format(CP=sys.path[0],VCDN=VCDirName)
    copyFile(nameFrom,dirTo)

    dirFrom = r'{PF}\MSBuild\Microsoft.Cpp\v4.0\Platforms\x64\1033'.format(PF=GetPFX86Dir())
    dirTo = r'{CP}\Bin\MSBuild\{VCDN}\Platforms\x64\1033'.format(CP=sys.path[0],VCDN=VCDirName)
    copyDir(dirFrom,dirTo)

    dirFrom = r'{PF}\MSBuild\Microsoft.Cpp\v4.0\Platforms\x64\2052'.format(PF=GetPFX86Dir())
    dirTo = r'{CP}\Bin\MSBuild\{VCDN}\Platforms\x64\2052'.format(CP=sys.path[0],VCDN=VCDirName)
    copyDir(dirFrom,dirTo)

    dirFrom = r'{PF}\MSBuild\Microsoft.Cpp\v4.0\Platforms\x64\PlatformToolsets\{VCDN}'.format(PF=GetPFX86Dir(),VCDN=VCDirName)
    dirTo = r'{CP}\Bin\MSBuild\{VCDN}\Platforms\x64\PlatformToolsets\{VCDN}'.format(CP=sys.path[0],VCDN=VCDirName)
    copyDir(dirFrom,dirTo)
    

def copyMSBuildV110AndUp(VCDirName):
    dirFrom = r'{PF}\MSBuild\Microsoft.Cpp\v4.0\{VCDN}'.format(PF=GetPFX86Dir(),VCDN=VCDirName)
    dirTo = r'{CP}\Bin\MSBuild\{VCDN}'.format(CP=sys.path[0],VCDN=VCDirName)
    copyDir(dirFrom,dirTo)

def copyMSBuild(VCDirName):
    temp = VCDirName[1:]
    if int(temp) > 110:
        copyMSBuildV110AndUp(VCDirName)
    else:
        copyMSBuildV110Down(VCDirName)

def getWindowsKitsDir(WKRegName):
    wkDir = getHKLMValue(r'SOFTWARE\Wow6432Node\Microsoft\Windows Kits\Installed Roots',WKRegName)
    if wkDir:
        return wkDir.rstrip('\\')
    wkDir = getHKLMValue(r'SOFTWARE\Microsoft\Windows Kits\Installed Roots',WKRegName)
    if wkDir:
        return wkDir.rstrip('\\')
    return None

def copyWindowsKits(WKVer,WKRegName):
    dirFrom = getWindowsKitsDir(WKRegName)
    if dirFrom :
        dirTo = r'{CP}\Bin\MicrosoftKits\Windows\{WKV}'.format(CP=sys.path[0],WKV=WKVer)
        copyDir(dirFrom,dirTo)

def getInnoSetupDir():
    ISDir = getHKLMValue(r'SOFTWARE\Classes\InnoSetupScriptFile\shell\Compile\command',r'')
    #Always ISDir = '"C:\Program Files (x86)\Inno Setup 5\Compil32.exe" /cc "%1"'
    if ISDir :
        ISDir = ISDir.lstrip('"')
        ISDir = ISDir[:ISDir.find('"')]
    return ISDir

def callInnoSetup():
    ISDir = getInnoSetupDir()
    if ISDir:
        cmd = r'"{ISD}" /cc "{CF}\{ISS}"'.format(ISD=ISDir,CF=sys.path[0],ISS=r'VSMCPSetup.iss')
        os.system(cmd)

if __name__ == '__main__' :
    '''
    for VSVer,VCVer,VCDirName,MSDKVer,WKVer,WKRegName in VerList:
        if not VSVer or not VCVer:
            continue

        if not isInstallVC(VCVer):
            continue
        copyVC(VCVer,VCDirName)

        if MSDKVer:
            copyMicrosoftSDKs(MSDKVer)
            
        if WKVer and WKRegName:
            copyWindowsKits(WKVer,WKRegName)
        
        #copy MSBuild
        print('Copy MSBuild')
        copyMSBuild(VCDirName)
'''
    callInnoSetup()

    

    

