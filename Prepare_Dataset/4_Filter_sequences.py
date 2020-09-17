from Bio import SeqIO
import subprocess

Alignment = "Alignment/ND3_msa.fa"
Alignment_Clean= "tmp/ND3_clean.fa"


subprocess.call(["bash", "Others/Clean_alignment.sh", Alignment, Alignment_Clean])

OUT=[]
Keep_seqs = []
dic_filter= {}
with open(Alignment_Clean,"r") as handle:
	Entry = SeqIO.parse(handle,"fasta")
	for Sequence in Entry:
		Name = Sequence.id
		Nucl = Sequence.seq 
		if len(set(Nucl))  < 3: dic_filter[Name] = "Gaps/N" ; continue
		if Name in ["Euphlyctis_karaavali","Barbastella_pacifica"]: dic_filter[Name] = "Weird_sequence" ; continue
		if Name[0] == "(":  dic_filter[Name] = "Naming" ; continue
		if "Cyclemys_pulchristriata" in Name: dic_filter[Name] = "Ambiguous_alignment"	
		if Nucl[170:178].count("-") > 1 or Nucl[170:178].count("n") > 1:
			dic_filter[Name] = "Gaps_Ns_around_174"
			continue

		OUT.append(">"+Name+"\n"+str(Nucl)+"\n")
		Keep_seqs.append(Name)
print("Sequences Kept {N}".format(N= len(Keep_seqs)))

with open("tmp/ND3_foralignment2.fa", "w") as O:
	O.write("".join(OUT))
with open("Others/Seqs_filterd.txt","w") as O2:
	for key in dic_filter:
		Reason = dic_filter[key]
		O2.write(key+"\t"+Reason+"\n")		
OUT2 = []
For_align = []
with open("Merging/ND3_merged.fa", "r") as handle:
	Entry = SeqIO.parse(handle,"fasta")
	for Sequence in Entry:
		if Sequence.id not in Keep_seqs: continue
		OUT2.append(">"+Sequence.id+"\n"+str(Sequence.seq)+"\n")
print(len(OUT2))
with open("tmp/Filtered_ND3_seqs.fa", "w") as Out:
	Out.write("".join(OUT2))
			
