File = "Table_CompleteTaxa.tsv"


dic_organisms = {}
Intraspecific = []
with open(File) as F:
	for line in F:
		l = line.rstrip().split()
		Org = "-".join(l[0].split("-")[0:-1])
		Status = l[1]
		if Org not in dic_organisms:
			dic_organisms[Org] = [Status]
		else:
			if Status not in list(set(dic_organisms[Org])): 
				Intraspecific.append(Org)
			dic_organisms[Org].append(Status)
for Int in Intraspecific:
	print(Int,dic_organisms[Int])

