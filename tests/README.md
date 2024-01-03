Test test.PyPi artifact

```bash
mkdir tmp
python -m venv .
source bin/activate
pip install -i https://test.pypi.org/simple/ ncpeek --extra-index-url=https://pypi.org/simple
```
