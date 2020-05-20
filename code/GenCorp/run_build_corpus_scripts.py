# Use python 2.7
# Run the scripts to generate the IAA first. 
# These IAA scripts create intermediate files
# used to build the corpus-in-ontology format.
# This current script hard codes the calls needed to build first the "prep" file
# and then the final updated OBO file.
# It hard codes the paths to the corpus files and of the annotators.
# It is a convenience script to make building the ontology-corpus easier.
import os
import sys

top_corpus_dir = sys.argv[1]
eco_obo_file = sys.argv[2]
team_uuids_fname = sys.argv[3]
corpus_name = sys.argv[4]
source = sys.argv[5]
version_info = sys.argv[6]
out_fname = sys.argv[7] # the corpus-in-ontology OBO file to create

num_teams = 3 # 3 separate teams
corpora_dirs = ["ECO_1_2", "ECO_3", "ECO_4_5"]
sub_dirs = ["ECO_annotation_1_2", "ECO_annotation3", "ECO_annotation_4_5"]
num_annotators = [3, 3, 4]
annot_teams = [["T1", "S1", "A1", "M1"], ["T1", "A2", "D1"], ["A1", "A2", "D1", "M2"]]
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
sys_cmd = "python build_corpus_in_ontology.py " + concat_fname +" "+eco_obo_file+" "+team_uuids_fname+" "+corpus_name+" "+source+" "+version_info+" "+out_fname 
print sys_cmd
ret_val = os.system(sys_cmd)
