# -*- coding: utf-8 -*-
"""
Created on Thu May 22 11:56:34 2025
@author: buckjoh
"""

import streamlit as st
import plotly.graph_objs as go
import numpy as np

st.set_page_config(layout="wide")

# Define category sets
categories_prod = ['B1GQ', 'B1G', 'D21X31', 'A', 'BTE', 'C', 'F', 'GTI', 'J', 'K', 'L', 'M_N', 'OTQ', 'RTU']
categories_exp = ['B1GQ', 'S13_P3', 'S1M_P31', 'P5', 'P6', 'P7']

tab_names = ["Production - EA", "Production - EU", "Expenditure EA", "Expenditure EU"]
quarters = ["2023Q1","2023Q2","2023Q3","2023Q4","2024Q1","2024Q2","2024Q3","2024Q4"]

np.random.seed(42)  # for reproducibility

data = {}
data2 = {}

for tab in tab_names:
    if tab.startswith("Production"):
        categories = categories_prod
    else:
        categories = categories_exp

    # Time series data
    data_list = []
    for quarter in quarters:
        t45 = np.random.uniform(-0.01, 0.01, size=len(categories))
        t65 = t45 + np.random.uniform(-0.001, 0.001, size=len(categories))
        d = t65 - t45

        c = 0.8 + np.random.uniform(-0.2, 0.2, size=len(categories))
        c = np.clip(c, 0, 1)

        cont_8ms = (1 - c) * d
        cont_12ms = c * d

        data_list.append({
            "name": quarter,
            "t45": t45,
            "t65": t65,
            "cont_8ms": cont_8ms,
            "cont_12ms": cont_12ms
        })
    data[("QoQ Growth Rate", tab)] = data_list

    # Revision data
    mr = np.random.uniform(-0.1, 0.1, size=len(categories))
    mc1 = np.random.uniform(-0.05, 0.05, size=len(categories))
    mc2 = np.random.uniform(-0.05, 0.05, size=len(categories))

    mar = np.random.uniform(0, 0.2, size=len(categories))
    mac1 = np.random.uniform(0, 0.1, size=len(categories))
    mac2 = np.random.uniform(0, 0.1, size=len(categories))

    data2[("QoQ Growth Rate", tab)] = [{
        "name": "Mean Revision",
        "Mean Revision": mr,
        "Mean Revision Early MS": mc1,
        "Mean Revision Other MS": mc2
    },{
        "name": "Mean Absolute Revision",
        "Mean Revision": mar,
        "Mean Revision Early MS": mac1,
        "Mean Revision Other MS": mac2
    }]


def create_revision_figure(data_item, categories):
    fig = go.Figure()
    name = data_item.get("name", "")

    for i, (label, values) in enumerate(data_item.items()):
        if label == "name":
            continue
        fig.add_trace(go.Bar(
            x=categories,
            y=values * 100,
            name=label + " (%)",
            marker_color=["blue", "orange", "red", "green", "purple"][i % 5],
            offsetgroup=i,
            hovertemplate=f"{label}: "+"%{y:.3f} %<extra></extra>"
        ))

    fig.update_layout(
        barmode='group',
        height=500,
        margin=dict(l=200, r=200, t=80, b=80),
        bargap=0.15,
        bargroupgap=0.1,
        title=dict(text=name, font=dict(size=24), x=0.5, xanchor='center'),
        yaxis_title="Percentage (%)",
        xaxis_title="Category",
        xaxis=dict(tickangle=-45, tickfont=dict(family='Arial', size=14, color='black')),
        yaxis=dict(tickfont=dict(family='Arial', size=14, color='black')),
        hoverlabel=dict(font_size=18),
        hovermode='x unified',
        legend=dict(orientation='v', yanchor='top', y=1.15, xanchor='right', x=1.0, font=dict(size=12))
    )
    return fig


def create_qoq_figure(data_item, categories):
    fig = go.Figure()
    cont_8ms = data_item["cont_8ms"]
    cont_12ms = data_item["cont_12ms"]

    fig.add_trace(go.Bar(
        x=categories,
        y=data_item['t45'] * 100,
        name='T+45 (%)',
        marker_color='blue',
        offsetgroup=0,
        legendgroup='T+45',
        hovertemplate='T+45: %{y:.3f} %<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        x=categories,
        y=data_item['t65'] * 100,
        name='T+65 (%)',
        marker_color='green',
        offsetgroup=1,
        legendgroup='T+65',
        hovertemplate='T+65: %{y:.3f} %<extra></extra>'
    ))

    for i, cat in enumerate(categories):
        c1 = cont_8ms[i] * 100
        c2 = cont_12ms[i] * 100

        base1, base2 = 0, c1 if c1 >= 0 and c2 >= 0 else (0 if c1 <= 0 and c2 <= 0 else 0)

        fig.add_trace(go.Bar(
            x=[cat],
            y=[c1],
            base=[base1],
            name='Cont. Early MS (pps)',
            marker_color='orange',
            showlegend=(i == 0),
            hovertemplate='Contribution Early MS: %{y:.3f} pps<extra></extra>'
        ))

        fig.add_trace(go.Bar(
            x=[cat],
            y=[c2],
            base=[base2],
            name='Cont. Other MS (pps)',
            marker_color='red',
            showlegend=(i == 0),
            hovertemplate='Contribution Other MS: %{y:.3f} pps<extra></extra>'
        ))

    fig.update_layout(
        barmode='stack',
        height=500,
        margin=dict(l=200, r=200, t=80, b=80),
        bargap=0.15,
        bargroupgap=0.1,
        title=dict(text=data_item.get("name", ""), font=dict(size=30), x=0.5, xanchor='center'),
        yaxis_title="Percentage (%)",
        xaxis=dict(tickangle=-45, tickfont=dict(family='Arial', size=16, color='black', weight='bold')),
        yaxis=dict(tickfont=dict(family='Arial', size=16, color='black')),
        hoverlabel=dict(font_size=18),
        hovermode='x unified',
        legend=dict(orientation='v', yanchor='bottom', y=1, xanchor='right', x=1.0, font=dict(size=12))
    )
    return fig


# --- Streamlit UI ---
st.title("Early Breakdown Estimations")

option = st.selectbox("Select metric:", ["QoQ Growth Rate", "Contribution to growth"])
tabs = st.tabs(tab_names)

for tab_name, tab in zip(tab_names, tabs):
    with tab:
        st.header(f"{option} - {tab_name}")
        key = (option, tab_name)

        # Determine correct category set
        if tab_name.startswith("Production"):
            categories = categories_prod
        elif tab_name.startswith("Expenditure"):
            categories = categories_exp
        else:
            categories = []

        if key in data2:
            for i, data_item in enumerate(data2[key]):
                fig = create_revision_figure(data_item, categories)
                st.plotly_chart(fig, use_container_width=True, key=f"meanrev_{key}_{i}")
        else:
            st.warning("No mean revision data available for this tab.")

        if key in data:
            for i, data_item in enumerate(data[key]):
                fig = create_qoq_figure(data_item, categories)
                st.plotly_chart(fig, use_container_width=True, key=f"qoq_{key}_{i}")
        else:
            st.warning("No data available for this selection.")
