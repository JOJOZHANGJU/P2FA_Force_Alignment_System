#!/usr/bin/env python

""" Usage:
      align.py wavfile trsfile output_file
"""

import os
import sys
import wave

def prep_wav(orig_wav, out_wav):
    f = wave.open(orig_wav, 'r')
    SR = f.getframerate()
    f.close()
    if (SR not in [8000, 11025, 16000]):
        SR = 16000
        os.system("sox " + orig_wav + " -c 1" + " -r 16000 " + out_wav + " rate")
    else:
        os.system("cp -f " + orig_wav + " " + out_wav)

    return SR


def prep_mlf(trsfile, mlffile, reffile):

    f = open('./model/dict', 'r')
    lines = f.readlines()
    f.close()
    dict = []
    for line in lines:
        dict.append(line.split()[0])

    f = open(trsfile, 'r')
    lines = f.readlines()
    f.close()

    fw = open(mlffile, 'w')
    fw2 = open(reffile, 'w')
    fw.write('#!MLF!#\n')
    fw.write('"*/tmp.lab"\n')
    fw.write('sp\n')
    i = 0
    while (i < len(lines)):
        txt = lines[i].replace('\n', '')
        txt = txt.replace('{breath}', '{BR}').replace('&lt;noise&gt;', '{NS}')
        txt = txt.replace('{laugh}', '{LG}').replace('{laughter}', '{LG}')
        txt = txt.replace('{cough}', '{CG}').replace('{lipsmack}', '{LS}')

        for pun in [',', '.', ':', ';', '!', '?', '"', '%']:
            txt = txt.replace(pun,  '')
            
        #txt = txt.upper()

        if ('- ' in txt): #incomplete words
            txt = txt.split()
        else:
            txt = txt.replace('-', ' ').split() #words like twenty-two

        for wrd in txt:
            if ((wrd <> 'sp') and (wrd.upper() in dict)): #sp is reserved for not messing up refs.pop when generating textgrids.
                fw.write(wrd.upper() + '\n')
                fw.write('sp\n')
                fw2.write(wrd + '\n')
        i += 1
    fw.write('.\n')
    fw.close()
    fw2.close()

def TextGrid(infile, reffile, outfile, SR):
    
    f = open(infile, 'r')
    lines = f.readlines()
    f.close()
    f = open(reffile, 'r')
    refs = f.readlines()
    f.close()
    refs.reverse()

    fw = open(outfile, 'w')

    j = 2

    phons = []
    wrds = []
    while (lines[j] <> '.\n'):
        #print lines[j]
        ph = lines[j].split()[2]
        if (SR == 11025):
            st = (float(lines[j].split()[0])/10000000.0+0.0125)*(11000.0/11025.0)
            en = (float(lines[j].split()[1])/10000000.0+0.0125)*(11000.0/11025.0)
        else:
            st = float(lines[j].split()[0])/10000000.0 + 0.0125
            en = float(lines[j].split()[1])/10000000.0 + 0.0125   
        if (st <> en):
            phons.append([ph, st, en])

        if (len(lines[j].split()) == 5):
            wrd = lines[j].split()[4].replace('\n', '')
            if (SR == 11025):
                st = (float(lines[j].split()[0])/10000000.0+0.0125)*(11000.0/11025.0)
                en = (float(lines[j].split()[1])/10000000.0+0.0125)*(11000.0/11025.0)
            else:
                st = float(lines[j].split()[0])/10000000.0 + 0.0125
                en = float(lines[j].split()[1])/10000000.0 + 0.0125
            if (st <> en):
                if (wrd == 'sp'):
                    wrds.append([wrd, st, en])
                else:
                    wrds.append([refs.pop().strip(), st, en])
            else:
                1 == 1
                #for other samplein rate

        j += 1

    #write the phone interval tier
    fw.write('File type = "ooTextFile short"\n')
    fw.write('"TextGrid"\n')
    fw.write('\n')
    fw.write(str(phons[0][1]) + '\n')
    fw.write(str(phons[-1][2]) + '\n')
    fw.write('<exists>\n')
    fw.write('2\n')
    fw.write('"IntervalTier"\n')
    fw.write('"phone"\n')
    fw.write(str(phons[0][1]) + '\n')
    fw.write(str(phons[-1][-1]) + '\n')
    fw.write(str(len(phons)) + '\n')
    for k in range(len(phons)):
        fw.write(str(phons[k][1]) + '\n')
        fw.write(str(phons[k][2]) + '\n')
        fw.write('"' + phons[k][0] + '"' + '\n')


    #write the word interval tier
    fw.write('"IntervalTier"\n')
    fw.write('"word"\n')
    fw.write(str(phons[0][1]) + '\n')
    fw.write(str(phons[-1][-1]) + '\n')
    fw.write(str(len(wrds)) + '\n')
    for k in range(len(wrds) - 1):
        fw.write(str(wrds[k][1]) + '\n')
        fw.write(str(wrds[k+1][1]) + '\n')
        fw.write('"' + wrds[k][0] + '"' + '\n')

    fw.write(str(wrds[-1][1]) + '\n')
    fw.write(str(phons[-1][2]) + '\n')
    fw.write('"' + wrds[-1][0] + '"' + '\n')               

    fw.close()


if __name__ == '__main__':

    try:
        wavfile = sys.argv[1]
        trsfile = sys.argv[2]
        outfile = sys.argv[3]
    except IndexError:
        print __doc__


    # create working directory
    os.system("rm -r -f ./tmp")
    os.system("mkdir tmp")

    
    #prepare wavefile
    SR = prep_wav(wavfile, './tmp/tmp.wav')


    #prepare mlfile
    prep_mlf(trsfile, './tmp/tmp.mlf', './tmp/ref.mlf')



    #prepare scp files
    fw = open('./tmp/codetr.scp', 'w')
    fw.write('./tmp/tmp.wav ./tmp/tmp.plp\n')
    fw.close()
    fw = open('./tmp/test.scp', 'w')
    fw.write('./tmp/tmp.plp\n')
    fw.close()

    #call plp.sh and align.sh
    os.system('HCopy -T 1 -C .//model/' + str(SR) + '/config -S ./tmp/codetr.scp')

    os.system('HVite -T 1 -a -m -I ./tmp/tmp.mlf -H ./model/' + str(SR) + '/macros -H ./model/' + str(SR) + '/hmmdefs  -S ./tmp/test.scp -i ./tmp/aligned.mlf -p 0.0 -s 5.0 ./model/dict ./model/monophones > ./tmp/aligned.results')
    os.path.split(trsfile)[1].split('.')[0] + '.TextGrid'

    TextGrid('./tmp/aligned.mlf', './tmp/ref.mlf', outfile, SR)   
