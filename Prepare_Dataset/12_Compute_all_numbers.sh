echo "Total number of sequences from which I pulled ND3 records:"
echo "GenBank: " ; grep ">" Fasta_generation/ND3_GenBank | wc -l  
echo "RefSeq: " ; grep ">" Fasta_generation/ND3_RefSeq_genes.fa | wc -l
echo "After filters: " ; wc -l "Whole_Sample/Supplemenetary_Table_1.tsv"
echo "B10K" ; grep "B10K" "Whole_Sample/Supplemenetary_Table_1.tsv" | wc -l
echo "Unique species: " ;  grep ">" Merging/ND3_merged.fa | wc -l
echo "After filters: " ; wc -l  Summary_Table.tsv
echo "Filtering after alignments :" ; cut -f 2 Others/Seqs_filterd.txt | sort | uniq -c
echo "Taxonomy of final table: " ; cut -f 3 Summary_Table.tsv  | sort | uniq -c
echo "Number of insertions: " ; awk '$2 != "-" {print $0}' Summary_Table.tsv | cut -f 3 | sort | uniq -c
echo "Diapsida: " ; wc -l Diapsida/Diapsida_table.tsv
echo "In tree: " ;  wc -l Diapsida/Table_in_tree.tsv
