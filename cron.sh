#!/opt/local/bin/zsh
source ~/.zshrc
git checkout master
asv run NEW
git commit -a -m "New results"
git push origin master
asv gh-pages
