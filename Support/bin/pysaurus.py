import subprocess, os, sys

class Proposal(object):
  def __init__(self, name="", _type=None):
    super(Proposal, self).__init__()
    self.name = name
    self.type = _type
  
  def __repr__(self):
    t_string = self.type if self.type else "NoType"
    return t_string+": "+self.name

def _filter_and_to_dict(out_lines):
  ''' dirty code written in 10 minutes to "parse" the dictionary.app's output '''
  if not out_lines:
    return {}
  limits = []
  for i, l in enumerate(out_lines):
    if l.strip() in ["noun","verb","adjective"]:
      limits.append(i)
  parts = []
  if len(limits) == 1:
    parts = [(out_lines[0],out_lines[1:])]
  else:
    for x in range(len(limits)-1):
      parts.append(
        (out_lines[limits[x]], out_lines[limits[x]+1:limits[x+1]])
      )
    parts.append(
      (out_lines[limits[x+1]], out_lines[limits[x+1]+1:])
    )
      
  results = [] 
  for t, p in parts:
    p = "".join(p)
    for digit in ["1","2","3","4","5","6","7","8","9","0"]:
      p = p.replace(digit,"")
    p = p.replace(".",",").replace(";",",").strip()[:-1]
    antonyms_idx = p.find("ANTONYMS")
    if antonyms_idx != -1:
      p = p[:antonyms_idx]
    words = [w.strip() for w in p.split(",")]
    words = filter(lambda x: x!="",words)
    results.append((t.strip(),words))
    
  results = dict(results)
  return results

def _call_thesaurus(term):
  path = os.path.dirname(sys.argv[0])
  if path:
    os.chdir(path)
  popen = subprocess.Popen(
               "./thesaurus "+term,
               stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
  out, _ = popen.communicate()
  out_lines = filter(lambda x: x!="", out.split("\n"))
  if len(out_lines) == 1 and out_lines[0] == '(null)':
    return None
  return out_lines


def get_synonyms(term, limit=None):  
  out_lines = _call_thesaurus(term)
  synonyms = _filter_and_to_dict(out_lines)
  result = [] 
  if limit:
    x = len(synonyms.keys())
    if x==0:
      return []
      
    y = limit/x
    for key in synonyms.keys():
      words = synonyms[key]
      num_words = min(len(words), y)
      for w in words[:num_words]:
        result.append(Proposal(w, key))
  else:
    for key in synonyms.keys():
      for w in synonyms[key]:
        result.append(Proposal(w, key))

  return result
    
if __name__ == '__main__':
  print get_synonyms("object")