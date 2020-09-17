#!/bin/bash
#SBATCH --partition normal
#SBATCH --mem-per-cpu 15G #memory per CPU
#SBATCH -c 6 #one core
#SBATCH -t 48:00:00

mafft --add Merged/All_seqs.fa --reorder ../Clean_alignment/ND3_final.fa > output_aligned


#https://mafft.cbrc.jp/alignment/software/addsequences.html
