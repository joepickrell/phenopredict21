# phenopredict21

Predict phenotypes and/or probabilities of disease from a VCF file on the 21 Bitcoin Computer. 

The setup is: you have a genome sequence in a VCF file, and want to predict the phenotypes of the person who the genome belongs to. This command line tool pulls a phenotype prediction model from an external server that hosts the model in JSON format (https://github.com/joepickrell/pheno-server-21) and then returns the prediction. 

Right now the server only has a model for predicting Alzheimer's disease. 

## Set up ##

>git clone https://github.com/joepickrell/phenopredict21.git

>cd phenopredict21

>sudo pip3 install .

## Run ##

>phenoredict21 --pheno AD --vcf vcf/chr19.vcf.gz

