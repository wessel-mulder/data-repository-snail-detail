import os
main = 'splitter/HQ_cls'
dirs = os.listdir(main)

for dir in dirs:
    path = os.path.join(main,dir)
    with open('splitter/cls_runfile_example.sh','r') as example:
        filedata = example.read()
    
    filedata = filedata.replace('_model_',dir)
    
    with open(os.path.join(path,dir+'_runfile.sh'),'w') as run:
        run.write(filedata)


