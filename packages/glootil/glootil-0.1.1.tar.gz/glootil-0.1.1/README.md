# Glootil

A Python 3 library to create [gloodata](https://gloodata.com) extensions.

## Usage

```sh
mkdir gd-finances
cd gd-finances
uv init
uv add glootil uvicorn fastapi
```

edit `main.py` to contain:

```python
from datetime import datetime
from glootil import DynEnum, Toolbox

tb = Toolbox(
    "finances",
    "Finances",
    "Provides tools to do financial calculations",
)


@tb.tool(
    name="Compound Interest Rate Calculator",
    ui_prefix="Compound Interest Rate",
    args={
        "principal": "Principal",
        "interest_rate": "Interest Rate",
        "years": "Years",
    },
    examples=[
        "calculate compound interest for initial 1500 dollars, 2.5% interests for 8 years"
    ],
)
def compound_interest_calculator(
    principal: float = 1.0, interest_rate: float = 3.0, years: int = 5
):
    cols = [("year", "Year"), ("amount", "$")]
    val_cols = ["amount"]
    year = datetime.now().year
    amount = principal
    rows = []

    for i in range(0, years + 1):
        rows.append((year + i, amount))
        amount += amount * (interest_rate / 100)

    return {
        "type": "Series",
        "title": "Compound Interest by Year",
        "xColTitle": "Year",
        "yColTitle": "$",
        "xCol": "year",
        "valCols": val_cols,
        "cols": cols,
        "rows": rows,
    }


tb.serve(port=8087)
```

Start:

```sh
uv run main.py
```

On gloodata write in the prompt bar:

> Add extension Fincance at port 8087

Click `Test` and then `Save`

Now in the prompt bar write something like:

> calculate compound interest for initial 2500 dollars, 3.5% interests for 15 years


## License

MIT, see LICENSE file for details
