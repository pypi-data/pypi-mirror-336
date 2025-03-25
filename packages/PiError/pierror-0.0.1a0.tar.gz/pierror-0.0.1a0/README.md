# PiError

PiError is an attempt at simplifying Python error propagation.
This Python package follows the "Errors as Values" principle giving the user
control of how errors are stored, used, and raised without worrying about
immediate runtime crashes. It takes a very simple approach, which may already
be boilerplate for some but may aide in simplifying ones code base. The best
part about it, is that there are no dependencies.

---

## Installation
<details open>
<summary><strong>Pip</strong></summary>

```bash
# Create a virtual environment
python3 -m venv ~/venv-name

# Activate the virtual environment
source "~/venv-name/bin/activate"

# Upgrade pip
~/venv-name/bin/pip install --upgrade pip

# Install PiError package
~/venv-name/bin/pip install PiError
```
</details>

<details>
<summary><strong>Uv</strong> <i>(<strong>Recommended</strong>)</i></summary>

```bash
# Create virtual environment
uv venv ~/venv-name

# Activate virtual environment
source ~/venv-name/bin/activate

# Upgrade pip
uv pip install --upgrade pip

# Install PiError
uv pip install PiError
```
</details>

Copy the following code below into your text editor to see how it works:
```python3
from PiError import PiError

@PiError({0: {int}, 1: {int}}, TypeError, "'x' and 'y' should be of type 'int'")
def addition(x: int, y: int) -> PiError | int:
    return x + y

result = addition('a', 1)
if type(result) is PiError:
    raise result.error(result.cause)
else:
    print(result)
```





