db_GENES: /raid/molineri/bioinfotree/task/annotations/dataset/ensembl/hsapiens/73/gene-readable.map.gz
	bawk '$$gene_id~/^ENS/ {if($$biotype!="protein_coding" && $$biotype!="pseudogene" && $$biotype!="lincRNA" && $$biotype!="antisense" && $$biotype!="antisense"){$$biotype="other"} \
		print $$gene_id, $$gene_name, $$biotype, $$description, $$status}' $< \
	| enumerate_rows > $@

#echo "LOAD DATA LOCAL INFILE 'db_GENES' INTO TABLE funcpred_gene" | mysql --local-infile -u funcpred -p -h 130.192.147.6 funcpred


.META: db_GENES
	1  pk
	2  gene_id      ENSG00000208234
	3  gene_name    AC019043.8
	4  biotype      scRNA_pseudogene
	5  description  cippo lippo
	6  status       NOVEL

