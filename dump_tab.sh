#!/bin/bash
seq 0 1000000 142000000 | parallel -j 1 'echo "SELECT ensg, funcpred_gene.name, fdr, known, keyword, ontology_id, funcpred_function.description, funcpred_expressionsource.name FROM funcpred_genefunction INNER JOIN funcpred_gene ON funcpred_genefunction.gene_id = funcpred_gene.id INNER JOIN funcpred_function ON funcpred_genefunction.function_id = funcpred_function.id INNER JOIN funcpred_expressionsource ON funcpred_genefunction.expression_source_id  = funcpred_expressionsource.id LIMIT {}, 100000" | mysql -BCAN -u funcpred2 -p"funcpred" funcpred2'