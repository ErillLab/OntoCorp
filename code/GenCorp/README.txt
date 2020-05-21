1. Preliminary:
a. Run ECO-CollecTF_run_iaa_scripts.py in the IAA subdirectory of code.
b. Follow the instructions there for each of the corpus sections for the 3 teams.
(ECO_1_2, ECO_3, ECO_4_5).


2. Run the run_build_corpus_scripts.py
This script is a convenience script to rebuild the ECO-CollecTF Ontology-Corpus.

If you wish to build your own corpus or you have added new brat folders to the corpus, modify the run_build_corpus_scripts.py file to point to the various paths for the different subfolders and for the different annotators. 


python run_build_corpus_scripts.py \path\to\config-file \path\to\corpus \path\to\eco.obo \path\to\team_uuids.txt corpus-DOI output-OBO.obo

The output-OBO.obo file contains the ontology with corpus.

How to generate the ECO-CollecTF ontology-corpus:
python run_build_corpus_scripts.py eco_collectf_config.txt \your\path\to\OntoCorp\corpus \your\path\to\OntoCorp\corpus\eco_v2018-09-14.obo team_uuids.txt ECO-CollecTF_eco_v2018-09-14.obo

team_uuids.txt is a tab delimited file that maps the brat annotator directory name to the annotator's uuid.

For the corpus-DOI, do NOT include the DOI: in the value.

The eco_collectf_config.txt file is a JSON-formatted file that contains the following keys:
*corpus_name: a string containing the corpus name. Here, ECO-CollecTF
*source: a string the source of the corpus. Here, erilllab.umbc.edu
*num_teams: an integer with the number of teams who worked on the corpus. Here, 3
*num_annotators: a list of length num_teams containing integers for how many curators were on each team. Here, [3, 3, 4]
*annotator_teams: a list of length num_teams, each element is a list of strings. The strings are the brat folder names for the curators. Here, [["T1", "S1", "A1", "M1"], ["T1", "A2", "D1"], ["A1", "A2", "D1", "M2"]]
*sub_dirs: a list of length num_teams, each element is a string. The strings are the folder names in the brat subdirectory under the data directory. Here, ["ECO_annotation_1_2", "ECO_annotation3", "ECO_annotation_4_5"], 
*corpora_dirs: a list of length num teams, each element is a string of the folder name of the corpus root. Here, "ECO_1_2", "ECO_3", "ECO_4_5"]

