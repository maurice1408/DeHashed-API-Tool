# Running from github

1. Open a terminal window

2. Make sure you have the `uv` command installed, if not then you
   can install it using either:

   a) if you are a Homebrew user

   ```
   brew install uv
   ```

   b) Otherwise, from a terminal window use the command:

   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   Verify that `uv` is installed using the command

   ```
   uv --version
   ```

   Which should return something like this:

   ```
   uv --version
   uv 0.8.24 (252f88733 2025-10-07)
   ```

2. Then to load the DeHashed marimo notebook issue the
   `uvx` command below:

```
 uvx marimo run --sandbox  https://raw.githubusercontent.com/maurice1408/DeHashed-API-Tool/refs/heads/main/deh.py
```

The notebook should open in a browser window.

To end the session, close the browser window and terminate the
`uvx` command by `Ctrl+c` in the terminal window.


