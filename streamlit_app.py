import streamlit as st
import plotly.graph_objs as go
import numpy as np

# Data as decimals (already provided)
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

categories = ['B1GQ','B1G','D21X31','A','BTE','C','F','GTI','J','K','L','M_N','OTQ','RTU']

def create_grouped_stacked_figure():
    fig = go.Figure()

    # T+45 bars, offset group per category, all in same legendgroup for color
    fig.add_trace(go.Bar(
        x=categories,
        y=growth_t45 * 100,
        name='GR T+45 (%)',
        marker_color='blue',
        offsetgroup=0,
        legendgroup='T+45',
        hovertemplate='%{x}<br>T+45: %{y:.3f}%<extra></extra>'
    ))

    # T+65 bars, offset group 1 (so side by side)
    fig.add_trace(go.Bar(
        x=categories,
        y=growth_t65 * 100,
        name='GR T+65 (%)',
        marker_color='green',
        offsetgroup=1,
        legendgroup='T+65',
        hovertemplate='%{x}<br>T+65: %{y:.3f}%<extra></extra>'
    ))

    # cont_8ms bars (part of stacked bar), offset group 2
    fig.add_trace(go.Bar(
        x=categories,
        y=cont_8ms * 100,
        name='Cont. 8 MS (pps)',
        marker_color='orange',
        offsetgroup=2,
        legendgroup='Contribution',
        hovertemplate='%{x}<br>Cont. 8 MS: %{y:.3f} pps<extra></extra>',
        showlegend=True,
    ))

    # cont_12ms bars (stacked on cont_8ms), same offset group 2, legendgroup "Contribution"
    fig.add_trace(go.Bar(
        x=categories,
        y=cont_12ms * 100,
        name='Cont. 12 MS (pps)',
        marker_color='red',
        offsetgroup=2,
        legendgroup='Contribution',
        hovertemplate='%{x}<br>Cont. 12 MS: %{y:.3f} pps<extra></extra>',
        showlegend=True,
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
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    return fig

# Streamlit UI

st.title("Interactive Plotly Chart with Menus and Tabs")

option = st.selectbox("Select metric:", ["QoQ Growth Rate", "Contribution to growth"])

tab_names = ["Production - EA", "Production - EU", "Expenditure EA", "Expenditure EU"]
tabs = st.tabs(tab_names)

for tab_name, tab in zip(tab_names, tabs):
    with tab:
        st.header(f"{option} - {tab_name}")
        if option == "QoQ Growth Rate" and tab_name == "Production - EA":
            fig = create_grouped_stacked_figure()
        else:
            fig = go.Figure()
            fig.update_layout(title="No data yet for this tab")
        st.plotly_chart(fig, use_container_width=True, key=f"{option}_{tab_name}")
