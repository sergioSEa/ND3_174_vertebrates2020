import sys
import subprocess
from Bio import SeqIO

Prev = []
with open("../Clean_alignment/ND3_final.fa") as F:
	Info = SeqIO.parse(F, "fasta")
	for Item in Info:
		Prev.append(Item.id)	


FILE = "Aligned/ND3_msa_merged.fa"#ND3_msa_2.fa" #sys.argv[1]
Alignment_Clean = "tmp/ND3_clean2.fa"
subprocess.call(["bash", "Clean_alignment.sh", FILE, Alignment_Clean])


Final = ""
dic_filter = {}
#Remove ambiguous alignments
with open(Alignment_Clean) as MSA:
	Info = SeqIO.parse(MSA, "fasta")
	for Item in Info:
		Name = Item.id
		if Name in Prev: continue
		Nucl = Item.seq
		if len(set(Nucl))  < 3: dic_filter[Name] = "Gaps/N" ; continue
		if Name[0] == "(":  dic_filter[Name] = "Naming" ; continue
		if Nucl[188:197].count("-") > 1 or Nucl[187:194].count("n") > 1:
			dic_filter[Name] = "Gaps_Ns_around_174"
			continue
		if "Cyclemys_pulchristriata" in Name: dic_filter[Name] = "Ambiguous_alignment"
		Final += ">{N}\n{S}\n".format(N=Item.id, S=str(Item.seq))

with open(Alignment_Clean, "w")  as O:
	O.write(Final)

with open("Others/Seqs_filterd.txt","w") as O2:
	for key in dic_filter:
		Reason = dic_filter[key]
		O2.write(key+"\t"+Reason+"\n")

save = []

with open(Alignment_Clean) as MSA:
	for line in MSA:
		if line[0] == ">":
			save.append(line)
			continue
		#if line[174] != "-": print(line[170:180])
		
		#print(line[190:195])


		if line[192] != "-" and line[193] == "-":	
			#print(line[170:173] + "-" + line[173:180])
			line = line[0:192] + "-" +line[192] +  line[194:]	
		save.append(line)

with open("Clean_alignment/ND3_final.fa", "w") as O:
	TO_add = "".join(save)
	O.write(TO_add)
