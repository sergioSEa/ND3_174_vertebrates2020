FILE = "Supplemenetary_Table_1.tsv"


B10K_calls = {}
with open(FILE) as F:
	for line in F:
		l = line.rstrip().split()
		
		if "-B10K" not in l[0]: continue
		ID = "-".join(l[0].split("-")[0:-1])
		B10K_calls[ID] = l[1]
Not_match = []
Match = []

with open(FILE) as F:
	for line in F:
		l = line.rstrip().split()
		ID = "-".join(l[0].split("-")[0:-1])
		if "-B10K" in l[0]: continue
		if ID in B10K_calls:
			B10K = B10K_calls[ID]
			No_B10K = l[1]
			if B10K != No_B10K:
				Not_match.append(ID)
			else:
				Match.append(ID)
print(len(set(Match)))
print(len(set(Not_match)))

print(set(Not_match))
