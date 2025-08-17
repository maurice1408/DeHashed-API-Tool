# DeHashed Client

A small Marimo Notebook that acts as a browser based client for
DeHashed.

In an attempt to avoid Python "dependency hell" the client runs
through the 'uv` package manager.

Install `uv` on your mac using the command:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

or if you are more comfortable using Homebrew then ...

```bash
brew install uv
```

if `uv` installs successfully then the command uv --version
should give you something along the lines of...

```bash
uv --version 
uv 0.7.12 (dc3fd4647 2025-06-06)
```

Create a new directory e.g. `mkdir deh` cd to that directory `cd
deh` and copy the attached `deh.py` file into that directory.

From that directory issue the command

```bash
uvx marimo run --sandbox deh.py
```

That should open up the search tool in your browser. 

From there you should be able to enter a search term in the Enter
search text input field then click on the **Go!** button to execute
the search. The results should appear in the table below.  

The 2 icons at the bottom left of the results table let you:

1. Search the results
2. Toggle the row viewer that will appear to the right of the
   table

Selecting rows (checkbox to left of row) will populate rows in
the table below the main results table. So selecting rows can be
used to bookmark rows of interest.

Either table can be downloaded or copied to the clipboard using the
`Download` at the bottom right of either table.

To shutdown the app:

1. Close the web page
2. Back in the terminal hit Ctrl(⌘)+c to terminate the Marimo
   server.

Hopefully you will not hit any issues that highlight dependencies
on my environment!  Let me know how it goes and / or any
questions or suggestions!
