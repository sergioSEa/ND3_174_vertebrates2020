#!/bin/bash
#SBATCH --partition normal 
#SBATCH --mem-per-cpu 15G #memory per CPU
#SBATCH -c 6 #one core
#SBATCH -t 48:00:00

## Argument 1: Merged ND3, eg: ND3_merged.fa
#mafft $1 > Alignment/ND3_msa.fa
mafft --localpair --maxiterate 1000 --thread 6 tmp/Filtered_ND3_seqs.fa  > Alignment/ND3_msa2.fa
#java -jar scripts/macse_v2.03.jar -prog alignSequences -seq ND3_merged.fa -out_NT TEST/OUT_test.fa -gc_def 02
#java -jar -Xmx5000m scripts/macse_v2.03.jar -prog refineAlignment -align ND3_msa.fa -out_NT TEST/OUT_test.fa -gc_def 02 -optim 1

