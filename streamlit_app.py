import streamlit as st
import plotly.graph_objs as go
import numpy as np

# Updated precise data (percentages converted to decimals)
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

diff = growth_t65 - growth_t45

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

categories = ['B1GQ','B1G','D21X31','A','BTE','C','F','GTI','J','K','L','M_N','OTQ','RTU']

def create_real_data_figure():
    fig = go.Figure()

    # Growth bars side by side for T+45 and T+65
    fig.add_trace(go.Bar(
        x=categories,
        y=growth_t45 * 100,  # back to percentage scale
        name='GR T+45 (%)',
        marker_color='blue'
    ))

    fig.add_trace(go.Bar(
        x=categories,
        y=growth_t65 * 100,
        name='GR T+65 (%)',
        marker_color='green'
    ))

    # Stacked contribution bars
    fig.add_trace(go.Bar(
        x=categories,
        y=cont_8ms * 100,
        name='Cont. 8 MS (pps)',
        marker_color='orange'
    ))

    fig.add_trace(go.Bar(
        x=categories,
        y=cont_12ms * 100,
        name='Cont. 12 MS (pps)',
        marker_color='red'
    ))

    fig.update_layout(
        barmode='stack',
        title="QoQ Growth Rate and Contribution - Production EA",
        yaxis_title="Percentage (%)",
        xaxis_title="Category",
        hovermode='x unified'
    )
    return fig

# Sample fallback figure (same as before)
def create_figure():
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
        if 1==1:#option == "QoQ Growth Rate" and tab_name == "Production - EA":
            fig = create_real_data_figure()
        else:
            fig = create_figure()
        st.plotly_chart(fig, use_container_width=True, key=f"{option}_{tab_name}")
