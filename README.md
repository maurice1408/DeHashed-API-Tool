# Running from github

1. Open a terminal window

2. Make sure you have the `uv` command installed, if not then you
   can install it on your Mac using either:

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
   uv 0.9.26 (ee4f00362 2026-01-15)
   ```

3. Create a directory and an environment file using the commands

   ```
   mkdir ./deh
   cd ./deh
   echo -e 'deh_api_key = "9n7d1t3A+WlqnaSQ9RFHAr28BF7lF8ScGSTO6ok0DwcVgpKBiD1jeg=="\nlogfire_token = "pylf_v1_eu_CBXVK697GrxCT11jysbwN6DTJH52GXZ3JsNLNghnWnp1"\nlow_balance_alert = 1500' > ./.env
   ```

4. Then to load the DeHashed marimo notebook issue the
   `uvx` command below:

   ```
   uvx marimo run --sandbox --trusted https://raw.githubusercontent.com/maurice1408/DeHashed-API-Tool/refs/heads/main/deh.py
   ```

The notebook should open in a browser window.

To end the session, close the browser window and terminate the
`uvx` command by `Ctrl+c` in the terminal window (respond 'y').

In subsequent invocations, you can skip Step 2 a,d simply `cd` to
the directory you created in Step 3, and then execute the `uvx`
command given in Step 4.


