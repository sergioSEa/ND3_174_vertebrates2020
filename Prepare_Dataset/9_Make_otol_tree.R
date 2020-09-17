#source activate /faststorage/home/sersan/ND3_insertion/Proper_Analysis/Rebootal/Diapsida/R_packages

library(dplyr)
library(tibble)
library(readr)
library(ape)
#library(phytools)
library(rotl)




dataset = read_tsv("Diapsida/Diapsida_table.tsv",col_names=F)


#############################################################
#######################Get tree##############################
#############################################################



taxa = gsub(" ","_",dataset$X1)
resolved_names = vector()

resolved_names = tibble(search_string=character(),unique_name=character(),approximate_match=logical(),ott_id=numeric(),is_synonym=logical(),flags=character(),number_matches=numeric())
resolved_names = as.data.frame(resolved_names)

###For each species, get otol name
for (item in 1:length(taxa)){
  tryCatch({
   Name = tnrs_match_names(taxa[item])
    resolved_names = rbind(resolved_names, Name)
  }, error=function(e){cat(paste(c("ERROR: ",item, taxa[item], collapse=F)) , "\n")})  
 
}
write_csv(x = resolved_names, path = "Diapsida/OTL_tree/R_names_itol.csv")
#resolved_names = read_csv("Diapsida/OTL_tree/R_names_itol.csv")

print("Read tree")
#Tree with all vertebrades
my_tree  = read.tree("Diapsida/OTL_tree/opentree11.4_tree/labelled_supertree/labelled_supertree_ottnames.tre")
print("Get Diapsida clade")
#Extract diapsida
my_tree = extract.clade(my_tree, "mrcaott59ott1662")


add_tonumber = function(vector_id){ paste(c("ott",vector_id), collapse="") }
print("Make the resolved names match names in the tree tips")
v_d = vector()
#Prepare names in the same format than seen in the Otol tree. Save them in v_d  vector
for (i in seq(dim(resolved_names)[1])){
  I = resolved_names[i,]
  name = I$search_string
  name = paste(c(toupper(substring(name, 1, 1)), substring(name, 2)), collapse="")
  vector_id =  I$OTT_name
  d = paste(c(name,vector_id), collapse="_")
  v_d = c(v_d,d)
}
naming = sapply(resolved_names$ott_id,FUN=add_tonumber)
print("Check names missing in the tree")
print(v_d)
#Check for names in the Otol tree
resolved_names %>% mutate(OTT_name = naming, Match_name = v_d) -> resolved_names
resolved_names %>% filter(! Match_name %in% my_tree$tip.label) -> not_found
print(not_found)

get_N = function(NAME, OUT){
  N = strsplit(NAME,split = "_")
  ott = N[[1]][3]
  N = paste(N[[1]][1:2],collapse=" ")
  if (OUT == "ott"){return(ott)
    }else{ return(N)}
}

print("Get tree names")
###Try to match the unmatched either by NAME or OTT, then change the tip names so they all look the same.
Name = unlist(lapply(FUN = get_N,X = my_tree$tip.label, OUT="name"))
OTTs = unlist(lapply(FUN = get_N,X = my_tree$tip.label, OUT="ott"))

#resolved_names %>% mutate(unique_name = ifelse(search_string=="chinemys_reevesi","Chinemys_reevesi",unique_name)) -> resolved_names

print("Check names that do not match between the search string and the unique name")
Remove = which((toupper(resolved_names$search_string) == gsub(" ","_",toupper(resolved_names$unique_name))) == F)
resolved_names = resolved_names[-Remove,]
print("Check matching names with tree")
resolved_names %>% filter(unique_name %in% Name) -> RN
resolved_names %>% filter(! unique_name %in% Name) %>% filter(!search_string == "chinemys_reevesi") -> not_found2
#Species not found in the tree somehow
dim(not_found2)


####RN are the ones found
RN  %>% filter(search_string == "chinemys_reevesi") -> INCLUDE
RN %>% filter(is_synonym==F) -> RN
RN = rbind(RN, INCLUDE)
my_tree$tip.label = Name

###There are unique names which are repeated length(unique(RN$unique_name)) != length(RN$unique_name)

my_tree = keep.tip(my_tree, RN$unique_name)

write.tree(my_tree, "Diapsida/OTL_tree/Total_tree.tree")

resolved_names %>% filter(! search_string %in% RN$search_string) -> dataset_notused
write_tsv(dataset_notused,"Diapsida/OTL_tree/discarted.tsv")
write_tsv(RN,"Diapsida/OTL_tree/nondiscarted.tsv")

dataset %>% filter(X1 %in% RN$Match_name) -> dataset
write_tsv(dataset, "Diapsida/Table_in_tree.tsv")

