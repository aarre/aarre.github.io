


# Generate static pages and serve them through a website at
# https://localhost:4000/

serve:
	bundle exec jekyll serve


# Read the Gemfile that lists the gems this application depends on,
# resolve these dependencies, fetch the needed gems from a remote
# source (https://rubygems.org) and install them into the Ruby
# environment.

update:
	bundle config set path 'vendor/bundle'
	bundle update --bundler



png:	${FILE}.pdf
	 pdftoppm -png -f 1 -l 1 -singlepage $@
