#!/usr/bin/env python
import sys, os, subprocess
tm_support_path = os.environ['TM_SUPPORT_PATH'] + '/lib'
if tm_support_path not in sys.path:
    sys.path.insert(0, tm_support_path)
from tm_helpers import to_plist
import pysaurus

TM_DIALOG2 = os.environ['DIALOG']

def completion_popup(proposals, already_typed=None):
    command = TM_DIALOG2+" popup"
    options = [dict([['display',p.name], 
                    ['image', p.type if p.type else "None"]])
                    for p in proposals]
    call_dialog(command, {'suggestions' : options})
        
def call_dialog(command, options=None, shell=True):
    popen = subprocess.Popen(
                 command,
                 stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=shell)
    if options:
        out, _ = popen.communicate(to_plist(options))
    else:
        out, _ = popen.communicate()
    return out
    
def register_completion_images():
    icon_dir = os.environ['TM_BUNDLE_SUPPORT'] + '/icons'

    images = {
        "noun"   : icon_dir+"/Noun.png",
        "adjective" : icon_dir+"/Adjective.png",
        "adverb" : icon_dir+"/Adverb.png",
        "verb"   : icon_dir+"/Verb.png",
        "None"    : icon_dir+"/None.png",
    }
    call_dialog(TM_DIALOG2+" images", {'register' : images})

term = os.environ['TM_CURRENT_WORD']
if not term:
  sys.exit()

data = pysaurus.get_synonyms(term,24)
  
if hasattr(data, "__iter__"):
  index = reduce(lambda acc, item: item if item.name==term else None,
                  data, None)
  if index:
    data.pop(index)
  data.insert(0, pysaurus.Proposal(term,None))
  
  register_completion_images()
  completion_popup(data)
else:
  sys.stdout.write(term)