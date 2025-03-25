import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def create_bar_chart(
        df: pd.DataFrame,
        x: str,
        title: str,
        x_title: str,
        y_title: str = "Number of Files",
        key_suffix: str = "",
        hover_columns: list = None,
) -> px.bar:  # TODO: Maybe delete and only stay with go bar chart

    bar_mode = get_bar_mode(key_suffix)

    fig = px.bar(
        df,
        x=x,
        y='value',
        color='selected_folder_short',
        barmode='stack' if bar_mode == "Stacked" else 'group',
        color_discrete_map=dict(zip(
            df['selected_folder_short'].unique(),
            df.groupby('selected_folder_short')['color'].first()
        )),
        title=title,
        labels={
            x: x_title,
            'value': y_title,
            'selected_folder_short': 'Folder'
        },
        hover_data=hover_columns,
    )
    fig.update_traces(
        marker_line_color="white",
        marker_line_width=0.5, # TODO: Makes plot opaque when too many bars - FIX!
        opacity=1,
    )
    fig.update_layout(
        height=500,
        margin=dict(l=50, r=50, t=80, b=100),
        hovermode='closest',
        bargap=0.1,
        bargroupgap=0.05,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )

    return fig


def create_bar_chart_go_w_pattern(
    df,
    x_col,        # e.g. "dtype"
    sub_x_col,    # e.g. "selected_folder"
    pattern_col,  # e.g. "file_extension"
    value_col="value",
    title="Distribution",
    hover_cols=None
):
    folder_colors = df[[sub_x_col, "color"]].drop_duplicates().set_index(sub_x_col)["color"].to_dict()

    all_x = df[x_col].unique()
    all_sub = df[sub_x_col].unique()
    all_patterns = df[pattern_col].unique()
    grid = pd.MultiIndex.from_product([all_x, all_sub, all_patterns],
                                      names=[x_col, sub_x_col, pattern_col]).to_frame(index=False)
    df = pd.merge(grid, df, on=[x_col, sub_x_col, pattern_col], how="left")
    df[value_col] = df[value_col].fillna(0)

    x_data = [df[x_col].values, df[sub_x_col].values]
    unique_patterns = df[pattern_col].unique()
    fig = go.Figure()
    pattern_shapes = create_pattern_shapes(len(unique_patterns))

    for pattern_val, shape in zip(unique_patterns, pattern_shapes):
        mask = df[pattern_col] == pattern_val
        for folder in df[sub_x_col].unique():
            folder_color = folder_colors.get(folder, "rgba(50,50,50,0.5)")
            y_data = df[value_col].mask(~(mask & (df[sub_x_col] == folder)), pd.NA)
            hover_text = df[pattern_col].astype(str)
            if hover_cols:
                available_hover_cols = [col for col in hover_cols if col in df.columns]
                combined_cols = df[available_hover_cols].astype(str).agg('\n'.join, axis=1)
                hover_text = hover_text + '<br>' + combined_cols
            fig.add_bar(
                x=x_data,
                y=y_data,
                marker_color=folder_color,
                name=folder,
                legendgroup=folder,
                showlegend=(pattern_val == unique_patterns[0]),
                hovertext=hover_text,
                marker_pattern_shape=shape,
            )
    fig.update_layout(
        barmode="relative",
        title=title,
        xaxis_title=x_col,
        yaxis_title=value_col,
        height=500,
        margin=dict(l=50, r=50, t=80, b=100),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
        ),
        yaxis=dict(title="Number of Files"),
        xaxis=dict(title="Data Type", tickangle=0)
    )
    return fig


def create_histogram_chart(
        df: pd.DataFrame,
        x: str,
        title: str,
        x_title: str,
        y_title: str = "Number of Files",
        key_suffix: str = "",
) -> go.Figure:

    bar_mode = get_bar_mode(key_suffix)

    x_min, x_max = df[x].min(), df[x].max()
    bin_size = get_bin_size(x_min, x_max)
    end, start, tick_text, tick_vals = get_x_ticks_params(bin_size, x_max, x_min)

    fig = go.Figure()

    for folder in df['selected_folder_short'].unique():
        folder_data = df[df['selected_folder_short'] == folder]
        color = folder_data['color'].iloc[0]

        # Calculate the histogram data manually
        hist, bin_edges = np.histogram(folder_data[x], bins=np.arange(start, end + bin_size, bin_size))

        hover_text = get_hover_text(bin_edges, bin_size, folder, folder_data, hist, x)

        fig.add_trace(go.Histogram(
            x=folder_data[x],
            name=folder,
            marker_color=color,
            xbins=dict(size=bin_size),
            hovertemplate="%{customdata}",  # Use customdata for hover text
            customdata=hover_text,  # Assign hover text to customdata
            text=[],  # Ensure no text is displayed on the bars
        ))

    fig.update_layout(
        barmode='stack' if bar_mode == "Stacked" else 'group',
        title=title,
        height=500,
        margin=dict(l=50, r=50, t=80, b=100),
        hovermode='closest',
        bargap=0.1,
        bargroupgap=0.05,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        xaxis_title=x_title,
        yaxis_title=y_title,
        xaxis=dict(
            tickmode='array',
            tickvals=tick_vals,
            ticktext=tick_text,
            range=[x_min - 1, x_max + 1] if x_min == x_max else [start, end],
        ),
    )

    return fig


def create_heatmap_chart(df: pd.DataFrame,
                         x: str,
                         y: str,
                         title: str,
                         x_title: str,
                         y_title: str,
                         key_suffix: str = ""):

    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    groups = df['selected_folder_short'].unique()
    n = len(groups)

    fig = make_subplots(rows=1, cols=n, subplot_titles=groups)

    for i, group in enumerate(groups):
        group_df = df[df['selected_folder_short'] == group]
        count_df = group_df.groupby([x, y]).size().reset_index(name='count')

        # Build full (x, y) grid
        x_vals = np.arange(df[x].min(), df[x].max() + 1)
        y_vals = np.arange(df[y].min(), df[y].max() + 1)
        full_grid = pd.MultiIndex.from_product([x_vals, y_vals], names=[x, y]).to_frame(index=False)

        # Merge actual counts into full grid
        full_df = full_grid.merge(count_df, on=[x, y], how='left').fillna(0)

        # Pivot for heatmap
        pivot = full_df.pivot(index=y, columns=x, values='count')

        folder_color = df.loc[df['selected_folder_short'] == group, 'color'].iloc[0]

        heatmap = go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale=[[0, 'white'], [1, folder_color]],
            zmin=0,
            zmax=pivot.values.max(),
            showscale=False,
        )

        fig.add_trace(heatmap, row=1, col=i+1)
        fig.update_xaxes(scaleanchor=f'y{i+1}', row=1, col=i+1)

    fig.update_layout(
        title_text=title,
        height=500,
        margin=dict(l=50, r=50, t=80, b=80),
    )

    return fig



def create_bubble_chart(df: pd.DataFrame,
                         x: str,
                         y: str,
                         title: str,
                         x_title: str,
                         y_title: str,
                         key_suffix: str = "",):

    df['bubble_size'] = df.groupby([x, y, 'selected_folder_short'])[x].transform('count')
    df = df.sort_values('bubble_size', ascending=False)

    fig = px.scatter(
        df,
        x=x,
        y=y,
        size='bubble_size',
        color='selected_folder_short',
        color_discrete_map=dict(zip(
            df['selected_folder_short'].unique(),
            df.groupby('selected_folder_short')['color'].first()
        )),
        title=title,
        labels={
            x: x_title,
            y: y_title,
            'selected_folder_short': 'Selected Folder',
            'bubble_size': 'Count'
        },
        hover_data=[x, y, 'bubble_size', 'selected_folder_short'],
    )

    # Update traces for better visualization
    fig.update_traces(
        marker=dict(
            #line=dict(color='white', width=0.5),
            opacity=1
        )
    )

    # Update layout for better visualization
    fig.update_layout(
        height=500,
        margin=dict(l=50, r=50, t=80, b=100),
        hovermode='closest',
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )

    return fig


def get_hover_text(bin_edges, bin_size, folder, folder_data, hist, x):
    hover_text = []
    for i in range(len(hist)):
        if hist[i] > 0:
            if bin_size == 1:
                hover_text.append(f"Folder: {folder}<br>Size: {bin_edges[i]}<br>Total number of images: {hist[i]}")
            else:
                size_range = f"{bin_edges[i]}-{bin_edges[i + 1]}"
                breakdown = folder_data[(folder_data[x] >= bin_edges[i]) & (folder_data[x] < bin_edges[i + 1])][
                    x].value_counts().sort_index()
                breakdown_text = "<br>".join([f"{count} images with size {size}" for size, count in breakdown.items()])
                hover_text.append(
                    f"Folder: {folder}<br>Sizes: {size_range}<br>Total number of images: {hist[i]}<br>Breakdown:<br>{breakdown_text}")
        else:
            if hover_text:
                hover_text.append("")
    return hover_text


def get_x_ticks_params(bin_size, x_max, x_min):
    if x_min == x_max:
        start = x_min - 1
        end = x_max + 1
        tick_vals = [x_min - 1, x_min, x_min + 1]
        tick_text = [str(int(val)) for val in tick_vals]
    elif bin_size == 1:
        start = x_min - 1
        end = x_max + 1
        tick_vals = list(range(int(start + 1), int(end)))  # Exclude start and end
        tick_text = [str(val) for val in tick_vals]
    else:
        start = x_min - (x_min % bin_size)
        end = x_max + (bin_size - (x_max % bin_size))
        tick_vals = list(range(int(start), int(end) + int(bin_size), int(bin_size)))
        tick_text = [f"{val}-{val + bin_size - 1}" for val in tick_vals[:-1]]
        tick_vals = [val - bin_size / 2 for val in tick_vals[1:]]
    return end, start, tick_text, tick_vals


def get_bar_mode(key_suffix):
    bar_mode = st.radio(
        "Select Bar Mode",
        ["Stacked", "Grouped"],
        horizontal=True,
        key=f"bar_mode_{key_suffix}"
    )
    return bar_mode


def get_chart_type(key_suffix, chart_types_list):  # TODO: unite with get_bar_mode
    chart_type = st.radio(
        "Select Chart Type",
        chart_types_list,
        horizontal=True,
        key=f"chart_type_{key_suffix}"
    )
    return chart_type


def get_bin_size(x_min, x_max):
    range_value = x_max - x_min
    if range_value <= 100:
        bin_size = 1
    elif range_value <= 1000:
        bin_size = 10
    else:
        bin_size = 100
    return bin_size


def create_pattern_shapes(num_file_extensions):
    base_patterns = ['', '/', '\\', 'x', '+', '.']

    if num_file_extensions <= len(base_patterns):
        return base_patterns[:num_file_extensions]

    # For more file types, combine patterns
    extended_patterns = []
    for i in range(num_file_extensions):
        if i < len(base_patterns):
            extended_patterns.append(base_patterns[i])
        else:
            pattern1 = base_patterns[i % len(base_patterns)]
            pattern2 = base_patterns[(i + 1) % len(base_patterns)]
            extended_patterns.append(f"{pattern1}{pattern2}")
    return extended_patterns
