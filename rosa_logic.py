"""Core computation logic extracted from Assignment1.ipynb.

Pure Python / NumPy only: no Streamlit imports and no user-interface code.
"""
import numpy as np
from starter import ZONES, TIME_BLOCKS, COSTS, PROMISE, delivery_times

SEED = 12


def _collect_times(zone, time_block, promised_time):
    """Gather delivery times for a zone/time block; either may be 'all'."""
    zones = ZONES if zone == "all" else [zone]
    blocks = TIME_BLOCKS if time_block == "all" else [time_block]
    return np.concatenate([
        delivery_times(z, tb, promised_time, seed=SEED)
        for z in zones for tb in blocks
    ])


def late_rate(zone, time_block, promised_time):
    """Percentage of orders delivered later than the promised time."""
    times = _collect_times(zone, time_block, promised_time)
    return round(float((times > promised_time).sum() / len(times) * 100), 2)


def average_delivery_time(zone, time_block, promised_time):
    """Average delivery time in minutes."""
    times = _collect_times(zone, time_block, promised_time)
    return round(float(times.mean()), 2)


def sort_late_rate(promised_time):
    """[zone, time block, late rate] rows, highest late rate first."""
    rows = [[z, tb, late_rate(z, tb, promised_time)]
            for z in ZONES for tb in TIME_BLOCKS]
    return sorted(rows, key=lambda r: r[2], reverse=True)


def sort_average_delivery_time(promised_time):
    """[zone, time block, average delivery time] rows, slowest first."""
    rows = [[z, tb, average_delivery_time(z, tb, promised_time)]
            for z in ZONES for tb in TIME_BLOCKS]
    return sorted(rows, key=lambda r: r[2], reverse=True)


def late_order_cost(cost):
    """Total cost of one late order: refund plus lost future margin from churn."""
    return cost["refund"] + cost["churn_orders"] * cost["margin"]


def evaluate_promises(zone, time_block, range_promise, cost):
    """Net profit for every promised time tried.

    Returns a list of dicts with promise, orders, late orders, late rate and net profit.
    """
    late_cost = late_order_cost(cost)
    results = []
    for promise in range_promise:
        times = delivery_times(zone, time_block, promise, seed=SEED)
        late_orders = int((times > promise).sum())
        net_profit = cost["margin"] * len(times) - late_orders * late_cost
        results.append({
            "promise": promise,
            "orders": len(times),
            "late_orders": late_orders,
            "late_rate": round(late_orders / len(times) * 100, 2),
            "net_profit": round(float(net_profit), 2),
        })
    return results


def best_promise_time(zone, time_block, range_promise, cost):
    """(best promised time, its net profit). Ties keep the earliest promise."""
    results = evaluate_promises(zone, time_block, range_promise, cost)
    best = results[0]
    for row in results[1:]:
        if row["net_profit"] > best["net_profit"]:
            best = row
    return best["promise"], best["net_profit"]
