genes.gz: ../../local/share/data/gene.txt ../db_GENES
	translate -v -e NA -a -d -f 3 $^2 1 < $< | gzip >$@

