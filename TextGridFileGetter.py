__author__ = 'Mydy'

import os

def getTextGridFile(labelAndWavDir, P2FADir):
    textGridDir = os.path.join(labelAndWavDir, 'TextGrid')
    os.system("rm -r -f " + textGridDir)
    os.system("mkdir " + textGridDir)
    files = os.listdir(labelAndWavDir)
    for file in files:
        labelFileName = file.split('.')[0] + '.txt'
        textGridFileName = file.split('.')[0] + '.TextGrid'
        if file.endswith('.wav'):
            os.system("python " + os.path.join(P2FADir, 'align.py') + ' ' + \
                      os.path.join(labelAndWavDir, file) + ' ' + \
                      os.path.join(labelAndWavDir, labelFileName) + ' ' + \
                      os.path.join(textGridDir, textGridFileName))

if __name__ == '__main__':
    getTextGridFile(r'D:\DrZhang\ResearcholicZhang\Mine\PhDRelatedIdea\Branch\ArtiASR\USCTIMITRelated\tools\forcealignment\forcealignment\p2fa_ch\test', os.path.abspath(os.path.curdir))