import streamlit as st
import plotly.graph_objs as go
import numpy as np

# Generate data
x = np.linspace(0, 10, 100)
y = x

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

option = st.selectbox("Select metric:", ["QoQ Growth Rate", "Contribution to growth"])

tab_names = ["Production - EA", "Production - EU", "Expenditure EA", "Expenditure EU"]
tabs = st.tabs(tab_names)

for tab_name, tab in zip(tab_names, tabs):
    with tab:
        st.header(f"{option} - {tab_name}")
        fig = create_figure()
        # Add unique key to avoid duplicate ID errors
        st.plotly_chart(fig, use_container_width=True, key=f"{option}_{tab_name}")
