from plotly.graph_objects import (Figure, Layout)
from plotly.graph_objs.layout import (XAxis, Margin)

myLayout = Layout(
    paper_bgcolor='#0a0a0a',
    plot_bgcolor='#0a0a0a',
    margin={
        'b': 16, 'l': 16, 'pad': 0, 'r': 16, 't': 32
    },
    xaxis = {
        'showline' : True,
        'linecolor' : '#282828',
        'linewidth' : 4,
        'gridcolor' : '#282828',
        'gridwidth' : 1,
        'mirror': True,
    },
    yaxis = {
        'showline' : True,
        'linecolor' : '#282828',
        'linewidth' : 4,
        'gridcolor' : '#282828',
        'gridwidth' : 1,
        'mirror': True,
        'side': 'right',
    },
    xaxis2={
        'showline': True,
        'linecolor': '#282828',
        'linewidth': 4,
        'gridcolor': '#282828',
        'gridwidth': 1,
        'mirror': True,
        'anchor': 'y2'  # Tells this axis to align with y2
    },
    yaxis2={
        'showline': True,
        'linecolor': '#282828',
        'linewidth': 4,
        'gridcolor': '#282828',
        'gridwidth': 1,
        'mirror': True,
        'side': 'right',
        'anchor': 'x2'  # Tells this axis to align with x2
    }
    
)