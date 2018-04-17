#!/usr/bin/env bash
pip install -e .
bcftools query -f '%CHROM\t%POS0\t%REF\t%ALT\n' -i 'TYPE!="snp"' ./single_chromosome/inputs/indels.vcf | awk 'BEGIN {chr=""} {if (chr!=$1){chr=$1; balance=0; print $1"\t"0"\t"0}; diff=length($4)-length($3); if (diff<0) print $1"\t"$2+1+balance"\t"balance+diff; else for(i=1;i<=diff;i++){print $1"\t"$2+1+i+balance"\t"balance+i}; balance=balance+diff}' | sort -k 1,1 -k 2,2n > ./single_chromosome/outputs/chr_pos0_ref_alt.tsv
allele-project -r ./single_chromosome/outputs/chr_pos0_ref_alt.tsv -b ./single_chromosome/inputs/reads.bedGraph -o ./single_chromosome/outputs/reads.bedGraph
diff ./single_chromosome/outputs/reads.bedGraph ./single_chromosome/controls/reads.bedGraph