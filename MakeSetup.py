#!/usr/bin/env python
#coding=utf-8

import winreg
import enum
import sys

class VSVersion(enum.Enum):
    VS2005 = 1
    VS2008 = 2
    VS2010 = 3
    VS2012 = 4
    VS2013 = 5
    VS2015 = 6
    

class WindowsSdkVersion:



key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r'SYSTEM\CurrentControlSet\Services\Tcpip\Performance')

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
    else
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

def IsInstallVS(vsVersion):
    if GetVCInstallDir(vsVersion) != None :
        return True
    return False

def CopyDir(dirFrom,dirTo):
    os.system(r'xcopy %s %s /I /E /Y'%(dirFrom,dirTo))

def CopyVCToBin(vsVersion):
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

    vcInstallDir = GetVCInstallDir(vsVersion)
    if vcInstallDir != None:
        dirFrom = vcInstallDir + r'\..\..'
        dirTo = sys.[path0]+r'\Bin\Compiler\v'+vcVersion
        CopyDir(dirFrom,dirTo)


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

def IsInstallVS(vsVersion):
    if GetVCInstallDir(vsVersion) != None :
        return True
    return False

if __name__ == '__main__' :
    #copy VC
    if IsInstallVS(VSVersion.VS2005)
        CopyVCToBin(VSVersion.VS2005)
    elif IsInstallVS(VSVersion.VS2008)
        CopyVCToBin(VSVersion.VS2008)
    elif IsInstallVS(VSVersion.VS2010)
        CopyVCToBin(VSVersion.VS2010)
    elif IsInstallVS(VSVersion.VS2010)
        CopyVCToBin(VSVersion.VS2010)
    elif IsInstallVS(VSVersion.VS2012)
        CopyVCToBin(VSVersion.VS2012)
    elif IsInstallVS(VSVersion.VS2013)
        CopyVCToBin(VSVersion.VS2013)
    elif IsInstallVS(VSVersion.VS2015)
        CopyVCToBin(VSVersion.VS2015)

    #copy MicrosoftSDKs

    #copy MSBuild

    #copy WindowsKits

    #download vcredist

    

    

