import sys, gzip
import json
import click

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
			print(line)
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
	print(allsnps)
	vcfsnps = readVCF(vcffile, allsnps)
	print(vcfsnps)
	return

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
        	predict(model, vcf)
	else:
		click.echo('no phenotype: '+pheno)
