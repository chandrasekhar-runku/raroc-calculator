import numpy as np
import pandas as pd
import streamlit as st
from risk_engine import calculate_raroc

st.set_page_config(page_title="RAROC & Basel RWA Calculator", layout="wide")
st.title("RAROC & Basel IRB RWA Calculator")
st.caption("Corporate exposure, foundation/advanced IRB risk-weight function.")

with st.sidebar:
    st.header("Credit risk inputs")
    ead = st.number_input("EAD (Exposure at Default)", 1000.0, value=1_000_000.0, step=50_000.0)
    pd_pct = st.slider("PD (%)", 0.01, 30.0, 1.0, 0.01)
    lgd_pct = st.slider("LGD (%)", 5.0, 100.0, 45.0, 1.0)
    maturity = st.slider("Effective maturity (years)", 1.0, 5.0, 2.5, 0.5)

    st.header("Pricing & cost inputs")
    interest = st.number_input("Interest rate (%)", value=5.0, step=0.25) / 100
    funding = st.number_input("Funding cost (%)", value=3.0, step=0.25) / 100
    fees = st.number_input("Upfront/annual fees", value=2_000.0, step=500.0)
    opex = st.number_input("Operating cost (% of EAD)", value=0.4, step=0.1) / 100

    st.header("Capital assumptions")
    cap_ratio = st.number_input("Capital ratio (%)", value=10.5, step=0.5) / 100
    tax = st.number_input("Tax rate (%)", value=0.0, step=1.0) / 100
    hurdle = st.number_input("Hurdle rate (%)", value=12.0, step=0.5)

res = calculate_raroc(ead, pd_pct / 100, lgd_pct / 100, maturity,
                      interest, funding, fees, opex, cap_ratio, tax)

c1, c2, c3, c4 = st.columns(4)
c1.metric("RWA", f"{res['RWA']:,.0f}")
c2.metric("Risk weight", f"{res['Risk weight (%)']:.1f}%")
c3.metric("Capital held", f"{res['Capital held']:,.0f}")
c4.metric("RAROC", f"{res['RAROC (%)']:.1f}%",
          delta=f"{res['RAROC (%)'] - hurdle:.1f} pts vs hurdle")

if res["RAROC (%)"] >= hurdle:
    st.success("Clears the hurdle rate: value-creating at this price.")
else:
    st.warning("Below hurdle: consider repricing, collateral, or declining.")

st.subheader("Income breakdown")
st.dataframe(pd.DataFrame({
    "Item": ["Revenue", "Funding cost", "Opex", "Expected loss", "Net income"],
    "Amount": [res["Revenue"], -res["Funding cost"], -res["Opex"],
               -res["Expected loss"], res["Net income"]],
}).style.format({"Amount": "{:,.0f}"}), hide_index=True)

st.subheader("How RAROC changes with PD")
pds = np.linspace(0.1, 10, 40)
curve = [calculate_raroc(ead, p / 100, lgd_pct / 100, maturity, interest, funding,
                         fees, opex, cap_ratio, tax)["RAROC (%)"] for p in pds]
st.line_chart(pd.DataFrame({"PD (%)": pds, "RAROC (%)": curve}).set_index("PD (%)"))
