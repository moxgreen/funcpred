DATA_PRJ_ROOT=$(BIOINFO_ROOT)/prj/lncrna2function_clone/dataset/
MYSQL=mysql --local-infile -BCAN -u funcpred --password=funcpred -h 130.192.147.6 funcpred

db_GENES: /raid/molineri/bioinfotree/task/annotations/dataset/ensembl/hsapiens/73/gene-readable.map.gz
	bawk '$$gene_id~/^ENS/ {if($$biotype!="protein_coding" && $$biotype!="pseudogene" && $$biotype!="lincRNA" && $$biotype!="antisense" && $$biotype!="antisense"){$$biotype="other"} \
		print $$gene_id, $$gene_name, $$biotype, $$description, $$status}' $< \
	| uniq \
	| enumerate_rows > $@

db_GeneFunction.max_pk:
	$(MYSQL)<<<"SELECT MAX(id) from funcpred_genefunction;" > $@

db_GeneFunction.DO.%: $(DATA_PRJ_ROOT)/DO/%/all/predictions.fdr.gz db_ExpressionSource db_function db_GENES db_GeneFunction.max_pk
	bawk '$$H<0.05 {print $$GO,$$gene,$$H,$$leave_one_out}' $< \
	| translate <(bawk '{print $$GO,$$pk}' $^3) 1 \
	| translate <(bawk '{print $$gene_id,$$pk}' $^4) 2 \
	| append_each_row `bawk '$$4=="$*" {print $$1}' $^2` \
	| enumerate_rows -s `cat $^5`\
	| select_columns 1 4 2 3 5 6 > $@
#echo "LOAD DATA LOCAL INFILE 'db_GENES' INTO TABLE funcpred_gene" | mysql --local-infile -u funcpred -p -h 130.192.147.6 funcpred


.META: db_GENES
	1  pk
	2  gene_id      ENSG00000208234
	3  gene_name    AC019043.8
	4  biotype      scRNA_pseudogene
	5  description  cippo lippo
	6  status       NOVEL

db_function:
	echo "SELECT * FROM funcpred_function;" | mysql -BCAN -u funcpred -p -h 130.192.147.6 funcpred > $@

.META: db_function
	1	pk
	2	GO

db_ExpressionSource:
	echo "SELECT * FROM funcpred_expressionsource;" | mysql -BCAN -u funcpred --password=funcpred -h 130.192.147.6 funcpred > $@

