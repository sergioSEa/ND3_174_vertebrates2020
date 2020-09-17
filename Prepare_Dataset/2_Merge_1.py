from Bio import SeqIO

#Given two sets of ND3 (NCBI and B10K), merge them and remove duplicates





#####Get the translation to latin name from B10K ID
translation = {}
with open("../../../NAME-ID.txt") as File:
	for line in File:
		if "ID" in line: continue
		l = line.split(",")
		translation[l[0]] = l[1].rstrip().replace(" ","_")

####Save in a dic the B10K sequences. Latin_name : Sequence
Available = {}
Remove_b10K =  ["Nipponia_nippon","Pygoscelis_adeliae","Mohoua_ochrocephala", "Coturnix_japonica", "Zosterops_lateralis", "Meleagris_gallopavo","Falco_cherrug", "Gallus_gallus", "Taeniopygia_guttata","Pseudopodoces_humilis", "Serinus_canaria","Phalacrocorax_brasilianus", "Lonchura_striata", "Anas_platyrhynchos","Sylvia_atricapilla","Poecile_atricapillus","Chlorodrepanis_virens","Phasianus_colchicus", "Nannopterum_brasilianus", "Eurystomus_gularis"]
with open("../Aligned_ND3_seqs_B10K.fa") as B10K:
	S = SeqIO.parse(B10K, "fasta")
	for Species in S:
		N = Species.name.split("_")[0]
		if N == "NCBI-030": continue
		N = translation[N]
		if N in Remove_b10K: continue
		Available[N] = str(Species.seq).upper()

####Go through ND3 NCBI records. If they are already in B10K, add them to a list of already done. If they  have been already seen between the NCBI ones, add them to a second list of repeated in NCBI. 
#Otherwise: Attach to a string including all seqs

FINAL = ""
Repeated = []
Done_NCBI = []
repeated_NCBI = []
Chosen  = []
with open("Merging/ND3_genes.fa","r") as File:
	Entry = SeqIO.parse(File,"fasta")
	for Species in Entry:
		#if "-" in Species.name:
		#	N = Species.name.split("-")[0:-1]
		#	N = "-".join(N)
		N = Species.name
		if N in Available:
			Repeated.append(N)
			#continue
		
		if N in Done_NCBI:
			repeated_NCBI.append(Species.name)
			continue
		Done_NCBI.append(N)
		
		ADD = ">{NAME}\n{sequence}\n".format(NAME=N, sequence=str(Species.seq))	
		FINAL += ADD
##Attach the B10K in the FINAL (the NCBI which passed all restrictions).
for key in Available:
	if key in Repeated: continue
	Chosen.append(key + "-B10K")
	ADD = ">{NAME}\n{sequence}\n".format(NAME=key, sequence=str(Available[key]))
	FINAL += ADD

with open("Merging/Chosen.tsv", "a") as F:
	F.write("\t".join(Chosen))
##Get some numbers

print("Number of unique records: " + str(len(Available.keys())))
print("Number of records from NCBI already in B10K:" + str(len(Repeated)))
print("Number of records from NCBI who were removed because repeated:" + str(len(repeated_NCBI)))


with open("Merging/ND3_merged.fa","w") as OUT:
	OUT.write(FINAL)
with open("Merging/Overlapping_B10K-NCBI.txt", "w") as OUT:
	OUT.write("\n".join(Repeated))
