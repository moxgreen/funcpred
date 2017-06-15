- ancestor.tsv
    - column 1: phenotype id
    - column 2: phenotype id of the closest ancestor for which we have a predictions: the phenotype in column 1 must be translated into the phenotype in column 2 to obtain a prediction
    
- phenotype_disease.tsv
    - column 1: phenotype id
    - column 2: a disease id to which the phenotype in col 1 is associated
    
- score.tsv
    - one row per gene
    - one column per phenotype
    - each cell contains the rank of the gene as predicted to be involved in the phenotype (low rank = highly likely)
