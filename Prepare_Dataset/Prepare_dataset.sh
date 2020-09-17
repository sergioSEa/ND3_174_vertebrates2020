#Pipeline script for ND3-174 identification from GenBank records
#Multiple origins of a frameshift insertion in a mitochondrial gene in birds and turtles ; Author: S. Andreu-Sanchez
#Steps: 1. Get Fastas from GenBank 2. Select and Merge fasta records 3. Make MSA  4. Remove alignment positions not seen in 95% of sequences 5. Change gaps in position 175 to position 174 6. Assess the nucleotide found at position 174

mkdir Alignment
mkdir Clean_alignment
mkdir Diapsida
mkdir Fasta_generation
mkdir Merging
mkdir Taxonomy
mkdir tmp

####Prepare NCBI sequences#
echo 'ND3 extraction from genebank'
python  0_Prepare_fasta.py
python  0_Prepare_taxonomy.py
####First merge
echo 'Merging refseq complete mitochondria and Genebank records'
python 1_*


####Merging
echo 'Merging with B10K data'
python 2_*



###Align
echo 'Alinmgnet 1 (fast)'
bash  3_MSA.sh Merging/ND3_merged.fa

echo 'Filter 1'
python 4_Filter_sequences.py

echo 'Alignment 2 (slow)'
bash 5_MSA2.sh

echo 'Cleaning alignment 2'
python 6_Clean_and_adjustment.py

echo 'Generation of table with ND3-174 info'
python 7_Make_table.py

echo 'Generate Diapsida table'
python 8_Prepare_diapsida.py

echo 'Make Otol tree of diapsida'
Rscript 9_Make_otol_tree.R

echo 'Fix taxonomy issues in table'
python 11_Fix_taxonomy.py

echo 'Get numbers'
bash 12_Compute_all_numbers.sh


