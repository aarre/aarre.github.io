
ALL_PDF = $(wildcard _portfolio/*.pdf)
# $(info $$ALL_PDF = ${ALL_PDF})
ALL_PNG = $(ALL_PDF:.pdf=.png)
# $(info $$ALL_PNG = ${ALL_PNG})

# Generate static pages and serve them through a website at
# https://localhost:4000/

serve:
	bundle exec jekyll serve --incremental


# Read the Gemfile that lists the gems this application depends on,
# resolve these dependencies, fetch the needed gems from a remote
# source (https://rubygems.org) and install them into the Ruby
# environment.

update:
	bundle config set path 'vendor/bundle'
	bundle update --bundler


# The title in this one is in the middle of the page
_portfolio/digital_entrepreneurship_and_innovation_in_central_america.png:	_portfolio/digital\ entrepreneurship\ and\ innovation\ in\ central\ america.pdf
	pdftoppm -png -f 1 -l 1 -y 400 -H 800 -singlefile $< > $@

# The titles in these ones are toward the top of the page
_portfolio/scaling_up_romania.png:	_portfolio/scaling\ up\ romania.pdf
	pdftoppm -png -f 1 -l 1 -y 0 -H 800 -singlefile $< > $@

# The titles in these ones are toward the top of the page
_portfolio/starting_up_romania.png:	_portfolio/starting\ up\ romania.pdf
	pdftoppm -png -f 1 -l 1 -y 0 -H 800 -singlefile $< > $@

# Make PNG files from PDF, general case
# %.png: %.pdf
#	pdftoppm -png -f 1 -l 1 -y 400 -H 800 -singlefile $< > $@

.PHONY:	clean

clean:
	$(RM) $(ALL_PNG) ;\

