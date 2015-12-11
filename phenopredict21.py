import sys
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


@click.command()
@click.option('--pheno', help = 'Phenotype to predict')
@click.option('--vcf', help = 'input VCF file')
def cli(pheno, vcf):

    sel_url = server_url+'phenos'
    response = requests.get(url=sel_url)
    phenos = json.loads(response.text)
    click.echo(phenos)
    if pheno in phenos['phenolist']:
        url2 = server_url+'phenos/'+pheno
        response = requests.get(url=url2)
        model = json.loads(response.text)
        click.echo(model)
    else:
        coords = json.loads(response.text)
        click.echo(coords)
