#!/usr/bin/env python3
#12.04.2019 by Artur Wu
# system rsync of files and linking source and dest and some file logging
# used for managing studies on pacs

import sys
import os
import subprocess
import time
from os.path import join, getsize

# source_fs = sys.argv[1]
# dest_dir = ''
filetolog = '/tmp/rsync_check.txt'

def file_writer(title,writeit):
    f = open(filetolog, "a+")
    t = time.ctime()
    logMe0 = str(writeit)
    sidx = (str(t) + " " + title + logMe0 + "\n")
    f.write(sidx)
    f.close()

def check_user_login():
    try:
        loginname=os.getlogin()
    except:
        loginname=os.getenv('SUDO_USER')
        if loginname == None:
            loginname=os.getenv('USER')
        else:
            loginname='Niema'
    return(loginname)

def check_space_fs(fspath):
    """
    checks statvfs and calculates free space based on block_size and number of blocks
    """
    statvfs = os.statvfs(fspath)
    total_space_fs = statvfs.f_frsize * statvfs.f_blocks
    free_space_fs = statvfs.f_frsize * statvfs.f_bfree
    print("Total space on fs containing", fspath, "is:", int(total_space_fs/(1024**3)), "Free space: ", int(free_space_fs/(1024**3)))
    return(total_space_fs,free_space_fs)

def count_files(dirroot):
    # for root, dirs, files in os.walk(dirroot):
    #     print(root, sum(getsize(join(root, name)) for name in files), "Bytes in:", len(files), "files")
    filescount=0
    for files in os.walk(dirroot,followlinks=False):
        c = int(len(files[2]))
        filescount=filescount + c
    return(filescount)

def rsync(sourceDir, destDir):
    a = check_user_login()
    writeit = ( "user:", a, "pliki z: ", sourceDir, "przenoszone do: ", destDir)
    file_writer("Rsync start:", writeit)
    subprocess.call(['rsync','-avu','--remove-source-files', sourceDir, destDir])
    file_writer("Rsync koniec:", writeit)

def move_dir(oldname,newname):
    a = check_user_login()
    subprocess.call(['mv', oldname, newname])
    writeit = ( "user:", a, "katalog: ", oldname, "przeniesiony na: ", newname)
    file_writer("Old dir move:", writeit)

def link_to_dest(newdest, oldname):
    a = check_user_login()
    subprocess.call(['ln', '-s', newdest, oldname])
    writeit = ( "user:", a, "katalog: ", newdest, "zlinkowany do: ", oldname)
    file_writer("Link:", writeit)

########################################

def main():
    """
        Skrypt odpalamy w screenie: screen -S mojaNazwa

        Nalezy skonfigurowac rootdcmdir w skrypcie. Domyslnie --> rootdcmdir='/var/lib/expacs/ONLINE'

        Jako argumenty skryptu podaj:
        ./move_rsync_study.py rok miesiac dzien1 dzien2 dzien3 /katalog/docelowy
        /katalog/docelowy to miejsce gdzie zostanie stworzona struktura katalogow poczawszy od lat
        
            example: ./move_rsync_study.py 2016 4 6 24 30 /mnt/worek/BACK_ONLINE/
        
        --> przeniesie 6,25,30 kwietnia 2016 roku do /mnt/worek/BACK_ONLINE/
        stworzy drzewo katalogow:
        /mnt/worek/BACK_ONLINE/2016/4/6
        /mnt/worek/BACK_ONLINE/2016/4/24
        /mnt/worek/BACK_ONLINE/2016/4/30
        
        Jesli jako dni podamy 0, przeniesie caly miesiac

            example: ./move_rsync_study.py 2016 4 0 /mnt/worek/BACK_ONLINE/
    """
    rootdcmdir='/var/lib/expacs/ONLINE'
    # rootdcmdir='/home/arturwu/projects/python'
    
    if int(len(sys.argv)) < 5:
        print(main.__doc__)
        # import test
    else:
        # if os.path.exists(sourceDir):
        #     print("Src:", sourceDir)
        # else:
        #     print('Katalog zrodlowy NIE istnieje !')

        sourceY=sys.argv[1]
        sourceM=sys.argv[2]
        days=sys.argv[3:-1]
        gooddays=[]
        destDirRoot = sys.argv[-1]
        srcfilecount = {}
        sourceDir = []
        fc = 0
        totalfc = 0

        if days[0] == '0':
            print("Whole month")
            p=os.path.join(rootdcmdir,sourceY,sourceM)
            gooddays.append(sourceM)
            sourceDir.append(p)
            destDir = os.path.join(destDirRoot, sourceY)
            if os.path.islink(sourceDir[0]):
                pass
            else:
                fc = count_files(sourceDir[0])
                totalfc = int(fc)
            srcfilecount.update({sourceDir[0]:fc})
            # print("Src:", sourceDir)
        else:
            print("Several days", len(days))
            destDir = os.path.join(destDirRoot, sourceY, sourceM)
            for d in days:
                sd = os.path.join(rootdcmdir,sourceY,sourceM,d)
                if os.path.exists(sd):
                    if os.path.islink(sd):
                        print("To link")
                    else:
                        gooddays.append(d)
                        sourceDir.append(sd)
                        fc = count_files(sd)
                        totalfc += fc
                    srcfilecount.update({sd:fc})

        countbefore = count_files(destDir)

        # petla robi rsynca
        for d in sourceDir:
            if os.path.exists(destDir):
                rsync(d,destDir)
            else:
                subprocess.call(['mkdir','-p',destDir])
                rsync(d,destDir)

        countafter = count_files(destDir)


        # print()
        # print("Pliki w celu przed:", countbefore)
        # print("Pliki w celu po:", countafter)
        # print("Pliki/katalog:", srcfilecount)
        # print("Src:", sourceDir)
        # print("Days req:", days)
        # print("Days ok:", gooddays)
        # print("Dest:", destDir)

        # zaloguj0 = ("Src:", sourceDir, "Dest:", destDir)
        zaloguj1 = ("Pliki w zrodle:", totalfc, "Pliki w celu przed:", countbefore, "Pliki w celu po:", countafter)
        # file_writer("Dane",zaloguj0)
        file_writer("Dane",zaloguj1)

        if totalfc + countbefore == countafter:
            file_writer("STATUS","RSYNC - Dobrze")
            print("Dobrze")
            for num in range(len(sourceDir)):
                print(num)
                namechange = (sourceDir[num] + "_old")
                move_dir(sourceDir[num],namechange)
                logstring1 = str(("Move from:",sourceDir[num],"to:",namechange))
                file_writer("STATUS MOVE",logstring1)
                print("Move:",sourceDir[num],"to:",namechange)
                linkdest = os.path.join(destDir, str(gooddays[num]))
                print("Link dest:", linkdest)
                link_to_dest(linkdest,sourceDir[num])
                logstring2 = str(("link from:",linkdest,"to:",sourceDir[num]))
                file_writer("STATUS LINK",logstring2)
        else:
            print("Niedobrze, czyli ERROR")
            print("Suma plikow w zrodle jest rozna od sumy plikow w celu.")
            print("Moze rsync byl przerwany? Nie robie linkow...")



if __name__ == '__main__':
    main()