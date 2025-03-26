# decimal-binary-converter
Python packge for converting decimal numbers into binary.

This package is used to provide an example of how to create a Python package. ✨

---

### How to make the package available 🙌

If necessary, use a virtual environment:
1. Add the virtual environment to the `.gitignore` file by writing `<name-of-venv>/`.
2. Set up the virtual environment using: `python -m venv <name-of-venv>`.
3. Activate the virtual environment using: `venv/Scripts/activate` (Windows).


Run the following commands:
1. Install dependencies using: `pip install setuptools build wheel twine`.
2. Build source code and binary distribution wheel using: `python -m build`.
3. A: Upload the distribution wheel to the Test Python Package Index using: `twine upload --repository testpypi dist/*`. (Requires an API Key. Get it by [registering an account](https://test.pypi.org/manage/unverified-account/?next=%2Fmanage%2Faccount%2F#api-tokens)).
4. B: Upload the distribution wheel to the Python Package Index using: `twine upload dist/*`.
5. Install the package using `pip install <your-package>`.

---

### Details 🔎

In the `__init__.py` file, we leave it non-empty to make it easier to import stuff from the pacakge.
- Instead of having to write `from decimal_binary_converter.converter import decimal_to_binary` when importing,
- We can write `from decimal_binary_converter import decimal_to_binary`.

