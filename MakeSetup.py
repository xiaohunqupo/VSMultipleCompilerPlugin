#!/usr/bin/env python
#coding=utf-8

import winreg
import enum
import sys
import os

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
#%programfiles%
#%programfiles(x86)%


#        (VSVer,VCVer,VCDirName,MSDKVer, WKVer, WKRegName)
VerList = (
         ('2005', '8.0',  'v80',  '',      '',    '',),
         ('2008', '9.0',  'v90',  'v7.0A', '',    '',),
         ('2010', '10.0', 'v100', 'v7.0A', '',    '',),
         ('2012', '11.0', 'v110', 'v8.0', '8.0',  'KitsRoot',),
         ('2013', '12.0', 'v120', 'v8.1', '8.1',  'KitsRoot81',),
         ('2015', '14.0', 'v140', 'v8.1', '10',   'KitsRoot82',)
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
    if getVCInstallDir(vsVersion) :
        return True
    return False

def copyDir(dirFrom,dirTo):
    cmd = r'xcopy "%s" "%s" /I /E /Y'%(dirFrom,dirTo)
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

def copyMSBuild():
    pass

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
        if !isInstallVS(VSVer):
            continue
        if VCVer && VCDirName:
            copyVC(VCVer,VCDirName)
        if MSDKVer:
            copyMicrosoftSDKs(MSDKVer)
        if WKVer && WKRegName:
            copyWindowsKits(WKVer,WKRegName)
        
    #copy MSBuild
    print('Copy MSBuild')
    copyMSBuild

    #copy WindowsKits
    print('Copy MSBuild')
    copyWindowsKits()

    #download vcredist

    

    

