import os
import sys
import time

if(len(sys.argv)<2):
    print 'the target path is required'
    sys.exit(0)

path = sys.argv[1]
new_name_file = 'vins.txt'
log_name = 'rename_' + time.strftime('%Y%m%d',time.localtime(time.time())) + '.log'

# parse args
has_f = False
for arg in sys.argv[2:]:
    if(has_f):
        new_name_file = arg
        has_f = False
        continue
    if(arg=='-f'):
        has_f = True

new_names = open(new_name_file).readlines()
finished_names = []
log = open(log_name,'a')
for root, dirs, files in os.walk(path):
    for index, name in enumerate(files):
        if(index>=len(new_names)):
            break
        suffix = name[name.index('.'):len(name)]
        old_name = root+"/"+name
        new_name = new_names[index].strip('\n')+suffix
        if(finished_names.count(new_name)):
            log.write('error: repetitive file ' + new_name + '\n')
            continue
        os.rename(old_name, root+'/'+new_name)
        log.write('success:' + name+' rename to ' + new_name + '\n')
        finished_names += new_name
log.close()

