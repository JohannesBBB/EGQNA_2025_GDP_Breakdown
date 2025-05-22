import streamlit as st
import plotly.graph_objs as go
import numpy as np

# Data setup: components and data arrays
components = ["B1GQ", "B1G", "D21X31", "A", "BTE", "C", "F", "GTI", "J", "K", "L", "M_N", "OTQ", "RTU"]

growth_t45 = np.array([
    0.000366, 0.003099, -0.025091, 0.005045, 0.007375, 0.008180, 0.032566,
    -0.000515, -0.001903, -0.020046, 0.006428, 0.000650, -0.002256, 0.015999
])
growth_t65 = np.array([
    -0.000924, 0.002349, -0.030616, 0.009127, -0.007329, -0.008399, 0.025454,
    0.002927, 0.008900, -0.013183, 0.006696, 0.005052, 0.000251, 0.017114
])
diff = growth_t65 - growth_t45
cont_8ms = np.array([
    -0.000884, -0.000023, -0.008313, -0.000088, -0.002572, -0.002227, -0.007573,
    0.001121, 0.000052, 0.001353, 0.000054, 0.002903, 0.001199, 0.001336
])
cont_12ms = np.array([
    -0.000406, -0.000726, 0.002788, 0.004169, -0.012133, -0.014352, 0.000460,
    0.002322, 0.010752, 0.005510, 0.002140, 0.001499, 0.001309, -0.000220
])

def create_stacked_bar_chart():
    fig = go.Figure()

    # Add T+45 bars
    fig.add_trace(go.Bar(
        x=components,
        y=growth_t45,
        name="T+45",
        marker_color="royalblue",
        hovertemplate='%{y:.3%}',
    ))

    # Add T+65 bars
    fig.add_trace(go.Bar(
        x=components,
        y=growth_t65,
        name="T+65",
        marker_color="orange",
        hovertemplate='%{y:.3%}',
    ))

    # Add stacked bars for cont_8ms and cont_12ms (difference broken down)
    fig.add_trace(go.Bar(
        x=components,
        y=cont_8ms,
        name="Contribution 8 MS",
        marker_color="green",
        hovertemplate='%{y:.3%}',
    ))
    fig.add_trace(go.Bar(
        x=components,
        y=cont_12ms,
        name="Contribution 12 MS",
        marker_color="lightgreen",
        hovertemplate='%{y:.3%}',
    ))

    fig.update_layout(
        barmode='stack',
        title="Growth Rate Breakdown by Component",
        xaxis_title="Component",
        yaxis_title="Growth Rate",
        hovermode="x unified",
        # Bold x-axis labels
        xaxis=dict(
            tickfont=dict(family='Arial', size=12, color='black', weight='bold')
        ),
        # Make legend compact and move left a bit
        legend=dict(
            y=1,
            x=0.75,
            traceorder="normal",
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)',
            orientation="h",
            xanchor="left",
            font=dict(size=11)
        ),
        margin=dict(l=40, r=40, t=80, b=40),
    )

    # Customize hover label: show component name bold once at top left, values below
    # Using "hoverlabel" to style, but can't set bold header directly per se, workaround:
    # Use unified hovermode and customize hovertemplate for each trace with only value
    
    # So hovermode='x unified' shows component once on top left automatically
    # And each trace hovertemplate just shows value
    
    return fig

st.title("Growth Rate Analysis")

# Center and limit plot width with columns
col1, col2, col3 = st.columns([1,4,1])
with col2:
    fig = create_stacked_bar_chart()
    st.plotly_chart(fig, use_container_width=False, width=900)
