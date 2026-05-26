import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

# ---------- Page Config ----------
st.set_page_config(page_title="Quantum Universe Pro", layout="wide", initial_sidebar_state="expanded")

# ---------- Google Analytics ----------
# Apni GA4 ID yahan daalo, fir uncomment karo
# GA_ID = "G-XXXXXXXXXX"
# ga_code = f"""
# <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
# <script>
# window.dataLayer = window.dataLayer || [];
# function gtag(){{dataLayer.push(arguments);}}
# gtag('js', new Date());
# gtag('config', '{GA_ID}');
# </script>
# """
# components.html(ga_code, height=0)

# ---------- Sidebar ----------
st.sidebar.title("🌌 Quantum Lab Pro")
menu = st.sidebar.selectbox("Choose Module", [
    "📊 Data Analytics Dashboard",
    "🪐 Exoplanet Explorer (Real NASA Data)",
    "Big Bang Timeline",
    "3D Galaxy Universe",
    "Black Hole + Galaxy",
    "Schrödinger Wave Packet",
    "Cosmic Inflation",
    "Quantum Fluctuations + NASA CMB"
])
st.sidebar.markdown("---")
st.sidebar.success("Pro Analytics Mode Active")

# ---------- Shared Data ----------
@st.cache_data
def get_galaxy_data(n=3000):
    rng = np.random.default_rng(42)
    r = rng.power(2.5, n) * 12
    theta = rng.uniform(0, 2*np.pi, n)
    phi = np.arccos(rng.uniform(-1, 1, n))
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi) * 0.4
    mass = 10**(rng.normal(10, 0.8, n))
    redshift = r * 0.05 + rng.normal(0, 0.1, n)
    velocity = redshift * 3e5
    galaxy_type = rng.choice(['Spiral','Elliptical','Irregular'], n, p=[0.6,0.3,0.1])
    df = pd.DataFrame({
        'x':x, 'y':y, 'z':z,
        'Distance_Mpc': r,
        'Mass_Solar': mass,
        'Redshift': redshift.clip(0),
        'Velocity_km_s': velocity.clip(0),
        'Type': galaxy_type
    })
    return df

df_gal = get_galaxy_data()

# ---------- DATA ANALYTICS DASHBOARD ----------
if menu == "📊 Data Analytics Dashboard":
    st.title("Data Analytics Dashboard — Galaxy Survey")
    st.caption("Simulated survey data derived from quantum fluctuation model")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Galaxies", f"{len(df_gal):,}")
    c2.metric("Avg Redshift", f"{df_gal['Redshift'].mean():.2f}")
    c3.metric("Avg Mass", f"{df_gal['Mass_Solar'].mean():.2e} M☉")
    c4.metric("Spiral %", f"{(df_gal['Type']=='Spiral').mean()*100:.1f}%")

    st.markdown("---")
    left, right = st.columns([1.2,1])
    with left:
        st.subheader("Galaxy Distribution 3D")
        fig3d = px.scatter_3d(df_gal.sample(1500), x='x', y='y', z='z',
                              color='Redshift', color_continuous_scale='Plasma', opacity=0.7)
        fig3d.update_layout(scene=dict(bgcolor='black'), paper_bgcolor='black', font_color='white',
                            margin=dict(l=0,r=0,b=0,t=30))
        st.plotly_chart(fig3d, use_container_width=True)
        html = fig3d.to_html(include_plotlyjs='cdn')
        st.download_button("⬇️ Download 3D Plot (HTML)", html, "galaxy_3d.html", "text/html")

    with right:
        st.subheader("Summary Statistics")
        st.dataframe(df_gal.describe().round(2), use_container_width=True)
        st.subheader("Galaxy Type Count")
        type_count = df_gal['Type'].value_counts()
        fig_bar = px.bar(type_count, x=type_count.index, y=type_count.values,
                         color=type_count.index, text_auto=True)
        fig_bar.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white', showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    st.subheader("Correlation Heatmap")
    corr = df_gal[['Distance_Mpc','Mass_Solar','Redshift','Velocity_km_s']].corr()
    fig_corr = px.imshow(corr, text_auto='.2f', color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
    fig_corr.update_layout(paper_bgcolor='black', font_color='white')
    st.plotly_chart(fig_corr, use_container_width=True)

    st.subheader("Key Insights")
    st.markdown("""
    - **Hubble's Law visible**: Redshift strongly correlates with Distance
    - **Mass distribution log-normal**: Typical for astrophysical populations
    - **Spiral galaxies dominate** ~60%
    - **Velocity dispersion** increases with distance
    """)
    csv = df_gal.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Galaxy Dataset (CSV)", csv, "quantum_galaxy_survey.csv", "text/csv")

    with st.expander("📐 Analytics Methods Used"):
        st.markdown("""
        - EDA: describe, value_counts, correlation
        - Visualization: 3D scatter, bar, heatmap
        - Statistical Insight: correlation analysis
        """)

# ---------- EXOPLANET EXPLORER ----------
elif menu == "🪐 Exoplanet Explorer (Real NASA Data)":
    st.title("Exoplanet Explorer — Real NASA Data")
    st.caption("Data source: NASA Exoplanet Archive")

    @st.cache_data(ttl=3600)
    def load_exoplanets():
        url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,hostname,discoverymethod,disc_year,pl_orbper,pl_rade,pl_bmasse,sy_dist+from+ps&format=csv"
        try:
            df = pd.read_csv(url)
            return df.dropna(subset=['pl_name'])
        except Exception:
            # Fallback sample
            return pd.DataFrame({
                'pl_name':['Kepler-22b','Proxima Cen b','TRAPPIST-1e'],
                'discoverymethod':['Transit','Radial Velocity','Transit'],
                'disc_year':[2011,2016,2017],
                'pl_orbper':[289.9,11.2,6.1],
                'pl_rade':[2.4,1.1,0.92],
                'pl_bmasse':[36,1.27,0.62],
                'sy_dist':[195,1.3,12.1]
            })

    df_exo = load_exoplanets()

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Planets", f"{len(df_exo):,}")
    c2.metric("Discovery Methods", df_exo['discoverymethod'].nunique())
    c3.metric("Avg Radius (Earth)", f"{df_exo['pl_rade'].mean():.2f}")
    c4.metric("Closest (pc)", f"{df_exo['sy_dist'].min():.2f}")

    method = st.multiselect("Discovery Method", sorted(df_exo['discoverymethod'].dropna().unique()),
                            default=sorted(df_exo['discoverymethod'].dropna().unique())[:3])
    year_range = st.slider("Discovery Year", int(df_exo['disc_year'].min()), int(df_exo['disc_year'].max()), (2010,2024))

    df_f = df_exo[df_exo['discoverymethod'].isin(method) & df_exo['disc_year'].between(year_range[0], year_range[1])]

    left, right = st.columns(2)
    with left:
        st.subheader("Radius vs Mass")
        fig_sc = px.scatter(df_f.dropna(subset=['pl_rade','pl_bmasse']), x='pl_rade', y='pl_bmasse',
                            color='discoverymethod', hover_name='pl_name', log_y=True)
        fig_sc.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')
        st.plotly_chart(fig_sc, use_container_width=True)

    with right:
        st.subheader("Discoveries per Year")
        yr = df_f['disc_year'].value_counts().sort_index()
        fig_yr = px.bar(x=yr.index, y=yr.values, labels={'x':'Year','y':'Count'})
        fig_yr.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')
        st.plotly_chart(fig_yr, use_container_width=True)

    st.subheader("Top 20 Closest Exoplanets")
    st.dataframe(df_f.sort_values('sy_dist').head(20)[['pl_name','hostname','sy_dist','pl_rade','pl_bmasse','discoverymethod','disc_year']], use_container_width=True)

    csv_exo = df_f.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Filtered Exoplanets (CSV)", csv_exo, "exoplanets.csv", "text/csv")

# ---------- BIG BANG TIMELINE ----------
elif menu == "Big Bang Timeline":
    st.title("Big Bang Timeline — 0 to 13.8 Billion Years")
    time_gyr = st.slider("Universe Age", 0.0, 13.8, 0.38, 0.01, format="%.2f Gyr")

    if time_gyr < 0.001:
        scale = np.exp(time_gyr*1000) * 1e-30
        era = "Inflation"
        desc = "10⁻³⁶ sec me universe 10²⁶ times expand hua"
    elif time_gyr < 0.38:
        scale = (time_gyr/0.38)**0.5 * 0.001
        era = "Radiation Era"
        desc = "Universe plasma se bhara tha"
    elif time_gyr < 9.8:
        scale = (time_gyr/13.8)**(2/3)
        era = "Matter Era"
        desc = "Galaxies aur stars bane"
    else:
        scale = 0.7 * np.exp((time_gyr-9.8)*0.1)
        era = "Dark Energy Era"
        desc = "Accelerated expansion"

    n = 2000
    rng = np.random.default_rng(42)
    r = rng.power(2.5, n) * 12 * (scale**0.3 + 0.1)
    theta = rng.uniform(0, 2*np.pi, n)
    phi = np.arccos(rng.uniform(-1, 1, n))
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi) * 0.4

    fig = go.Figure(data=go.Scatter3d(x=x, y=y, z=z, mode='markers',
        marker=dict(size=2, color=r, colorscale='Plasma', opacity=0.8)))
    fig.update_layout(scene=dict(bgcolor='black', xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
                      paper_bgcolor='black', font_color='white',
                      title=f"Era: {era} | Scale Factor ≈ {scale:.2e}")
    st.plotly_chart(fig, use_container_width=True)

    c1,c2 = st.columns(2)
    with c1:
        st.metric("Age", f"{time_gyr:.2f} Gyr")
        st.metric("Scale Factor", f"{scale:.2e}")
    with c2:
        st.info(f"**{era}**: {desc}")

    with st.expander("📐 Physics Equation"):
        st.latex(r"a(t) \propto \begin{cases} e^{Ht} & \text{Inflation} \\ t^{1/2} & \text{Radiation} \\ t^{2/3} & \text{Matter} \end{cases}")

# ---------- 3D GALAXY ----------
elif menu == "3D Galaxy Universe":
    st.title("3D Galaxy Universe")
    fig = go.Figure(data=go.Scatter3d(x=df_gal['x'], y=df_gal['y'], z=df_gal['z'],
        mode='markers', marker=dict(size=2, color=df_gal['Redshift'], colorscale='Plasma')))
    fig.update_layout(scene=dict(bgcolor='black'), paper_bgcolor='black', font_color='white')
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("📐 Physics"):
        st.latex(r"\delta\rho/\rho \sim 10^{-5}")

# ---------- BLACK HOLE ----------
elif menu == "Black Hole + Galaxy":
    st.title("Supermassive Black Hole")
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(x=df_gal['x'], y=df_gal['y'], z=df_gal['z'], mode='markers',
        marker=dict(size=2, color=df_gal['Distance_Mpc'], colorscale='Hot')))
    fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers',
        marker=dict(size=20, color='black', line=dict(color='cyan', width=3))))
    fig.update_layout(scene=dict(bgcolor='black'), paper_bgcolor='black', font_color='white')
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("📐 Physics"):
        st.latex(r"R_s = \frac{2GM}{c^2}")

# ---------- SCHRÖDINGER ----------
elif menu == "Schrödinger Wave Packet":
    st.title("Schrödinger Wave Packet")
    x = np.linspace(-10,10,500)
    sigma = st.slider("Wave Spread σ", 0.3, 2.0, 0.8, 0.1)
    prob = np.exp(-x**2/(sigma**2))
    fig = go.Figure(go.Scatter(x=x, y=prob, fill='tozeroy', line_color='#00e5ff'))
    fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("📐 Physics"):
        st.latex(r"\Delta x \,\Delta p \geq \frac{\hbar}{2}")

# ---------- INFLATION ----------
elif menu == "Cosmic Inflation":
    st.title("Cosmic Inflation")
    t = np.linspace(0,10,500)
    a = np.exp(t); a[t>6] = a[300]*(t[t>6]/6)**0.5
    fig = go.Figure(go.Scatter(x=t, y=a, line=dict(color='#ff3d8a', width=4)))
    fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white', yaxis_type='log')
    st.plotly_chart(fig, use_container_width=True)

# ---------- CMB ----------
else:
    st.title("Quantum Fluctuations + NASA CMB")
    size = 256
    rng = np.random.default_rng(0)
    kx = np.fft.fftfreq(size)[:,None]; ky = np.fft.fftfreq(size)[None,:]
    k = np.sqrt(kx**2 + ky**2); k[0,0]=1e-6
    Pk = k**(-0.035)
    phase = rng.uniform(0,2*np.pi,(size,size))
    field = np.fft.ifft2(np.sqrt(Pk)*(np.cos(phase)+1j*np.sin(phase))).real
    fig = go.Figure(data=go.Heatmap(z=field, colorscale='RdBu'))
    fig.update_layout(paper_bgcolor='black', font_color='white')
    st.plotly_chart(fig, use_container_width=True)