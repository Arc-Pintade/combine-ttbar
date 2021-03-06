import os, sys
import argparse 

###################
## Initialisation
###################

parser = argparse.ArgumentParser()
parser.add_argument('observable', help='display your observable')
parser.add_argument('year', help='year of samples')
parser.add_argument('asimov',nargs='?', help='set if asimov test', default='')

args = parser.parse_args()
observable = args.observable
year = args.year
asimov = args.asimov

asi = ''
if asimov == 'asimov':
    print '################'
    print '# Asimov test : '
    print '################'    
    print ''
    asi = '--expectSignal 1 -t -1'

test = False

###################
## Core
###################

nbin = 24
for i in range(1):
    print '-----------------------------------------'
    print ' >>> combine on datacard '+str(i+1)+'/24 '
    print '-----------------------------------------'
    
    if test:
        cmd = 'text2workspace.py ./inputs/test_datacard.txt '
    else:
        cmd = 'text2workspace.py ./inputs/'+year+'/'+observable+'_'+str(nbin)+'_'+str(i)+'_datacard.txt '
    cmd += '-o '+observable+'_impacts'+str(i)+'.root'


    cmd1 = 'combineTool.py -M Impacts -d '+observable+'_impacts'+str(i)+'.root '+asi+' -m 125 '
    cmd2 = cmd1
    cmd3 = cmd1
    cmd1 += '--doInitialFit --robustFit 1'
    cmd2 += '--robustFit 1 --doFits'
    cmd3 += '-o '+observable+'_impacts'+str(i)+'.json '
    
    cmd4 = 'plotImpacts.py -i '+observable+'_impacts'+str(i)+'.json -o '+observable+'_impacts'+str(i)+''
        
    os.system(cmd)
    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)
    os.system(cmd4)

    if test:
        exit()
    else:
        if asimov == 'asimov':
            os.system('mv '+observable+'_impacts'+str(i)+'* impacts/'+year+'/'+str(i)+'/asimov/')
            os.system('mv *.png impacts/'+year+'/'+str(i)+'/asimov/')
            os.system('mv *.root impacts/'+year+'/'+str(i)+'/asimov/')
            os.system('mv *.out impacts/'+year+'/'+str(i)+'/asimov/')
        else:
            os.system('mv '+observable+'_impacts'+str(i)+'* impacts/'+year+'/'+str(i)+'/')
            os.system('mv *.png impacts/'+year+'/'+str(i)+'/')
            os.system('mv *.root impacts/'+year+'/'+str(i)+'/')
            os.system('mv *.out impacts/'+year+'/'+str(i)+'/')
