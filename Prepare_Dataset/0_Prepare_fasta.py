from pathlib import Path
from Bio import SeqIO



def Write_Fasta(Path_file, Output_f, Taxonomy_output, Missing_file):
	Output_f = "Fasta_generation/" + Output_f
	Taxonomy_output = "Fasta_generation/" + Taxonomy_output
	Missing_file =  "Fasta_generation/" + Missing_file
	for F in [Taxonomy_output, Output_f]:
		with open(F, "w") as O:
			pass	
	MISS = []
	Output = ""
	for File in Path(Path_file).glob("*.gb"):
		IN = False
		with open(File,"r") as handle:
			Entry = SeqIO.parse(handle,"genbank")
			for i in Entry:
				NCBI_ID = i.name
				organism = i.annotations['organism'].replace(" ","_")
				if "UNVERIFIED" in i.description: continue
				sequence = str(i.seq)
				Tx = i.annotations['taxonomy']
	
				if "Bifurcata" in Tx: taxonomy = "Bifurcata"
				elif "Aves" in Tx: taxonomy = "Aves"
				elif "Crocodylia" in Tx: taxonomy = "Crocodylia"
				elif "Testudines" in Tx: taxonomy = "Testudines"
				elif "Squamata" in Tx: taxonomy = "Squamata"
				elif "Mammalia" in Tx: taxonomy = "Mammalia"
				elif "Amphibia" in Tx: taxonomy = "Amphibia"
				elif "Actinopterygii" in Tx: taxonomy = "Actinopterygii"
				elif "Elasmobranchii" in Tx: taxonomy = "Elasmobranchii"
				else: taxonomy = "unknown"

			for gene in i.features:				
				try: g = gene.qualifiers["gene"][0].strip("'")
				except: 
					try:
						if gene.type == "CDS":
							g = gene.qualifiers["product"][0].strip('"')
						else: continue
					except:
						continue
				if g == "ND3" or  g== "NADH dehydrogenase subunit 3":
					IN = True
					sequence = str(i.seq)			
					l = list(gene.location)
					try: b= l[0]
					except: continue
					e=l[-1]
					s = sequence[b:e]
			if IN == True:		
				Output = ">" + organism + "-" + NCBI_ID + "\n" + s
				with open(Taxonomy_output, "a") as O:
					O.write(organism + "\t" + taxonomy + "\n")
				with open(Output_f, "a") as O:
					O.write(Output + "\n")
			else:
				MISS.append(str(File))

	with open(Missing_file,"w") as F:
		F.write("\n".join(MISS))			

dic_file = {"../NCBI_SEQ/complete_gbs": ["ND3_RefSeq_genes.fa", "Taxon_RefSeq","Miss_RefSeq" ], "../NCBI_SEQ/gbs/": ["ND3_GenBank", "Taxon_GenBank", "Miss_GenBank"]}
for FILE in dic_file:
	Write_Fasta(FILE, dic_file[FILE][0],  dic_file[FILE][1],  dic_file[FILE][2])


