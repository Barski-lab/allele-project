#!/usr/bin/env bash
bcftools query -f '%CHROM\t%POS0\t%REF\t%ALT\n' -i 'TYPE!="snp"' ./single_chromosome/inputs/indels.vcf | awk 'BEGIN {chr=""} {if (chr!=$1){chr=$1; balance=0; print $1"\t"0"\t"0}; diff=length($4)-length($3); if (diff<0) print $1"\t"$2+1+balance"\t"balance+diff; else for(i=1;i<=diff;i++){print $1"\t"$2+1+i+balance"\t"balance+i}; balance=balance+diff}' | sort -k 1,1 -k 2,2n > ./single_chromosome/outputs/chr_pos0_ref_alt.tsv
python ../main.py -r ./single_chromosome/outputs/chr_pos0_ref_alt.tsv -b ./single_chromosome/inputs/coverage.bedGraph -o ./single_chromosome/outputs/coverage.bedGraph
diff ./single_chromosome/outputs/coverage.bedGraph ./single_chromosome/controls/coverage.bedGraph


bcftools query -f '%CHROM\t%POS0\t%REF\t%ALT\n' -i 'TYPE!="snp"' ./multiple_chromosome/inputs/indels.vcf | awk 'BEGIN {chr=""} {if (chr!=$1){chr=$1; balance=0; print $1"\t"0"\t"0}; diff=length($4)-length($3); if (diff<0) print $1"\t"$2+1+balance"\t"balance+diff; else for(i=1;i<=diff;i++){print $1"\t"$2+1+i+balance"\t"balance+i}; balance=balance+diff}' | sort -k 1,1 -k 2,2n > ./multiple_chromosome/outputs/chr_pos0_ref_alt.tsv
python ../main.py -r ./multiple_chromosome/outputs/chr_pos0_ref_alt.tsv -b ./multiple_chromosome/inputs/coverage.bedGraph -o ./multiple_chromosome/outputs/coverage.bedGraph
diff ./multiple_chromosome/outputs/coverage.bedGraph ./multiple_chromosome/controls/coverage.bedGraph