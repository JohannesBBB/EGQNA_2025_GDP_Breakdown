# -*- coding: utf-8 -*-
"""
Created on Thu May 22 11:56:34 2025

@author: buckjoh
"""

import streamlit as st
import plotly.graph_objs as go
import numpy as np

# Generate data
x = np.linspace(0, 10, 100)
y = x

# Create Plotly figure function to reuse
def create_figure():
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
        title="Interactive Chart: f(x) = x",
        xaxis_title="x",
        yaxis_title="f(x)",
        hovermode='closest'
    )
    return fig

st.title("Interactive Plotly Chart with Menus and Tabs")

# Main menu selectbox
option = st.selectbox("Select metric:", ["QoQ Growth Rate", "Contribution to growth"])

# Create tabs
tabs = st.tabs(["Production - EA", "Production - EU", "Expenditure EA", "Expenditure EU"])

# For each tab, display the plot
for tab in tabs:
    with tab:
        st.header(f"{option} - {tab.title}")
        fig = create_figure()
        st.plotly_chart(fig, use_container_width=True)

