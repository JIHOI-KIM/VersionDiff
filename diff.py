import sys
import os
import hashlib

def Listing(fileList, Dir, Parent="") :
    WorkDir = os.path.join(Dir, Parent)
    items = os.listdir(WorkDir)
    for item in items :
        link = os.path.join(Parent, item)
        AbsLink = os.path.join(Dir, link)

        if os.path.isdir(AbsLink) :
            Listing(fileList, Dir, link)
        else :
            fileList.append(link)

if len(sys.argv) != 3 :
    print("Usage : script.py [DIR OLD] [DIR NEW]")

DirA = sys.argv[1]
DirB = sys.argv[2]

print("[=======================================]")
print("[+] Diffing [%s] vs [%s]" %(DirA, DirB))

error = 0
if not os.path.isdir(DirA) :
    print("[!] Dir %s Not Exist." % DirA)
    error += 1 
if not os.path.isdir(DirB) :
    print("[!] Dir %s Not Exist." % DirB)
    error += 1
if error > 0 :
    print("[-] Error Found. Quit Program.")

print("[=======================================]")

FileAList = []
FileBList = []

Listing(FileAList, DirA)
print("[+] Listing %s Done. (%d item)" %(DirA, len(FileAList)))
Listing(FileBList, DirB)
print("[+] Listing %s Done. (%d item)" %(DirB, len(FileBList)))

SAME    = []
NEW     = []
DELETED = []
DIFF    = {}

for i in FileAList :
    if i in FileBList :
        SAME.append(i)
    else :
        DELETED.append(i)

for i in FileBList :
    if i not in FileAList :
        NEW.append(i)

count = 0
sameSize = len(SAME)

for name in SAME :
    fileA = os.path.join(DirA, name)
    fileB = os.path.join(DirB, name)
    
    fpA = open(fileA, "rb")
    fpB = open(fileB, "rb")

    contentA = fpA.read()
    contentB = fpB.read()

    fpA.close()
    fpB.close()

    encA = hashlib.md5()
    encB = hashlib.md5()

    encA.update(contentA)
    encB.update(contentB)

    hashA = encA.hexdigest()
    hashB = encB.hexdigest()
    
    if not hashA == hashB :
        DIFF[name] = [hashA, hashB]
    
    count = count + 1
    print("[~] DIFFING... %05d / %05d" % (count, sameSize), end="\r")

print("")
print("[=======================================]")
print("[+] NEW ITEMS : %d" % len(NEW))
print("[+] DELETED ITEMS : %d" % len(DELETED))
print("[+] DIFF ITEMS : %d" % len(DIFF)) 
print("[+] SAME ITEMS : %d" % (len(SAME) - len(DIFF))) 

print("[=======================================]")

outfile = "out.txt"
if os.path.isfile(outfile) :
    print("[!] WARNING : Overwriting file [%s]..." % outfile)

fout = open(outfile, "wt")

print("[=======================================]")
count = 0
for item in NEW : 
    count = count+1
    if count < 5 :
        print("[NEW    ] %s" % item)
    elif count == 5 :
        print("WRITING ...")
    else :
        print("[NEW     ] %05d / %05d" % (count, len(NEW)), end="\r")

    fout.write("[NEW     ] %s\n" % item)
print("")
print("DONE.")


print("[=======================================]")
count = 0
for item in DELETED : 
    count = count+1
    if count < 5 :
        print("[DELETED] %s" % item)
    elif count == 5 :
        print("WRITING ...")
    else :
        print("[DELETED] %05d / %05d" % (count, len(DELETED)), end="\r")

    fout.write("[DELETED] %s\n" % item)
print("")
print("DONE.")


print("[=======================================]")
count = 0
for item in DIFF : 
    count = count+1
    if count < 5 :
        print("[DIFF   ] %s" % item)
    elif count == 5 :
        print("WRITING ...")
    else :
        print("[DIFF    ] %05d / %05d" % (count, len(DIFF)), end="\r")

    fout.write("[DIFF    ] %s\n" % item)
print("")
print("DONE.")

fout.close()
print("[=======================================]")
