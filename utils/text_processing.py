"""
Text processing module for NLP tasks in the pharma CI platform.
Handles entity extraction, sentiment analysis, and text summarization.
"""
import re

# Try to import optional packages
try:
    from textblob import TextBlob
    HAS_TEXTBLOB = True
except ImportError:
    HAS_TEXTBLOB = False

try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
        HAS_SPACY = True
    except OSError:
        # Model not found, try to download it
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        nlp = spacy.load("en_core_web_sm")
        HAS_SPACY = True
except Exception as e:
    print(f"Warning: spaCy not available: {e}")
    HAS_SPACY = False
    nlp = None

def extract_entities(text, entity_types=None):
    """
    Extract named entities from text.
    
    Args:
        text (str): Text to extract entities from
        entity_types (list): Types of entities to extract (ORG, PERSON, etc.)
        
    Returns:
        dict: Dictionary of entity types and values
    """
    if not text or not HAS_SPACY or nlp is None:
        return {}
    
    # Process the text with spaCy
    doc = nlp(text)
    
    # Dictionary to store entities by type
    entities = {}
    
    # Filter by entity type if specified
    for ent in doc.ents:
        if entity_types and ent.label_ not in entity_types:
            continue
            
        if ent.label_ not in entities:
            entities[ent.label_] = []
            
        # Add entity if it's not already in the list
        if ent.text not in entities[ent.label_]:
            entities[ent.label_].append(ent.text)
    
    return entities

def extract_drug_entities(text):
    """
    Extract drug names and related entities from pharmaceutical text.
    
    Args:
        text (str): Text to extract entities from
        
    Returns:
        dict: Dictionary of pharmaceutical entities
    """
    # Use general NER first if available
    entities = extract_entities(text) if HAS_SPACY else {}
    
    # Look for specific drug-related patterns
    drug_patterns = [
        r'\b[A-Z][a-z]*mab\b',  # Monoclonal antibodies
        r'\b[A-Z][a-z]*nib\b',  # Kinase inhibitors
        r'\b[A-Z][a-z]*zumab\b',  # Humanized antibodies
        r'\b[A-Z][a-z]*tinib\b',  # Tyrosine kinase inhibitors
        r'\b[A-Z][a-z]*ciclib\b',  # CDK inhibitors
    ]
    
    drug_candidates = set()
    
    # Extract using regex patterns
    for pattern in drug_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            drug_candidates.add(match.group(0))
    
    # Add drug candidates to entities
    if drug_candidates:
        if 'DRUG' not in entities:
            entities['DRUG'] = []
        entities['DRUG'].extend(list(drug_candidates))
    
    return entities

def analyze_sentiment(text):
    """
    Analyze sentiment of text (positive, negative, neutral).
    
    Args:
        text (str): Text to analyze
        
    Returns:
        str: Sentiment classification
    """
    if not text:
        return "neutral"
    
    if not HAS_TEXTBLOB:
        # Simple fallback sentiment analysis
        positive_words = ['good', 'great', 'excellent', 'positive', 'success', 'approved', 'effective']
        negative_words = ['bad', 'poor', 'negative', 'failed', 'rejected', 'adverse', 'risk']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        else:
            return "neutral"
    
    # Use TextBlob for sentiment analysis
    blob = TextBlob(text)
    
    # Get polarity score (-1 to 1)
    polarity = blob.sentiment.polarity
    
    # Classify sentiment
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"

def summarize_text(text, max_length=150):
    """
    Generate a summary of the given text.
    
    Args:
        text (str): Text to summarize
        max_length (int): Maximum length of summary
        
    Returns:
        str: Summarized text
    """
    if not text:
        return ""
    
    # Simple truncation for summary
    if len(text) <= max_length:
        return text
    
    # Find the last complete sentence within max_length
    truncated = text[:max_length]
    last_period = truncated.rfind('.')
    
    if last_period > 0:
        return text[:last_period + 1]
    else:
        return truncated + "..."

def identify_kols(publications):
    """
    Identify potential KOLs from a set of publications.
    
    Args:
        publications (list): List of publication dictionaries
        
    Returns:
        list: List of potential KOLs with their metrics
    """
    # Count author occurrences
    author_counts = {}
    author_publications = {}
    
    for pub in publications:
        authors = pub.get('all_authors', [])
        
        for author in authors:
            if author not in author_counts:
                author_counts[author] = 1
                author_publications[author] = [pub]
            else:
                author_counts[author] += 1
                author_publications[author].append(pub)
    
    # Create KOL list
    kols = []
    
    for author, count in sorted(author_counts.items(), key=lambda x: x[1], reverse=True):
        if count >= 2:  # Consider authors with at least 2 publications
            # Get journals for this author
            journals = set(pub.get('journal', 'Unknown') for pub in author_publications[author])
            
            # Get most recent publication safely
            try:
                # Filter out publications with None pub_date
                valid_pubs = [p for p in author_publications[author] if p.get('pub_date') is not None]
                
                if valid_pubs:
                    recent_pub = max(valid_pubs, key=lambda x: x.get('pub_date', ''))
                    recent_title = recent_pub.get('title', 'Unknown title')
                else:
                    recent_title = author_publications[author][0].get('title', 'Unknown title')
            except:
                recent_title = "Publication information unavailable"
            
            kol = {
                'name': author,
                'publication_count': count,
                'journals': list(journals),
                'recent_publication': recent_title,
                'url': author_publications[author][0].get('url', '')
            }
            
            kols.append(kol)
    
    return kols[:20]  # Return top 20 KOLs

