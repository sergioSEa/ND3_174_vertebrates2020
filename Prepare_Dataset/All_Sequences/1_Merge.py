from Bio import SeqIO
from subprocess import call

#####Get the translation to latin name from B10K ID
translation = {}
with open("../../../../NAME-ID.txt") as File:
	for line in File:
		if "ID" in line: continue
		l = line.split(",")
		translation[l[0]] = l[1].rstrip().replace(" ","_")

####Save in a dic the B10K sequences. Latin_name : Sequence
Available = {}
Remove_b10K =  ["Nipponia_nippon","Pygoscelis_adeliae","Mohoua_ochrocephala", "Coturnix_japonica", "Zosterops_lateralis", "Meleagris_gallopavo","Falco_cherrug", "Gallus_gallus", "Taeniopygia_guttata","Pseudopodoces_humilis", "Serinus_canaria","Phalacrocorax_brasilianus", "Lonchura_striata", "Anas_platyrhynchos","Sylvia_atricapilla","Poecile_atricapillus","Chlorodrepanis_virens","Phasianus_colchicus", "Nannopterum_brasilianus", "Eurystomus_gularis"]
Species = ""
B10K_info = ""
with open("../../Aligned_ND3_seqs_B10K.fa") as B10K:
	S = SeqIO.parse(B10K, "fasta")
	for Species in S:
		N = Species.name.split("_")[0]
		if N == "NCBI-030": continue
		N = translation[N]
		if N in Remove_b10K: continue
		Available[N] = str(Species.seq).upper()
		
		B10K_info += ">"+N+"-B10K" + "\n" + str(Species.seq) + "\n"
with open("tmp/B10K_seqs.fa", "w") as F:
	F.write(B10K_info)

Command = "cat ../Fasta_generation/ND3_GenBank  ../Fasta_generation/ND3_RefSeq_genes.fa tmp/B10K_seqs.fa > Merged/All_seqs.fa"
call(Command, shell=True)

New = ""
with open("Merged/All_seqs.fa") as F:
	S = SeqIO.parse(F, "fasta")
	for Species in S:
		if len(set(str(Species.seq).upper())) > 5: continue
		New +=  ">"+Species.name + "\n" + str(Species.seq) + "\n"
with open("Merged/All_seqs.fa","w") as F:
	F.write(New)
