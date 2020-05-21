import os
import sys
import json
import uuid
from datetime import datetime

def read_in_uuids(fname, name_pos):
  the_dict = {}
  with open(fname, "r") as fpi:
    for l in fpi:
      line = l.strip()
      if len(line) > 0:
        items = line.split("\t")
        key = items[name_pos]
        uuid = items[-1]
        the_dict[key] = uuid
  return the_dict

def create_s_info(s, sid, sp, ep):
  return [{"sentence":s, "sentence_id":sid, "start":sp, "end":ep}]

def create_entry(c_name, sce, doi, cd, pm, annr, s_info, the_annot_props, r_id, r_type, r_props):
  entry = {}
  entry["corpus"] = c_name
  entry["source"] = sce # doi
  entry["doi"] = doi
  entry["date"] = cd
  entry["pmid"] = pm
  entry["annotation_id"] = str(uuid.uuid4()) 
  entry["annotator"] = annr # the id
  entry["sentences"] = s_info
  entry["annotation_properties"] = the_annot_props
  entry["relationship_id"] = r_id
  entry["relationship_type"] = r_type
  entry["relationship_properties"] = r_props
  return entry

def output_entry(the_entry):
  # This is done simply to make the output record sensible. 
  # json.dumps puts the fields in a random order.
  out_str = '{'
  out_str+=  '"corpus": "'+ the_entry["corpus"]+'", '
  out_str+=  '"source": "'+ the_entry["source"]+'", '
  out_str+=  '"doi": "'+ the_entry["doi"]+'", '
  out_str+=  '"date": "'  + the_entry["date"]  +'", '
  out_str+=  '"pmid": "'  + the_entry["pmid"]  +'", '
  out_str+= '"annotation_id": "'+the_entry["annotation_id"]+'", '
  out_str+= '"annotator": "'    +the_entry["annotator"]    +'", '
  out_str+= '"sentences": '            +json.dumps(the_entry["sentences"])+', '
  out_str+= '"annotation_properties": '+json.dumps(the_entry["annotation_properties"])+', '
  out_str+= '"relationship_id": "'   +the_entry["relationship_id"]+'", '
  out_str+= '"relationship_type": "' +the_entry["relationship_type"]+'", '
  out_str+= '"relationship_properties": ' + json.dumps(the_entry["relationship_properties"])
  out_str+= '}'
  return out_str
  
prep_fname = sys.argv[1]
obo_fname = sys.argv[2]
team_uuids_fname = sys.argv[3]
corpus_name = sys.argv[4]
source = sys.argv[5]
doi_info = sys.argv[6]
out_fname = sys.argv[7]

cdate = datetime.today().strftime('%Y-%m-%d')

rel_mapping = {"BioProc": "GO:0008150", "MolFn": "GO:0003674", "CellComp": "GO:0005575", "SeqFeat": "SO:0000110", "Phen": "OMP:0000000", "Tax":"Taxonomy/Phylogeny"}
team_uuids = read_in_uuids(team_uuids_fname, 0)

# Read in the prep'd corpus first
corpus = {}
ma_eid = "ECO:0000218" # Only had manual assertions
with open(prep_fname, "r") as fpi:
  for l in fpi:
    line = l.strip()
    items = line.split("\t")
    eid = items[0]
    pmid = items[1]
    annotator = team_uuids[items[6]] # a uuid per annotator
    sentence_id1 = items[2]
    sentence_id2 = items[4]
    annotated_text = items[13] # not needed because of start, end array. 
    #print annotated_text, sentence_id1, sentence_id2
    sentence1 = items[3] # generalize to array, just use S with the ECO. Make array of dictionaries: sentence_id, text, start, end
    sentence2 = items[5]
    start_pos = int(items[14]) # make array of start, end. Would need to have 1 pair for each S. We're only having 1 S now
    end_pos = int(items[15])
    if annotated_text=="sentence1":
      # Sentence info is an array of sentence attributes dictionary
      sentence_info = create_s_info(sentence1, sentence_id1, start_pos, end_pos)
      if len(sentence_id2) > 0:
        assertion_s_id = sentence_id2
        assertion_s = sentence2
      else:
        assertion_s_id = sentence_id1 # just use S with ECO term in it
        assertion_s = sentence1
      assertion_info = create_s_info(assertion_s, assertion_s_id, 0, len(assertion_s))
    else:
      sentence_info = create_s_info(sentence2, sentence_id2, start_pos, end_pos)
      # s id1 should be filled in, but just in case
      if len(sentence_id1) > 0:
        assertion_s_id = sentence_id1
        assertion_s = sentence1
      else:
        assertion_s_id = sentence_id2 # just use S with ECO term in it
        assertion_s = sentence2
      assertion_info = create_s_info(assertion_s, assertion_s_id, 0, len(assertion_s))  
    #print "Sentence_info:", sentence_info, "Assertion ", assertion_info
    
    our_conf = items[8]
    if len(our_conf) < 1:
      our_conf = "None"
    confidence = our_conf
    s_annot_props = {"Confidence":confidence}
    our_str = items[9]
    if len(our_str) < 1:
      our_str = "None"
    strength = our_str
    our_neg = items[11]
    if len(our_neg) < 1:
      our_neg = "None"
    negative = our_neg
    a_annot_props = {"Strength": strength, "Negative": negative}
    our_cat = items[10]
    if our_cat and (not our_cat=="None"):
      category = rel_mapping[items[10]] 
    else:
      category = "None"
    rel_id = str(uuid.uuid4())
    rel_type = "RO:0002559"
    rel_props = {"Category":category}
    
    entry = create_entry(corpus_name, source, doi_info, cdate, pmid, annotator, sentence_info, s_annot_props, rel_id, rel_type, rel_props)
    entry_ma = create_entry(corpus_name, source, doi_info, cdate, pmid, annotator, assertion_info, a_annot_props, rel_id, rel_type, rel_props)
    #if len(sentence_id1)>0 and len(sentence_id2) > 0:
      #print pmid, eid, sentence_id1, sentence_id2, entry["annotation_id"], entry['annotation_properties'], entry['sentences'], entry['relationship_properties']
      #print "   ", entry_ma["sentences"], "\n"    
    entry_str = output_entry(entry) #json.dumps(entry) # json makes the order wacky
    entry_ma_str = output_entry(entry_ma) #json.dumps(entry_ma)
    
    # check the manually built json is valid
    etemp = json.loads(entry_str)
    matemp = json.loads(entry_ma_str)
    
    #print "ENTRY:", entry
    if eid not in corpus:
      corpus[eid] = [entry_str]
    else:
      corpus[eid].append(entry_str)
    if ma_eid not in corpus:
      corpus[ma_eid] = [entry_ma_str]
    else:
      corpus[ma_eid].append(entry_ma_str)
      
num_annots_added = 0
fpo = open(out_fname, "w")
with open(obo_fname) as fpi:
  in_term = False
  cur_eid = ""
  for l in fpi:
    line = l.strip()
    if line.find("[Term]") > -1:
      #print "in term"
      in_term = True
    if in_term and len(line)==0:
      # Reached end of term, output any corpora
      if cur_eid in corpus:
        annots = corpus[cur_eid]
        for a in annots:
          out_str = "annotation: "+a
          fpo.write("%s\n" % out_str)
          num_annots_added += 1
      in_term = False
    if in_term and line[0:3]=="id:":
      cur_eid = line.split(" ")[1]
      if not cur_eid[0:4] == "ECO:":
        #print "not eco, so out term"
        in_term = False # don't care about non-ecos
    fpo.write("%s\n" % line)
    
fpo.close()
# If interested, these are entries that only had "ECO" with no ID
# Basically, errors on the part of the curators or items they thought might be annotated
# but couldn't find an ECO term for.
#if "ECO" in corpus:
#  not_done = corpus["ECO"]
#  for n in not_done:
#    print n
print "Num annotations added:", num_annots_added
