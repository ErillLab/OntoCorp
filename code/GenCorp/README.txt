1. Preliminary:
a. Run ECO-CollecTF_run_iaa_scripts.py in the IAA subdirectory of code.
b. Follow the instructions there for each of the corpus sections for the 3 teams.
(ECO_1_2, ECO_3, ECO_4_5).


2. Run the run_build_corpus_scripts.py
This script is a convenience script to rebuild the ECO-CollecTF Ontology-Corpus.

If you wish to build your own corpus or you have added new brat folders to the corpus, modify the run_build_corpus_scripts.py file to point to the various paths for the different subfolders and for the different annotators. 


python run_build_corpus_scripts.py \path\to\corpus \path\to\eco.obo \path\to\team_uuids.txt corpus-name corpus-source corpus-version output-OBO.obo

The output-OBO.obo file contains the ontology with corpus.

How to generate the ECO-CollecTF ontology-corpus:
python run_build_corpus_scripts.py \your\path\to\OntoCorp\corpus \your\path\to\OntoCorp\corpus\eco_v2018-09-14.obo team_uuids.txt ECO-CollecTF erilllab.umbc.edu VERSION1 ECO-CollecTF_eco_v2018-09-14.obo

team_uuids.txt is a tab delimited file that maps the brat annotator directory name to the annotator's uuid.
