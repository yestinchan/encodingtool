# -*- coding : utf-8 -*-

import chardet,os,re,shutil,getopt,sys,codecs

def query_encoding(filename):
    content = codecs.open(filename,'r').read()
    encoding = chardet.detect(content)['encoding']
    return encoding

def convert_file(filename,to_encoding,is_single = True):
    if is_single:
        backup_file(filename)
    content = codecs.open(filename,'r').read()
    encoding = chardet.detect(content)['encoding']
    if encoding :
        content = content.decode(encoding)
        codecs.open(filename,'w',encoding=to_encoding).write(unicode(content))
    else:
        print("Sorry,Couldnot guess the file encoding.Please handle it manually.\
            \nFile: [{}]".format(filename))

def convert_dir(path,to_encoding):
    backup_dir(path)
    for root,dirs,files in os.walk(path):
        for file in files:
            try:
                convert_file(os.path.join(root,file),to_encoding,False)
            except TypeError ,err:
                print err
                print "{0}/{1}".format(root,file)

def backup_file(filename):
    '''
    Back up file
    '''
    shutil.copyfile(filename,filename+".bk")

def backup_dir(path):
    '''
    Backup dir
    '''
    path = os.path.normcase(path)
    newPath = os.path.normcase(os.path.dirname(path)+"-bk/")

    print("back up files... to {0}".format(newPath))

    if not os.path.isdir(newPath):
        os.makedirs(newPath)
    for root , dirs , files in os.walk(path):
        for dir in dirs:
            #create dir if not exists.
            if not os.path.isdir(os.path.join(root.replace(path,newPath),dir)):
                os.makedirs(os.path.join(root.replace(path,newPath),dir))
        for file in files:
            filename = os.path.join(root,file)
            shutil.copyfile(filename,filename.replace(path,newPath))

def main(argv):
    reload(sys)
    sys.setdefaultencoding('utf8')
    try:
        opts, args = getopt.getopt(argv[1:],'hf:d:q:',["help","file=","dir=","query="])
    except getopt.GetoptError, err:
        print (str(err))
        sys.exit(2)
    for k,v in opts:
        if k in ('-h','--help'):
            usage = '''==========encoding tool @Yestin=========
usage:
    -f [fileName] change the file to utf-8 encoding.
    -p [dir] change the whole files in the dir including sub dir to utf-8 encoding.
    -q [fileName] query the encoding of the file.
    -h help
            '''
            print(usage)
        elif k in ('-f','--file'):
            #check file.
            if os.path.isfile(v):
                convert_file(v,'utf-8')
                print("Done!")
            else:
                print("Please input a file name.")
        elif k in ('-d','--dir'):
            if os.path.isdir(v):
                if not v.endswith('/'):
                    v = v + '/'
                convert_dir(v,'utf-8')
                print("Done!")
            else:
                print("Please input a dir path.")
        elif k in ('-q','--query'):
            print("The encoding of the file {0} is {1}".format(v,query_encoding(v)))
        else:
            print("what?")
            sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)