#!/bin/bash
# Download the Atlantic cod (Gadus morhua) mitochondrial genome from NCBI.
# Accession: NC_002081.1 (part of reference assembly gadMor3.0)

mkdir -p data/raw
curl -o data/raw/cod_mito.fasta "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_002081.1&rettype=fasta&retmode=text"
