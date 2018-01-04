#!/bin/bash

build() {
  jekyll build
  exit
}

if [[ "$CONTEXT" == "production" ]]; then
  build
fi

GITLAB_PREFIX="git@gitlab.com:"
REPO_SLUG=${REPOSITORY_URL#$GITLAB_PREFIX}
REPO_SLUG=${REPO_SLUG/\//"%2F"}

GITLAB_COMMIT_API="https://gitlab.com/api/v4/projects/$REPO_SLUG/repository/commits/$COMMIT_REF"
GITLAB_DIFF_API="$GITLAB_COMMIT_API/diff"

# Get commit information
COMMIT=$(curl --fail -sS $GITLAB_COMMIT_API) || exit

if [[ "$COMMIT" == *"[full-build]"* ]]; then
  echo "Commit message contains [full-build] keyword; Doing full build ..."
  build
fi

# List all modified files in the commit
MODIFIED_FILES=$(curl --fail -sS $GITLAB_DIFF_API | \
python3 -c "import sys, json; \
print(' '.join(list(map(lambda x: x['new_path'], json.load(sys.stdin)))))") \
|| exit

echo "Fast build mode"
echo "Removing: $PATH_TO_EXCLUDE"
echo "These committed file(s) are not removed:"

tar -cvf modified.tar $MODIFIED_FILES; echo
rm -rf $PATH_TO_EXCLUDE
tar -xf modified.tar
rm modified.tar

build
