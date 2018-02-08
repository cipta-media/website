var netlifyRootUrl = window.NETLIFY_ENV.url.replace(/https?:\/\//, '');

function submissionTemplate(submission) {
  return [
    '<tr>',
      '<td class="col-md-1 text-center">',
        '<a href="' + submission.previewUrl + '">' + submission.number + '</a>',
      '</td>',
      '<td>' + submission.project + '</td>',
      '<td>' + submission.author + '</td>',
    '</tr>',
  ].join('');
}

function fetchSubmissions() {
  var GITLAB_MR_URL = 'https://gitlab.com/api/v4/projects/' +
                       window.NETLIFY_ENV.repository_slug +
                       '/merge_requests?state=opened';

  return $.get(GITLAB_MR_URL).then(function(res) {
    var submissions = [];

    res.forEach(function(MR) {
      var arr = escapeHtml(MR.title).split(' - ');
      var title;

      if (arr.length < 3) return;

      if (arr.length > 3) {
        title = arr.splice(0, 2);
        title.push(arr.join(' - '));
      } else {
        title = arr
      }

      var number = String('000' + title[0]).slice(-3);

      submissions.push({
        number: number,
        author: title[1],
        project: title[2],
        previewUrl: 'https://deploy-preview-' + MR.iid + '--' + netlifyRootUrl
                 + '/hibahcme/' + number,
      });
    });

    submissions.sort(function(a, b) { return b.number - a.number })

    return submissions;
  });
}

function escapeHtml(string) {
  return $('<div>').text(string).html();
}

$(function() {
  var $submissionsEl = $('#submission');
  var $submissionTbody = $submissionsEl.find('tbody');
  var $loading = $('#loading');

  if (!netlifyRootUrl) {
    return console.error(
      "No Netlify environment variables, cannot get repository url"
    );
  }

  fetchSubmissions().then(function(submissions) {
    $submissionsEl.removeClass('hidden');
    $loading.hide();

    submissions.forEach(function(submission) {
      $submissionTbody.append(submissionTemplate(submission));
    });
  });
});
