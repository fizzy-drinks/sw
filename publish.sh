if which python3 > /dev/null && which twine > /dev/null; then
  python3 setup.py sdist bdist_wheel && \
    twine upload dist/*
else
  echo "Publishing requires python3 and twine!"
fi
