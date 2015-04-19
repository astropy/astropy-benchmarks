#!/opt/local/bin/zsh
export PATH=~/bin:$PATH
source ~/.zshrc
cd astropy
git fetch origin
git reset --hard origin/master
cd ..
git checkout master
git pull
asv run NEW
git add -A
git commit -m "New results"
git push origin master
asv gh-pages
