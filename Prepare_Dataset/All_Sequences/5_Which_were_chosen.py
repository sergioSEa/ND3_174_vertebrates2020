

#All records Supp_Mat_source.tsv Name ID File
#Prioritized Refseq > Genbank   Repeated_NCBI.txt "Overlapping_Refseq-Genebank.txt"
In_table = []
with open("../Summary_Table.tsv") as F:
	for line in F:
		l = line.split()
		In_table.append(l[0])



Selected = []
with open("../Merging/Chosen.tsv") as F:
	for line in F:
		ID = "-".join(line.rstrip().split("-")[0:-1])
		if ID not in In_table : continue
		Selected.append(line.rstrip())
OUT = "Supplemenetary_Table_1.tsv"

with open(OUT, "w") as F: pass

###Addd IF chosen
with open("Table_CompleteTaxa.tsv") as Final:
	for line in Final:
		l = line.rstrip().split()
		if l[0] in Selected: Chosen = True
		else: Chosen = False
		Status = l[1]
		Source = l[-1]
		

		if Source == "ND3_GenBank": Source = "GenBank"
		elif Source == "ND3_RefSeq_genes.fa": Source = "RefSeq"
		

		ll = "\t".join([l[0], Status, Source, str(Chosen)])
		#print(ll)
		with open(OUT,"a") as O:
			O.write(ll + "\n")
