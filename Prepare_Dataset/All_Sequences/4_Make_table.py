from Bio import SeqIO
import sys

#dic_GenBank = {}
#dic_RefSeq = {}
#def Taxonomy(File, dic_taxon):
dic_taxon = {}
with open("../Fasta_generation/Taxonomy_Table.tsv") as F:
	for line in F:
		l = line.rstrip().split()
		#dic_taxon["-".join(l[0].split("-")[0:-1])] = [l[1],l[2]]
		dic_taxon[l[0]] =  [l[1],l[2]]
	
#	return(dic_taxon)
#dic_GenBank = Taxonomy("Fasta_generation/Taxon_GenBank", dic_GenBank)
#dic_RefSeq = Taxonomy("Fasta_generation/Taxon_GenBank", dic_RefSeq)



INPUT="Clean_alignment/ND3_final.fa"
#INPUT = "tmp/ND3_clean.fa"

Output = ""
with open(INPUT) as handle:
	entries = SeqIO.parse(handle, "fasta")
	for entry in entries:
		ID = entry.name
		if ID == "Eurystomus_gularis-B10K": continue #Wrong sequence
		
		#ID2 = "-".join(ID.split("-")[0:-1])
		if ID in dic_taxon:
			taxon = dic_taxon[ID][0]
			origin = dic_taxon[ID][1]
		#elif ID in dic_GenBank:
		#	taxon = dic_taxon[ID]
		#	origin = "GenBank"
		else:
			if "B10K" in ID:
				taxon = "Aves"
				origin = "B10K"
			else: "Subset_orgin_unknown"
		#print(entry.seq[170:180])
		position = entry.seq[192]
		#if entry.seq[174] != "-": print(entry.seq[170:180],ID)
		if ID == "Tyto_alba-B10K": position = "c"
		if "Celeus_elegans" in ID: position = "-"
		if ID == "Hydrobates_castro-MK170187" : position = "c"
		if ID == "Todiramphus_chloris-AY998958" : position = "-"
		#position = entry.seq[174]
		Output += ID + "\t" + position + "\t" + taxon + "\t" + origin + "\n"

with open("Table_CompleteTaxa.tsv", "w") as O:
	O.write(Output)
