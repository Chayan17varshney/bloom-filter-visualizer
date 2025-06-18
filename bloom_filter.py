# bloom_filter_app.py

import torch
import hashlib
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# ---------------------------
# Core Bloom Filter Class
# ---------------------------
class BloomFilter:
    def __init__(self, size=500, num_hashes=3):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = torch.zeros(size, dtype=torch.bool)
        self.items = set()

    def _hashes(self, item):
        hashes = []
        for i in range(self.num_hashes):
            data = f"{item}_{i}".encode()
            digest = hashlib.md5(data).hexdigest()
            index = int(digest, 16) % self.size
            hashes.append(index)
        return hashes

    def add(self, item):
        for idx in self._hashes(item):
            self.bit_array[idx] = True
        self.items.add(item)

    def might_contain(self, item):
        return all(self.bit_array[idx] for idx in self._hashes(item))

    def fill_ratio(self):
        return self.bit_array.float().mean().item()

    def false_positive_rate(self):
        p = self.fill_ratio()
        return (p ** self.num_hashes)

# ---------------------------
# Dash App Setup
# ---------------------------
bloom = BloomFilter()

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = "Bloom Filter Visualizer"

app.layout = dbc.Container([
    html.H2("🔍 Bloom Filter Visualizer (Python + PyTorch)", className="my-3 text-center"),

    dbc.Row([
        dbc.Col([
            dbc.Input(id='item-input', placeholder='Enter an item...', type='text', debounce=True),
        ], width=6),
        dbc.Col([
            dbc.Button("Add", id='add-btn', n_clicks=0, color='primary', className='me-2'),
            dbc.Button("Check", id='check-btn', n_clicks=0, color='secondary')
        ], width=6),
    ], className='mb-3'),

    html.Div(id='message-output', className='my-2'),

    dcc.Graph(id='bit-array-graph'),

    html.Div([
        html.P("Fill Ratio: ", style={'display': 'inline'}),
        html.Span(id='fill-ratio', style={'fontWeight': 'bold'}),
        html.P("False Positive Rate: ", style={'display': 'inline', 'marginLeft': '20px'}),
        html.Span(id='fp-rate', style={'fontWeight': 'bold'}),
    ], className='mt-3')
])

# ---------------------------
# Callback Logic
# ---------------------------
@app.callback(
    Output('bit-array-graph', 'figure'),
    Output('message-output', 'children'),
    Output('fill-ratio', 'children'),
    Output('fp-rate', 'children'),
    Input('add-btn', 'n_clicks'),
    Input('check-btn', 'n_clicks'),
    State('item-input', 'value')
)
def update_output(n_add, n_check, item):
    if not item:
        return go.Figure(), "⚠️ Please enter an item.", "", ""

    action = "add" if n_add >= n_check else "check"
    if action == "add":
        bloom.add(item)
        msg = f'✅ "{item}" added to Bloom Filter.'
    else:
        result = bloom.might_contain(item)
        msg = f'🔎 "{item}" is {"possibly present" if result else "definitely not present"}.'

    # Visualization
    fig = go.Figure(data=go.Heatmap(
        z=[bloom.bit_array.int().tolist()],
        showscale=False,
        colorscale='Viridis'
    ))
    fig.update_layout(
        height=120,
        margin=dict(t=20, b=20, l=20, r=20),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        title="Bloom Filter Bit Array"
    )

    # Stats
    fill = f"{bloom.fill_ratio() * 100:.2f}%"
    fp = f"{bloom.false_positive_rate() * 100:.4f}%"
    return fig, msg, fill, fp

# ---------------------------
# Run the App
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)

