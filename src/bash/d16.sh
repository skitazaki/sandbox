#!/bin/sh
# Sets up 'git' environments and alias.
# see https://git.wiki.kernel.org/index.php/Aliases
# example:
# $ GIT_NAME="KITAZAKI Shigeru" GIT_MAIL="skitazaki@gmail.com" sh d16.sh

gitconfig="git config --global"

[ -n "$GIT_NAME" ] && $gitconfig user.name  "$GIT_NAME"
[ -n "$GIT_MAIL" ] && $gitconfig user.email "$GIT_MAIL"

$gitconfig color.ui auto

$gitconfig alias.a "add -u"
$gitconfig alias.alias "!sh -c '[ \$# = 2 ] && \
git config --global alias.\"\$1\" \"\$2\" && exit 0 || \
echo \"usage: git alias <new alias> <original command>\" >&2 && exit 1' -"
$gitconfig alias.amend "commit --verbose --amend"
$gitconfig alias.ci "commit --verbose"
$gitconfig alias.co "!sh -c '[ \$# = 1 ] && git checkout \"\$1\" && exit 0 || \
echo \"specify one of branch name:\" >&2 && git branch && exit 1' -"
$gitconfig alias.df "diff --cached"
$gitconfig alias.di "diff --color -U1" # show whitespaces
$gitconfig alias.i "add -p" #interactive
$gitconfig alias.st status
$gitconfig alias.unstage "reset HEAD"

$gitconfig core.autocrlf false
$gitconfig core.excludesfile $HOME/.git-excludes
[ -f $HOME/.git-excludes ] || cat <<EOT >$HOME/.git-excludes
*~
*.swp
EOT
$gitconfig core.editor vim
$gitconfig core.quotepath false
$gitconfig core.whitespace "-blank-at-eof"

# experimental
[ -n "$IMAP_HOST" ] && $gitconfig imap.host "$IMAP_HOST"
[ -n "$IMAP_PORT" ] && $gitconfig imap.port "$IMAP_PORT"
[ -n "$IMAP_USER" ] && $gitconfig imap.user "$IMAP_USER"
[ -n "$IMAP_PASS" ] && $gitconfig imap.pass "$IMAP_PASS"
[ -n "$IMAP_FOLDER" ] && $gitconfig imap.folder "$IMAP_FOLDER"

echo "updated config file:" $HOME/.gitconfig
echo "committer: " `git var GIT_COMMITTER_IDENT`
echo "author:    " `git var GIT_AUTHOR_IDENT`
echo "to see full variables, type following:"
echo "    git var -l"

