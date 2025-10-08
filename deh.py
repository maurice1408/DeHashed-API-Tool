# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests==2.31.0",
#   "pydantic==2.10.5",
#   "polars==1.18.0",
#   "altair==5.5.0",
#   "marimo",
# ]
# ///

import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium", app_title="DeHashed")

with app.setup:


    # Initialization code that runs before all other cells
    pass


@app.cell
def _():
    import marimo as mo
    import requests

    import hashlib
    import polars as pl
    from pydantic import BaseModel, Field
    from typing import Optional, List

    import urllib.parse

    import asyncio

    # api_key = "wAHd3cTDijZItfXV2wYJLNYypfFgHrjedUBvpK6owbUVLhqWkPDOqnI="
    return BaseModel, Field, hashlib, mo, pl, requests


@app.cell
def _(conv_to_str, mo, pl):
    def disply_res(results):
        df = pl.DataFrame(results)
        df_str = conv_to_str(df)
        y = mo.ui.table(df_str, selection="multi")
        # s = y.value

        return y
    return (disply_res,)


@app.cell
def _(api_key, requests):
    async def v2_search(
        query: str,
        page: int,
        size: int,
        wildcard: bool,
        regex: bool,
        de_dupe: bool,
    ) -> dict:
        qry = {
            "query": query,
            "page": page,
            "size": size,
            "wildcard": wildcard,
            "regex": regex,
            "de_dupe": de_dupe,
        }

        res = requests.post(
            "https://api.dehashed.com/v2/search",
            json=qry,
            headers={
                "Content-Type": "application/json",
                "DeHashed-Api-Key": api_key,
            },
        )
        return res.json()
    return (v2_search,)


@app.cell
def _(api_key, hashlib, requests):
    def get_sha256(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()


    def v2_search_password(password: str) -> dict:
        sha256_hash = get_sha256(password)
        res = requests.post(
            "https://api.dehashed.com/v2/search-password",
            json={
                "sha256_hashed_password": sha256_hash,
            },
            headers={
                "Content-Type": "application/json",
                "DeHashed-Api-Key": api_key,
            },
        )
        return res.json()
    return


@app.cell
def _(mo):
    def show_resp(rsp, srch):
        # print("In function show_resp")
        # print(type(rsp))
        # print(rsp.keys())

        if "error" in rsp.keys():
            return mo.callout(
                f"""
                Error: {rsp["error"]}
                """,
                kind="warn",
            )
        else:
            # return mo.md(f"""
            #    The search against **{srch}** returned
            #    **{len(rsp["entries"])}** entries in **{rsp["took"]}**,
            #    you have a remaining balance of **{rsp["balance"]}** API calls.
            #    """
            srch_term = mo.stat(label="Search Term", value=srch)
            srch_ent = mo.stat(label="Entries Returned", value=len(rsp["entries"]))
            srch_time = mo.stat(label="Execution Time", value=rsp["took"])
            # srch_bal = mo.stat(label="API Balance", value=rsp["balance"])

            return mo.hstack(items=[srch_term, srch_ent, srch_time])
    return (show_resp,)


@app.cell
def _(BaseModel, Field):
    class Dehashed(BaseModel):
        id: str
        email: list = Field(default_factory=list)
        ip_address: list = Field(default_factory=list)
        username: list = Field(default_factory=list)
        password: list = Field(default_factory=list)
        hashed_password: list = Field(default_factory=list)
        name: list = Field(default_factory=list)
        dob: list = Field(default_factory=list)
        license_plate: list = Field(default_factory=list)
        address: list = Field(default_factory=list)
        phone: list = Field(default_factory=list)
        company: list = Field(default_factory=list)
        url: list = Field(default_factory=list)
        social: list = Field(default_factory=list)
        cryptocurrency_address: list = Field(default_factory=list)
        database_name: str
    return (Dehashed,)


@app.cell
def _(pl):
    def conv_to_str(df):
        """DeHashed returns data elemets as Lists.

        This function converts the Lists to Strings
        """

        join_str = " / "

        return df.with_columns(
            pl.col("email").cast(pl.List(pl.String)).list.join(join_str),
            pl.col("ip_address").cast(pl.List(pl.String)).list.join(join_str),
            pl.col("username").cast(pl.List(pl.String)).list.join(join_str),
            pl.col("password").cast(pl.List(pl.String)).list.join(join_str),
            pl.col("hashed_password").cast(pl.List(pl.String)).list.join(join_str),
            pl.col("name").cast(pl.List(pl.String)).list.join(join_str),
            pl.col("dob").cast(pl.List(pl.String)).list.join(join_str),
            pl.col("license_plate").cast(pl.List(pl.String)).list.join(join_str),
            pl.col("address").cast(pl.List(pl.String)).list.join(join_str),
            pl.col("phone").cast(pl.List(pl.String)).list.join(join_str),
            pl.col("company").cast(pl.List(pl.String)).list.join(join_str),
            pl.col("url").cast(pl.List(pl.String)).list.join(join_str),
            pl.col("social").cast(pl.List(pl.String)).list.join(join_str),
            pl.col("cryptocurrency_address")
            .cast(pl.List(pl.String))
            .list.join(join_str),
        )
    return (conv_to_str,)


@app.cell
def _(mo):
    mo.md(
        r"""
    # DeHashed Search

    ## Introduction

    This notebook will allow you to enter a search phrase against [DeHashed](https://app.dehashed.com/search)

    The results will be returned in a Polars DataFrame. The Marimo UI on the DataFrame will allow you to, search, sort and download the returned data.

    Expand the "Instructions" below for usage help.
    """
    )
    return


@app.cell
def _(mo):
    mo.accordion(

        {"Instructions": mo.md(f"""
    Specific attributes may be searched for by prefixing the search value with the attribute name e.g.

    ```
    username:maurice1408
    ```

    Attributes that can be searched for are

    1. email
    2. username
    3. ip_address
    4. name
    5. address
    6. phone
    7. vin
    8. domain
    9. database_name

    It is possible to combine multiple operators - separated with an & - in one search (criteria are AND'd) e.g.

    ```
    email:maurice1408@gmail.com&username:maurice1408
    ```

    To use wildcards or regular expressions in the search value, click the corresponding radio button.

    For reference see the DeHashed documentation at [Search Guide](https://app.dehashed.com/documentation/search-guide)

    /// note | Note 

    _not_ all elements in each row will be populated, it will depend on the search results.
    ///
    """
    )})
    return


@app.cell
def _(mo):
    key=mo.ui.text(label="DeHashed API Key", value="wAHd3cTDijZItfXV2wYJLNYypfFgHrjedUBvpK6owbUVLhqWkPDOqnI=")
    key
    return (key,)


@app.cell
def _(key):
    api_key = key.value
    return (api_key,)


@app.cell
def _(mo):
    res_slider = mo.ui.slider(start=0, 
                              stop=10000, 
                              step=1000, 
                              value=1000, 
                              show_value=True,
                              label="Number of results to return"
                             )

    dedupe_check = mo.ui.checkbox(label="Dedupe search results", value=True)

    search_type = mo.ui.radio(
        options=["normal", "wildcard", "regexp"], value="normal", label="Choose Search Type"
    )
    return dedupe_check, res_slider, search_type


@app.cell
def _(dedupe_check, mo, res_slider, search_type):
    mo.vstack(align="center", items=[res_slider, dedupe_check, search_type])
    return


@app.cell
def _(mo):
    input_srch = mo.ui.text(
        label="Search for:", full_width=True, placeholder="Enter search text and hit Enter ↩️ or tab ⇥"
    )
    input_srch
    return (input_srch,)


@app.cell
def _(input_srch):
    if len(input_srch.value.strip()) > 0: 
        srch = input_srch.value
    return (srch,)


@app.cell
def _(search_type):
    rexexp = False
    wildcard = False

    match search_type.value:
        case "normal":
            regexp=False
            wildcard=False
        case "wildcard":
            regexp=False
            wildcard=True
        case "regexp":
            regexp=True
            wildcard=False
    return regexp, wildcard


@app.cell
async def _(
    dedupe_check,
    input_srch,
    mo,
    regexp,
    res_slider,
    srch,
    v2_search,
    wildcard,
):
    # response = v2_search_password(pwd.value)
    _output = None

    response = {}

    if len(input_srch.value.strip()) > 0: 
        with mo.status.spinner(title="searching...") as _spinner:
            response = await v2_search(
                srch, 1, res_slider.value, wildcard, regexp, dedupe_check.value
            )
            _spinner.update("Done")



    _output
    return (response,)


@app.cell
def _(input_srch, mo, response, show_resp, srch):
    _op = None

    if len(input_srch.value.strip()) > 0: 
        _stat = show_resp(response, srch)
        if _bal := response.get("balance"):
            if _bal < 100:
                _callout = mo.callout(
                    f"Low API credit balance: {_bal}", kind="warn"
                )
            else:
                _callout = mo.callout(
                    f"Balance is {_bal} API credits", kind="info"
                )
        else:
            _callout = mo.callout("no balance returned", kind="warn")

        _op = mo.vstack(items=[_stat, _callout])
    _op
    return


@app.cell
def _(Dehashed, input_srch, response):
    l = []
    if len(input_srch.value.strip()) > 0: 
        if "entries" in response.keys() and len(response["entries"]) > 0:
            for i in range(len(response["entries"])):
                m = Dehashed.model_validate(response["entries"][i])
                l.append(m)
    return (l,)


@app.cell
def _(l, pl):
    df = pl.DataFrame(l)
    return (df,)


@app.cell
def _(df, input_srch, pl):
    tbl = None
    if len(input_srch.value.strip()) > 0: 
        df_str = df.with_columns(
                pl.col("email").cast(pl.List(pl.String)).list.join(", "),
                pl.col("ip_address").cast(pl.List(pl.String)).list.join(", "),
                pl.col("username").cast(pl.List(pl.String)).list.join(", "),
                pl.col("password").cast(pl.List(pl.String)).list.join(", "),
                pl.col("hashed_password").cast(pl.List(pl.String)).list.join(", "),
                pl.col("name").cast(pl.List(pl.String)).list.join(", "),
                pl.col("dob").cast(pl.List(pl.String)).list.join(", "),
                pl.col("license_plate").cast(pl.List(pl.String)).list.join(", "),
                pl.col("address").cast(pl.List(pl.String)).list.join(", "),
                pl.col("phone").cast(pl.List(pl.String)).list.join(", "),
                pl.col("company").cast(pl.List(pl.String)).list.join(", "),
                pl.col("url").cast(pl.List(pl.String)).list.join(", "),
                pl.col("social").cast(pl.List(pl.String)).list.join(", "),
                pl.col("cryptocurrency_address").cast(pl.List(pl.String)).list.join(", ")
            )

        # tbl = mo.ui.table(df_str, selection="multi")

    tbl
    return


@app.cell
def _(disply_res, input_srch, l):
    r = None

    if len(input_srch.value.strip()) > 0: 
        r = disply_res(l)

    r
    return (r,)


@app.cell
def _(l, r):
    v = None
    if len(l):
        v = r.value
    v
    return


if __name__ == "__main__":
    app.run()
