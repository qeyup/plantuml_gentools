# Overview

PlantUML gen Tools 

# To upload to pypi

```bash
python3 setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

> **url:** https://packaging.python.org/tutorials/packaging-projects/