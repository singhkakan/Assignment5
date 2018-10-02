#!/usr/bin/python

import sys
import fileinput
import re
import json
import urllib

gene_name = raw_input("Please type your gene name, all caps, and press enter : ")

# get gene_ID from file
matched=False
for line in fileinput.input(['/home/singhkak/assignment3/data/Homo_sapiens.GRCh37.75.gtf']):
    if re.match (r'.*\t.*\tgene\t', line):
        GN = re.findall('gene_name \"(.*?)\";', line)
        if gene_name == GN[0]:
            gene_id = re.findall('gene_id \"(.*?)\";', line)
            matched=True

# Fail Safe
if matched == False:
    print "Incorrect HUGO gene name"
    while matched == False:
        quit()

print "The variants within the gene " + gene_name + " (" + gene_id[0] + ") are :"

# Access the HUGO gene name specific json
link = "http://rest.ensembl.org/overlap/id/{}.json?feature=variation".format(gene_id[0])
data = urllib.urlopen(link).read()
json_output = json.loads(data)


# Getting data out of json
for i in json_output:
    x = i["id"]
    y = i["consequence_type"]
    a = y.replace("_", " ")
    z = i["clinical_significance"]
    if z == []:
        print "Variant " + x + " is a " + a + "."
    else:
        for b in z:
            print "Variant " + x + " is a " + a + ", and is clinically " + b.upper()
