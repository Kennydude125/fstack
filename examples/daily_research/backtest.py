"""Invented long-only daily mechanics case. No claim of historical or future alpha."""

import argparse
import csv
from decimal import Decimal, getcontext
import json
from pathlib import Path

getcontext().prec = 28
D = Decimal


def calculate(rows, metadata):
    """Buy once at next session open after the first completed bar; hold to final close."""
    if len(rows) < 2:
        raise ValueError("At least two sessions required")
    cash, shares = D("10000"), D("0")
    fee_rate = D(str(metadata["cost_bps"])) / D("10000")
    costs, dividends = D("0"), D("0")
    equity = [cash]
    orders = []
    for index, row in enumerate(rows[1:], 1):
        shares *= D(row["split_ratio"])
        payment = shares * D(row["dividend"])
        cash += payment
        dividends += payment
        if index == 1:
            shares = cash / (D(row["open"]) * (D("1") + fee_rate))
            cost = shares * D(row["open"]) * fee_rate
            costs += cost
            cash = D("0")
            orders.append({"signal_available_at": rows[0]["available_at"],
                           "execute_at": metadata["sessions"][index]["open_at"],
                           "execution_price": row["open"]})
        equity.append(cash + shares * D(row["close"]))
    terminal = equity[-1]
    return {"currency": metadata["currency"], "initial_equity": "10000", "final_equity": str(terminal),
            "return": str(terminal / D("10000") - D("1")), "transaction_cost": str(costs),
            "cash_dividends": str(dividends), "orders": orders,
            "equity": [str(value) for value in equity], "price_basis": "raw",
            "limitations": "Synthetic development illustration. Fractional shares; cash dividends credited at supplied event date; no reinvestment or terminal sale; no liquidity, taxes, FX or real-market inference."}


def self_check(result, market):
    expected = D("11200") / (D("102") * D("1.001")) * D("100") if market == "US" else D("22400") / (D("204") * D("1.001")) * D("100")
    if abs(D(result["final_equity"]) - expected) > D("0.00000001"):
        raise AssertionError("Split/dividend/cost golden calculation disagrees")
    if not D(result["transaction_cost"]) > 0:
        raise AssertionError("Declared transaction costs were not deducted")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv")
    parser.add_argument("metadata")
    parser.add_argument("output")
    args = parser.parse_args()
    with Path(args.csv).open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    metadata = json.loads(Path(args.metadata).read_text(encoding="utf-8"))
    result = calculate(rows, metadata)
    self_check(result, metadata["market"])
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
