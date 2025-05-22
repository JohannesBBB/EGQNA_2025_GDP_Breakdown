# -*- coding: utf-8 -*-
"""
Created on Thu May 22 11:56:34 2025

@author: buckjoh
"""

import streamlit as st
import plotly.graph_objs as go
import numpy as np

# Set wide page layout
st.set_page_config(layout="wide")

# Add CSS to limit plot width and center it
st.markdown("""
    <style>
    .my-plotly-container {
        max-width: 70vw;
        margin-left: auto;
        margin-right: auto;
    }
    /* Bold x-axis tick labels */
    .xtick > text {
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sample data (categories and values)
categories = ['B1GQ', 'B1G', 'D21X31', 'A', 'BTE', 'C', 'F', 'GTI', 'J', 'K', 'L', 'M_N', 'OTQ', 'RTU']

growth_t45 = np.array([
    0.000366, 0.003099, -0.025091, 0.005045,
    0.007375, 0.008180, 0.032566, -0.000515,
    -0.001903, -0.020046, 0.006428, 0.000650,
    -0.002256, 0.015999
])

growth_t65 = np.array([
    -0.000924, 0.002349, -0.030616, 0.009127,
    -0.007329, -0.008399, 0.025454, 0.002927,
    0.008900, -0.013183, 0.006696, 0.005052,
    0.000251, 0.017114
])

cont_8ms = np.array([
    -0.000884, -0.000023, -0.008313, -0.000088,
    -0.002572, -0.002227, -0.007573, 0.001121,
    0.000052, 0.001353, 0.000054, 0.002903,
    0.001199, 0.001336
])

cont_12ms = np.array([
    -0.000406, -0.000726, 0.002788, 0.004169,
    -0.012133, -0.014352, 0.000460, 0.002322,
    0.010752, 0.005510, 0.002140, 0.001499,
    0.001309, -0.000220
])

def create_grouped_stacked_figure():
    fig = go.Figure()

    # T+45 bars
    fig.add_trace(go.Bar(
        x=categories,
        y=growth_t45 * 100,
        name='GR T+45 (%)',
        marker_color='blue',
        offsetgroup=0,
        legendgroup='T+45',
        hovertemplate='%{y:.3f}%<extra></extra>'  # value only, no trace name or category repeat
    ))

    # T+65 bars
    fig.add_trace(go.Bar(
        x=categories,
        y=growth_t65 * 100,
        name='GR T+65 (%)',
        marker_color='green',
        offsetgroup=1,
        legendgroup='T+65',
        hovertemplate='%{y:.3f}%<extra></extra>'
    ))

    # cont_8ms bars (stacked)
    fig.add_trace(go.Bar(
        x=categories,
        y=cont_8ms * 100,
        name='Cont. 8 MS (pps)',
        marker_color='orange',
        offsetgroup=2,
        legendgroup='Contribution',
        hovertemplate='%{y:.3f} pps<extra></extra>'
    ))

    # cont_12ms bars (stacked)
    fig.add_trace(go.Bar(
        x=categories,
        y=cont_12ms * 100,
        name='Cont. 12 MS (pps)',
        marker_color='red',
        offsetgroup=2,
        legendgroup='Contribution',
        hovertemplate='%{y:.3f} pps<extra></extra>'
    ))

    fig.update_layout(
        barmode='stack',
        title="QoQ Growth Rate and Contribution - Production EA",
        yaxis_title="Percentage (%)",
        xaxis_title="Category",
        hovermode='x unified',
        xaxis_tickangle=-45,
        bargap=0.15,
        bargroupgap=0.1,
        legend=dict(
            orientation='h',
            yanchor='top',
            y=1.02,
            xanchor='left',
            x=0.05,
            font=dict(size=12)
        ),
        xaxis=dict(
            tickfont=dict(family='Arial', size=12, color='black', weight='bold')
        ),
        margin=dict(t=60, b=100)
    )

    return fig

st.title("Interactive Plotly Chart with Menus and Tabs")

option = st.selectbox("Select metric:", ["QoQ Growth Rate", "Contribution to growth"])

tab_names = ["Production - EA", "Production - EU", "Expenditure EA", "Expenditure EU"]
tabs = st.tabs(tab_names)

for tab_name, tab in zip(tab_names, tabs):
    with tab:
        st.header(f"{option} - {tab_name}")

        # For demonstration, only QoQ Growth Rate and Production EA has the detailed plot
        if option == "QoQ Growth Rate" and tab_name == "Production - EA":
            fig = create_grouped_stacked_figure()
        else:
            # Placeholder boring plot
            x = np.linspace(0, 10, 100)
            y = x
            hover_text = [f"x value: {xi:.2f}<br>y value: {yi:.2f}" for xi, yi in zip(x, y)]
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x,
                y=y,
                mode='lines+markers',
                hovertext=hover_text,
                hoverinfo='text',
                line=dict(color='royalblue'),
                marker=dict(size=6)
            ))
            fig.update_layout(
                title=f"Placeholder chart for {option} - {tab_name}",
                xaxis_title="x",
                yaxis_title="f(x)",
                hovermode='closest'
            )

        with st.container():
            st.markdown('<div class="my-plotly-container">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=False, width=1100, key=f"{option}_{tab_name}")
            st.markdown('</div>', unsafe_allow_html=True)
