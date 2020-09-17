from Bio import SeqIO



Diapsida = ["Squamata", "Testudines","Crocodylia", "Bifurcata", "Aves"]
Diapsida_taxa = []
with open("Diapsida/Diapsida_table.tsv","w"): pass
with open("Table_UniqueTaxa.tsv") as F:
	for line in F:
		l = line.rstrip().split("\t")
		if l[2] in Diapsida: 
			Diapsida_taxa.append(l[0])
			with open("Diapsida/Diapsida_table.tsv", "a") as O:
				O.write(line)
with open("Diapsida/Alignment_diapsida.tsv","w"): pass
with open("Clean_alignment/ND3_final.fa") as F:
	Records = SeqIO.parse(F, "fasta")
	for Organism in Records:
		if Organism.id not in Diapsida_taxa: continue
		ADD = ">{ID}\n{SEQ}\n".format(ID=Organism.id, SEQ=str(Organism.seq))
		with open("Diapsida/Alignment_diapsida.tsv", "a") as O:
			O.write(ADD)
