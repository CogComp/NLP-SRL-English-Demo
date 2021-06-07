
makefiles:
	$(SHELL) ../../makedefs > Makefile.tmp
	cat Makefile.in >> Makefile.tmp
	mv Makefile.tmp Makefile
clean:
	rm -rf *~ \#* *core

tidy: clean
	cp Makefile.init Makefile
