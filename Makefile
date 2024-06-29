
# Generate static pages and serve them through a website at
# https://localhost:4000/

publish:
	make update
	make build

ready:
	make clean
	make serve

build:
	bundle exec jekyll build

serve:
	bundle exec jekyll serve --incremental


# Read the Gemfile that lists the gems this application depends on,
# resolve these dependencies, fetch the needed gems from a remote
# source (https://rubygems.org) and install them into the Ruby
# environment.

update:
	bundle config set path 'vendor/bundle'
	bundle install --redownload
	bundle update --bundler
	gem update --system

.PHONY:	clean

clean:
	bundle exec jekyll clean
