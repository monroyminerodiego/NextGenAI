import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Employee Analysis Dashboard",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with modern tech colors and Tabler icons
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css');
    
    /* Modern tech color scheme */
    :root {
        --primary-blue: #0066ff;
        --secondary-purple: #6366f1;
        --accent-cyan: #06b6d4;
        --dark-bg: #0f172a;
        --light-bg: #1e293b;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --success-green: #10b981;
        --warning-orange: #f59e0b;
        --error-red: #ef4444;
        --gradient-primary: linear-gradient(135deg, #0066ff, #6366f1);
        --gradient-secondary: linear-gradient(135deg, #06b6d4, #8b5cf6);
    }
    
    .main > div {
        background: var(--dark-bg);
        color: var(--text-primary);
    }
    
    .stApp {
        background: var(--dark-bg);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: var(--light-bg);
    }
    
    /* Metric cards styling */
    .metric-card {
        background: var(--gradient-primary);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        color: var(--text-primary);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: var(--text-primary);
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 2rem 0 1rem 0;
        color: var(--text-primary);
    }
    
    .section-icon {
        font-size: 1.5rem;
        color: var(--accent-cyan);
    }
    
    /* Chart containers */
    .chart-container {
        background: var(--light-bg);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }
    
    .chart-description {
        background: rgba(99, 102, 241, 0.1);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid var(--secondary-purple);
        margin-top: 1rem;
        color: var(--text-primary);
        font-size: 0.95rem;
        line-height: 1.8;
    }
    
    /* Improved list styling */
    .chart-description ul {
        margin: 1rem 0;
        padding-left: 1.5rem;
    }
    
    .chart-description li {
        margin-bottom: 0.8rem;
        list-style: none;
        position: relative;
        color: var(--text-primary);
    }
    
    .chart-description li:before {
        content: "▶";
        color: var(--accent-cyan);
        font-size: 0.8rem;
        position: absolute;
        left: -1.2rem;
        top: 0.1rem;
    }
    
    .chart-description strong {
        color: var(--accent-cyan);
        font-weight: 600;
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        color: var(--text-secondary);
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    /* Filter section */
    .filter-header {
        color: var(--accent-cyan);
        font-weight: bold;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Insight boxes */
    .insight-box {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .insight-title {
        color: var(--success-green);
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .insight-content {
        color: var(--text-primary);
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("work (1).csv")

df = load_data()

# Header section with title and brief description
st.markdown("""
<div class="main-title">
    <i class="ti ti-chart-dots"></i> Employee Analysis Dashboard
</div>
<div class="subtitle">
    This interactive dashboard provides comprehensive analysis of employee data, allowing exploration of various aspects such as salaries, 
    productivity, department distribution, and more. Use the filters in the sidebar to customize the visualization and gain insights 
    into workforce patterns and trends.
    <br><br>
    <strong>Created by:</strong> Sergio Barrera, Ariel Buenfil, Damaris Dzul, Diego Monroy, and Alan Valbuena
</div>
""", unsafe_allow_html=True)

# Sidebar with filters
st.sidebar.markdown("""
<div class="filter-header">
    <i class="ti ti-filter"></i> Filters
</div>
""", unsafe_allow_html=True)

# Department filter
departments = df['departamento'].unique()
selected_depts = st.sidebar.multiselect(
    "🏢 Department(s)", 
    departments, 
    default=departments
)

# Education level filter
education = df['nivel_educacion'].unique()
selected_edu = st.sidebar.multiselect(
    "🎓 Education Level", 
    education, 
    default=education
)

# Geographic zone filter
zones = df['zona_geografica'].unique()
selected_zones = st.sidebar.multiselect(
    "🌍 Geographic Zone", 
    zones, 
    default=zones
)

# Work modality filter
modalities = df['modalidad_trabajo'].unique()
selected_modal = st.sidebar.multiselect(
    "💻 Work Modality", 
    modalities, 
    default=modalities
)

# Age range filter
min_age, max_age = int(df['edad'].min()), int(df['edad'].max())
age_range = st.sidebar.slider(
    "📅 Age Range", 
    min_age, max_age, 
    (min_age, max_age)
)

# Salary range filter
min_salary, max_salary = int(df['salario_anual'].min()), int(df['salario_anual'].max())
salary_range = st.sidebar.slider(
    "💰 Annual Salary Range", 
    min_salary, max_salary, 
    (min_salary, max_salary)
)

# Apply filters
filtered_df = df[
    (df['departamento'].isin(selected_depts)) &
    (df['nivel_educacion'].isin(selected_edu)) &
    (df['zona_geografica'].isin(selected_zones)) &
    (df['modalidad_trabajo'].isin(selected_modal)) &
    (df['edad'].between(age_range[0], age_range[1])) &
    (df['salario_anual'].between(salary_range[0], salary_range[1]))
]

# Summary statistics / KPI cards
st.markdown("""
<div class="section-header">
    <i class="ti ti-dashboard section-icon"></i>
    <h2>Key Performance Indicators</h2>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon"><i class="ti ti-users"></i></div>
        <div class="metric-value">{len(filtered_df)}</div>
        <div class="metric-label">Total Employees</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    avg_salary = filtered_df['salario_anual'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon"><i class="ti ti-cash"></i></div>
        <div class="metric-value">${avg_salary:,.0f}</div>
        <div class="metric-label">Average Salary</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_age = filtered_df['edad'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon"><i class="ti ti-calendar"></i></div>
        <div class="metric-value">{avg_age:.1f} years</div>
        <div class="metric-label">Average Age</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_productivity = filtered_df['productividad_score'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon"><i class="ti ti-target"></i></div>
        <div class="metric-value">{avg_productivity:.1f}/100</div>
        <div class="metric-label">Average Productivity</div>
    </div>
    """, unsafe_allow_html=True)

# Visualization 1: Salary distribution by department
st.markdown("""
<div class="section-header">
    <i class="ti ti-chart-box section-icon"></i>
    <h2>Salary Distribution by Department</h2>
</div>
""", unsafe_allow_html=True)

# High contrast color palette for better differentiation
dept_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF', '#5F27CD']

fig1 = px.box(
    filtered_df, 
    x='departamento', 
    y='salario_anual',
    color='departamento',
    labels={'salario_anual': 'Annual Salary', 'departamento': 'Department'},
    height=500,
    color_discrete_sequence=dept_colors
)
fig1.update_layout(
    showlegend=False,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#f8fafc',
    xaxis_title_font_size=14,
    yaxis_title_font_size=14
)
fig1.update_traces(
    marker_line_color='rgba(255,255,255,0.5)',
    marker_line_width=1.5
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("""
<div class="chart-description">
<div class="insight-box">
    <div class="insight-title">📊 Chart Analysis</div>
    <div class="insight-content">
        This box plot visualization reveals the salary distribution patterns across different departments, providing critical insights into compensation equity and departmental value propositions. Each box represents the interquartile range (IQR) containing 50% of salaries, with the median salary displayed as a horizontal line within the box.
    </div>
</div>

<div class="insight-box">
    <div class="insight-title">🔍 Key Insights</div>
    <div class="insight-content">
        <ul>
            <li><strong>Median Comparison:</strong> The horizontal line in each box allows direct comparison of typical salaries across departments</li>
            <li><strong>Salary Spread:</strong> Box height indicates salary consistency within departments - taller boxes suggest more varied compensation</li>
            <li><strong>Outlier Analysis:</strong> Individual points reveal exceptional high or low salaries that may warrant investigation</li>
            <li><strong>Departmental Equity:</strong> This visualization helps identify potential pay gaps and informs compensation standardization efforts</li>
        </ul>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

# Visualization 2: Relationship between salary and experience
st.markdown("""
<div class="section-header">
    <i class="ti ti-chart-scatter section-icon"></i>
    <h2>Salary vs Experience Relationship</h2>
</div>
""", unsafe_allow_html=True)

# High contrast colors for education levels
education_colors = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6', '#1ABC9C']

fig2 = px.scatter(
    filtered_df,
    x='experiencia_anos',
    y='salario_anual',
    color='nivel_educacion',
    size='productividad_score',
    hover_data=['edad', 'genero'],
    labels={
        'experiencia_anos': 'Years of Experience',
        'salario_anual': 'Annual Salary',
        'nivel_educacion': 'Education Level',
        'productividad_score': 'Productivity Score'
    },
    height=500,
    color_discrete_sequence=education_colors
)
fig2.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#f8fafc',
    legend=dict(
        bgcolor='rgba(30, 41, 59, 0.8)',
        bordercolor='rgba(255,255,255,0.3)',
        borderwidth=1
    )
)
fig2.update_traces(
    marker_line_color='rgba(255,255,255,0.3)',
    marker_line_width=0.5
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
<div class="chart-description">
<div class="insight-box">
    <div class="insight-title">📊 Chart Analysis</div>
    <div class="insight-content">
        This advanced scatter plot explores the multifaceted relationship between professional experience, compensation, education, and productivity. Each point represents an individual employee, with position indicating their experience-salary relationship, color denoting education level, and size reflecting productivity score.
    </div>
</div>

<div class="insight-box">
    <div class="insight-title">🔍 Key Insights</div>
    <div class="insight-content">
        <ul>
            <li><strong>Experience-Salary Correlation:</strong> The upward trend reveals how experience typically translates to higher compensation</li>
            <li><strong>Education Premium:</strong> Color clustering shows whether advanced degrees command salary premiums at similar experience levels</li>
            <li><strong>Productivity Impact:</strong> Larger circles indicate high-performing employees - analyze if they receive proportional compensation</li>
            <li><strong>Career Progression:</strong> Steep salary increases with experience suggest clear advancement opportunities</li>
            <li><strong>Outlier Investigation:</strong> Points that deviate from the trend may indicate unique circumstances worth exploring</li>
        </ul>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

# Visualization 3: Distribution by gender and work modality
st.markdown("""
<div class="section-header">
    <i class="ti ti-chart-pie section-icon"></i>
    <h2>Gender and Work Modality Distribution</h2>
</div>
""", unsafe_allow_html=True)

# High contrast colors for sunburst
sunburst_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3']

fig3 = px.sunburst(
    filtered_df,
    path=['genero', 'modalidad_trabajo'],
    color='genero',
    height=600,
    color_discrete_sequence=sunburst_colors
)
fig3.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='#f8fafc',
    font_size=12
)
fig3.update_traces(
    textinfo='label+percent parent',
    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent parent}<extra></extra>'
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
<div class="chart-description">
<div class="insight-box">
    <div class="insight-title">📊 Chart Analysis</div>
    <div class="insight-content">
        This hierarchical sunburst visualization provides a comprehensive view of workforce composition through the lens of gender and work modality preferences. The inner ring displays gender distribution, while the outer segments reveal work arrangement patterns within each gender group.
    </div>
</div>

<div class="insight-box">
    <div class="insight-title">🔍 Key Insights</div>
    <div class="insight-content">
        <ul>
            <li><strong>Gender Balance:</strong> The inner ring proportions indicate overall gender representation in the organization</li>
            <li><strong>Work Preference Patterns:</strong> Outer segments reveal if certain work modalities are preferred by specific gender groups</li>
            <li><strong>Flexible Work Adoption:</strong> The relative sizes of remote, hybrid, and on-site segments show organizational flexibility</li>
            <li><strong>Diversity Metrics:</strong> This visualization supports diversity and inclusion initiatives by highlighting potential disparities</li>
            <li><strong>Policy Impact:</strong> Understanding these patterns helps inform work-from-home policies and accommodation strategies</li>
        </ul>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

# Visualization 4: Job satisfaction vs. working hours
st.markdown("""
<div class="section-header">
    <i class="ti ti-chart-area section-icon"></i>
    <h2>Job Satisfaction vs Working Hours</h2>
</div>
""", unsafe_allow_html=True)

# High contrast colors for departments in contour plot
contour_colors = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6', '#1ABC9C', '#E67E22', '#34495E']

fig4 = px.density_contour(
    filtered_df,
    x='horas_semanales',
    y='satisfaccion_laboral',
    color='departamento',
    marginal_x='histogram',
    marginal_y='histogram',
    height=600,
    labels={
        'horas_semanales': 'Weekly Hours',
        'satisfaccion_laboral': 'Job Satisfaction',
        'departamento': 'Department'
    },
    color_discrete_sequence=contour_colors
)
fig4.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#f8fafc',
    legend=dict(
        bgcolor='rgba(30, 41, 59, 0.8)',
        bordercolor='rgba(255,255,255,0.3)',
        borderwidth=1
    )
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("""
<div class="chart-description">
<div class="insight-box">
    <div class="insight-title">📊 Chart Analysis</div>
    <div class="insight-content">
        This sophisticated density contour plot with marginal histograms examines the critical relationship between working hours and job satisfaction across different departments. The contour lines represent concentration zones where multiple employees share similar hour-satisfaction combinations.
    </div>
</div>

<div class="insight-box">
    <div class="insight-title">🔍 Key Insights</div>
    <div class="insight-content">
        <ul>
            <li><strong>Optimal Work-Life Balance:</strong> Dense concentration areas reveal the 'sweet spot' where employees report highest satisfaction</li>
            <li><strong>Overwork Detection:</strong> Employees with high hours but low satisfaction may be experiencing burnout</li>
            <li><strong>Departmental Patterns:</strong> Different colored contours show if certain departments have unique hour-satisfaction relationships</li>
            <li><strong>Distribution Analysis:</strong> Marginal histograms reveal the overall distribution of working hours and satisfaction levels</li>
            <li><strong>Policy Implications:</strong> This visualization informs decisions about maximum working hours and workload management</li>
            <li><strong>Early Warning System:</strong> Areas with high hours but declining satisfaction can identify at-risk employee groups</li>
        </ul>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

# Visualization 5: Correlation heatmap
st.markdown("""
<div class="section-header">
    <i class="ti ti-chart-grid-dots section-icon"></i>
    <h2>Variable Correlation Matrix</h2>
</div>
""", unsafe_allow_html=True)

numeric_cols = filtered_df.select_dtypes(include=['int64', 'float64']).columns
corr_matrix = filtered_df[numeric_cols].corr()

# High contrast heatmap colors
fig5 = go.Figure(
    go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns.values,
        y=corr_matrix.columns.values,
        colorscale=[
            [0, '#E74C3C'],      # Strong negative (red)
            [0.25, '#F39C12'],   # Weak negative (orange)
            [0.5, '#2C3E50'],    # No correlation (dark)
            [0.75, '#3498DB'],   # Weak positive (blue)
            [1, '#2ECC71']       # Strong positive (green)
        ],
        zmin=-1,
        zmax=1,
        text=corr_matrix.round(2).values,
        texttemplate="%{text}",
        textfont={"size": 11, "color": "#f8fafc"},
        hoverongaps=False,
        hovertemplate='<b>%{y} vs %{x}</b><br>Correlation: %{z}<extra></extra>'
    )
)
fig5.update_layout(
    height=600,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#f8fafc',
    xaxis_title_font_size=12,
    yaxis_title_font_size=12
)
st.plotly_chart(fig5, use_container_width=True)

st.markdown("""
<div class="chart-description">
<div class="insight-box">
    <div class="insight-title">📊 Chart Analysis</div>
    <div class="insight-content">
        This comprehensive correlation heatmap reveals the linear relationships between all numerical variables in the dataset, using a high-contrast color scheme for maximum clarity. Each cell represents the correlation coefficient between two variables, ranging from -1 (perfect negative correlation) to +1 (perfect positive correlation).
    </div>
</div>

<div class="insight-box">
    <div class="insight-title">🎨 Color Interpretation</div>
    <div class="insight-content">
        <ul>
            <li><strong>Green (0.7 to 1.0):</strong> Strong positive correlation - variables move together</li>
            <li><strong>Blue (0.3 to 0.7):</strong> Moderate positive correlation - some relationship exists</li>
            <li><strong>Dark (-0.3 to 0.3):</strong> Weak or no correlation - variables are independent</li>
            <li><strong>Orange (-0.7 to -0.3):</strong> Moderate negative correlation - variables move in opposite directions</li>
            <li><strong>Red (-1.0 to -0.7):</strong> Strong negative correlation - variables are inversely related</li>
        </ul>
    </div>
</div>

<div class="insight-box">
    <div class="insight-title">🎯 Strategic Applications</div>
    <div class="insight-content">
        <ul>
            <li><strong>Performance Drivers:</strong> Identify which factors most strongly correlate with productivity and satisfaction</li>
            <li><strong>Compensation Equity:</strong> Understand if salary correlates appropriately with experience, education, and performance</li>
            <li><strong>Workforce Planning:</strong> Use correlations to predict outcomes and plan interventions</li>
            <li><strong>Risk Assessment:</strong> Identify concerning negative correlations that might indicate systemic issues</li>
        </ul>
    </div>
</div>
</div>
""", unsafe_allow_html=True)
# Visualization 6: Dendrogram for Employee Clustering
st.markdown("""
<div class="section-header">
    <i class="ti ti-git-branch section-icon"></i>
    <h2>Employee Hierarchical Clustering</h2>
</div>
""", unsafe_allow_html=True)

# Prepare data for clustering
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist
import numpy as np

# Select numerical columns for clustering
clustering_cols = ['edad', 'salario_anual', 'experiencia_anos', 'productividad_score', 
                  'satisfaccion_laboral', 'horas_semanales']
clustering_data = filtered_df[clustering_cols].fillna(filtered_df[clustering_cols].mean())

# Normalize the data for better clustering
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
normalized_data = scaler.fit_transform(clustering_data)

# Sample data for better visualization (reduce to 30 for cleaner display)
if len(normalized_data) > 30:
    sample_indices = np.random.choice(len(normalized_data), 30, replace=False)
    sample_data = normalized_data[sample_indices]
    sample_df = filtered_df.iloc[sample_indices].reset_index(drop=True)
else:
    sample_data = normalized_data
    sample_df = filtered_df.reset_index(drop=True)

# Perform hierarchical clustering
linkage_matrix = linkage(sample_data, method='ward')

# Calculate dendrogram for plotly
from scipy.cluster.hierarchy import dendrogram as scipy_dendrogram
dendro = scipy_dendrogram(linkage_matrix, 
                         orientation='top',
                         distance_sort='descending',
                         show_leaf_counts=False,
                         no_plot=True)

# Create interactive dendrogram with Plotly
fig6 = go.Figure()

# Extract dendrogram data
icoord = np.array(dendro['icoord'])
dcoord = np.array(dendro['dcoord'])

# Add dendrogram lines
for i in range(len(icoord)):
    fig6.add_trace(go.Scatter(
        x=icoord[i], 
        y=dcoord[i],
        mode='lines',
        line=dict(color='#06b6d4', width=2),
        showlegend=False,
        hoverinfo='none'
    ))

# Add interactive leaf nodes with employee information
leaf_positions = []
for i, label_idx in enumerate(dendro['leaves']):
    x_pos = 10 * i + 5
    y_pos = 0
    
    # Get employee data
    emp_data = sample_df.iloc[label_idx]
    
    # Create simplified employee ID for display
    emp_id = f"E{label_idx + 1:02d}"
    
    # Create detailed hover text
    hover_text = f"""
    <b>Employee {emp_id}</b><br>
    <b>Department:</b> {emp_data.get('departamento', 'N/A')}<br>
    <b>Age:</b> {emp_data.get('edad', 'N/A')} years<br>
    <b>Annual Salary:</b> ${emp_data.get('salario_anual', 0):,.0f}<br>
    <b>Experience:</b> {emp_data.get('experiencia_anos', 'N/A')} years<br>
    <b>Productivity:</b> {emp_data.get('productividad_score', 'N/A')}/100<br>
    <b>Job Satisfaction:</b> {emp_data.get('satisfaccion_laboral', 'N/A')}/10<br>
    <b>Weekly Hours:</b> {emp_data.get('horas_semanales', 'N/A')} hrs<br>
    <b>Education:</b> {emp_data.get('nivel_educacion', 'N/A')}<br>
    <b>Work Mode:</b> {emp_data.get('modalidad_trabajo', 'N/A')}<br>
    <b>Gender:</b> {emp_data.get('genero', 'N/A')}<br>
    <b>Geographic Zone:</b> {emp_data.get('zona_geografica', 'N/A')}
    """
    
    # Add interactive leaf node
    fig6.add_trace(go.Scatter(
        x=[x_pos],
        y=[y_pos],
        mode='markers',  # Removed text from here
        marker=dict(
            size=10,
            color='#f59e0b',
            symbol='circle',
            line=dict(width=2, color='#06b6d4')
        ),
        hovertemplate=hover_text + "<extra></extra>",
        showlegend=False,
        name=f"Employee {emp_id}"
    ))

# Add cluster information nodes at branch points
for i, (x_coords, y_coords) in enumerate(zip(icoord, dcoord)):
    # Add hover info at branch merge points
    merge_x = (x_coords[1] + x_coords[2]) / 2
    merge_y = y_coords[1]
    
    if merge_y > 1:  # Only for significant branches
        cluster_info = f"""
        <b>Cluster Merge Point</b><br>
        <b>Distance:</b> {merge_y:.2f}<br>
        <b>Cluster Level:</b> {i + 1}<br>
        <b>Similarity:</b> {((max(dcoord.flatten()) - merge_y) / max(dcoord.flatten()) * 100):.1f}%
        """
        
        fig6.add_trace(go.Scatter(
            x=[merge_x],
            y=[merge_y],
            mode='markers',
            marker=dict(
                size=8,
                color='#8b5cf6',
                symbol='diamond',
                opacity=0.7
            ),
            hovertemplate=cluster_info + "<extra></extra>",
            showlegend=False,
            name=f"Cluster {i + 1}"
        ))

# Update layout
fig6.update_layout(
    height=700,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#f8fafc',
    title=dict(
        text='Interactive Employee Similarity Clustering',
        font=dict(color='#f8fafc', size=18),
        x=0.5
    ),
    xaxis=dict(
        title='Employees (Hover over orange circles for details)',
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        color='#f8fafc'
    ),
    yaxis=dict(
        title='Distance (Lower = More Similar)',
        showgrid=True,
        gridcolor='rgba(255,255,255,0.1)',
        zeroline=False,
        color='#f8fafc'
    ),
    margin=dict(b=80, t=100, l=60, r=60),
    hovermode='closest'
)

st.plotly_chart(fig6, use_container_width=True)

# Add usage instructions
st.markdown("""
<div class="insight-box">
    <div class="insight-title">📊 Chart Analysis</div>
    <div class="insight-content">
        This interactive hierarchical clustering dendrogram reveals natural groupings within the employee population based on key characteristics including age, salary, experience, productivity, satisfaction, and working hours. The tree structure shows how employees cluster together based on similarity, with branch height indicating the degree of difference between groups.
    </div>
</div>

<div class="insight-box">
    <div class="insight-title">🔍 Key Insights</div>
    <div class="insight-content">
        <ul>
            <li><strong>Natural Segments:</strong> The branching pattern reveals distinct employee archetypes with similar characteristics</li>
            <li><strong>Similarity Measurement:</strong> Lower branch points indicate employees with very similar profiles</li>
            <li><strong>Organizational Structure:</strong> Clustering patterns may reflect informal organizational hierarchies or team compositions</li>
            <li><strong>Talent Management:</strong> Similar employee groups can inform targeted development programs and career progression paths</li>
            <li><strong>Compensation Equity:</strong> Employees in the same cluster should ideally have similar compensation structures</li>
            <li><strong>Team Formation:</strong> Use clustering insights to create balanced, complementary team compositions</li>
            <li><strong>Succession Planning:</strong> Identify employees with similar profiles for backup and succession strategies</li>
        </ul>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

# Additional visualization: Geographic distribution
if 'ciudad' in filtered_df.columns:
    st.markdown("""
    <div class="section-header">
        <i class="ti ti-map section-icon"></i>
        <h2>Geographic Distribution</h2>
    </div>
    """, unsafe_allow_html=True)
    
    city_counts = filtered_df['ciudad'].value_counts().reset_index()
    city_counts.columns = ['ciudad', 'count']
    
    # High contrast colors for geographic distribution
    geo_colors = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6', '#1ABC9C', '#E67E22', '#34495E', '#FF6B6B', '#4ECDC4']
    
    fig6 = px.bar(
        city_counts,
        x='ciudad',
        y='count',
        color='ciudad',
        labels={'count': 'Number of Employees', 'ciudad': 'City'},
        height=500,
        color_discrete_sequence=geo_colors
    )
    fig6.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#f8fafc',
        xaxis_title_font_size=14,
        yaxis_title_font_size=14
    )
    fig6.update_traces(
        marker_line_color='rgba(255,255,255,0.3)',
        marker_line_width=1
    )
    st.plotly_chart(fig6, use_container_width=True)
    
    st.markdown("""
    <div class="chart-description">
    <div class="insight-box">
        <div class="insight-title">📊 Chart Analysis</div>
        <div class="insight-content">
            This geographic distribution bar chart provides critical insights into workforce location patterns and organizational presence across different cities. Each bar represents the employee concentration in a specific geographic location, using high-contrast colors to ensure clear differentiation between cities.
        </div>
    </div>

    <div class="insight-box">
        <div class="insight-title">🔍 Key Insights</div>
        <div class="insight-content">
            <ul>
                <li><strong>Talent Hubs:</strong> Taller bars indicate primary talent concentration areas and major operational centers</li>
                <li><strong>Market Presence:</strong> Geographic spread reveals organizational reach and market penetration</li>
                <li><strong>Remote Work Impact:</strong> Distribution patterns may reflect remote work policies and geographic flexibility</li>
                <li><strong>Expansion Opportunities:</strong> Cities with lower employee counts might represent growth opportunities</li>
                <li><strong>Cost Analysis:</strong> Geographic distribution helps analyze location-based operational costs and salary variations</li>
                <li><strong>Risk Management:</strong> Identifies concentration risks and informs business continuity planning</li>
            </ul>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

# Show filtered data
st.markdown("""
<div class="section-header">
    <i class="ti ti-table section-icon"></i>
    <h2>Filtered Dataset</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("Below is the complete filtered dataset based on your selected criteria:")
st.dataframe(filtered_df, height=300)