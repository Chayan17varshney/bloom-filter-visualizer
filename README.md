# Bloom Filter Visualizer

An interactive, educational web app that demonstrates how Bloom Filters work using Python, Dash, Plotly, and PyTorch.

This tool lets you add or test elements, view live updates to a bit array, and observe real-time stats like fill ratio and estimated false positive rate. Ideal for learning, teaching, and exploring probabilistic data structures.

---

## Features

- Add and test items in a Bloom Filter
- Visual heatmap of the bit array
- Real-time stats:
  - Bits set
  - Fill ratio
  - False positive rate
- Multiple hash functions
- Clean, responsive web UI (Dash + Bootstrap)

---

## Tech Stack

- **Python 3.8+**
- [Dash](https://dash.plotly.com/) for interactive UI
- [Plotly](https://plotly.com/python/) for visualizations
- [PyTorch](https://pytorch.org/) for efficient bit manipulation
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)

---

## Getting Started

### 1. Clone the repo

git clone https://github.com/your-username/bloom-filter-visualizer.git
cd bloom-filter-visualizer

### 2. Install dependencies
pip install -r requirements.txt

### 3. Run the app

python bloom_filter.py

Then open your browser at: http://127.0.0.1:8050/

### About Bloom Filters

A Bloom Filter is a space-efficient, probabilistic data structure used to test whether an element is a member of a set. False positives are possible, but false negatives are not.

### Credits

Created by @Chayan17varshney



