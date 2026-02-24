# streamlit_app.py
import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.workflow import create_workflow
from state import AgentState
import time

# Page configuration
st.set_page_config(
    page_title="AI Factory Growth Ranker",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 5px solid #1f77b4;
}
.company-card {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    background-color: #f9f9f9;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_companies_data():
    """Load companies data from JSON file."""
    try:
        with open('data/companies.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback data if file doesn't exist
        return [
            {"company_name": "Vertiv", "sector": "Cooling/Power", "operating_margin": 0.15, "growth_forecast": 1.40},
            {"company_name": "Arista Networks", "sector": "Networking", "operating_margin": 0.35, "growth_forecast": 1.25},
            {"company_name": "Schneider Electric", "sector": "Power", "operating_margin": 0.18, "growth_forecast": 1.15},
            {"company_name": "NVIDIA", "sector": "Compute/AI Hardware", "operating_margin": 0.60, "growth_forecast": 1.80}
        ]

@st.cache_resource
def get_workflow():
    """Create and cache the workflow."""
    return create_workflow()

def analyze_company(company_data, workflow):
    """Analyze a single company."""
    try:
        result = workflow.invoke(company_data)
        return result
    except Exception as e:
        st.error(f"Error analyzing {company_data['company_name']}: {str(e)}")
        return None

def main():
    st.markdown('<h1 class="main-header">🏭 AI Factory Growth Ranker</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("📊 Analysis Controls")
    
    # Load workflow
    try:
        workflow = get_workflow()
        st.sidebar.success("✅ LangGraph workflow loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"❌ Error loading workflow: {str(e)}")
        st.stop()
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Analysis", "📈 Rankings", "➕ Add Company", "ℹ️ About"])
    
    with tab1:
        analysis_tab(workflow)
    
    with tab2:
        rankings_tab(workflow)
    
    with tab3:
        add_company_tab()
    
    with tab4:
        about_tab()

def analysis_tab(workflow):
    """Analysis tab content."""
    st.header("Company Analysis")
    
    # Load companies
    companies = load_companies_data()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Company selection
        company_names = [comp['company_name'] for comp in companies]
        selected_company = st.selectbox("Select a company to analyze:", company_names)
        
        if selected_company:
            # Find selected company data
            company_data = next((comp for comp in companies if comp['company_name'] == selected_company), None)
            
            if company_data:
                # Display company info
                st.subheader(f"📊 {selected_company} Details")
                
                info_col1, info_col2, info_col3 = st.columns(3)
                with info_col1:
                    st.metric("Sector", company_data['sector'])
                with info_col2:
                    st.metric("Operating Margin", f"{company_data['operating_margin']:.1%}")
                with info_col3:
                    st.metric("Growth Forecast", f"{company_data['growth_forecast']:.2f}x")
                
                # Analyze button
                if st.button("🔍 Run Analysis", type="primary"):
                    with st.spinner(f"Analyzing {selected_company}..."):
                        result = analyze_company(company_data, workflow)
                        
                        if result:
                            st.success("Analysis completed!")
                            
                            # Display results
                            st.subheader("📋 Analysis Results")
                            
                            # Metrics
                            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                            with metric_col1:
                                st.metric("Margin Score", result.get('margin_score', 'N/A'))
                            with metric_col2:
                                st.metric("Moat Score", result.get('moat_score', 'N/A'))
                            with metric_col3:
                                st.metric("Final Score", f"{result.get('final_score', 0):.2f}")
                            with metric_col4:
                                st.metric("Growth Forecast", f"{result.get('growth_forecast', 1):.2f}x")
                            
                            # Moat analysis summary
                            if 'report_summary' in result:
                                st.subheader("🏰 Moat Analysis")
                                st.write(result['report_summary'])
                            
                            # Final report
                            if 'report' in result:
                                st.subheader("📄 Final Report")
                                st.info(result['report'])
    
    with col2:
        st.subheader("📚 TAFGS Formula")
        st.latex(r"TAFGS = (Moat\ Score \times Margin\ Score) \times Growth\ Forecast")
        
        with st.expander("Formula Components"):
            st.write("""
            **Moat Score (0-5):** Competitive defensibility analysis using LLM
            - Architectural lock-in
            - Ecosystem dominance
            - Switching costs
            - Supply chain position
            
            **Margin Score (1-5):** Operating margin strength
            - >40%: Score 5
            - >30%: Score 4  
            - >20%: Score 3
            - >10%: Score 2
            - ≤10%: Score 1
            
            **Growth Forecast:** Future growth multiplier
            """)

def rankings_tab(workflow):
    """Rankings tab content."""
    st.header("📈 Company Rankings")
    
    companies = load_companies_data()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🚀 Analyze All Companies", type="primary"):
            results = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, company in enumerate(companies):
                status_text.text(f"Analyzing {company['company_name']}...")
                result = analyze_company(company, workflow)
                if result:
                    results.append(result)
                progress_bar.progress((i + 1) / len(companies))
                time.sleep(0.5)  # Small delay for better UX
            
            status_text.text("Analysis complete!")
            
            if results:
                # Sort by final score
                ranked_results = sorted(results, key=lambda x: x.get('final_score', 0), reverse=True)
                
                # Display rankings
                st.subheader("🏆 Top Companies Ranking")
                
                for rank, result in enumerate(ranked_results, 1):
                    with st.container():
                        st.markdown(f"""
                        <div class="company-card">
                            <h4>#{rank} {result['company_name']}</h4>
                            <p><strong>Score:</strong> {result.get('final_score', 0):.2f}</p>
                            <p><strong>Sector:</strong> {result.get('sector', 'N/A')}</p>
                            <p><strong>Summary:</strong> {result.get('report_summary', 'N/A')[:200]}...</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Create visualization
                st.subheader("📊 Score Visualization")
                
                # Prepare data for plotting
                chart_data = pd.DataFrame([
                    {
                        'Company': result['company_name'],
                        'Final Score': result.get('final_score', 0),
                        'Moat Score': result.get('moat_score', 0),
                        'Margin Score': result.get('margin_score', 0),
                        'Sector': result.get('sector', 'N/A')
                    } for result in ranked_results
                ])
                
                # Bar chart
                fig = px.bar(
                    chart_data, 
                    x='Company', 
                    y='Final Score',
                    color='Sector',
                    title="TAFGS Scores by Company"
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
                
                # Scatter plot
                fig2 = px.scatter(
                    chart_data,
                    x='Moat Score',
                    y='Margin Score',
                    size='Final Score',
                    color='Sector',
                    hover_name='Company',
                    title="Moat Score vs Margin Score"
                )
                st.plotly_chart(fig2, use_container_width=True)

def add_company_tab():
    """Add company tab content."""
    st.header("➕ Add New Company")
    
    st.info("Add a new company to analyze. The data will be used for this session only.")
    
    with st.form("add_company_form"):
        company_name = st.text_input("Company Name")
        sector = st.selectbox("Sector", [
            "Cooling/Power", 
            "Networking", 
            "Power", 
            "Compute/AI Hardware",
            "Storage",
            "Software",
            "Other"
        ])
        operating_margin = st.slider("Operating Margin", 0.0, 1.0, 0.2, 0.01, format="%.2f")
        growth_forecast = st.slider("Growth Forecast", 0.5, 3.0, 1.2, 0.05, format="%.2f")
        
        submitted = st.form_submit_button("Add Company")
        
        if submitted and company_name:
            new_company = {
                "company_name": company_name,
                "sector": sector,
                "operating_margin": operating_margin,
                "growth_forecast": growth_forecast
            }
            
            # Add to session state
            if 'custom_companies' not in st.session_state:
                st.session_state.custom_companies = []
            
            st.session_state.custom_companies.append(new_company)
            st.success(f"Added {company_name} successfully!")
            
            # Show analysis option
            if st.button("🔍 Analyze This Company"):
                workflow = get_workflow()
                with st.spinner(f"Analyzing {company_name}..."):
                    result = analyze_company(new_company, workflow)
                    if result:
                        st.json(result)

def about_tab():
    """About tab content."""
    st.header("ℹ️ About AI Factory Growth Ranker")
    
    st.markdown("""
    ## 🎯 Project Objective
    
    The AI Factory Growth Ranker analyzes and ranks companies in the AI Factory Capital Stack using the **TAFGS (Total AI Factory Growth Score)** formula.
    
    ## 📊 TAFGS Formula
    
    ```
    TAFGS = (Moat Score × Margin Score) × Growth Forecast
    ```
    
    ### Components:
    
    - **🏰 Moat Score (0-5)**: Competitive defensibility analysis using LLM
      - Architectural lock-in (e.g., proprietary standards like CUDA)
      - Ecosystem dominance (design wins, reference architectures)
      - Switching costs / standard-setting influence
      - Scarcity or bottleneck position in the supply chain
    
    - **💰 Margin Score (1-5)**: Operating margin strength
      - Categorizes companies based on profitability metrics
    
    - **📈 Growth Forecast**: Future growth multiplier
      - AI-driven growth projections
    
    ## 🛠️ Technology Stack
    
    - **LangGraph**: Workflow orchestration
    - **Google Gemini**: LLM for moat analysis
    - **Streamlit**: Web interface
    - **Plotly**: Data visualization
    
    ## 🏗️ Architecture
    
    The system uses a multi-agent workflow:
    1. **Margin Analysis Agent**: Calculates margin scores
    2. **Moat Analysis Agent**: LLM-powered competitive analysis
    3. **Ranking Agent**: Computes final TAFGS score
    4. **Report Agent**: Generates investor-ready summaries
    """)
    
    # Technical details
    with st.expander("🔧 Technical Implementation"):
        st.code("""
        # Workflow Structure
        workflow = StateGraph(AgentState)
        workflow.add_node("analyze_margin", margin_analysis_agent)
        workflow.add_node("analyze_moat", moat_analysis_agent)
        workflow.add_node("calculate_rank", ranking_agent)
        workflow.add_node("generate_report", report_agent)
        """, language="python")

if __name__ == "__main__":
    main()