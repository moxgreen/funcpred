DATA_PRJ_ROOT=$(BIOINFO_ROOT)/prj/lncrna2function_clone/dataset/
DATA_VERSION?=gtex_single_tissue_log.GO.noIEA.BP
MYSQL=mysql --local-infile -BCAN -u funcpred --password=funcpred -h 130.192.147.6 funcpred
H_CUTOFF?=0.05

db_GENES: /raid/molineri/bioinfotree/task/annotations/dataset/ensembl/hsapiens/73/gene-readable.map.gz
	bawk '$$gene_id~/^ENS/ {if($$biotype!="protein_coding" && $$biotype!="pseudogene" && $$biotype!="lincRNA" && $$biotype!="antisense" && $$biotype!="antisense"){$$biotype="other"} \
		print $$gene_id, $$gene_name, $$biotype, $$description, $$status}' $< \
	| uniq \
	| enumerate_rows > $@

db_GeneFunction.$(DATA_VERSION).%: $(DATA_PRJ_ROOT)/$(DATA_VERSION)/%/all/predictions.fdr.gz db_ExpressionSource db_function db_GENES
	bawk '$$H<$(H_CUTOFF) {print $$H,$$GO,$$gene,$$leave_one_out}' $< \
	| translate <(bawk '{print $$GO,$$pk}' $^3) 2 \
	| translate <(bawk '{print $$gene_id,$$pk}' $^4) 3 \
	| append_each_row `bawk '$$4=="$*" {print $$1}' $^2` \
	| bawk '{tmp=$$4; $$4=$$5; $$5=tmp; print}'\      *scambio due colonne per ordine in db 
	| enumerate_rows -s $(shell tail -n 1 `ls -tr db_GeneFunction.* | grep -v LOADED | tail -n 1` | cut -f 1) > $@
#echo "LOAD DATA LOCAL INFILE 'db_GENES' INTO TABLE funcpred_gene" | mysql --local-infile -u funcpred -p -h 130.192.147.6 funcpred

db_GeneFunction.LOADED.%: db_GeneFunction.%
	$(MYSQL)<<<"LOAD DATA LOCAL INFILE '$<' INTO TABLE funcpred_genefunction";
	touch $@

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


UPDATE_DO_descriptions:
	zcat /raid/molineri/bioinfotree/task/annotations/dataset/disease_ontology/do_ensg_inclusive.gz \
	| cut -f 2,3 | sort | uniq \
	| bawk '$$2!~"^ENSP"' | bawk '{print "UPDATE funcpred_function SET description=\"" $$2 "\" WHERE keyword=\"" $$1 "\";"}' \
	| $(MYSQL)

