"""
Visualization module for the pharma CI platform.
Creates charts and visualizations for the dashboard.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def create_pipeline_phase_chart(pipeline_data):
    """
    Create a bar chart showing drug count by development phase.

    Args:
        pipeline_data (pd.DataFrame): DataFrame with pipeline data

    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    if pipeline_data.empty:
        return go.Figure()

    # Count drugs by phase
    phase_counts = pipeline_data['phase'].value_counts().reset_index()
    phase_counts.columns = ['Phase', 'Count']

    # Define phase order
    phase_order = ['Preclinical', 'Phase 1', 'Phase 1/2', 'Phase 2', 'Phase 2/3', 'Phase 3', 'Phase 4', 'Approved']

    # Filter and order phases
    phase_counts = phase_counts[phase_counts['Phase'].isin(phase_order)]
    phase_counts['Phase'] = pd.Categorical(phase_counts['Phase'], categories=phase_order, ordered=True)
    phase_counts = phase_counts.sort_values('Phase')

    # Create the figure
    fig = px.bar(
        phase_counts, 
        x='Phase', 
        y='Count',
        color='Phase',
        title='Drug Pipeline by Phase',
        labels={'Count': 'Number of Drugs', 'Phase': 'Development Phase'},
        color_discrete_sequence=px.colors.qualitative.G10
    )

    # Update layout
    fig.update_layout(
        xaxis={'categoryorder': 'array', 'categoryarray': phase_order},
        hovermode='closest',
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig

def create_company_comparison_chart(pipeline_data, top_n=5):
    """
    Create a stacked bar chart comparing top companies' pipelines.

    Args:
        pipeline_data (pd.DataFrame): DataFrame with pipeline data
        top_n (int): Number of top companies to display

    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    if pipeline_data.empty:
        return go.Figure()

    # Get top companies by drug count
    top_companies = pipeline_data['company'].value_counts().nlargest(top_n).index.tolist()

    # Filter data for top companies
    company_data = pipeline_data[pipeline_data['company'].isin(top_companies)]

    # Count drugs by company and phase
    company_phase_counts = company_data.groupby(['company', 'phase']).size().reset_index(name='count')

    # Define phase order
    phase_order = ['Preclinical', 'Phase 1', 'Phase 1/2', 'Phase 2', 'Phase 2/3', 'Phase 3', 'Phase 4', 'Approved']

    # Create figure
    fig = px.bar(
        company_phase_counts,
        x='company',
        y='count',
        color='phase',
        title=f'Pipeline Comparison - Top {top_n} Companies',
        labels={'company': 'Company', 'count': 'Number of Drugs', 'phase': 'Phase'},
        category_orders={'phase': phase_order},
        color_discrete_sequence=px.colors.qualitative.Plotly
    )

    # Update layout
    fig.update_layout(
        xaxis_title='Company',
        yaxis_title='Number of Drugs',
        legend_title='Phase',
        height=500,
        margin=dict(l=20, r=20, t=40, b=100)
    )

    # Rotate x-axis labels if needed
    fig.update_xaxes(tickangle=45)

    return fig

def create_therapeutic_area_chart(pipeline_data):
    """
    Create a pie chart showing distribution of therapeutic areas.

    Args:
        pipeline_data (pd.DataFrame): DataFrame with pipeline data

    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    if pipeline_data.empty:
        return go.Figure()

    # Clean and categorize conditions
    keywords = {
        'Oncology': ['cancer', 'oncology', 'tumor', 'neoplasm', 'carcinoma', 'leukemia', 'melanoma', 'lymphoma'],
        'Neurology': ['brain', 'neural', 'alzheimer', 'parkinson', 'epilepsy', 'seizure', 'neurology', 'cognitive'],
        'Cardiovascular': ['heart', 'cardio', 'vascular', 'hypertension', 'stroke', 'artery', 'thrombosis'],
        'Immunology': ['immune', 'antibody', 'rheumatoid', 'autoimmune', 'psoriasis', 'arthritis'],
        'Infectious Disease': ['infection', 'bacterial', 'viral', 'antibacterial', 'antiviral', 'vaccine'],
        'Metabolic': ['diabetes', 'metabolic', 'obesity', 'lipid', 'cholesterol'],
        'Respiratory': ['respiratory', 'asthma', 'pulmonary', 'lung', 'copd', 'bronchitis'],
    }

    def categorize_condition(condition):
        condition = str(condition).lower()
        for category, terms in keywords.items():
            if any(term in condition for term in terms):
                return category
        return 'Other'

    # Add therapeutic area category
    pipeline_data['therapeutic_area'] = pipeline_data['condition'].apply(categorize_condition)

    # Count by therapeutic area
    area_counts = pipeline_data['therapeutic_area'].value_counts().reset_index()
    area_counts.columns = ['Therapeutic Area', 'Count']

    # Create pie chart
    fig = px.pie(
        area_counts,
        values='Count',
        names='Therapeutic Area',
        title='Distribution by Therapeutic Area',
        color_discrete_sequence=px.colors.sequential.Plasma_r
    )

    # Update layout
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    # Update traces
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig

def create_sentiment_chart(news_data):
    """
    Create a donut chart showing sentiment distribution of news.

    Args:
        news_data (list): List of news article dictionaries

    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    if not news_data:
        return go.Figure()

    # Count sentiment occurrences
    sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}

    for article in news_data:
        sentiment = article.get('sentiment', 'neutral')
        if sentiment in sentiment_counts:
            sentiment_counts[sentiment] += 1

    # Prepare data for chart
    labels = list(sentiment_counts.keys())
    values = list(sentiment_counts.values())

    # Color mapping
    colors = {'positive': '#2ECC71', 'neutral': '#3498DB', 'negative': '#E74C3C'}

    # Create donut chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.4,
        marker_colors=[colors[label] for label in labels]
    )])

    # Update layout
    fig.update_layout(
        title='News Sentiment Analysis',
        height=350,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig

def create_recent_activity_timeline(pipeline_data, news_data, max_items=10):
    """
    Create a combined timeline of recent pipeline and news activity with enhanced UI.

    Args:
        pipeline_data (pd.DataFrame): DataFrame with pipeline data
        news_data (list): List of news article dictionaries
        max_items (int): Maximum number of items to display

    Returns:
        plotly.graph_objects.Figure: Plotly figure object with improved styling
    """
    from datetime import datetime

    # Create a combined list of events
    events = []
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Add pipeline events
    if not pipeline_data.empty:
        try:
            # Get the most recent updates
            recent_pipeline = pipeline_data.head(max_items)

            for _, row in recent_pipeline.iterrows():
                # Handle any date format issues
                date_str = current_date  # Use current date as default
                try:
                    if isinstance(row['last_updated'], str):
                        date_str = row['last_updated']
                    elif hasattr(row['last_updated'], 'strftime'):
                        date_str = row['last_updated'].strftime('%Y-%m-%d')
                except:
                    pass  # Keep default date

                # Truncate long titles
                drug_name = str(row['drug_name'])[:30] + '...' if len(str(row['drug_name'])) > 30 else str(row['drug_name'])
                condition = str(row['condition'])[:40] + '...' if len(str(row['condition'])) > 40 else str(row['condition'])
                
                events.append({
                    'date': date_str,
                    'title': f"{drug_name} - {row['phase']}",
                    'description': f"{row['company']}: {condition}",
                    'type': 'pipeline',
                    'icon': '💊'
                })
        except Exception as e:
            print(f"Error processing pipeline data for timeline: {e}")

    # Add news events
    if news_data:
        try:
            for article in news_data[:max_items]:
                # Handle any date format issues
                date_str = current_date  # Use current date as default
                try:
                    pub_date = article.get('published_at', '')
                    if isinstance(pub_date, str):
                        date_str = pub_date
                    elif hasattr(pub_date, 'strftime'):
                        date_str = pub_date.strftime('%Y-%m-%d')
                except:
                    pass  # Keep default date

                # Truncate long titles
                title = str(article.get('title', 'News Update'))
                title = title[:50] + '...' if len(title) > 50 else title
                
                events.append({
                    'date': date_str,
                    'title': title,
                    'description': article.get('source', ''),
                    'type': 'news',
                    'icon': '📰'
                })
        except Exception as e:
            print(f"Error processing news data for timeline: {e}")

    # If we have no events, add a placeholder to avoid empty chart
    if not events:
        events.append({
            'date': current_date,
            'title': 'No recent activity',
            'description': 'Check back later for updates',
            'type': 'news',
            'icon': '📋'
        })

    # Sort by date and take most recent - with error handling
    try:
        events = sorted(events, key=lambda x: x['date'], reverse=True)[:max_items]
    except Exception as e:
        print(f"Error sorting timeline events: {e}")
        # Just take the first max_items without sorting
        events = events[:max_items]

    # Create the figure with improved styling
    fig = go.Figure()

    # Calculate proper spacing
    y_spacing = 1.5  # Increased spacing between items
    
    # Create custom timeline layout with enhanced visuals
    for i, event in enumerate(events):
        y_pos = i * y_spacing
        
        # Add vertical line for timeline
        if i > 0:
            fig.add_shape(
                type="line",
                x0=1, x1=1,
                y0=(i-1) * y_spacing, y1=y_pos,
                line=dict(color="#e1e8ed", width=3),
            )

        # Add event marker with improved visibility
        marker_color = '#3498db' if event['type'] == 'news' else '#e74c3c'
        fig.add_trace(go.Scatter(
            x=[1],
            y=[y_pos],
            mode='markers',
            marker=dict(
                size=20,
                color=marker_color,
                symbol='circle',
                line=dict(color='white', width=3),
                opacity=1
            ),
            showlegend=False,
            hoverinfo='skip'
        ))

        # Add icon inside marker
        fig.add_trace(go.Scatter(
            x=[1],
            y=[y_pos],
            mode='text',
            text=[event['icon']],
            textfont=dict(size=10),
            showlegend=False,
            hoverinfo='skip'
        ))

        # Add date on the left side with better formatting
        # Convert date to more readable format
        try:
            from datetime import datetime
            date_obj = datetime.strptime(event['date'], '%Y-%m-%d')
            formatted_date = date_obj.strftime('%b %d, %Y')  # e.g., "Feb 12, 2026"
        except:
            formatted_date = event['date']
        
        fig.add_annotation(
            x=0.1,
            y=y_pos,
            text=f"<b>{formatted_date}</b>",
            showarrow=False,
            xanchor='right',
            yanchor='middle',
            font=dict(size=10, color='#7f8c8d', family='Arial'),
            bgcolor='rgba(255, 255, 255, 0.9)',
            borderpad=4
        )

        # Add event title on the right side
        fig.add_annotation(
            x=1.7,
            y=y_pos + 0.15,
            text=f"<b>{event['title']}</b>",
            showarrow=False,
            xanchor='left',
            yanchor='middle',
            font=dict(size=12, color='#2c3e50', family='Arial'),
            align='left'
        )
        
        # Add event description below title
        fig.add_annotation(
            x=1.7,
            y=y_pos - 0.25,
            text=f"<span style='color:#95a5a6'>{event['description']}</span>",
            showarrow=False,
            xanchor='left',
            yanchor='middle',
            font=dict(size=10, family='Arial'),
            align='left'
        )

    # Update layout with improved spacing and dimensions
    fig.update_layout(
        title=dict(
            text='Recent Activity Timeline',
            font=dict(size=18, family='Arial', color='#2c3e50', weight='bold'),
            x=0.5,
            xanchor='center',
            y=0.98
        ),
        height=max(450, len(events) * 100),  # Dynamic height based on items
        margin=dict(l=120, r=20, t=60, b=20),  # Increased left margin for dates
        xaxis=dict(
            visible=False, 
            range=[-1, 4],  # Extended left range for date display
            fixedrange=True
        ),
        yaxis=dict(
            visible=False, 
            range=[-0.5, (len(events) - 1) * y_spacing + 0.5],
            autorange='reversed',
            fixedrange=True
        ),
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='white',
        showlegend=False,
        hovermode=False
    )

    return fig