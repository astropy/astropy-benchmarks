#!/opt/local/bin/zsh
export PATH=~/bin:$PATH
source ~/.zshrc
git checkout master
git pull
asv run NEW
git add -A
git commit -m "New results"
git push origin master
asv gh-pages
