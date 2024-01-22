# q2-pysyndna
QIIME 2 plugin for pysyndna functionality

WIP usage instructions:
```
qiime tools import \
    --input-path syndna_concs.csv \
    --output-path syndna_concs.qza \
    --type SyndnaPoolConcentrationTable
```

# TODO: check this
If you have a biom table that is not already imported into an artifact, run:
```
qiime tools import \
    --input-path syndna_counts.biom \
    --output-path syndna_counts.qza \
    --type FeatureTable[Frequency]
```

```
qiime pysyndna \
     --i-syndna-concs syndna_concs.qza \
     --i-syndna-counts syndna_counts.qza \
     --m-metadata-file sample_syndna_pool_weights_and_total_reads.tsv \
     --p-min-sample-count 1 \
     --o-regression-models regression_models.qza
```
