source "https://rubygems.org"
ruby "2.4.3"

# This will help ensure the proper Jekyll version is running.
gem "jekyll", "3.6.2"
gem "html-proofer", :groups => [:development, :test]
gem "git-set-mtime", github: "jayvdb/git-set-mtime", branch: "file-exists"

group :jekyll_plugins do
  gem "github-pages"
  gem "jekyll-netlify", github: 'jayvdb/jekyll-netlify', ref: 'e7efada3'
  gem "disqus-for-jekyll"
  gem "jekyll-last-modified-at", github: "jayvdb/jekyll-last-modified-at", branch: "fix-no-git-check"
  gem 'jekyll-include-cache'
  gem 'jekyll-analytics', github: 'jayvdb/jekyll-analytics', branch: 'allow-missing'
end

# Windows does not include zoneinfo files, so bundle the tzinfo-data gem
gem 'tzinfo-data', platforms: [:mingw, :mswin, :x64_mingw, :jruby]
