Remove = []
dic_changes= {}
with open("Taxonomy/Taxonomy_unknown.txt") as F:
	for line in F:
		l = line.rstrip().split()
		
		if len(l) == 3 : 
			if "?" not in l[2]: Remove.append(l[0]) ; print(l)
		dic_changes[l[0]] =  l[1]


with open("Summary_Table.tsv","w") as O: pass

with open("Table_UniqueTaxa.tsv") as F:
	for line in F:
		l = line.rstrip().split()
		Tax = l[2]
		if l[0] in Remove: continue
		
		if l[0] in dic_changes:
			Tax = dic_changes[l[0]]
		if Tax == "Bifurcata": Tax = "Squamata"
		elif l[0] == "Sphenodon_punctatus": Tax = "Squamata"
		elif Tax == "Elasmobranchii": Tax = "Chondrichthyes"
		elif l[0] in ["Latimeria_chalumnae","Latimeria_menadoensis"]: Tax = "coelacanth"
		l[2] = Tax
		with open("Summary_Table.tsv", "a") as O:
			O.write("\t".join(l) + "\n")

