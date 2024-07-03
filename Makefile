
# Publish to GitHub/Netlify


push:
	make build
	make git


git:
	git add .
	git commit
	git push

# Build for a production environment

build:
	bundle exec jekyll build

# Publish to localhost

local:
	make clean
	make serve

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
	gem update --system

# Some things take a long time and only need to be done,
# for example, after upgrading ruby

imdesperate:
	bundle install --redownload

# Build the site (to generate current HTML) and then validate the HTML
check:
	make clean
	make build
	make validate

validate:
	html5validator --root ../aarre.github.io/_site --also-check-css

.PHONY:	clean

# Remove what can be removed to ensure a good build

clean:
	bundle exec jekyll clean
