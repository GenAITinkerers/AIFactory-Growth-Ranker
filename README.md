# AI Factory Growth Ranker

## Project Objective

Analyze and rank companies in the AI Factory Capital Stack using the TAFGS (Total AI Factory Growth Score) formula.

## TAFGS Formula

```
TAFGS = (Moat Score × Margin Score) × Growth Forecast
```

Where:

- **Moat Score** (0-5): Competitive defensibility analysis using LLM
- **Margin Score** (1-5): Operating margin strength
- **Growth Forecast**: Future growth multiplier

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd AIFactory-Growth-Ranker
```

2. Create and activate virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up your Google API key in `config/settings.py`

## Usage

Run the main analysis:

```bash
python main.py
```

## Project Structure

```
AIFactory-Growth-Ranker/
├── agents/           # Individual agent modules
├── config/           # Configuration and settings
├── data/            # Company data files
├── notebooks/       # Jupyter notebooks
├── utils/           # Utility functions
├── main.py          # Entry point
├── state.py         # Shared state definition
└── requirements.txt # Dependencies
```

# AIFactory-Growth-Ranker

AI factory

AIFactory-Growth-Ranker/
│
├── agents/                    # Individual agent modules
│   ├── moat_agent.py
│   ├── margin_agent.py
│   ├── growth_agent.py
│   └── __init__.py
│
├── data/                      # Company data (CSVs, JSONs, etc.)
│   ├── companies.csv
│   └── sample_input.json
│
├── notebooks/                 # Jupyter notebooks for prototyping and visualization
│   ├── deep_research.ipynb
│   └── deep_research_with_llm.ipynb
│
├── state.py                   # AgentState TypedDict and shared types
├── main.py                    # Entry point: runs the full Top 20 ranking pipeline
├── requirements.txt           # All dependencies (langgraph, langchain, etc.)
├── README.md                  # Project Objective, TAFGS Formula, usage instructions
└── .gitignore                 # Ignore venvs, __pycache__, .ipynb_checkpoints, etc.

**Key Points:**

* Each agent (moat, margin, growth) is a separate module in `agents/`.
* All data files are in `data/`.
* Notebooks are in `notebooks/` for experimentation and visualization.
* `main.py` is the CLI/entry point for running the ranking end-to-end.
* `state.py` holds the shared state definition (`AgentState`).
* `requirements.txt` for reproducible environments.

###### Running python app:

`python main.py`

### Web Interface (Streamlit)

Launch the interactive web app:

```bash
streamlit run streamlit_app.py
```

Or use the launch script:

```bash
chmod +x run_streamlit.sh
./run_streamlit.sh
```

The app will be available at `http://localhost:8501`

### Command Line Interface

Run the CLI version:

```bash
python main.py
```

## Features

### Web App Features:

- 🔍 **Interactive Analysis**: Select and analyze individual companies
- 📈 **Batch Rankings**: Analyze all companies and view rankings
- ➕ **Add Companies**: Add new companies for analysis
- 📊 **Visualizations**: Interactive charts and graphs
- 📱 **Responsive Design**: Works on desktop and mobile

### Analysis Capabilities:

- Real-time LLM-powered moat analysis
- TAFGS score calculation
- Competitive positioning insights
- Growth forecasting



## Key Features of the Streamlit App:

1. **🔍 Analysis Tab** :

* Select companies for individual analysis
* View detailed results with metrics
* Interactive formula explanation

1. **📈 Rankings Tab** :

* Batch analyze all companies
* Visual rankings with charts
* Comparative analysis

1. **➕ Add Company Tab** :

* Add new companies dynamically
* Immediate analysis capability

1. **ℹ️ About Tab** :

* Project documentation
* Technical implementation details

1. **📊 Visualizations** :

* Bar charts for scores
* Scatter plots for comparisons
* Interactive Plotly charts
