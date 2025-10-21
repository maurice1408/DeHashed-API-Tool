# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests>=2.31.0",
#   "pydantic>=2.10.5",
#   "polars>=1.18.0",
#   "altair>=5.5.0",
#   "marimo",
#   "python-dotenv==1.1.1",
#   "logfire",
# ]
# ///

import marimo

__generated_with = "0.17.0"
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
    from pydantic import BaseModel, Field, BeforeValidator
    from typing import Optional, List, Any, Annotated

    from dotenv import dotenv_values

    from dataclasses import dataclass

    import urllib.parse

    import asyncio

    import logfire

    # api_key = "wAHd3cTDijZItfXV2wYJLNYypfFgHrjedUBvpK6owbUVLhqWkPDOqnI="
    return (
        Annotated,
        Any,
        BaseModel,
        BeforeValidator,
        dataclass,
        dotenv_values,
        hashlib,
        logfire,
        mo,
        pl,
        requests,
    )


@app.cell
def _(dataclass, dotenv_values, logfire):
    env_settings = dotenv_values(".env")


    @dataclass
    class Settings:
        deh_api_key: str = env_settings["deh_api_key"]
        logfire_token: str = env_settings["logfire_token"]
        low_balance_alert: int = env_settings["low_balance_alert"]


    settings = Settings()

    logfire.configure(token=settings.logfire_token, service_name="deh")
    logfire.info("Session initialised")
    return (settings,)


@app.cell
def _(mo, pl):
    def disply_res(results):
        df = pl.DataFrame(results)
        # df_str = conv_to_str(df)
        y = mo.ui.table(
            df,
            show_data_types=False,
            selection="multi",
        )
        # s = y.value

        return y
    return (disply_res,)


@app.cell
def _(api_key, logfire, requests):
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

        logfire.debug("Query: {query=!r}", query=qry)

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
def _(Response, logfire, pl, settings):
    def show_resp(rsp, srch):
        # print("In function show_resp")
        # print(type(rsp))
        # print(rsp.keys())

        responses = []

        for i, r in enumerate(rsp):
            # print(i)
            # print(r)

            if "error" in r.keys():
                d = {"search": srch[i], "error": r["error"]}
                logfire.error("Error: {error}", error=r["error"])
            else:
                d = {
                    "search": srch[i],
                    "balance": r["balance"],
                    "took": r["took"],
                    "total": r["total"],
                    "error": "",
                }
                logfire.info(
                    "Results - Search: {search}, total: {total}, balance: {balance}",
                    search=srch[i],
                    total=r["total"],
                    balance=r["balance"],
                )

                if int(r["balance"]) < int(settings.low_balance_alert):
                    logfire.warning(
                        "Balance is low: {balance}", balance=int(r["balance"])
                    )

            responses.append(Response.model_validate(d))

        return pl.DataFrame(responses)

        #        return mo.callout(
        #         f"""
        #         Error: {rsp["error"]}
        #         """,
        #         kind="warn",
        #     )
        # else:
        # return mo.md(f"""
        #    The search against **{srch}** returned
        #    **{len(rsp["entries"])}** entries in **{rsp["took"]}**,
        #    you have a remaining balance of **{rsp["balance"]}** API calls.
        #    """
        #     srch_term = mo.stat(label="Search Term", value=srch)
        #     srch_ent = mo.stat(label="Entries Returned", value=len(rsp["entries"]))
        #     srch_time = mo.stat(label="Execution Time", value=rsp["took"])
        #     # srch_bal = mo.stat(label="API Balance", value=rsp["balance"])

        #     return mo.hstack(items=[srch_term, srch_ent, srch_time])
    return (show_resp,)


@app.cell
def _(Annotated, Any, BaseModel, BeforeValidator):
    def ensure_string(value: Any) -> Any:
        if isinstance(value, list):
            return " ".join(value)
        else:
            return value


    class Dehashed(BaseModel):
        search_value: str = ""
        id: str
        email: Annotated[str, BeforeValidator(ensure_string)] = None
        ip_address: Annotated[str, BeforeValidator(ensure_string)] = None
        username: Annotated[str, BeforeValidator(ensure_string)] = None
        password: Annotated[str, BeforeValidator(ensure_string)] = None
        hashed_password: Annotated[str, BeforeValidator(ensure_string)] = None
        name: Annotated[str, BeforeValidator(ensure_string)] = None
        dob: Annotated[str, BeforeValidator(ensure_string)] = None
        license_plate: Annotated[str, BeforeValidator(ensure_string)] = None
        address: Annotated[str, BeforeValidator(ensure_string)] = None
        phone: Annotated[str, BeforeValidator(ensure_string)] = None
        company: Annotated[str, BeforeValidator(ensure_string)] = None
        url: Annotated[str, BeforeValidator(ensure_string)] = None
        social: Annotated[str, BeforeValidator(ensure_string)] = None
        cryptocurrency_address: Annotated[str, BeforeValidator(ensure_string)] = (
            None
        )
        database_name: str


    class Response(BaseModel):
        search: str = ""
        balance: int = 0
        took: str = ""
        total: int = 0
        error: str = ""
    return Dehashed, Response


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    # DeHashed Search

    ## Introduction

    This notebook will allow you to enter a search phrase against [DeHashed](https://app.dehashed.com/search)

    The input search term can be one or _multiple_ search terms (separated by ';'). You can also use a file of search terms (one search term per line) by dragging the file to the input file area.

    The results will be returned in a table. The Marimo UI on the table will allow you to, search, sort and download the returned data.

    Expand the "Instructions" below for usage help.
    """
    )
    return


@app.cell
def _(mo):
    mo.accordion(
        {
            "Instructions": mo.md(f"""
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
    """)
        }
    )
    return


@app.cell
def _(mo, settings):
    key = mo.ui.text(
        kind="password",
        label="DeHashed API Key",
        value=settings.deh_api_key,
    )

    key
    return (key,)


@app.cell
def _(key):
    api_key = key.value
    return (api_key,)


@app.cell
def _(mo):
    res_slider = mo.ui.slider(
        start=0,
        stop=10000,
        step=1000,
        value=1000,
        show_value=True,
        label="Number of results to return",
    )

    dedupe_check = mo.ui.checkbox(label="Dedupe search results", value=True)

    search_type = mo.ui.radio(
        options=["normal", "wildcard", "regexp"],
        value="wildcard",
        label="Choose Search Type",
    )
    return dedupe_check, res_slider, search_type


@app.cell
def _(dedupe_check, mo, res_slider, search_type):
    mo.vstack(align="center", items=[res_slider, dedupe_check, search_type])
    return


@app.cell
def _(mo):
    input_srch = mo.ui.text(
        label="Search for:",
        full_width=True,
        debounce=True,
        placeholder="Enter search text (separate multiple search values with ';') and hit Enter ↩️ or tab ⇥",
    )

    fileup = mo.ui.file(kind="area", label="Drag input file here")

    input_area = mo.vstack([input_srch, fileup])

    input_area
    return fileup, input_srch


@app.cell
def _(fileup, input_srch, logfire, mo):
    srch = []

    try:
        if len(input_srch.value.strip()) > 0:
            srch = [n.strip() for n in input_srch.value.split(";")]

            logfire.info("Search: {input}", input=";".join(srch))

        else:
            if len(fileup.contents()):
                srch = [i.decode() for i in fileup.contents().split(b"\n")[:-1]]
                logfire.info(
                    "filename: {filename}, entries: {entries}",
                    filename=fileup.name(),
                    entries=len(srch),
                )
    except TypeError:
        mo.stop(1 == 1)
    return (srch,)


@app.cell
def _(search_type):
    rexexp = False
    wildcard = False

    match search_type.value:
        case "normal":
            regexp = False
            wildcard = False
        case "wildcard":
            regexp = False
            wildcard = True
        case "regexp":
            regexp = True
            wildcard = False
    return regexp, wildcard


@app.cell
async def _(
    dedupe_check,
    logfire,
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

    response_list = []

    if len(srch):
        with logfire.span("Processing {cnt} searches", cnt=(len(srch))):
            for s in srch:
                with mo.status.spinner(title="searching...") as _spinner:
                    response = await v2_search(
                        s,
                        1,
                        res_slider.value,
                        wildcard,
                        regexp,
                        dedupe_check.value,
                    )
                    _spinner.update("Done")

                response_list.append(response)
            logfire.info("Finished")

    _output
    return (response_list,)


@app.cell
def _(mo, res_slider, response_list, show_resp, srch):
    _op = None

    if len(response_list) > 0:  # len(input_srch.value.strip()) > 0:
        _hdr = mo.md("## Search Summary").center()
        _summary = show_resp(response_list, srch)

        # if _bal := response.get("balance"):
        #     if _bal < 100:
        #         _callout = mo.callout(
        #             f"Low API credit balance: {_bal}", kind="warn"
        #         )
        #     else:
        #         _callout = mo.callout(
        #             f"Balance is {_bal} API credits", kind="info"
        #         )
        # else:
        #     _callout = mo.callout("no balance returned", kind="warn")

        # _op = mo.vstack(items=[_stat, _callout])

        _op = mo.vstack(
            [
                _hdr,
                mo.ui.table(
                    _summary,
                    show_data_types=False,
                    header_tooltip={
                        "balance": "DeHashed API Credits Remaining",
                        "took": "Query milliseconds",
                        "total": f"Total results available limited by slider to {res_slider.value}",
                    },
                ),
            ]
        )

    _op
    return


@app.cell
def _(Dehashed, response_list, srch):
    detail_list = []

    if len(response_list) > 0:
        for _s, _r in enumerate(response_list):
            if "entries" in _r.keys() and len(_r["entries"]) > 0:
                for i in range(len(_r["entries"])):
                    d = {"search_value": srch[_s]}
                    d.update(_r["entries"][i])
                    m = Dehashed.model_validate(d)
                    detail_list.append(m)
    return (detail_list,)


@app.cell
def _(detail_list, disply_res, mo, response_list):
    r = None

    try:
        if len(response_list) > 0:
            if len(detail_list) > 0:
                r = mo.vstack(
                    [mo.md("## Search Detail").center(), disply_res(detail_list)]
                )
            else:
                r = mo.md(f"No results found")
    except:
        pass

    r
    return (r,)


@app.cell
def _(l, r):
    v = None

    try:
        if len(l):
            v = r.value
    except:
        pass
    v
    return


if __name__ == "__main__":
    app.run()
