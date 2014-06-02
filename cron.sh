#!/opt/local/bin/zsh
source ~/.zshrc
git checkout master
asv run NEW
git add -A
git commit -m "New results"
git push origin master
asv gh-pages
