import os
import sys
import glob
import string

def get_id(text):
  id_str = "id=\""
  id_str_len = len(id_str)
  ibpos = text.find(id_str)
  iepos = text.find('"', ibpos+id_str_len+1)
  id_val = text[ibpos:iepos+1]
  return id_val
  
def process_tag_text(text):
  print "process tag text:", text
  eco_id_len = 11
  eco_conf_str = "ECOConfidence=\""
  eco_conf_len = len(eco_conf_str)
  assertion_str = "AssertionStrength=\""
  assertion_str_len = len(assertion_str)
  category_str = "Category=\""
  category_str_len = len(category_str)
  next_s_str = "NextSentence=\""
  next_s_str_len = len(next_s_str)
  neg_s_str = "NegativeStatement=\""
  neg_s_str_len = len(neg_s_str)
  
  # Check if not normalized
  bpos = text.find('normalized="False"')
  if bpos > -1:
    return {"skip_eco":True}
    
  # Get ECO id
  bpos = text.find("ECO:")
  epos = bpos+eco_id_len
  eco_id = text[bpos:epos]
  # Get ECO Confidences
  bpos = text.find(eco_conf_str)
  epos = text.find('"', bpos+eco_conf_len+1)
  eco_conf_val = text[bpos+eco_conf_len:epos]
  # Get Assertion strength         
  bpos = text.find(assertion_str)
  epos = text.find('"', bpos+assertion_str_len+1)
  assertion_val = text[bpos+assertion_str_len:epos]
  # Get category
  bpos = text.find(category_str)
  epos = text.find('"', bpos+category_str_len+1)
  category_val = text[bpos+category_str_len:epos]
  # Get if sentence pair
  bpos = text.find(next_s_str)
  epos = text.find('"', bpos+next_s_str_len)
  next_s_val = text[bpos+next_s_str_len:epos]
  # Get if Negative
  bpos = text.find(neg_s_str)
  epos = text.find('"', bpos+neg_s_str_len)
  neg_s_val = text[bpos+neg_s_str_len:epos]
  
  #print text
  print "RECOVERED tag:"
  print "ECO:", eco_id+".", eco_conf_val+"."
  print "  Category:", category_val+".", "AS:", assertion_val+"."
  print "  Next?", next_s_val+".", "Neg?", neg_s_val+"."
  return {"skip_eco":False, "eco":eco_id, "econf":eco_conf_val, "astr":assertion_val, "cat":category_val, "next":next_s_val, "neg":neg_s_val}
  
   
def process_tags(tag_list, tagged_text):
  # Need to remove the </term stuff
  # Could be a problem if not nested
  # tags need to be popped
  eco_info = {}
  num_tags_in_s = len(tag_list)
  for i in range(num_tags_in_s-1, -1, -1):
    tag_text = tag_list[i]
    id_str = get_id(tag_text)
    print "Tag:", i, tag_text, id_str
    eco_data = process_tag_text(tag_text)
    eco_data["tagged"] = "SKIPPED"
    eco_info[id_str] = eco_data
  return eco_info
  
def format_tag(tag_map):
  sep = ";:;"
  str = tag_map["eco"]+sep+tag_map["econf"]+sep+tag_map["cat"]+sep+tag_map["astr"]+sep+tag_map["tagged"]+sep+tag_map["next"]+sep+tag_map["neg"]
  return str

  
def get_plain_fname(fname):
  plain_fname = fname.replace("data_as_tags", "data")
  plain_fname = plain_fname.replace("_ef", "")
  return plain_fname
  
#def count_annots(l1, l2, l3):
#  num_a_tags = l1.count("<term")
#  num_b_tags = l2.count("<term")
#  num_c_tags = l3.count("<term")
#  return (num_a_tags, num_b_tags, num_c_tags)
  
def get_annotations(num_term_tags, sent_str):
  s_tags = []
  print "Incoming:", sent_str

  # Gather info 
  etpos = 0
  spos = 0
  for i in range(num_term_tags):
    bpos = sent_str.find("<term", spos)
    nspos = sent_str.find("NextSentence", bpos+10)
    epos = sent_str.find(">", nspos)
    tag_text = sent_str[bpos:epos]
    id_str = get_id(tag_text)
    print "TAG:", tag_text
    print "ID STR:", id_str
    s_tags.append(tag_text)
    etpos = epos
    spos = epos
  print "last pos:", etpos
  print s_tags
  print "REST:", sent_str[etpos+1:]
        
  if len(s_tags) > 0:
    tag_data = process_tags(s_tags, sent_str[etpos+1:])
    for t in tag_data:
      tdata = tag_data[t]
      print "TDATA:", tdata
      if tdata["skip_eco"]:
        print "Skipping", tdata
        continue
###########################################################
def get_next_sentence(spos, slines):
  plain_ns = ""
  if i < len(slines)-1: 
    plain_ns = slines[i+1].strip()
    if len(plain_ns) < 1:
      j=i+2
      while j < len(slines):
        plain_ns = slines[j].strip()
        j += 1
        if len(plain_ns) > 1:
          break
  return plain_ns
  
def grab_term_tag(pos, sstr):
  #print "grab term:", pos, len(sstr), sstr
  ret_pos = len(sstr)
  chars = ""
  for i in range(pos, len(sstr)):
    chars += sstr[i]
    #print i, sstr[i]
    if sstr[i] == '>':
      ret_pos = i
      break
  if ret_pos == len(sstr):
    print "Error -- no end of term tag", len(sstr)
    print sstr
    sys.exit(0)
  items = chars.split()
  #print "ITEMS:", items
  data = {}
  for item in items:
    #print "item:", item
    if not item.find("=")>-1:
      continue
    item = item.replace("\"", "")
    item = item.replace(">", "")
    parts = item.split("=")
    #print parts
    data[parts[0]] = parts[1]
  #print "Data to return:", data
  return (ret_pos, data)
      
def grab_attrib(sstr):
  items = sstr.split("=")
  return items[1][1:-1]
  
def handle_sentence(s):
  i=0
  ni=0
  run_ni = 0
  new_line = ""
  tags = {}
  slen = len(s)
  annots = {}
  #print "INCOMING:", s
  while i < slen:
    #print "i:", i, "char:", s[i]
    if i+5<slen and s[i:i+5]=="<term":
      beg_pos = run_ni
      (i, info) = grab_term_tag(i,s)
      sstr = info["sem"]
      idstr = info["id"]
      i+= 1
      if idstr in tags:
        print "Error: repeated id in tag", idstr
        sys.exit(0)
      tags[idstr] = {"start":beg_pos, "sem":sstr}
      tags[idstr]["text_ni"] = ni
      #print "BEGIN:", tags[idstr]
      annots[idstr] = info
      annots[idstr]["start"] = beg_pos
      #print "      ", annots[idstr]
    elif i+6<slen and s[i:i+6]=="</term":
      end_pos = run_ni
      (i, info) = grab_term_tag(i, s)
      idstr = info["id"]
      i+= 1
      if idstr not in tags:
        print "Error: missing beginning id tag", idstr
        sys.exit(0)
      tags[idstr]["end"] = end_pos
      tags[idstr]["text"] = new_line[tags[idstr]["text_ni"]:ni]
      #print "END:", tags[idstr]
      annots[idstr]["end"] = end_pos
      annots[idstr]["text"] = tags[idstr]["text"]
      #print "    ", annots[idstr]
    else:
      new_line += s[i]
      i+=1
      ni+=1
      run_ni+=1
  #if len(tags):
  #  for tag in tags:
  #    item = tags[tag]
  #    print "tags found:",tag, item, new_line[item["start"]:item["end"]]+"."
        
  return annots
  

def gather_annots(count, s):
  annots = []
  if count > 0:
    s_annots = handle_sentence(s)
    #print "s_annots:", s_annots
    for s_a in s_annots:
      a = s_annots[s_a] # remove the brat tag id's
      # check for complete ECO id
      ecoid = a["sem"]
      #if len(ecoid) >= 11:
      annots.append(a)
  return annots
  
###########################################################
  
root_dir = sys.argv[1] 
sub_dir = sys.argv[2]
num_annotators = int(sys.argv[3]) # # annotators per doc
out_fname = sys.argv[4]
annotator_arr = sys.argv[5:]  # All annotators, Leader first

tags_dir = os.path.join(root_dir, "data_as_tags")
tags_dir = os.path.join(tags_dir, sub_dir)

data_dir = os.path.join(root_dir, "data")
data_dir = os.path.join(data_dir, sub_dir)

fpo = open(out_fname, "w")
for annr in annotator_arr:
  annotator_id = annr
  print "Annotator:", annr, annotator_id

  annr_dir = os.path.join(tags_dir, annr)
  file_to_glob = os.path.join(annr_dir, "r*.txt")
  annr_array = glob.glob(file_to_glob)
  plain_dir = os.path.join(data_dir, annr)
  for ar_tags_fname in annr_array:
    base_name = os.path.basename(ar_tags_fname)
    doc = os.path.splitext(base_name)[0]
    pmid = doc.split("_")[1]
    
    scnt = 0
    fpa = open(ar_tags_fname,"r")
    tlinesa = fpa.readlines()
    fpa.close()

    plain_fnamea = get_plain_fname(ar_tags_fname)
    fpa = open(plain_fnamea, "r")
    plinesa = fpa.readlines()
    fpa.close()
    
    for i in range(len(tlinesa)):
      if i==0:
        continue
      
      # Count the annotations NOT split, just if they are there are not
      linea = tlinesa[i].strip()
      if len(linea) < 1:
        continue
      plaina = plinesa[i].strip()
      plain_ns = get_next_sentence(i, plinesa)
  
      scnt += 1
      print "\n"

      counta = linea.count("<term")
      print annr, pmid, "S regular:", scnt, "count:", counta
      print linea
      a_annots = gather_annots(counta, linea)
      for the_annot in a_annots:
        the_annot["sentence1"] = plaina
        the_annot["sid1"] = scnt
        if the_annot["NextSentence"]=="Yes":
          the_annot["sentence2"] = plain_ns
          the_annot["sid2"] = scnt+1
        else:
          the_annot["sentence2"]=""
          the_annot["sid2"]=""
        annot_text = the_annot["text"]
        spos = the_annot["start"]
        epos = the_annot["end"]
        which_s = "sentence1"
        s_text = the_annot[which_s][spos:epos]
        if not annot_text==s_text:
          print "Differ:", pmid, scnt, annot_text, s_text, plain_fnamea
          sys.exit(0)
        next_s = the_annot["NextSentence"]
        if next_s == "Yes":
          next_s_text = the_annot["sentence2"]
          if len(next_s_text) < 1:
            print "ERROR: no 2nd s", pmid, scnt, which_s, plain_fnamea
            sys.exit(0)
        print the_annot
        out_str = the_annot["sem"]+"\t"+pmid+"\t"+str(the_annot["sid1"])+"\t"+the_annot["sentence1"]+"\t"
        out_str += str(the_annot["sid2"])+"\t"+the_annot["sentence2"]+"\t"+annotator_id+"\t"+str(num_annotators)+"\t"
        out_str += the_annot["ECOConfidence"]+"\t"+the_annot["AssertionStrength"]+"\t"+the_annot["Category"]+"\t"+the_annot["NegativeStatement"]+"\t"
        out_str += the_annot["NextSentence"]+"\tsentence1\t"+str(the_annot["start"])+"\t"+str(the_annot["end"])
        out_str += "\t"+s_text+"\t"+the_annot["id"]
        fpo.write("%s\n" % out_str)
fpo.close() 