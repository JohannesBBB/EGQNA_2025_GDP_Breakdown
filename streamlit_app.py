# -*- coding: utf-8 -*-
"""
Created on Thu May 22 11:56:34 2025
@author: buckjoh
"""

import streamlit as st
import plotly.graph_objs as go
import numpy as np

st.set_page_config(layout="wide")

# --- Data Storage: key = (metric, tab), value = list of items (each item is a dict with 4 series) ---
# --- Data Storage: key = (metric, tab), value = list of named plot items ---
data = {
    ("QoQ Growth Rate", "Production - EA"): [
        {
            "name": "2023Q1",
            "t45": np.array([0.000366, 0.003099, -0.025091, 0.005045, 0.007375, 0.008180, 0.032566, -0.000515,
                             -0.001903, -0.020046, 0.006428, 0.000650, -0.002256, 0.015999]),
            "t65": np.array([-0.000924, 0.002349, -0.030616, 0.009127, -0.007329, -0.008399, 0.025454, 0.002927,
                             0.008900, -0.013183, 0.006696, 0.005052, 0.000251, 0.017114]),
            "cont_8ms": np.array([-0.000884, -0.000023, -0.008313, -0.000088, -0.002572, -0.002227, -0.007573, 0.001121,
                                  0.000052, 0.001353, 0.000054, 0.002903, 0.001199, 0.001336]),
            "cont_12ms": np.array([-0.000406, -0.000726, 0.002788, 0.004169, -0.012133, -0.014352, 0.000460, 0.002322,
                                   0.010752, 0.005510, 0.002140, 0.001499, 0.001309, -0.000220])
        },
        {
            "name": "2023Q3",
            "t45": np.array([0.010366, 0.003099, -0.025091, 0.005045, 0.007375, 0.008180, 0.032566, -0.000515,
                             -0.001903, -0.020046, 0.006428, 0.000650, -0.002256, 0.015999]),
            "t65": np.array([-0.000924, 0.002349, -0.030616, 0.009127, -0.007329, -0.008399, 0.025454, 0.002927,
                             0.008900, -0.013183, 0.006696, 0.005052, 0.000251, 0.017114]),
            "cont_8ms": np.array([-0.000884, -0.000023, -0.008313, -0.000088, -0.002572, -0.002227, -0.007573, 0.001121,
                                  0.000052, 0.001353, 0.000054, 0.002903, 0.001199, 0.001336]),
            "cont_12ms": np.array([-0.000406, -0.000726, 0.002788, 0.004169, -0.012133, -0.014352, 0.000460, 0.002322,
                                   0.010752, 0.005510, 0.002140, 0.001499, 0.001309, -0.000220])
        }
    ]
}


categories = ['B1GQ', 'B1G', 'D21X31', 'A', 'BTE', 'C', 'F', 'GTI', 'J', 'K', 'L', 'M_N', 'OTQ', 'RTU']

def create_qoq_figure(data_item):
    fig = go.Figure()

    # Ensure order: T+45, T+65, Early MS, Other MS
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
    
        # Stacking logic
        if c1 >= 0 and c2 >= 0:
            base1, base2 = 0, c1
        elif c1 <= 0 and c2 <= 0:
            base1, base2 = 0, c1
        else:
            base1, base2 = 0, 0
    
        # Early MS bar
        fig.add_trace(go.Bar(
            x=[cat],
            y=[c1],
            base=[base1],
            name='Cont. Early MS (pps)',
            marker_color='orange',
            showlegend=(i == 0),
            hovertemplate='Contribution Early MS: %{y:.3f} pps<extra></extra>'
        ))
    
        # Other MS bar
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
        margin=dict(l=200, r=200, t=80, b=80),  # Left and right margins = 200
        bargap=0.15,
        bargroupgap=0.1,
        title=dict(
            text=data_item.get("name", ""),
            font=dict(size=24),  # Larger title
            x=0.5,  # Center title
            xanchor='center'
        ),
        yaxis_title="Percentage (%)",
        xaxis_title="Category",
        xaxis=dict(
            tickangle=-45,
            tickfont=dict(family='Arial', size=12, color='black', weight='bold')
        ),
        hovermode='x unified',
        legend=dict(
            orientation='v',
            yanchor='top',
            y=1.0,
            xanchor='right',
            x=1.0,
            font=dict(size=12)
        )
    )
    return fig


# --- Streamlit UI ---
st.title("Early Breakdown Estimations")

option = st.selectbox("Select metric:", ["QoQ Growth Rate", "Contribution to growth"])

tab_names = ["Production - EA", "Production - EU", "Expenditure EA", "Expenditure EU"]
tabs = st.tabs(tab_names)

for tab_name, tab in zip(tab_names, tabs):
    with tab:
        st.header(f"{option} - {tab_name}")

        key = (option, tab_name)
        if key in data:
            for i, data_item in enumerate(data[key]):
                fig = create_qoq_figure(data_item)
                st.plotly_chart(fig, use_container_width=True, key=f"{key}_{i}")
        else:
            st.warning("No data available for this selection.")
