import sys
import subprocess
from Bio import SeqIO

FILE = "Alignment/ND3_msa2.fa" #sys.argv[1]
Alignment_Clean = "tmp/ND3_clean2.fa"
subprocess.call(["bash", "Others/Clean_alignment.sh", FILE, Alignment_Clean])

Final = ""
#Remove ambiguous alignments
with open(Alignment_Clean) as MSA:
	Info = SeqIO.parse(MSA, "fasta")
	for Item in Info:
		if Item.id in ["Bubo_virginianus", "Gallicrex_cinerea", "Peltocephalus_dumerilianus"]: continue
		area_interest = str(Item.seq[170:178])
		if area_interest.count("n") > 0 or area_interest.count("-") > 1:
			print(Item.id)
			with open("Others/Seqs_filterd.txt", "a") as F:
				F.write(Item.id+"\t"+"Gaps_Ns_around_174"+"\n")
				continue
		Final += ">{N}\n{S}\n".format(N=Item.id, S=str(Item.seq))
with  open(Alignment_Clean,"w") as MSA:
	MSA.write(Final)


save = []
with open(Alignment_Clean) as MSA:
	for line in MSA:
		if line[0] == ">":
			save.append(line)
			continue
		#if line[174] != "-": print(line[170:180])
				
		if line[174] == "-" and line[173] != "-":
			#if "Egretta_gularis" in save[-1]: print(line)
			line = line[0:173] +"-"+ line[173] + line[175:]
			#if "Egretta_gularis" in save[-1]: print(line)
		save.append(line)

with open("Clean_alignment/ND3_final.fa", "w") as O:
	TO_add = "".join(save)
	O.write(TO_add)
