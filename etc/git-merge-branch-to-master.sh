git checkout main

git reset --hard 1a11628d22b7f1b3d2dc58add4be4e065263358a

git reset --hard f414f31
git reset --soft HEAD@{1}
git commit -m "Reverting to the state of the project at 1a11628d22b7f1b3d2dc58add4be4e065263358a"
git push


git clone git@git.noc.ruhr-uni-bochum.de:thomaswoehlke/flask-covid19.git flask-covid19-branch-merging-part2

git fetch
git status
git tag
git branch -va

git checkout main
git merge --no-ff --no-commit REFACTORING_2021_05_20_START



git config pull.rebase false
git submodule init
cd data
git push --set-upstream origin main


git submodule update --remote --merge
