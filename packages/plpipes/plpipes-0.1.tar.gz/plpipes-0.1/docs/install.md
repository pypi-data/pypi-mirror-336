

# Installing `plpipes`

The Python module `plpipes` can be installed in two ways:

## Installing a packed version

This is the way to install the module we recommend when you don't want
to contribute to the development of the framework and just want to use
it.

*Note that In practice, as `plpipes` is still in a very early
development stage, that may not be a realistic assumption and you may
be required to switch to the development version available from git
quite soon!*

Somehow (!) obtain the module wheel and install it using pip:

```bash
pip install /path/to/.../plpipes-0.1-py2.py3-none-any.whl
```

Hopefully, `plpipes` would be directly available from
[PyPI](https://pypi.org/) soon.

In the meantime, you can pack it yourself as follows:

### Packing `plpipes`

`plpipes` packing is handled with
[flit](https://flit.pypa.io/en/stable/) (which can be installed with
the usual `pip` command: `pip install flit`).

A python wheel file for `plpipes` is generated running the following
command from inside `plpipes` root directory:

```bash
flit build
```

The generated wheel file is placed inside `dist`. That file is a
standard (pure) Python package that can be installed in any operating
system as shown above.

## Installing from git

1. Clone the repository outside of your project directory and switch
    to the `develop` branch:

    ```bash
    git clone git@github.com:PredictLand/PL-TEC-PLPipes.git
    cd PL-TEC-PLPipes
    git checkout develop
    ```

2. Add the `src` subdirectory to Python search path:

    ```bash
    # Linux and/or bash:
    export PYTHONPATH=path/to/.../PL-TEC-PLPipes/src
    # Windows
    set PYTHONPATH=C:\path\to\...\PL-TEC-PLPipes\src
    ```

3. Check that it works:

    ```bash
    python -m plpipes -c "print('ok')"
    ```

Alternatively you can modify your project main script to append
the`src` directory to the module search path so that you don't need to
set `PYTHONPATH` by hand every time you start a new session.

For instance:

```python
from pathlib import Path
import sys
sys.path.append(str(Path.cwd().parent.parent.parent / "PL-TEC-PLPipes/src"))

from plpipes.runner import main
main()
```

Or you could also set `PYTHONPATH` from your shell startup script
(`~/.profile`) or in the Windows registry.

