serve:
	bundle exec jekyll serve


png:	${FILE}.pdf
	 pdftoppm -png -f 1 -l 1 -singlepage $@
