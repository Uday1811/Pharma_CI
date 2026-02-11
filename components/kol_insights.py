"""
KOL insights component for the pharma CI platform.
Renders information about Key Opinion Leaders in the pharmaceutical industry.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.pubmed import get_pubmed_data
from utils.text_processing import identify_kols
from utils.news_scraper import get_kol_mentions

def render_kol_insights():
    """Render the KOL insights page with analysis of key opinion leaders"""
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .kol-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .kol-card-light {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e1e8ed;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .kol-card-light:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .kol-name {
        font-size: 20px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 8px;
    }
    .kol-stats {
        display: flex;
        gap: 20px;
        margin-top: 10px;
    }
    .kol-stat-item {
        display: flex;
        align-items: center;
        gap: 5px;
    }
    .stat-icon {
        font-size: 18px;
    }
    .stat-value {
        font-weight: bold;
        color: #667eea;
    }
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 5px;
    }
    .badge-primary {
        background-color: #e3f2fd;
        color: #1976d2;
    }
    .badge-success {
        background-color: #e8f5e9;
        color: #388e3c;
    }
    .badge-warning {
        background-color: #fff3e0;
        color: #f57c00;
    }
    .section-header {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        margin: 30px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid #667eea;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with gradient
    st.markdown("""
    <div class="kol-card">
        <h1 style="margin: 0; font-size: 32px;">🎓 Key Opinion Leaders Insights</h1>
        <p style="margin: 10px 0 0 0; opacity: 0.9;">Discover and track influential researchers and thought leaders in pharmaceutical research</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add sidebar filters
    with st.sidebar:
        st.markdown("### 🔍 KOL Filters")
        
        # Therapeutic area filter
        areas = ['Oncology', 'Immunology', 'Neurology', 'Cardiovascular', 
                 'Infectious Disease', 'Metabolic', 'Respiratory']
        
        selected_area = st.selectbox(
            "Therapeutic Area:",
            options=['All'] + areas,
            index=0
        )
        
        # Publication count minimum filter
        min_publications = st.slider(
            "Minimum Publications:",
            min_value=1,
            max_value=20,
            value=3
        )
        
        # Time period filter
        time_period = st.radio(
            "Time Period:",
            ["Last Year", "Last 5 Years", "All Time"]
        )
        
        # Refresh data option
        refresh_data = st.button("🔄 Refresh KOL Data", use_container_width=True)
    
    # Build search query based on filters
    search_terms = []
    
    if selected_area != 'All':
        search_terms.append(selected_area.lower())
    
    # Add time constraints based on selection
    if time_period == "Last Year":
        search_terms.append("2022[PDAT] OR 2023[PDAT]")
    elif time_period == "Last 5 Years":
        years = list(range(2018, 2024))
        year_query = " OR ".join([f"{year}[PDAT]" for year in years])
        search_terms.append(f"({year_query})")
    
    # Show loading spinner while data is being fetched
    with st.spinner("🔍 Loading KOL data..."):
        # Get publication data from PubMed
        publications = get_pubmed_data(
            drug_names=search_terms if search_terms else None,
            max_results=100,
            refresh=refresh_data
        )
        
        # Identify potential KOLs from publications
        kols = identify_kols(publications)
        
        # Filter by publication count
        kols = [kol for kol in kols if kol['publication_count'] >= min_publications]
    
    # KOL Statistics Overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total KOLs",
            value=len(kols),
            delta=f"+{len(kols) // 10}" if kols else "0"
        )
    
    with col2:
        total_pubs = sum(kol['publication_count'] for kol in kols) if kols else 0
        st.metric(
            label="Total Publications",
            value=total_pubs,
            delta=f"+{total_pubs // 20}" if total_pubs else "0"
        )
    
    with col3:
        avg_pubs = total_pubs // len(kols) if kols else 0
        st.metric(
            label="Avg Publications/KOL",
            value=avg_pubs
        )
    
    with col4:
        unique_journals = len(set(j for kol in kols for j in kol.get('journals', []))) if kols else 0
        st.metric(
            label="Unique Journals",
            value=unique_journals
        )
    
    # Top KOLs Section
    st.markdown('<div class="section-header">🌟 Top Key Opinion Leaders</div>', unsafe_allow_html=True)
    
    if kols:
        # Create three columns for better layout
        cols = st.columns(3)
        
        for i, kol in enumerate(kols[:12]):  # Show top 12 KOLs
            col_idx = i % 3
            
            with cols[col_idx]:
                # Determine badge based on publication count
                if kol['publication_count'] >= 10:
                    badge_class = "badge-success"
                    badge_text = "Top Contributor"
                elif kol['publication_count'] >= 5:
                    badge_class = "badge-primary"
                    badge_text = "Active"
                else:
                    badge_class = "badge-warning"
                    badge_text = "Emerging"
                
                # Get first 2 journals
                journals_display = ', '.join(kol['journals'][:2])
                if len(kol['journals']) > 2:
                    journals_display += f" +{len(kol['journals']) - 2} more"
                
                # Truncate recent publication
                recent_pub = kol['recent_publication'][:80] + '...' if len(kol['recent_publication']) > 80 else kol['recent_publication']
                
                st.markdown(f"""
                <div class="kol-card-light">
                    <div class="kol-name">👤 {kol['name']}</div>
                    <span class="badge {badge_class}">{badge_text}</span>
                    <div class="kol-stats">
                        <div class="kol-stat-item">
                            <span class="stat-icon">📄</span>
                            <span class="stat-value">{kol['publication_count']}</span>
                            <span style="color: #7f8c8d; font-size: 12px;">publications</span>
                        </div>
                    </div>
                    <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid #ecf0f1;">
                        <div style="font-size: 12px; color: #7f8c8d; margin-bottom: 5px;">📚 Journals</div>
                        <div style="font-size: 13px; color: #34495e;">{journals_display}</div>
                    </div>
                    <div style="margin-top: 10px;">
                        <div style="font-size: 12px; color: #7f8c8d; margin-bottom: 5px;">🔬 Recent Work</div>
                        <div style="font-size: 12px; color: #34495e; line-height: 1.4;">{recent_pub}</div>
                    </div>
                    <div style="margin-top: 12px;">
                        <a href="{kol['url']}" target="_blank" style="color: #667eea; text-decoration: none; font-size: 13px; font-weight: 600;">View Profile →</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("🔍 No KOLs found matching the selected criteria. Try adjusting your filters.")
    
    # KOL Activity Tracker
    # KOL Network Section
    st.markdown('<div class="section-header">🕸️ KOL Network</div>', unsafe_allow_html=True)
    
    if kols:
        # Show KOL data in an enhanced table
        kol_df = pd.DataFrame(kols)
        if not kol_df.empty:
            # Select and rename columns for display
            display_cols = ['name', 'publication_count', 'journals', 'recent_publication']
            display_names = {'name': 'KOL Name', 'publication_count': '# Journals', 
                            'journals': 'Top Journals', 'recent_publication': 'Recent Publication'}
            
            # Create displayable dataframe
            display_df = kol_df[display_cols].copy()
            display_df.columns = [display_names.get(col, col) for col in display_cols]
            
            # Convert journal lists to strings
            display_df['Top Journals'] = display_df['Top Journals'].apply(
                lambda x: ', '.join(x[:2]) + (f' +{len(x)-2}' if len(x) > 2 else '')
            )
            
            # Truncate recent publication
            display_df['Recent Publication'] = display_df['Recent Publication'].apply(
                lambda x: x[:100] + '...' if len(x) > 100 else x
            )
            
            # Calculate dynamic height based on number of rows (max 600px)
            row_height = 35  # approximate height per row
            header_height = 38
            dynamic_height = min(len(display_df) * row_height + header_height, 600)
            
            # Display the table with custom styling
            st.dataframe(
                display_df,
                use_container_width=True,
                height=dynamic_height if len(display_df) > 0 else 100
            )
    else:
        st.info("🔍 No KOL data available for network visualization.")
    
    # KOL Activity Tracker
    st.markdown('<div class="section-header">🔎 KOL Activity Tracker</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        kol_search = st.text_input("🔍 Search for a specific KOL:", placeholder="Enter KOL name...")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_button = st.button("Search", use_container_width=True, type="primary")
    
    if kol_search and search_button:
        with st.spinner(f"🔍 Searching for mentions of {kol_search}..."):
            # Get mentions of the KOL
            mentions = get_kol_mentions(kol_search)
            
            if mentions:
                st.success(f"✅ Found {len(mentions)} mentions of {kol_search}")
                
                # Display mentions in cards
                for mention in mentions:
                    st.markdown(f"""
                    <div class="kol-card-light">
                        <div style="font-size: 16px; font-weight: bold; color: #2c3e50; margin-bottom: 8px;">
                            📰 {mention['title']}
                        </div>
                        <div style="display: flex; gap: 15px; margin-bottom: 10px; font-size: 13px;">
                            <span style="color: #7f8c8d;">📅 {mention.get('date', 'Unknown')}</span>
                            <span style="color: #7f8c8d;">📌 {mention.get('type', 'Publication')}</span>
                            <span style="color: #7f8c8d;">🏢 {mention['source']}</span>
                        </div>
                        <div style="color: #34495e; font-size: 14px; line-height: 1.6; margin-bottom: 12px;">
                            {mention.get('context', 'No context available')}
                        </div>
                        <a href="{mention.get('url', '#')}" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 600; font-size: 13px;">
                            View Source →
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning(f"⚠️ No mentions found for {kol_search}")
    
    # KOL Publication Trends
    st.markdown('<div class="section-header">📊 KOL Publication Trends</div>', unsafe_allow_html=True)
    
    if kols:
        # Sort by publication count
        top_active_kols = sorted(kols, key=lambda x: x['publication_count'], reverse=True)[:10]
        
        # Create interactive bar chart with Plotly
        kol_names = [kol['name'] for kol in top_active_kols]
        pub_counts = [kol['publication_count'] for kol in top_active_kols]
        
        fig = go.Figure(data=[
            go.Bar(
                y=kol_names,
                x=pub_counts,
                orientation='h',
                marker=dict(
                    color=pub_counts,
                    colorscale='Viridis',
                    showscale=False
                ),
                text=pub_counts,
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Publications: %{x}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=dict(
                text='Most Active KOLs by Publication Count',
                font=dict(size=18, color='#2c3e50')
            ),
            xaxis_title='Number of Publications',
            yaxis_title='',
            height=400,
            margin=dict(l=20, r=20, t=60, b=40),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Arial', size=12),
            yaxis=dict(autorange='reversed')
        )
        
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#ecf0f1')
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("🔍 No KOL data available for trend analysis.")
