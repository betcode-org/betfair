rm -r build
rm -r dist
rm -r betfairlightweight.egg-info

python setup.py sdist bdist_wheel

twine upload dist/*
