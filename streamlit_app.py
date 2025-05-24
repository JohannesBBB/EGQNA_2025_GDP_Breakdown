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
    data_list2= []
    for quarter in quarters:
        t45 = np.random.uniform(-0.01, 0.01, size=len(categories))
        t45_2 = np.random.uniform(-0.01, 0.01, size=len(categories))
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
        
        data_list2.append({
            "name": quarter,
            "t45_1": t45,
            "t45_2": t45_2,
            "t65": t65,
            "dif_1": (t65-t45),
            "dif_2": (t65-t45_2)
        })
        
    data[("QoQ Growth Rate", tab)] = data_list
    data[("Contribution to growth", tab)] = data_list2
    
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
    "Mean Contribution to Revision Early MS": mc1,
    "Mean Contribution to Revision Other MS": mc2
    },{
    "name": "Mean Absolute Revision",
    "Mean Abs. Revision": mar,
    "Mean Abs. Contr. to Revision Early MS": mac1,
    "Mean Abs. Contr. to Revision Other MS": mac2
    }]

    data2[("Contribution to growth", tab)] = [{
    "name": "Mean Revision",
    "Mean Revision (1)": mr,
    "Mean Revision (2)": mar
    },{
    "name": "Mean Absolute Revision",
    "Mean Absolute Revision (1)": mr,
    "Mean Absolute Revision (2)": mar
    }]


def create_revision_figure(data_item, categories):
    fig = go.Figure()
    name = data_item.get("name", "")
    items = [(k, v) for k, v in data_item.items() if k != "name"]
    
    if len(items) != 3:
        # Default case: plot all as bars
        for i, (label, values) in enumerate(items):
            fig.add_trace(go.Bar(
                x=categories,
                y=values * 100,
                name=label + " (%)",
                marker_color=["blue", "green", "orange", "red", "purple"][i % 5],
                offsetgroup=i,
                hovertemplate=f"{label}: "+"%{y:.3f} %<extra></extra>"
            ))
    else:
        # Special case for 3 items: first as bar, next two as markers
        # First item as bar
        label, values = items[0]
        fig.add_trace(go.Bar(
            x=categories,
            y=values * 100,
            name=label + " (%)",
            marker_color="blue",
            offsetgroup=0,
            hovertemplate=f"{label}: "+"%{y:.3f} %<extra></extra>"
        ))
        
        # Second item as "o" marker
        label, values = items[1]
        fig.add_trace(go.Scatter(
            x=categories,
            y=values * 100,
            mode='markers+text',
            marker=dict(
                color='orange',
                symbol='circle-open',
                size=12,
                line=dict(width=3)
            ),
            name=label + " (%)",
            hovertemplate=f"{label}: "+"%{y:.3f} %<extra></extra>"
        ))
        
        # Third item as "x" marker
        label, values = items[2]
        fig.add_trace(go.Scatter(
            x=categories,
            y=values * 100,
            mode='markers',
            marker=dict(
                color='red',
                symbol='x-thin-open',
                size=12,
                line=dict(width=2)
            ),
            name=label + " (%)",
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
    fig.add_hline(
        y=0,
        line_dash="solid",
        line_width=1,
        line_color="black",
        opacity=0.8
    )
    return fig


def create_qoq_figure(data_item, categories,width_line):
    fig = go.Figure()
    
    t45 = data_item['t45'] * 100
    t65 = data_item['t65'] * 100
    cont_8ms = data_item["cont_8ms"] * 100
    cont_12ms = data_item["cont_12ms"] * 100

    # Create lists to hold bars per category
    y_t45, y_c1, y_c2 = [], [], []
    base_t45, base_c1, base_c2 = [], [], []

    for i in range(len(categories)):
        y0 = t45[i]
        c1 = cont_8ms[i]
        c2 = cont_12ms[i]

        # Initialize stacking base points
        pos_base = 0
        neg_base = 0

        # Stack in order: t45, cont_8ms, cont_12ms
        if y0 >= 0:
            y_t45.append(y0)
            base_t45.append(pos_base)
            pos_base += y0
        else:
            y_t45.append(y0)
            base_t45.append(neg_base)
            neg_base += y0

        if c1 >= 0:
            y_c1.append(c1)
            base_c1.append(pos_base)
            pos_base += c1
        else:
            y_c1.append(c1)
            base_c1.append(neg_base)
            neg_base += c1

        if c2 >= 0:
            y_c2.append(c2)
            base_c2.append(pos_base)
            pos_base += c2
        else:
            y_c2.append(c2)
            base_c2.append(neg_base)
            neg_base += c2

    # Add T+45 bar first (will appear first in legend)
    fig.add_trace(go.Bar(
        x=categories,
        y=y_t45,
        base=base_t45,
        name='T+45 (%)',
        marker_color='blue',
        hovertemplate='T+45: %{y:.3f} %<extra></extra>',
        legendrank=1  # First in legend
    ))

    # Add T+65 scatter next (will appear second in legend but on top visually)
    fig.add_trace(go.Scatter(
        x=categories,
        y=t65,
        mode='markers',
        marker=dict(
            color='black',
            symbol='line-ew-open',
            size=width_line,
            line=dict(width=4)
        ),
        name='T+65',
        hovertemplate='T+65: %{y:.3f} %<extra></extra>',
        legendrank=2  # Second in legend
    ))

    # Add remaining bars (will appear after in legend)
    fig.add_trace(go.Bar(
        x=categories,
        y=y_c1,
        base=base_c1,
        name='Contribution Early MS (pps)',
        marker_color='orange',
        hovertemplate='Contribution Early MS: %{y:.3f} pps<extra></extra>',
        legendrank=3  # Third in legend
    ))

    fig.add_trace(go.Bar(
        x=categories,
        y=y_c2,
        base=base_c2,
        name='Contribution Other MS (pps)',
        marker_color='red',
        hovertemplate='Contribution Other MS: %{y:.3f} pps<extra></extra>',
        legendrank=4  # Fourth in legend
    ))

    fig.update_layout(
        barmode='relative',
        height=500,
        margin=dict(l=200, r=200, t=80, b=80),
        bargap=0.15,
        bargroupgap=0.1,
        title=dict(text=data_item.get("name", ""), font=dict(size=30), x=0.5, xanchor='center'),
        yaxis_title="Percentage (%)",
        xaxis=dict(tickangle=-45, tickfont=dict(family='Arial', size=16, color='black')),
        yaxis=dict(tickfont=dict(family='Arial', size=16, color='black')),
        hoverlabel=dict(font_size=18),
        hovermode='x unified',
        legend=dict(
            orientation='v',
            yanchor='bottom',
            y=1,
            xanchor='right',
            x=1.0,
            font=dict(size=12),
            traceorder='normal'  # This respects the legendrank ordering
        )
    )
    fig.add_hline(
        y=0,
        line_dash="solid",
        line_width=1,
        line_color="black",
        opacity=0.8
    )
    return fig


def create_GO_One_figure(data_item, categories, width_line):
    fig = go.Figure()
    
    t45_1 = data_item['t45_1'] * 100
    t45_2 = data_item['t45_2'] * 100
    t65 = data_item['t65'] * 100
    dif_1 = data_item["dif_1"] * 100
    dif_2 = data_item["dif_2"] * 100

    # Create lists to hold bars per category
    y_t45, y_t45_2, y_c1, y_c2 = [], [], [], []
    base_t45, base_t45_2, base_c1, base_c2 = [], [], [], []

    for i in range(len(categories)):
        # First set (t45_1)
        y0 = t45_1[i]
        c1 = dif_1[i]
        
        # Second set (t45_2)
        y0_2 = t45_2[i]
        c2 = dif_2[i]

        # Stack first set
        if y0 >= 0:
            y_t45.append(y0)
            base_t45.append(0)
            y_c1.append(c1)
            base_c1.append(y0)
        else:
            y_t45.append(y0)
            base_t45.append(0)
            y_c1.append(c1)
            base_c1.append(y0)

        # Stack second set
        if y0_2 >= 0:
            y_t45_2.append(y0_2)
            base_t45_2.append(0)
            y_c2.append(c2)
            base_c2.append(y0_2)
        else:
            y_t45_2.append(y0_2)
            base_t45_2.append(0)
            y_c2.append(c2)
            base_c2.append(y0_2)

    # First bar group (t45_1)
    fig.add_trace(go.Bar(
        x=categories,
        y=y_t45,
        base=base_t45,
        name='T+45_1',
        marker_color='blue',
        hovertemplate='T+45_1: %{y:.3f}%<extra></extra>',
        legendrank=1,
        offsetgroup=0
    ))

    fig.add_trace(go.Bar(
        x=categories,
        y=y_c1,
        base=[b + y for b, y in zip(base_t45, y_t45)],
        name='Diff to T+65',
        marker_color='lightblue',
        hovertemplate='Diff to T+65: %{y:.3f}%<extra></extra>',
        legendrank=2,
        offsetgroup=0
    ))

    # Second bar group (t45_2)
    fig.add_trace(go.Bar(
        x=categories,
        y=y_t45_2,
        base=base_t45_2,
        name='T+45_2',
        marker_color='green',
        hovertemplate='T+45_2: %{y:.3f}%<extra></extra>',
        legendrank=3,
        offsetgroup=1
    ))

    fig.add_trace(go.Bar(
        x=categories,
        y=y_c2,
        base=[b + y for b, y in zip(base_t45_2, y_t45_2)],
        name='Diff to T+45_1',
        marker_color='lightgreen',
        hovertemplate='Diff to T+45_1: %{y:.3f}%<extra></extra>',
        legendrank=4,
        offsetgroup=1
    ))

    # T+65 markers (single legend entry)
    fig.add_trace(go.Scatter(
        x=categories,
        y=t65,
        mode='markers',
        marker=dict(
            color='black',
            symbol='line-ew-open',
            size=width_line,
            line=dict(width=4)
        ),
        name='T+65',
        hovertemplate='T+65: %{y:.3f}%<extra></extra>',
        legendrank=5,
        showlegend=True
    ))

    # Hidden duplicate for hover purposes
    fig.add_trace(go.Scatter(
        x=categories,
        y=t65,
        mode='markers',
        marker=dict(
            color='black',
            symbol='line-ew-open',
            size=width_line,
            line=dict(width=4)
        ),
        hoverinfo='skip',
        showlegend=False
    ))

    fig.update_layout(
        barmode='group',
        height=500,
        margin=dict(l=200, r=200, t=80, b=80),
        bargap=0.3,
        title=dict(text=data_item.get("name", ""), font=dict(size=30), x=0.5, xanchor='center'),
        yaxis_title="Percentage (%)",
        xaxis=dict(tickangle=-45, tickfont=dict(family='Arial', size=16, color='black')),
        yaxis=dict(tickfont=dict(family='Arial', size=16, color='black')),
        hoverlabel=dict(font_size=18),
        legend=dict(
            orientation='v',
            yanchor='bottom',
            y=1,
            xanchor='right',
            x=1.0,
            font=dict(size=12),
            traceorder='normal'
        )
    )

    fig.add_hline(
        y=0,
        line_dash="solid",
        line_width=1,
        line_color="black",
        opacity=0.8
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
            width_line=6
        elif tab_name.startswith("Expenditure"):
            categories = categories_exp
            width_line=13
        else:
            categories = []

        if key in data2:
            for i, data_item in enumerate(data2[key]):
                fig = create_revision_figure(data_item, categories)
                st.plotly_chart(fig, use_container_width=True, key=f"meanrev_{key}_{i}")
        else:
            st.warning("No mean revision data available for this tab.")

        if option == "QoQ Growth Rate":
            if key in data:
                for i, data_item in enumerate(data[key]):
                    fig = create_qoq_figure(data_item, categories,width_line)
                    st.plotly_chart(fig, use_container_width=True, key=f"qoq_{key}_{i}")
            else:
                st.warning("No data available for this selection.")
        else:
            if key in data:
                for i, data_item in enumerate(data[key]):
                    fig = create_GO_One_figure(data_item, categories,width_line)
                    st.plotly_chart(fig, use_container_width=True, key=f"goone_{key}_{i}")
            else:
                st.warning("No data available for this selection.")
