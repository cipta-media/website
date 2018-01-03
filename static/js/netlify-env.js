---
layout: null
---
window.NETLIFY_ENV = {{site.netlify | jsonify}}

if (window.NETLIFY_ENV) {
  var repoUrl = NETLIFY_ENV.repository_url;

  window.NETLIFY_ENV.repository_slug =
    encodeURIComponent(
      repoUrl.replace('git@gitlab.com:', '')
    );
}
