import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="Bangalore Hangout Finder",
    page_icon="🍽️",
    layout="wide"
)

# ── Custom CSS ─────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f0f0f; }
    .block-container { padding-top: 2rem; }

    .hero {
        text-align: center;
        padding: 2rem 1rem 1rem;
    }
    .hero h1 {
        font-size: 2.6rem;
        font-weight: 700;
        color: #e94560;
        margin-bottom: 0.2rem;
    }
    .hero p {
        font-size: 1.1rem;
        color: #aaa;
        margin-top: 0;
    }

    .card {
        background: #1a1a2e;
        border: 1px solid #e9456022;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.8rem;
        transition: border 0.2s;
    }
    .card:hover { border: 1px solid #e9456066; }

    .restaurant-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e94560;
        margin-bottom: 0.2rem;
    }
    .meta { color: #ccc; font-size: 0.88rem; margin: 0.15rem 0; }
    .tag {
        display: inline-block;
        background: #e9456022;
        color: #e94560;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.78rem;
        margin: 2px 2px 0 0;
    }
    .tag-green {
        background: #50fa7b22;
        color: #50fa7b;
    }
    .stat-box {
        background: #1a1a2e;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #ffffff11;
    }
    .stat-number { font-size: 1.8rem; font-weight: 700; color: #e94560; }
    .stat-label  { font-size: 0.82rem; color: #888; margin-top: 0.2rem; }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextInput"] label {
        color: #ccc !important;
        font-size: 0.9rem;
    }
    .stButton > button {
        background: #e94560;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        cursor: pointer;
        transition: background 0.2s;
    }
    .stButton > button:hover { background: #c73652; }
    .divider {
        border: none;
        border-top: 1px solid #ffffff11;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ── Data loading & model ────────────────────────────────────
@st.cache_data
def load_and_prepare():
    df = pd.read_csv("data/zomato_clean.csv")

    # Rate cleaning (in case raw strings slipped through)
    df['rate'] = pd.to_numeric(
        df['rate'].astype(str).str.replace('/5', '', regex=False).str.strip(),
        errors='coerce'
    )
    df['rate'].fillna(df['rate'].median(), inplace=True)

    # Cost cleaning
    cost_col = 'approx_cost(for two people)' if 'approx_cost(for two people)' in df.columns else 'cost_for_two'
    df.rename(columns={cost_col: 'cost_for_two'}, inplace=True)
    df['cost_for_two'] = pd.to_numeric(
        df['cost_for_two'].astype(str).str.replace(',', '', regex=False),
        errors='coerce'
    )
    df['cost_for_two'].fillna(df['cost_for_two'].median(), inplace=True)

    col_map = {
        'listed_in(type)': 'listing_type',
        'listed_in(city)': 'city_area'
    }
    df.rename(columns={k: v for k, v in col_map.items() if k in df.columns}, inplace=True)

    for col in ['rest_type', 'cuisines', 'dish_liked', 'location']:
        if col in df.columns:
            df[col].fillna('Unknown' if col != 'dish_liked' else '', inplace=True)
    if 'votes' in df.columns:
        df['votes'] = pd.to_numeric(
            df['votes'],
            errors='coerce'
        )
        df['votes'].fillna(0, inplace=True)

    # Feature engineering
    def budget_bucket(c):
        if c <= 300:    return 'Budget (≤300)'
        elif c <= 600:  return 'Mid-Range (301-600)'
        elif c <= 1000: return 'Premium (601-1000)'
        else:           return 'Luxury (1000+)'

    def ambience_map(rt):
        rt = str(rt).lower()
        if 'fine dining' in rt:           return 'Upscale / Romantic'
        elif 'casual dining' in rt:       return 'Casual / Social'
        elif 'cafe' in rt:                return 'Cozy / Chill'
        elif 'pub' in rt or 'bar' in rt:  return 'Lively / Party'
        elif 'quick bites' in rt or 'delivery' in rt: return 'Fast / Functional'
        elif 'dessert' in rt or 'bakery' in rt:       return 'Sweet / Relaxed'
        return 'General'

    def occasion_tag(row):

        cost = row.get('cost_for_two', 0)
        rating = row.get('rate', 0)

        rt = str(row.get('rest_type', '')).lower()
        lt = str(row.get('listing_type', '')).lower()

        tags = []

    # Date Night
        if (
            cost >= 1000
            and rating >= 4.0
            and (
                'fine dining' in rt
                or 'pub' in rt
                or 'bar' in rt
            )
        ):
            tags.append('Date Night')

    # Friends Hangout
        if (
            'cafe' in rt
            or 'lounge' in rt
            or 'pub' in rt
            or 'bar' in rt
            or 'drinks' in lt
        ):
            tags.append('Friends Hangout')

    # Family Outing
        if (
            cost >= 600
            and (
                'casual dining' in rt
                or 'buffet' in lt
                or 'dine-out' in lt
            )
        ):
            tags.append('Family Outing')

    # Night Out
        if (
            'pub' in rt
            or 'bar' in rt
            or 'nightlife' in lt
        ):
            tags.append('Night Out')

    # Solo
        if (
            cost <= 500
            and (
                'quick bites' in rt
                or 'delivery' in rt
                or 'mess' in rt
            )
        ):
            tags.append('Solo / Quick Meal')

        return ', '.join(tags) if tags else 'General'
    # TF-IDF
    def build_features(row):
        return ' '.join([
            str(row.get('cuisines', '')),
            str(row.get('rest_type', '')),
            str(row.get('listing_type', '')),
            str(row.get('ambience', '')),
            str(row.get('budget_category', '')),
            str(row.get('dish_liked', ''))
        ]).lower()

    df['features'] = df.apply(build_features, axis=1)
    df.reset_index(drop=True, inplace=True)

    tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
    matrix = tfidf.fit_transform(df['features'])

    return df, tfidf, matrix


def recommend(
    df,
    tfidf,
    matrix,
    occasion,
    budget,
    cuisine,
    location,
    top_n=10
):

    query_parts = [occasion]

    if cuisine != "Any":
        query_parts.append(cuisine)

    query_parts.append(budget)

    query = " ".join(query_parts).lower()

    query_vec = tfidf.transform([query])

    sim_scores = cosine_similarity(
        query_vec,
        matrix
    ).flatten()

    filtered = df.copy()

    filtered["sim_score"] = sim_scores

    # Occasion filter
    filtered = filtered[
        filtered["occasion_tags"]
        .str.contains(
            occasion,
            case=False,
            na=False
        )
    ]

    # Budget filter
    filtered = filtered[
        filtered["budget_category"] == budget
    ]

    # Cuisine filter
    if cuisine != "Any":
        filtered = filtered[
            filtered["cuisines"]
            .str.contains(
                cuisine,
                case=False,
                na=False
            )
        ]

    # Location filter
    if location != "Anywhere":
        filtered = filtered[
            filtered["location"]
            .str.contains(
                location,
                case=False,
                na=False
            )
        ]

    if filtered.empty:
        return filtered

    # Popularity score
    max_votes = filtered["votes"].max()

    if max_votes > 0:
        filtered["vote_score"] = (
            filtered["votes"] / max_votes
        )
    else:
        filtered["vote_score"] = 0

    # Hybrid ranking
    filtered["final_score"] = (
        filtered["sim_score"] * 0.40
        + (filtered["rate"] / 5) * 0.40
        + filtered["vote_score"] * 0.20
    )

    return (
        filtered
        .sort_values(
            "final_score",
            ascending=False
        )
        .drop_duplicates(
            subset="name"
        )
        .head(top_n)
    )

# ── Load data ───────────────────────────────────────────────
with st.spinner("Loading restaurant data..."):
    df, tfidf, matrix = load_and_prepare()

# ── Hero ────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🍽️ Bangalore Hangout Finder</h1>
    <p>Find the perfect spot for any occasion — date night, friends, family, or solo</p>
</div>
""", unsafe_allow_html=True)

# ── Stats row ───────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="stat-box"><div class="stat-number">{len(df):,}</div><div class="stat-label">Restaurants</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stat-box"><div class="stat-number">{df["location"].nunique()}</div><div class="stat-label">Areas in Bangalore</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stat-box"><div class="stat-number">{df["cuisines"].str.split(", ").explode().nunique()}</div><div class="stat-label">Cuisine Types</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="stat-box"><div class="stat-number">{df["rate"].mean():.1f}★</div><div class="stat-label">Avg Rating</div></div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Filters ─────────────────────────────────────────────────
st.markdown("### 🔍 Find Your Spot")

col1, col2, col3, col4 = st.columns(4)

with col1:
    occasion = st.selectbox("Occasion", [
        "Date Night", "Friends Hangout", "Family Outing",
        "Night Out", "Solo / Quick Meal"
    ])

with col2:
    budget = st.selectbox("Budget (for two)", [
        "Budget (≤300)", "Mid-Range (301-600)",
        "Premium (601-1000)", "Luxury (1000+)"
    ])

with col3:
    top_cuisines = ["Any"] + sorted(
        df['cuisines'].str.split(', ').explode()
        .value_counts().head(20).index.tolist()
    )
    cuisine = st.selectbox("Cuisine", top_cuisines)

with col4:
    locations = ["Anywhere"] + sorted(df['location'].dropna().unique().tolist())
    location  = st.selectbox("Location", locations)

col_btn, col_n = st.columns([3, 1])
with col_btn:
    search = st.button("🍽️  Find My Spot")
with col_n:
    top_n = st.selectbox("Show", [5, 10, 15, 20], index=1)

# ── Results ─────────────────────────────────────────────────
if search:
    with st.spinner("Finding the best spots for you..."):
        results = recommend(df, tfidf, matrix, occasion, budget, cuisine, location, top_n)

    if results.empty:
        st.warning("No restaurants found for this combination. Try changing the location or cuisine.")
    else:
        st.markdown(f"<br>**{len(results)} spots found** for **{occasion}** · **{budget}**"
                    + (f" · {cuisine}" if cuisine != "Any" else "")
                    + (f" · {location}" if location != "Anywhere" else ""),
                    unsafe_allow_html=True)
        st.markdown("")

        for _, row in results.iterrows():
            online  = "✅ Online Order" if str(row.get('online_order','')) == 'Yes' else ""
            booking = "📅 Table Booking" if str(row.get('book_table','')) == 'Yes'  else ""
            tags    = ' '.join([f'<span class="tag">{t.strip()}</span>'
                                for t in str(row.get('occasion_tags','')).split(',') if t.strip()])
            avail   = ' '.join([f'<span class="tag tag-green">{x}</span>'
                                for x in [online, booking] if x])

            st.markdown(f"""
            <div class="card">
                <div class="restaurant-name">{row['name']}</div>
                <div class="meta">📍 {row['location']} &nbsp;|&nbsp; 🍴 {row['cuisines'][:60]}{'...' if len(str(row['cuisines'])) > 60 else ''}</div>
                <div class="meta">⭐ {row['rate']:.1f} &nbsp;|&nbsp; 💰 ₹{int(row['cost_for_two'])} for two &nbsp;|&nbsp; 🏮 {row['ambience']}</div>
                <div style="margin-top:0.5rem">{tags} {avail}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Footer ──────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;color:#555;font-size:0.82rem">'
    'Built with Zomato Bangalore dataset · Content-Based Filtering · TF-IDF + Cosine Similarity'
    '</p>',
    unsafe_allow_html=True
)