from Bio import SeqIO

#Given two sets of ND3 (Refeseq compelte and non), merge them and remove duplicates






####Save in a dic the Refseq sequences. Latin_name : Sequence
repeated_NCBI = []
Available = {}
with open("Fasta_generation/ND3_RefSeq_genes.fa") as Refseq:
	S = SeqIO.parse(Refseq, "fasta")
	for Species in S:
		N = Species.name
		if "-" in N: 
			N = N.split("-")[0:-1]
			N = "-".join(N)
		if N in Available:
			repeated_NCBI.append(Species.name)
		Available[N] = str(Species.seq).upper()

FINAL = ""
Repeated = []

Done_NCBI = []
Selected = []
with open("Fasta_generation/ND3_GenBank","r") as File:
	Entry = SeqIO.parse(File,"fasta")
	for Species in Entry:
		N = Species.name
		if "-" in N:
			ID_N =  N.split("-")[-1]
			N = N.split("-")[0:-1]
			N = "-".join(N)
			if N == "Opisthocomus_hoazin":
				if ID_N != "AF076363": Repeated.append(Species.name) ; continue
		#If species from Genbank already in refseq, dont add them
		if N in Available:
			Repeated.append(Species.name)
			continue
		else:
			Selected.append(N+"-"+ID_N)
			#Get only the first sequence to be seen in NCBI
			if N in Done_NCBI:
				repeated_NCBI.append(Species.name)
				continue
		Done_NCBI.append(N)
		ADD = ">{NAME}\n{sequence}\n".format(NAME=N, sequence=str(Species.seq))	
		FINAL += ADD
##Attach the B10K in the FINAL (the NCBI which passed all restrictions).
for key in Available:
	ADD = ">{NAME}\n{sequence}\n".format(NAME=key, sequence=str(Available[key]))
	FINAL += ADD


##Get some numbers

with open("Merging/Chosen.tsv","w") as C:
	C.write("\n".join(Selected))
with open("Merging/ND3_genes.fa","w") as OUT:
	OUT.write(FINAL)
with open("Merging/Overlapping_Refseq-Genebank.txt", "w") as OUT:
	OUT.write("\n".join(Repeated))
with open("Merging/Repeated_NCBI.txt", "w") as OUT:
	OUT.write("\n".join(repeated_NCBI))
