import os
import sys 

main = 'splitter/models_sense2'
dirs = [d for d in os.listdir(main) if os.path.isdir(os.path.join(main, d))]
print(dirs)

for model in dirs:
    if not model == 'test':
        path = os.path.join(main,model)

        with open('splitter/det_runfile_example.sh','r') as example:
            filedata = example.read()
        
        filedata = filedata.replace('_model_',model)
        
        with open(os.path.join(path,'runfile.sh'),'w') as run:
            run.write(filedata)


