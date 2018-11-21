import datetime
import time
import datetime
import BaseFunction_Lovezuoye
import baseFunction_paizuoye
import paramiko
import os
import sys
from shutil import copyfile


host_name = "10.203.6.164"
username = "stf"
password = "stf"
port = 22


def get_remote_date():
    nowtime = datetime.datetime.now()
    gettime = nowtime + datetime.timedelta(days=-2)
    timer = gettime.strftime('%Y-%m-%d')
    return timer

sys_path="E:\\PycharmProjects\\paizhao_auto"
sys.path.append(sys_path)
import BaseFunction_Lovezuoye
import baseFunction_paizuoye

#localdir_orig = os.getcwd()+ "\\questionPic"
localdir_orig = "E:\\PycharmProjects\\paizhao_auto\\questionPic"
#localdir_labe = os.getcwd()+"\\questionPic_17zuoye"
localdir_labe = "E:\\PycharmProjects\\paizhao_auto\\questionPic_17zuoye"
#localdir_screenshot = os.getcwd()+"\\screenshots"
localdir_screenshot = "E:\\PycharmProjects\\paizhao_auto\\screenshots"
remote_orig = "/home/stf/arithmetic_check/pics/" + get_remote_date() + "/comp_orig/"
remote_labe = "/home/stf/arithmetic_check/pics/" + get_remote_date() + "/comp_labe/"

def auto_rename():
    filekey = os.listdir(localdir_labe)
    n=0
    for i in filekey:
        oldname = "E:\\PycharmProjects\\paizhao_auto\\questionPic_17zuoye\\"+filekey[n]
        timer = time.strftime('%m%d', time.localtime(time.time()))
        newname ="E:\\PycharmProjects\\paizhao_auto" + '\\screenshots\\'+filekey[n]+ "_17zuoye" + "__"+ get_remote_date() +'.png'
        #print(newname)
        n=n+1
        os.rename(oldname,newname)

auto_rename()

def autoMovFile_from_serv():
     conn = paramiko.Transport(host_name,port)
     conn.connect(username=username,password=password)
     sftp = paramiko.SFTPClient.from_transport(conn)

     pic_files = sftp.listdir(remote_orig)
     for f in pic_files:
         print("Downloading pic files in:"+ remote_orig)
         print("NOW IS:"+(remote_orig+"/"+f))
         sftp.get(remote_orig+"/"+f,os.path.join(localdir_orig,f))
         print("SUCCESS!")

     pic_lable_files=sftp.listdir(remote_labe)
     for f in pic_lable_files:
         print("Downloading pic files in:" + remote_labe)
         print("NOW IS:" + (remote_labe + "/" + f))
         sftp.get(remote_labe + "/" + f, os.path.join(localdir_labe, f))
         print("SUCCESS!")
     sftp.close()

def copyFiles(sourceDir,  targetDir):
    for file in os.listdir(sourceDir):
         sourceFile = os.path.join(sourceDir,  file)
         targetFile = os.path.join(targetDir,  file)
         if os.path.isfile(sourceFile):
             if not os.path.exists(targetDir):
                 os.makedirs(targetDir)
             if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                     open(targetFile, "wb").write(open(sourceFile, "rb").read())
         if os.path.isdir(sourceFile):
             First_Directory = False
             copyFiles(sourceFile, targetFile)

def auto_generate_files():
    dst_folder= "E:\\PycharmProjects\\paizhao_auto\\Finalresult\\"+get_remote_date()
    if not os.path.isdir("E:\\PycharmProjects\\paizhao_auto\\Finalresult\\"+get_remote_date()):
        os.mkdir("E:\\PycharmProjects\\paizhao_auto\\Finalresult\\"+get_remote_date())
    copyFiles(localdir_screenshot,dst_folder)
    copyFiles(localdir_orig,dst_folder)

def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)



if __name__ == '__main__':
    #autoMovFile_from_serv()
    auto_rename()
    baseFunction_paizuoye.syncpic_paizuoye()
    BaseFunction_Lovezuoye.syncpic_lovezuoye()
    auto_generate_files()
    del_file(localdir_orig)
    del_file(localdir_labe)
    del_file(localdir_screenshot)
