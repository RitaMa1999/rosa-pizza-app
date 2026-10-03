import pandas as pd
import streamlit as st

from rosa_logic import (
    ZONES, TIME_BLOCKS, COSTS, PROMISE,
    late_order_cost, evaluate_promises, best_promise_time,
)

st.set_page_config(page_title="Rosa's Pizza: Best Promise", page_icon="🍕")
st.title("🍕 Rosa's Pizza: Best Promised Delivery Time")
st.caption(f"Current promise is {PROMISE} minutes. Try other promised times "
           "to find the one with the highest net profit.")

if "result" not in st.session_state:
    st.session_state.result = None

# --- Inputs ---------------------------------------------------------------
col1, col2 = st.columns(2)
zone = col1.selectbox("Zone", ZONES, index=ZONES.index("Far West"))
time_block = col2.selectbox("Time block", TIME_BLOCKS,
                            index=TIME_BLOCKS.index("Fri/Sat eve"))

st.subheader("Promised times to try")
low, high = st.slider("Range (minutes)", min_value=15, max_value=90,
                      value=(45, 65), step=1)
step = st.number_input("Step (minutes)", min_value=1, max_value=30, value=5)
range_promise = list(range(low, high + 1, int(step)))
st.write("Trying:", ", ".join(str(p) for p in range_promise))

st.subheader("Costs")
c1, c2, c3 = st.columns(3)
margin = c1.number_input("Profit margin per order ($)", min_value=0.0,
                         value=float(COSTS["margin"]), step=0.5)
churn = c2.number_input("Churn per late order (orders)", min_value=0.0,
                        value=float(COSTS["churn_orders"]), step=0.1)
refund = c3.number_input("Refund per late order ($)", min_value=0.0,
                         value=float(COSTS["refund"]), step=0.5)
cost = {"refund": refund, "churn_orders": churn, "margin": margin}

# --- Action: mutate state only --------------------------------------------
if st.button("Find best promised time", type="primary"):
    best, profit = best_promise_time(zone, time_block, range_promise, cost)
    st.session_state.result = {
        "zone": zone,
        "time_block": time_block,
        "best": best,
        "net_profit": profit,
        "late_cost": late_order_cost(cost),
        "table": evaluate_promises(zone, time_block, range_promise, cost),
    }

# --- Render from session state --------------------------------------------
result = st.session_state.result
if result is not None:
    st.divider()
    st.subheader(f"Recommendation: {result['zone']}, {result['time_block']}")
    m1, m2, m3 = st.columns(3)
    m1.metric("Recommended promise", f"{result['best']} min")
    m2.metric("Net profit", f"${result['net_profit']:,.2f}")
    m3.metric("Cost per late order", f"${result['late_cost']:,.2f}")

    df = pd.DataFrame(result["table"]).rename(columns={
        "promise": "Promise (min)", "orders": "Orders",
        "late_orders": "Late orders", "late_rate": "Late rate (%)",
        "net_profit": "Net profit ($)",
    })
    st.line_chart(df, x="Promise (min)", y="Net profit ($)")
    st.dataframe(df, hide_index=True, width="stretch")
