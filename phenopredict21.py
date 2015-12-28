import sys, gzip
import json
import click
import math

#import from the 21 Developer Library
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests

#set up bitrequest client for BitTransfer requests
wallet = Wallet()
username = Config().username
requests = BitTransferRequests(wallet, username)

#server address
server_url = 'http://localhost:5000/'


def listsnps(phenomodel):
	toreturn = dict()
	allsnps = phenomodel['snps']
	for snplist in allsnps:
		for snp in snplist:
			# Using chr:pos as unique identifier. Dangerous but good enough for now. 
			id = snp['chr'][3:]+":"+str(snp['pos'])
			toreturn[id] = snp
	return toreturn			

def readVCF(vcffile, snps):
	infile = gzip.open(vcffile)
	toreturn = dict()
	line = infile.readline()
	i = 0
	while line:
		line = bytes.decode(line)
		line = line.strip().split()
		if line[0][0] == "#":
			line = infile.readline()
			continue
		# Using chr:pos as unique identifier
		if i % 10000 == 0:
			print('\r>> Scanned %d variants in VCF' % i, end='\r')
		id = line[0]+":"+line[1]
		if id in snps: 
			ref = line[3]
			alt = line[4]
			gtid = -9
			format = line[8].split(":")
			for i in range(len(format)):
				if format[i] == "GT":
					gtid = i
			if gtid == -9:
				print("Bad VCF")
				return 1
			geno = line[9].split(":")[gtid]
			a1 = ref
			if geno[0] == "1": a1 = alt
			a2 = ref
			if geno[2] == "1": a2 = alt
			toreturn[id] = {'a1': a1, 'a2': a2}
		i = i+1
		line = infile.readline()
	return toreturn
		
def predict(phenomodel, vcffile):
	allsnps = listsnps(phenomodel)
	vcfsnps = readVCF(vcffile, allsnps)
	ngt = 0
	nmiss = 0
	score = 0
	meanscore = 0
	snpvectors = phenomodel['snps']
	# going to use only the first SNP in each vector (remainder are backup SNPs in LD in case primary not genotypes)
	for snpvector in snpvectors:
		snp = snpvector[0]
		c = snp['chr'][3:]
		p = snp['pos']
		id = c+":"+str(p)
		if id in vcfsnps:
			effect = snp['alt_effect_het']
			alt = snp['alt']
			ref = snp['ref']
			gt = vcfsnps[id]
			if gt['a1'] != alt and gt['a1'] != ref:
				click.echo('bad snp genotype '+gt['a1']+','+gt['a2']+', alleles are '+ref+' and '+alt+' ('+c+':'+p+')\n')	
				nmiss = nmiss+1
				continue
			if gt['a1'] == alt:
				score=  score+effect
			if gt['a2'] == alt:
				score = score+effect
			euf = snp['eur_af']
			meanscore = meanscore+2*euf*effect
			ngt = ngt+1	
		else:
			nmiss = nmiss+1			

	odds = math.exp(score-meanscore)
	baselinerisk = phenomodel['baseline_prob']
	baselineodds = baselinerisk/(1-baselinerisk)
	absodds = baselineodds*odds
	absrisk = absodds/(1+absodds)
			
	return {'odds': odds, 'absolute_risk': absrisk, 'average_risk': baselinerisk, 'score': score, 'meanscore': meanscore, 'ngt': ngt, 'nmiss':nmiss}

@click.command()
@click.option('--pheno', help = 'Phenotype to predict')
@click.option('--phenos', is_flag=True, help = 'List phenotypes available')
@click.option('--vcf', help = 'input VCF file')
def cli(pheno, phenos, vcf):

	sel_url = server_url+'phenos'
	response = requests.get(url=sel_url)
	ps = json.loads(response.text)
	if phenos:
		click.echo(json.dumps(ps))
		return
 
	if pheno in ps['phenolist']:
		url2 = server_url+'phenos/'+pheno
		response = requests.get(url=url2)
		model = json.loads(response.text)
		prediction = predict(model, vcf)
		click.echo(json.dumps(prediction))
	else:
		click.echo('no phenotype: '+pheno)
