import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# CONFIG
FILE_PATH = "smartfinanceai_datasets_v3.xlsx"

COLORS = {
    "primary": "#185FA5",
    "danger":  "#A32D2D",
    "success": "#1D9E75",
    "purple":  "#534AB7",
    "amber":   "#854F0B",
    "gray":    "#5F5E5A",
}
PALETTE = list(COLORS.values())

plt.rcParams.update({
    "font.family":       "DejaVu Sans",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.alpha":        0.2,
    "grid.linestyle":    "--",
    "figure.dpi":        120,
    "axes.titlesize":    11,
    "axes.titleweight":  "bold",
    "axes.labelsize":    9,
    "xtick.labelsize":   8,
    "ytick.labelsize":   8,
})

# PAGE CONFIG
st.set_page_config(
    page_title="SmartFinanceAI Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# LOAD DATA
@st.cache_data
def load_data():
    df_tx   = pd.read_excel(FILE_PATH, sheet_name="1_Dummy_Testing", header=1)
    df_anal = pd.read_excel(FILE_PATH, sheet_name="2_Analitik",      header=1)
    df_ml   = pd.read_excel(FILE_PATH, sheet_name="3_ML_AI",         header=1)
    df_tx["transaction_date"] = pd.to_datetime(df_tx["transaction_date"])
    df_tx["month"] = df_tx["transaction_date"].dt.to_period("M").astype(str)
    df_anal["month"] = df_anal["month"].astype(str)
    return df_tx, df_anal, df_ml

df_tx, df_anal, df_ml = load_data()

# SIDEBAR
with st.sidebar:
    st.image("https://img.icons8.com/fluency/48/commercial-development-management.png", width=48)
    st.title("SmartFinanceAI")
    st.caption("Dashboard Analitik Keuangan")
    st.divider()

    page = st.radio(
        "Navigasi",
        ["🏠 Overview", "📊 EDA & Insight", "✅ Kesimpulan"],
        label_visibility="collapsed",
    )
    st.divider()

    st.subheader("Filter Data")

    all_styles   = sorted(df_tx["spending_style"].dropna().unique())
    sel_styles   = st.multiselect("Spending Style", all_styles, default=all_styles)

    all_ages     = sorted(df_tx["age_range"].dropna().unique())
    sel_ages     = st.multiselect("Age Range", all_ages, default=all_ages)

    all_months   = sorted(df_tx["month"].dropna().unique())
    sel_months   = st.multiselect("Bulan Transaksi", all_months, default=all_months)

    all_profiles = sorted(df_anal["risk_profile"].dropna().unique())
    sel_profiles = st.multiselect("Risk Profile", all_profiles, default=all_profiles)

    st.divider()
    st.caption("Proyek: SmartFinanceAI\nData Science Capstone")

# FILTER
tx = df_tx[
    df_tx["spending_style"].isin(sel_styles) &
    df_tx["age_range"].isin(sel_ages) &
    df_tx["month"].isin(sel_months)
]
anal = df_anal[df_anal["risk_profile"].isin(sel_profiles)]
ml   = df_ml[
    df_ml["spending_style"].isin(sel_styles) &
    df_ml["age_range"].isin(sel_ages)
]

# HELPER
def fig_to_st(fig):
    st.pyplot(fig)
    plt.close(fig)

# PAGE 1 — OVERVIEW
if page == "🏠 Overview":
    st.title("🏠 Overview — SmartFinanceAI")
    st.markdown(
        "Platform berbasis web yang mengintegrasikan AI untuk menganalisis data historis, "
        "mengidentifikasi pola perilaku finansial, dan memberikan saran personal kepada pengguna."
    )
    st.divider()

    # KPI Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    total_tx      = len(tx)
    total_users   = tx["user_id"].nunique()
    deficit_pct   = (anal["balance"] < 0).mean() * 100
    avg_sav       = anal["saving_rate_%"].mean()
    avg_exp_ratio = anal["expense_ratio_%"].mean()

    col1.metric("Total Transaksi",  f"{total_tx:,}")
    col2.metric("Total User",       f"{total_users}")
    col3.metric("User Defisit",     f"{deficit_pct:.1f}%",  delta="⚠ Balance negatif", delta_color="inverse")
    col4.metric("Avg Saving Rate",  f"{avg_sav:.1f}%",      delta="Target >30%")
    col5.metric("Avg Expense Ratio",f"{avg_exp_ratio:.1f}%",delta="⚠ Di atas 70%",     delta_color="inverse")

    st.divider()

    # Latar belakang masalah
    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("🔴 Masalah yang Diidentifikasi")
        problems = [
            "Rendahnya literasi finansial di kalangan generasi muda",
            "Kurangnya kebiasaan mencatat transaksi keuangan",
            "Gaya hidup konsumtif dan fenomena Pay Later",
            "Banyak individu tidak menyadari kondisi keuangan mereka",
            "Aplikasi keuangan hanya fokus pencatatan tanpa analisis mendalam",
            "Ketidakmampuan memahami pola pengeluaran berdampak jangka panjang",
        ]
        for p in problems:
            st.markdown(f"- {p}")

    with col_r:
        st.subheader("✅ Solusi SmartFinanceAI")
        solutions = [
            "Sistem manajemen keuangan dengan wawasan bermakna",
            "Analisis data untuk identifikasi pola pengeluaran & perilaku finansial",
            "Sistem rekomendasi berbasis AI yang efektif & mudah dipahami",
            "Platform berbasis web yang mengintegrasikan AI",
            "Analisis histori transaksi & identifikasi pola perilaku",
            "Arahan konkret agar pengguna bisa membuat keputusan finansial lebih cerdas",
        ]
        for s in solutions:
            st.markdown(f"- {s}")

    st.divider()
    st.subheader("📋 5 Business Questions")
    bqs = {
        "BQ 1 — Spending Prediction":
            "Berapa perkiraan total pengeluaran user di bulan berikutnya berdasarkan histori transaksi 3 bulan terakhir?",
        "BQ 2 — Anomaly Detection":
            "Apakah sebuah transaksi termasuk tidak wajar, berdasarkan jumlahnya yang melebihi 3× rata-rata pengeluaran harian user?",
        "BQ 3 — User Segmentation":
            "Termasuk tipe keuangan mana seorang user — saver, balanced, investor, atau overspender — berdasarkan saving rate dan budget utilization?",
        "BQ 4 — AI Recommendation":
            "Rekomendasi keuangan apa yang paling relevan untuk diberikan kepada user bulan ini berdasarkan pola pengeluaran dan kondisi budgetnya?",
        "BQ 5 — Financial Health":
            "Seberapa sehat kondisi keuangan user bulan ini, dinyatakan dalam skor 0–100 berdasarkan saving rate, budget utilization, dan konsistensi pemenuhan target?",
    }
    for title, desc in bqs.items():
        with st.expander(title):
            st.write(desc)

# PAGE 2 — EDA & INSIGHT
elif page == "📊 EDA & Insight":
    st.title("📊 EDA & Insight")
    st.caption("Exploratory Data Analysis berdasarkan filter yang dipilih di sidebar.")

    tab1, tab2, tab3 = st.tabs(["💳 Transaksi", "👤 Profil User", "🤖 ML/AI Features"])

    # TAB 1: TRANSAKSI 
    with tab1:
        st.subheader("Ringkasan Transaksi")
        c1, c2, c3, c4 = st.columns(4)
        exp_only = tx[tx["type"] == "expense"]
        c1.metric("Total Expense",     f"Rp {exp_only['amount'].sum()/1e6:.1f} jt")
        c2.metric("Avg per Transaksi", f"Rp {exp_only['amount'].mean()/1e3:.0f} rb")
        c3.metric("Transaksi Expense", f"{len(exp_only):,}")
        c4.metric("Kategori Terbesar", exp_only.groupby("category")["amount"].sum().idxmax() if len(exp_only) else "-")

        col_l, col_r = st.columns(2)

        with col_l:
            st.markdown("**Total pengeluaran per kategori**")
            cat_sum = exp_only.groupby("category")["amount"].sum().sort_values()
            fig, ax = plt.subplots(figsize=(5, 4))
            ax.barh(cat_sum.index, cat_sum.values / 1_000,
                    color=COLORS["primary"], edgecolor="white", linewidth=0.6, height=0.6)
            ax.set_xlabel("Rp ribu")
            fig.tight_layout()
            fig_to_st(fig)

        with col_r:
            st.markdown("**Tren income vs expense per bulan**")
            monthly = tx.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0)
            fig, ax = plt.subplots(figsize=(5, 4))
            x = range(len(monthly))
            w = 0.35
            if "income" in monthly.columns:
                ax.bar([i - w/2 for i in x], monthly["income"] / 1_000,
                       width=w, color=COLORS["success"], edgecolor="white", label="Income")
            if "expense" in monthly.columns:
                ax.bar([i + w/2 for i in x], monthly["expense"] / 1_000,
                       width=w, color=COLORS["danger"], edgecolor="white", label="Expense")
            ax.set_xticks(list(x))
            ax.set_xticklabels(monthly.index, rotation=10)
            ax.set_ylabel("Rp ribu")
            ax.legend(fontsize=8)
            fig.tight_layout()
            fig_to_st(fig)

        st.markdown("**Distribusi amount per kategori (boxplot)**")
        fig, ax = plt.subplots(figsize=(10, 3.5))
        order = exp_only.groupby("category")["amount"].median().sort_values(ascending=False).index
        sns.boxplot(data=exp_only, x="category", y="amount", order=order,
                    color=COLORS["primary"], ax=ax, linewidth=0.7,
                    flierprops={"markersize": 2, "alpha": 0.3})
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"Rp {v/1e6:.1f}jt"))
        ax.set_xlabel("")
        fig.tight_layout()
        fig_to_st(fig)

        # Insight
        st.info(
            f"💡 **Insight:** Kategori dengan total pengeluaran terbesar adalah "
            f"**{exp_only.groupby('category')['amount'].sum().idxmax()}**. "
            f"Terdapat **{(tx['amount'] > tx['amount'].mean()*3).sum()} transaksi anomali** "
            f"(>3× rata-rata) yang perlu diwaspadai."
        )

    # TAB 2: PROFIL USER
    with tab2:
        st.subheader("Profil & Kesehatan Keuangan User")
        c1, c2, c3, c4 = st.columns(4)
        deficit_n = (anal["balance"] < 0).sum()
        c1.metric("Avg Saving Rate",    f"{anal['saving_rate_%'].mean():.1f}%")
        c2.metric("Avg Expense Ratio",  f"{anal['expense_ratio_%'].mean():.1f}%")
        c3.metric("Avg Saving Progress",f"{anal['saving_progress_%'].mean():.1f}%")
        c4.metric("Records Defisit",    f"{deficit_n} / {len(anal)}")

        col_l, col_r = st.columns(2)

        with col_l:
            st.markdown("**Saving rate & expense ratio per risk profile**")
            rp = anal.groupby("risk_profile")[["saving_rate_%", "expense_ratio_%"]].mean()
            fig, ax = plt.subplots(figsize=(5, 3.5))
            x = range(len(rp))
            w = 0.35
            ax.bar([i - w/2 for i in x], rp["saving_rate_%"],
                   width=w, color=COLORS["success"], edgecolor="white", label="Saving rate")
            ax.bar([i + w/2 for i in x], rp["expense_ratio_%"],
                   width=w, color=COLORS["danger"], edgecolor="white", label="Expense ratio")
            ax.set_xticks(list(x)); ax.set_xticklabels(rp.index)
            ax.yaxis.set_major_formatter(mtick.PercentFormatter())
            ax.legend(fontsize=8)
            fig.tight_layout()
            fig_to_st(fig)

        with col_r:
            st.markdown("**Distribusi balance (histogram)**")
            fig, ax = plt.subplots(figsize=(5, 3.5))
            ax.hist(anal["balance"] / 1_000, bins=25, color=COLORS["primary"],
                    edgecolor="white", linewidth=0.5, alpha=0.85)
            ax.axvline(0, color="red", linestyle="--", linewidth=1.5, label="Balance = 0")
            neg_pct = (anal["balance"] < 0).mean() * 100
            ax.set_xlabel("Balance (Rp ribu)")
            ax.set_title(f"{neg_pct:.1f}% records balance negatif")
            ax.legend(fontsize=8)
            fig.tight_layout()
            fig_to_st(fig)

        st.markdown("**Scatter: expense ratio vs saving rate per user per bulan**")
        merged = anal.merge(
            ml[["user_id", "spending_style"]].drop_duplicates("user_id"), on="user_id", how="left"
        )
        style_colors = {
            "impulsive": COLORS["danger"],
            "balanced":  COLORS["primary"],
            "frugal":    COLORS["success"],
        }
        fig, ax = plt.subplots(figsize=(10, 3.5))
        for style, grp in merged.groupby("spending_style"):
            ax.scatter(grp["expense_ratio_%"], grp["saving_rate_%"],
                       c=style_colors.get(style, COLORS["gray"]),
                       label=style.capitalize(), alpha=0.55, s=30, edgecolors="none")
        ax.axvline(100, linestyle="--", color="red", alpha=0.3, linewidth=1)
        ax.set_xlabel("Expense Ratio (%)"); ax.set_ylabel("Saving Rate (%)")
        ax.legend(fontsize=8)
        fig.tight_layout()
        fig_to_st(fig)

        st.info(
            "💡 **Insight:** User usia **35+** memiliki expense ratio terendah (65.6%) "
            "dan saving rate tertinggi — pola keuangan paling sehat. "
            "Sebaliknya, **18–24** paling rentan dengan expense ratio 81.3%."
        )

    # TAB 3: ML/AI FEATURES
    with tab3:
        st.subheader("Distribusi Fitur ML/AI")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Records ML",   f"{len(ml):,}")
        c2.metric("Jenis Rekomendasi",  f"{ml['recommendation_type'].nunique()}")
        c3.metric("Priority High",      f"{(ml['priority_label']=='high').sum()} records")

        col_l, col_r = st.columns(2)

        with col_l:
            st.markdown("**Distribusi recommendation type**")
            rec = ml["recommendation_type"].value_counts()
            fig, ax = plt.subplots(figsize=(5, 3.5))
            ax.barh(rec.index, rec.values, color=PALETTE[:len(rec)],
                    edgecolor="white", linewidth=0.6, height=0.6)
            ax.set_xlabel("Jumlah Records")
            fig.tight_layout()
            fig_to_st(fig)

        with col_r:
            st.markdown("**Recommendation type per spending style**")
            rc = ml.groupby(["spending_style", "recommendation_type"]).size().unstack(fill_value=0)
            fig, ax = plt.subplots(figsize=(5, 3.5))
            rc.plot(kind="bar", ax=ax, stacked=True, color=PALETTE[:len(rc.columns)],
                    edgecolor="white", linewidth=0.4, width=0.6)
            ax.set_xlabel(""); ax.set_xticklabels(rc.index, rotation=0)
            ax.legend(fontsize=7, title="Rec type", title_fontsize=8)
            fig.tight_layout()
            fig_to_st(fig)

        st.markdown("**Heatmap korelasi fitur numerik**")
        num_cols = ["total_income", "total_expense", "expense_ratio_%",
                    "saving_rate_%", "saving_progress_%", "num_transactions"]
        corr = ml[num_cols].corr()
        corr.columns = ["tot_income", "tot_expense", "exp_ratio", "sav_rate", "sav_progress", "n_tx"]
        corr.index   = corr.columns
        fig, ax = plt.subplots(figsize=(10, 3.5))
        sns.heatmap(corr, ax=ax, annot=True, fmt=".2f", cmap="RdYlGn",
                    center=0, linewidths=0.4, annot_kws={"size": 8},
                    square=True, cbar_kws={"shrink": 0.7})
        ax.tick_params(axis="x", rotation=30)
        fig.tight_layout()
        fig_to_st(fig)

        st.info(
            "💡 **Insight:** Seluruh rekomendasi **behavior_based** diberikan ke user "
            "impulsive. User frugal dominan mendapat rekomendasi **budgeting** — "
            "fokus optimasi pengeluaran yang sudah terkendali."
        )

# PAGE 3 — KESIMPULAN
elif page == "✅ Kesimpulan":
    st.title("✅ Kesimpulan & Rekomendasi")
    st.divider()

    st.subheader("📌 Temuan Utama EDA")

    findings = [
        ("🔴 50.7% user defisit",
         "Lebih dari separuh user memiliki balance negatif minimal 1 bulan. "
         "Ini mengindikasikan kebutuhan mendesak fitur **budget alert** dan notifikasi real-time."),
        ("📉 Saving rate rata-rata hanya 31.9%",
         "Mayoritas user belum mencapai target tabungan bulanan mereka. "
         "Generasi 18–24 paling rentan dengan expense ratio 81.3%."),
        ("🛍️ Shopping & Education dominasi pengeluaran",
         "Kedua kategori ini memiliki total pengeluaran tertinggi dan variance terbesar — "
         "berpotensi menjadi area anomali transaksi."),
        ("⚠️ 7.3% transaksi berpotensi anomali",
         "Transaksi melebihi 3× rata-rata harian user sudah teridentifikasi — "
         "siap dijadikan baseline model Anomaly Detection (BQ 2)."),
        ("🧠 Data ML siap digunakan",
         "6 jenis rekomendasi tersedia sebagai label target klasifikasi. "
         "Fitur numerik memiliki korelasi yang sesuai untuk modeling — tidak ada multikolinearitas parah."),
    ]

    for title, desc in findings:
        with st.expander(title, expanded=True):
            st.write(desc)

    st.divider()
    st.subheader("🎯 Rekomendasi untuk Tahap Berikutnya")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Modeling yang Direkomendasikan**")
        recs = [
            ("BQ 1 Spending Prediction",  "Linear Regression / Prophet",   "Fitur: avg_daily_expense 3 bulan"),
            ("BQ 2 Anomaly Detection",    "Isolation Forest / Z-score",     "Threshold: >3× avg harian"),
            ("BQ 3 User Segmentation",    "K-Means Clustering",             "Fitur: saving_rate, expense_ratio"),
            ("BQ 4 AI Recommendation",    "Random Forest Classifier",       "6 label target tersedia"),
            ("BQ 5 Financial Health",     "Weighted Scoring Formula",       "Komponen: 3 fitur utama"),
        ]
        for bq, model, note in recs:
            st.markdown(f"**{bq}**")
            st.caption(f"Model: {model} — {note}")
            st.markdown("")

    with col2:
        st.markdown("**Kualitas Dataset**")
        quality = {
            "Missing values (kolom kunci)": "✅ 0 missing",
            "Jumlah transaksi":             "✅ 1.000 records",
            "Jumlah user":                  "✅ 50 user unik",
            "Periode data":                 "✅ 3 bulan (Mar–Mei 2026)",
            "Label ML tersedia":            "✅ spending_style, risk_profile, recommendation_type",
            "Imbalance label":              "⚠️ Perlu dicek sebelum modeling",
        }
        for k, v in quality.items():
            st.markdown(f"**{k}:** {v}")

    st.divider()
    st.subheader("💡 Kesimpulan Akhir")
    st.success(
        "Dataset SmartFinanceAI dalam kondisi bersih dan lengkap untuk seluruh 5 business questions. "
        "EDA mengkonfirmasi bahwa masalah literasi finansial generasi muda tercermin nyata dalam data — "
        "50.7% user defisit, saving rate rendah, dan pola konsumtif yang teridentifikasi. "
        "Platform SmartFinanceAI dengan pendekatan AI-driven recommendation memiliki dasar data yang "
        "kuat untuk dikembangkan ke tahap modeling."
    )

    st.divider()
    st.caption("SmartFinanceAI [CC26-PSU170]")