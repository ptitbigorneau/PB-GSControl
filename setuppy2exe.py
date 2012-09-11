import sys
import os
import glob
import re
from distutils.core import setup 
import py2exe

if len(sys.argv)==1:
    sys.argv.append('py2exe')

def listdirectory(path):
    def istocopy(path):
        return (
                os.path.isfile(path)
                and not path.endswith('.pyc') 
                and not path.endswith('.pyo') 
                )
    return map(os.path.normpath, filter(istocopy, glob.glob(path + os.sep + '*')))

myDataFiles = [
        ('', ['License.txt']),
        ('', ['icone.ico']),
        ('', ['conf.bmp']),
        ('', ['new.bmp']),
        ('', ['effa.bmp']),
        ('', ['modif.bmp']),
        ('', ['exit.bmp']),
        ('', ['enr.bmp']),
        ('', ['up.jpg']),
        ('', ['down.jpg']),
        ('', ['confpb-gscontrol.gif']),
        ('', ['pb-gscontrol.gif']),
    ]
    
options = {'py2exe':{'optimize': 1, 'dll_excludes': ['MSVCP90.dll'],"includes": ["pyquake3","dbhash",],}}

setup(name="PB-GSControl", version="1b", author="PtitBigorneau", url="http://ptitbigorneau.fr",zipfile = "pb-gscontrol.lib",windows=[{"script":"pb-gscontrol.py","icon_resources":[(1,"icone.ico")]}], data_files = myDataFiles, options=options)    
