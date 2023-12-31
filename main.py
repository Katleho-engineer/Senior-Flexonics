import panel as pn
from styleframe import StyleFrame

pn.extension('tabulator')

import hvplot.pandas
from models import (
    text_to_excel,
    read_excel_data,
    test_list,
    bound_list,
    plot_slopes,
    analyze,
)

text_to_excel('text_data', 'excel_data')

select_slope = pn.widgets.Select(name='Select', options=test_list())

select_hysteresis = pn.widgets.Select(name='Select', options=test_list())

# -------------------------------------  Slope  ------------------------------------- #

slope_slider_lower = pn.widgets.IntSlider(name='Slope lower boundary', start=min(bound_list()), end=max(bound_list()),
                                          step=1, value=0)
slope_slider_upper = pn.widgets.IntSlider(name='Slope upper boundary', start=min(bound_list()), end=max(bound_list()),
                                          step=1, value=2)

# ------------------------------------- Hysteresis slider ------------------------------------- #

hysteresis_slider = pn.widgets.IntSlider(name='Hysteresis', start=min(bound_list()), end=max(bound_list()), step=1,
                                         value=1)


# ------------------------------------- data ------------------------------------- #


@pn.depends(slope_slider_lower.param.value,
            slope_slider_upper.param.value,
            hysteresis_slider.param.value)
def data(slope_lower, slope_upper, hysteresis):
    slope_lower = slope_lower
    slope_upper = slope_upper
    hysteresis = hysteresis

    df = analyze(slope_lower, slope_upper, hysteresis)

    return df


# ------------------------------------- Results ------------------------------------- #
@pn.depends(slope_slider_lower.param.value,
            slope_slider_upper.param.value,
            hysteresis_slider.param.value)
def results(slope_lower, slope_upper, hysteresis):
    slope_lower = slope_lower
    slope_upper = slope_upper
    hysteresis = hysteresis

    df = analyze(slope_lower, slope_upper, hysteresis)

    table = pn.widgets.Tabulator(df)

    return table


# ------------------------------------- Plots ------------------------------------- #

@pn.depends(select_slope.param.value)
def plot_slopes(graph_name):
    df = read_excel_data(graph_name, 'excel_data')

    graph = df.hvplot.scatter(x='Extension (mm)', y='Load (N)', title=graph_name, color='#058805', padding=0.1,
                              legend='top', height=500, width=900)

    return graph


@pn.depends(select_hysteresis.param.value)
def plot_hysteresis(graph_name):
    df = read_excel_data(graph_name, 'excel_data')

    # graph = df.hvplot.line(x='Extension (mm)', y='Load (N)', title=graph_name)
    graph = df.hvplot.scatter(x='Extension (mm)', y='Load (N)', title=graph_name, color='#058805', padding=0.1,
                              legend='top', height=600, width=900)
    return graph


# ------------------------------------- Analysis ------------------------------------- #
select_x_axis = pn.widgets.Select(name='X-axis', options=list(data(slope_slider_lower.value,
                                                                   slope_slider_upper.value,
                                                                   hysteresis_slider.value)))

select_y_axis = pn.widgets.Select(name='Y-axis', options=list(data(slope_slider_lower.value,
                                                                   slope_slider_upper.value,
                                                                   hysteresis_slider.value)))


@pn.depends(slope_slider_lower.param.value,
            slope_slider_upper.param.value,
            hysteresis_slider.param.value,
            select_x_axis.param.value,
            select_y_axis.param.value)
def plot_analysis(slope_lower, slope_upper, hysteresis, x_axis, y_axis):
    slope_lower = slope_lower
    slope_upper = slope_upper
    hysteresis = hysteresis

    df = analyze(slope_lower, slope_upper, hysteresis)

    graph = df.hvplot.scatter(x=x_axis, y=y_axis, by='Test',
                              height=600, width=900)

    return graph


# ------------------------------------- Slope ------------------------------------- #

@pn.depends(slope_slider_lower.param.value, slope_slider_upper.param.value)
def slope_text(lower, upper):
    text = pn.widgets.TextInput(value=f'Slope is measured between {lower} and {upper}.')
    return text


@pn.depends(select_slope.param.value,
            hysteresis_slider.param.value,
            slope_slider_lower.param.value,
            slope_slider_upper.param.value)
def slope_number_below(graph_name, hysteresis, slope_lower, slope_upper):
    df = analyze(slope_lower, slope_upper, hysteresis)
    df.set_index("Test", inplace=True)

    low = df.loc[graph_name]['Slope below (N/mm)']
    text = pn.widgets.TextInput(value=f'Slope below is {round(low, 3)} N/mm.')
    return text


@pn.depends(select_slope.param.value,
            hysteresis_slider.param.value,
            slope_slider_lower.param.value,
            slope_slider_upper.param.value)
def slope_number_above(graph_name, hysteresis, slope_lower, slope_upper):
    df = analyze(slope_lower, slope_upper, hysteresis)
    df.set_index("Test", inplace=True)

    up = df.loc[graph_name]['Slope above (N/mm)']
    text = pn.widgets.TextInput(value=f'Slope below is {round(up, 3)} N/mm.')
    return text


# ------------------------------------- Hysteresis ------------------------------------- #


@pn.depends(select_hysteresis.param.value,
            hysteresis_slider.param.value,
            slope_slider_lower.param.value,
            slope_slider_upper.param.value)
def hysteresis_force(graph_name, hysteresis, slope_lower, slope_upper):
    df = analyze(slope_lower, slope_upper, hysteresis)
    df.set_index("Test", inplace=True)

    force = df.loc[graph_name][f'Hysteresis at {hysteresis}mm (N)']
    text = pn.widgets.TextInput(value=f'Force is {round(force, 4)} N')
    return text


@pn.depends(hysteresis_slider.param.value)
def hysteresis_text(hysteresis):
    text = pn.widgets.TextInput(value=f'Hysteresis is at {hysteresis} mm')
    return text


# ------------------------------------- Save------------------------------------- #

def save_results(event):
    df = data(slope_slider_lower.value, slope_slider_upper.value, hysteresis_slider.value)

    excel_writer = StyleFrame.ExcelWriter('save/Results.xlsx')
    sf = StyleFrame(df)
    sf.to_excel(excel_writer=excel_writer, row_to_add_filters=0, best_fit=list(df),
                columns_and_rows_to_freeze='B2')
    excel_writer.save()


save_button = pn.widgets.Button(name='Download results', button_type='success')

save_button.on_click(save_results)
# ------------------------------------- Tabs ------------------------------------- #

tabs = pn.Tabs(
    ('Settings', pn.Column(pn.pane.Markdown('# Instructions'),
                           pn.pane.Markdown('### 1. Set the lower boundary for slope.'),
                           pn.pane.Markdown('### 2. Set the upper boundary for slope.'),
                           pn.pane.Markdown('### 3. The value for lower boundary must be less than that of upper '
                                            'bouncary.'),
                           pn.pane.Markdown('### 4. Set the value for hysteresis.'),
                           pn.pane.Markdown('## The sliders are below!'),
                           slope_slider_lower,
                           slope_slider_upper,
                           hysteresis_slider,
                           pn.pane.Markdown('## You can go different tabs to see the results.')
                           )),
    ('Slope', pn.Column(select_slope, slope_text, pn.Row(slope_number_below, slope_number_above), plot_slopes)),
    ('Hysteresis', pn.Column(select_hysteresis, pn.Row(hysteresis_text, hysteresis_force), plot_hysteresis)),
    ('Results', pn.Column(results, save_button)),
    ('Analysis', pn.Column(pn.Row(select_x_axis, select_y_axis), plot_analysis)),
    dynamic=True
)

template = pn.template.FastListTemplate(
    site='Senior Flexonics',
    title='Data Processing',
    sidebar=[pn.pane.Markdown("# Global innovation from South Africa"),
             pn.pane.Markdown("#### Senior Flexonics Cape Town delivers world-class precision vehicle and engine "
                              "technology components to markets across the globe."),
             pn.pane.PNG('Images/SLR.png', sizing_mode='scale_both'),
             pn.pane.Markdown("#### At Senior Flexonics Cape Town, we have the technical expertise to design, develop "
                              "and manufacture solutions that exceed our customers’ expectations."),
             pn.pane.PNG('Images/Simulation-to-Product.png', sizing_mode='scale_both')
             ],
    main=[tabs],
)

template.show()
