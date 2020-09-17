# First argument is the aligned sequence


Input=$1
Output=$2

/faststorage/home/sersan/Coevolution/Genomic_aln/phyx/src/pxclsq -s $Input -p 0.05 > $Output
