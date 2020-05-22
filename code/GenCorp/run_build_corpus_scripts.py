# Use python 2.7
# Run the scripts to generate the IAA first. 
# These IAA scripts create intermediate files used to build the corpus-in-ontology format.
# 
# The current script is a convenience script to make building the ontology-corpus easier.
import os
import sys
import json

config_fname = sys.argv[1]
top_corpus_dir = sys.argv[2]
obo_file = sys.argv[3]
team_uuids_fname = sys.argv[4]
source = sys.argv[5]
corpus_output_fname = sys.argv[6]

with open(config_fname, 'r') as f:
  cdata = json.load(f)
  
corpus_name = cdata['corpus_name']
num_teams = cdata['num_teams']
corpora_dirs = cdata['corpora_dirs']
sub_dirs = cdata['sub_dirs']
num_annotators = cdata['num_annotators']
annot_teams = cdata['annotator_teams']

prep_fnames = []
# The preparation files
for i in range(num_teams): 
  corpus_path = os.path.join(top_corpus_dir, corpora_dirs[i])
  annots_str = " ".join(annot_teams[i])
  prep_fname = "onto_prep_"+corpora_dirs[i]+".txt"
  prep_fnames.append(prep_fname)
  sys_cmd = "python build_prep_corpus_for_ontology.py " + corpus_path+" "+sub_dirs[i]+" "+str(num_annotators[i])+" "+ prep_fname+" "+ annots_str+" > onto_prep_log_"+corpora_dirs[i]+".txt"
  print sys_cmd
  ret_val = os.system(sys_cmd)

# Concatenate into 1 prep file
concat_fname = "onto_prep_concatenated.txt"
with open(concat_fname, "w") as fpo:
  for fname in prep_fnames:
    with open(fname, "r") as fpi:
      fpo.write(fpi.read())
      
# And build the corpus-in-ontology OBO file
sys_cmd = "python build_corpus_in_ontology.py " + concat_fname +" "+obo_file+" "+team_uuids_fname+" "+corpus_name+" "+source+" "+corpus_output_fname 
print sys_cmd
ret_val = os.system(sys_cmd)
