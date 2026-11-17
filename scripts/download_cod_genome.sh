#!/bin/bash
# Download the Atlantic cod (Gadus morhua) reference genome assembly from NCBI.
# Assembly: gadMor3.0, accession GCF_902167405.1 (RefSeq)
# Requires: NCBI datasets CLI (conda install -c conda-forge ncbi-datasets-cli)

mkdir -p data/raw
datasets download genome accession GCF_902167405.1 \
  --include genome \
  --filename data/raw/cod_gadMor3.zip
unzip -o data/raw/cod_gadMor3.zip -d data/raw/cod_gadMor3