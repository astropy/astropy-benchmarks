#!/opt/local/bin/zsh
export PATH=~/bin:$PATH
source ~/.zshrc
git checkout master
git pull
asv run NEW
asv run MISSING --steps=10
git add -A
git commit -m "New results"
git push origin master
asv gh-pages
