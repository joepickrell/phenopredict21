# phenopredict21

Predict phenotypes and/or probabilities of disease from a VCF file on the 21 Bitcoin Computer. 

The setup is: you have a genome sequence in a VCF file*, and want to predict the phenotypes of the person who the genome belongs to. This command line tool pulls a phenotype prediction model from an external server that hosts the model in JSON (https://github.com/joepickrell/pheno-server-21) in exchange for BTC and then returns the prediction. 

Right now the server only has a model for predicting Alzheimer's disease risk (and note there are lots of caveats to risk prediction, this is intended only as a toy example). 

*To obtain your genome sequence, there are a few options (I am not affiliated with any of these except where noted): You could get whole genome sequencing from places like [Full Genomes](https://www.fullgenomes.com/), or get genotyped by companies like [23andMe](https://www.23andme.com/) or [AncestryDNA](http://dna.ancestry.com/). In the latter case, you will probabably want to do [genotype imputation](https://en.wikipedia.org/wiki/Imputation_(genetics)) using functionality available from places like [DNA.Land](https://dna.land/) (Note: I am affiliated with DNA Land). 

## Set up ##

>git clone https://github.com/joepickrell/phenopredict21.git

>cd phenopredict21

>sudo pip3 install .

## Run ##

>phenopredict21 --pheno AD --vcf vcf/chr19.vcf.gz


## Options ##

To see a list of available phenotypes, use the --phenos flag:

>phenopredict21 --phenos

Right now this will return only "AD", for Alzheimer's disease

To input a VCF file and a phenotype, use --pheno and --vcf, as in the example above

## Output ##

The output is a dict in JSON with the following entries:

1. 'odds': odds of developing the disease, relative to the average European-descent individual
2. 'absolute_risk': the absolute probability of developing the disease, calculated using the odds and the baseline probability
3. 'average_risk': the probability of developing the disease for an average person in the population (this is used as the baseline for calculating the absolute risk, and so this has a large effect on the risk calculation)
4. 'score': the polygenic risk score for the individual, used to calculate the odds
5. 'meanscore': the polygenic risk score for an average person of European ancestry
6. 'ngt': the number of SNPs in the risk prediction model that are also in the VCF file
7. 'nmiss': the number of SNPs in the risk prediction model that are absent from the VCF file


