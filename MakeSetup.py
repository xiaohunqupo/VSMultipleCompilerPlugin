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
    value = None
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,path)
        value,type = winreg.QueryValueEx(key,name)
    except WindowsError:
        pass
    return value

def getVCInstallDir(vsVersion):
    vcInstallDir = None
    vcVersion = None
    if vsVersion == VSVersion.VS2005:
        vcVersion = r'8.0'
    elif vsVersion == VSVersion.VS2008:
        vcVersion = r'9.0'
    elif vsVersion == VSVersion.VS2010:
        vcVersion = r'10.0'
    elif vsVersion == VSVersion.VS2012:
        vcVersion = r'11.0'
    elif vsVersion == VSVersion.VS2013:
        vcVersion = r'12.0'
    elif vsVersion == VSVersion.VS2015:
        vcVersion = r'14.0'
    else :
        return vsInstallDir

    vcInstallDir = getHKLMValue(r'SOFTWARE\Microsoft\VisualStudio\%s\Setup\VC'%vcVersion,'ProductDir')
    if vcInstallDir != None:
        return vcInstallDir
    vcInstallDir = getHKLMValue(r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\%s\Setup\VC'%vcVersion,'ProductDir')
    if vcInstallDir != None:
        return vcInstallDir
    vcInstallDir = getHKLMValue(r'SOFTWARE\Microsoft\VCExpress\%s\Setup\VC'%vcVersion,'ProductDir')
    if vcInstallDir != None:
        return vcInstallDir

    vcInstallDir = getHKLMValue(r'SOFTWARE\Wow6432Node\Microsoft\VCExpress\%s\Setup\VC'%vcVersion,'ProductDir')
    if vcInstallDir != None:
        return vcInstallDir
    return vcInstallDir

def isInstallVS(vsVersion):
    if getVCInstallDir(vsVersion) != None :
        return True
    return False

def copyDir(dirFrom,dirTo):
    cmd = r'xcopy "%s" "%s" /I /E /Y'%(dirFrom,dirTo)
    #print(cmd)
    os.system(cmd)

def copyVC(vsVersion):
    vcInstallDir = None
    vcVersion = None
    if vsVersion == VSVersion.VS2005:
        vcVersion = r'80'
    elif vsVersion == VSVersion.VS2008:
        vcVersion = r'90'
    elif vsVersion == VSVersion.VS2010:
        vcVersion = r'100'
    elif vsVersion == VSVersion.VS2012:
        vcVersion = r'110'
    elif vsVersion == VSVersion.VS2013:
        vcVersion = r'110'
    elif vsVersion == VSVersion.VS2015:
        vcVersion = r'140'

    vcInstallDir = getVCInstallDir(vsVersion)
    if vcInstallDir != None:
        dirFrom = vcInstallDir + r'\..\Common7'
        dirTo = sys.path[0]+r'\Bin\Compiler\v'+vcVersion+r'\Common7'
        copyDir(dirFrom,dirTo)
        dirFrom = vcInstallDir + r'\..\VC'
        dirTo = sys.path[0]+r'\Bin\Compiler\v'+vcVersion+r'\VC'
        copyDir(dirFrom,dirTo)

def getMSdkDir(vsVersion):
    msdkDir = None
    msdkVersion = none
    msdkVersion = None
    if vsVersion == VSVersion.VS2005:
        return msdkVersion   #No Need Copy
    elif vsVersion == VSVersion.VS2008:
        msdkVersion = r'7.0A'
    elif vsVersion == VSVersion.VS2010:
        msdkVersion = r'7.0A'
    elif vsVersion == VSVersion.VS2012:
        msdkVersion = r'8.0'
    elif vsVersion == VSVersion.VS2013:
        msdkVersion = r'8.1'
    elif vsVersion == VSVersion.VS2015:
        msdkVersion = r'8.1'
    else :
        return vsInstallDir

    msdkDir = getHKLMValue(r'SOFTWARE\Microsoft\Microsoft SDKs\Windows\v'%msdkVersion,'InstallationFolder')
    if msdkDir != None:
        return msdkDir
    msdkDir = getHKLMValue(r'SOFTWARE\Wow6432Node\Microsoft\Microsoft SDKs\Windows\v'%msdkVersion,'InstallationFolder')
    if msdkDir != None:
        return msdkDir
    return msdkDir

def copyMicrosoftSDKs(vsVersion):
    msdkDir = None
    msdkVersion = None
    if vsVersion == VSVersion.VS2005:
        return 
    elif vsVersion == VSVersion.VS2008:
        msdkVersion = r'7.0A'
    elif vsVersion == VSVersion.VS2010:
        msdkVersion = r'7.0A'
    elif vsVersion == VSVersion.VS2012:
        msdkVersion = r'8.0'
    elif vsVersion == VSVersion.VS2013:
        msdkVersion = r'8.1'
    elif vsVersion == VSVersion.VS2015:
        msdkVersion = r'8.1'
    else :
        return vsInstallDir

    msdkDir = getMicrosoftSDKsDir(vsVersion)
    if msdkDir != None:
        dirFrom = msdkDir
        dirTo = sys.path[0]+r'\Bin\MicrosoftSDKs\Windows\v'+msdkVersion
        copyDir(dirFrom,dirTo)

def copyMSBuild():
    

def getWindowsKitsDir():
    windowsKitsDir = None;
    windowsKitsDir = getHKLMValue(r'SOFTWARE\Wow6432Node\Microsoft\Windows Kits\Installed Roots','KitsRoot10')
    if windowsKitsDir != None:
        return windowsKitsDir
    windowsKitsDir = getHKLMValue(r'SOFTWARE\Microsoft\Windows Kits\Installed Roots','KitsRoot10')
    if windowsKitsDir != None:
        return windowsKitsDir
    return None

##versions=('')
def copyWindowsKits(versions):
    for version in versions:
        path = getWindowsKitsDir()


##def PrintReg() :
##    try:
##        i = 0
##        while 1:
##            name,value,type = winreg.EnumValue(key,i)
##            print(repr(name),value,type)
##            i+=1
##    except WindowsError:
##        pass
##
##    value,type = winreg.QueryValueEx(key,'Close')
##    print(value,type)
##
##    temp = winreg.QueryValueEx(key,'Close')
##    print(temp)

def isInstallVS(vsVersion):
    if getVCInstallDir(vsVersion) != None :
        return True
    return False

if __name__ == '__main__' :
    #copy VC
    print('Copy Visual C++ comilers')
    if isInstallVS(VSVersion.VS2005) :
        copyVC(VSVersion.VS2005)
    elif isInstallVS(VSVersion.VS2008) :
        copyVC(VSVersion.VS2008)
    elif isInstallVS(VSVersion.VS2010) :
        copyVC(VSVersion.VS2010)
    elif isInstallVS(VSVersion.VS2010) :
        copyVC(VSVersion.VS2010)
    elif isInstallVS(VSVersion.VS2012) :
        copyVC(VSVersion.VS2012)
    elif isInstallVS(VSVersion.VS2013) :
        copyVC(VSVersion.VS2013)
    elif isInstallVS(VSVersion.VS2015) :
        copyVC(VSVersion.VS2015)

    #copy MicrosoftSDKs
    print('Copy MicrosfotSDKs')

    if isInstallVS(VSVersion.VS2005) :
        copyMicrosoftSDKs(VSVersion.VS2005)
    elif isInstallVS(VSVersion.VS2008) :
        copyMicrosoftSDKs(VSVersion.VS2008)
    elif isInstallVS(VSVersion.VS2010) :
        copyMicrosoftSDKs(VSVersion.VS2010)
    elif isInstallVS(VSVersion.VS2010) :
        copyMicrosoftSDKs(VSVersion.VS2010)
    elif isInstallVS(VSVersion.VS2012) :
        copyMicrosoftSDKs(VSVersion.VS2012)
    elif isInstallVS(VSVersion.VS2013) :
        copyMicrosoftSDKs(VSVersion.VS2013)
    elif isInstallVS(VSVersion.VS2015) :
        copyMicrosoftSDKs(VSVersion.VS2015)

    #copy MSBuild
    print('Copy MSBuild')
    copyMSBuild

    #copy WindowsKits
    print('Copy MSBuild')
    copyWindowsKits()

    #download vcredist

    

    

