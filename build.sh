rm -r build
rm -r dist
rm -r betfairlightweight.egg-info

python3 setup.py sdist bdist_wheel

twine upload dist/*

mkdocs gh-deploy
