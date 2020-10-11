import os
import glob
import JackAnalyzer
out = os.walk("/cs/usr/arielleb/Nand2Tetris/ex10")
for root, dirs, files in out:
    for dir in dirs:
        files1 = glob.glob((dir + "/*.jack"))
        for file in files1:
            os.system("python3 JackAnalyzer.py "+file)
            name = file.rstrip("jack")
            print(name)
            os.system("TextComparer.sh "+name+"xml " + name +"xml.cmp" )
