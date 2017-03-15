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
    

class VSVersion(enum.Enum):
    VS2005 = 1
    VS2008 = 2
    VS2010 = 3
    VS2012 = 4
    VS2013 = 5
    VS2015 = 6
    
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
         ('2012', '11.0', 'V110', 'v8.0', '8.0',  'KitsRoot',),
         ('2013', '12.0', 'V120', 'v8.1', '8.1',  'KitsRoot81',),
         ('2015', '14.0', 'V140', 'v8.1', '10',   'KitsRoot82',)
         )


def getVCInstallDir(ver):
    dir = getHKLMValue(r'SOFTWARE\Microsoft\VisualStudio\%s\Setup\VC'%ver,'ProductDir')
    if dir :
        return dir
    dir = getHKLMValue(r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\%s\Setup\VC'%ver,'ProductDir')
    if dir :
        return dir
    dir = getHKLMValue(r'SOFTWARE\Microsoft\VCExpress\%s\Setup\VC'%ver,'ProductDir')
    if dir :
        return dir
    dir = getHKLMValue(r'SOFTWARE\Wow6432Node\Microsoft\VCExpress\%s\Setup\VC'%ver,'ProductDir')
    if dir :
        return dir
    return None

def isInstallVS(ver):
    if getVCInstallDir(vsVersion):
        return True
    return False

def copyFile(nameFrom,dirTo):
    cmd = r'xcopy "{namefrom}" "{dirto}" /Y'.format(namefrom=nameFrom,dirto=dirTo)
    os.system(cmd)

def copyDir(dirFrom,dirTo):
    cmd = r'xcopy "{dirFrom}" "{dirTo}" /I /E /Y'.format(diurFrom=dirFrom,dirTo=dirTo)
    #print(cmd)
    os.system(cmd)

def copyVC(vcVer,VCDirName):
    vcDir = getVCInstallDir(ver)
    if dir :
        dirFrom = r'{VCPath}\..\Common7'.format(VCPath=vcDir)
        dirTo = r'{currentPath}\Bin\Compiler\{ver}\Common7'.format(currentPath=sys.path[0],ver=VCDirName)
        copyDir(dirFrom,dirTo)
        dirFrom = r'{VCPath}\..\VC'.format(VCPath=vcInstallDir)
        dirTo = r'{currentPath}\Bin\Compiler\{ver}\VC'.format(currentPath=sys.path[0],ver=VCDirName)
        copyDir(dirFrom,dirTo)


def getMSdkDir(ver):
    msdir = getHKLMValue(r'SOFTWARE\Microsoft\Microsoft SDKs\Windows\{ver}'.format(ver=ver),'InstallationFolder')
    if msdir :
        return msdir
    msdir = getHKLMValue(r'SOFTWARE\Wow6432Node\Microsoft\Microsoft SDKs\Windows\{ver}'.format(ver=ver),'InstallationFolder')
    if msdir :
        return msdir
    return None

def copyMicrosoftSDKs(ver):
    dirFrom = getMSdkDir(ver)
    if dirFrom :
        dirTo = +r'{currentPath}\Bin\MicrosoftSDKs\Windows\{ver}'.format(currentPath=sys.path[0],ver=ver)
        copyDir(dirFrom,dirTo)

def copyMSBuildV110Down(VSVer,VCDirName):
    nameFrom = r'{pf}\MSBuild\Microsoft.Cpp\v4.0\*.*'.format(pf=GetPFX86Dir())
    dirTo = r'{currentPath}\MSBuild\{ver}'.format(currentPath=sys.path[0],ver=VCDirName)
    copyFile(nameFrom,dirTo)
    
    dirFrom = r'{pf}\MSBuild\Microsoft.Cpp\v4.0\1033'.format(pf=GetPFX86Dir())
    dirTo = r'{currentPath}\MSBuild\{ver}\1033'.format(currentPath=sys.path[0],ver=VCDirName)
    copyFile(nameFrom,dirTo)

    dirFrom = r'{pf}\MSBuild\Microsoft.Cpp\v4.0\2052'.format(pf=GetPFX86Dir())
    dirTo = r'{currentPath}\MSBuild\{ver}\2052'.format(currentPath=sys.path[0],ver=VCDirName)
    copyFile(nameFrom,dirTo)
    
    dirFrom = r'{pf}\MSBuild\Microsoft.Cpp\v4.0\BuildCustomizations'.format(pf=GetPFX86Dir())
    dirTo = r'{currentPath}\MSBuild\{ver}\BuildCustomizations'.format(currentPath=sys.path[0],ver=VCDirName)
    copyFile(nameFrom,dirTo)

    dirFrom = r'{pf}\MSBuild\Microsoft.Cpp\v4.0\Platforms'.format(pf=GetPFX86Dir())
    dirTo = r'{currentPath}\MSBuild\{ver}\Platforms'.format(currentPath=sys.path[0],ver=VCDirName)
    copyFile(nameFrom,dirTo)

def copyMSBuildV110AndUp(VCDirName):
    dirFrom = r'{pf}\MSBuild\Microsoft.Cpp\v4.0\{ver}'.format(pf=GetPFX86Dir(),ver=VCDirName)
    dirTo = r'{currentPath}\MSBuild\{ver}'.format(currentPath=sys.path[0],ver=VCDirName)
    copyDir(dirFrom,dirTo)

def getWindowsKitsDir(name):
    wkDir = getHKLMValue(r'SOFTWARE\Wow6432Node\Microsoft\Windows Kits\Installed Roots',name)
    if wkDir:
        return wkDir
    wkDir = getHKLMValue(r'SOFTWARE\Microsoft\Windows Kits\Installed Roots',name)
    if wkDir:
        return wkDir
    return None

def copyWindowsKits(ver,name):
    dirFrom = getWindowsKitsDir(name)
    if dirFrom :
        dirTo = r'{curpath}\Bin\MicrosoftKits\Windows\{ver}'.format(curpath=sys.path[0],ver=name)
        copyDir(dirFrom,dirTo)


def isInstallVS(vsVersion):
    if getVCInstallDir(vsVersion) != None :
        return True
    return False

if __name__ == '__main__' :
    for VSVer,VCVer,VCDirName,MSDKVer,WKVer,WKRegName,WKDir in VerList:
        if not isInstallVS(VSVer):
            continue
        if VCVer and VCDirName:
            copyVC(VCVer,VCDirName)
        if MSDKVer:
            copyMicrosoftSDKs(MSDKVer)
        if WKVer and WKRegName:
            copyWindowsKits(WKVer,WKRegName)
        
    #copy MSBuild
    print('Copy MSBuild')
    copyMSBuild

    #copy WindowsKits
    print('Copy MSBuild')
    copyWindowsKits()

    #download vcredist

    

    

