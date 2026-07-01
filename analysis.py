import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import warnings
warnings.filterwarnings('ignore')

# ── Brand palette ──────────────────────────────────────────────
RED     = '#E23744'
ORANGE  = '#FF6F2C'
DARK    = '#1A1A2E'
GREY    = '#2D2D44'
LIGHT   = '#F5F5F5'
WHITE   = '#FFFFFF'
ACCENT1 = '#FFB300'
ACCENT2 = '#00C9A7'
ACCENT3 = '#845EC2'

CUISINE_COLORS = {
    'North Indian': '#E23744', 'Chinese': '#FF6F2C', 'Italian': '#FFB300',
    'Fast Food': '#00C9A7',   'South Indian': '#845EC2','Japanese': '#4B7BEC',
    'Biryani': '#FD7272',     'Continental': '#A29BFE','Mughlai': '#FDCB6E',
    'Healthy/Salads': '#55EFC4',
}

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'text.color': DARK,
    'axes.labelcolor': DARK, 'xtick.color': DARK, 'ytick.color': DARK,
    'axes.spines.top': False, 'axes.spines.right': False,
})

df = pd.read_csv(r'C:\Users\Abhay\Documents\Zomato_analysis\zomato_orders.csv')
df['date'] = pd.to_datetime(df['date'])

# ═══════════════════════════════════════════════════════════════
# FIGURE 1 – DASHBOARD (3×2)
# ═══════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(20, 14), facecolor=LIGHT)
fig.suptitle('🍽  Zomato Order Pattern Analysis  |  2024', fontsize=22, fontweight='bold',
             color=DARK, y=0.97)

gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35,
                       top=0.92, bottom=0.05, left=0.05, right=0.97)

# ── KPI strip ─────────────────────────────────────────────────
kpi_ax = fig.add_axes([0.05, 0.88, 0.92, 0.07], facecolor=DARK)
kpi_ax.set_xlim(0, 4); kpi_ax.set_ylim(0, 1); kpi_ax.axis('off')
kpis = [
    ('Total Orders', f"{len(df):,}"),
    ('Avg Order Value', f"₹{df.order_value.mean():.0f}"),
    ('Avg Delivery Time', f"{df.delivery_time.mean():.1f} min"),
    ('Avg Rating', f"⭐ {df.rating.mean():.2f}"),
]
for i, (label, val) in enumerate(kpis):
    kpi_ax.text(i + 0.5, 0.72, val, ha='center', va='center', fontsize=17,
                fontweight='bold', color=RED if i == 0 else WHITE)
    kpi_ax.text(i + 0.5, 0.22, label, ha='center', va='center', fontsize=9,
                color='#AAAACC')
    if i < 3:
        kpi_ax.axvline(i + 1, color='#444466', linewidth=1)

# ── 1. Peak Ordering Hours ─────────────────────────────────────
ax1 = fig.add_subplot(gs[0, :2])
hourly = df.groupby('hour').size().reindex(range(24), fill_value=0)
colors = [RED if h in [12,13,19,20,21] else ORANGE if h in [1,2,8,9,14,18] else '#CCCCCC'
          for h in range(24)]
bars = ax1.bar(range(24), hourly.values, color=colors, width=0.75, edgecolor=WHITE, linewidth=0.4)
ax1.set_xticks(range(24))
ax1.set_xticklabels([f'{h:02d}:00' for h in range(24)], rotation=45, fontsize=7)
ax1.set_title('📊 Peak Ordering Hours (24h)', fontweight='bold', fontsize=12, pad=8)
ax1.set_ylabel('Orders', fontsize=9); ax1.set_facecolor(WHITE)
ax1.yaxis.grid(True, linestyle='--', alpha=0.4)
for i in [12, 19, 20]:
    ax1.annotate(f'{hourly[i]}', xy=(i, hourly[i]), xytext=(0, 5),
                 textcoords='offset points', ha='center', fontsize=7, color=RED, fontweight='bold')
ax1.legend(handles=[
    plt.Rectangle((0,0),1,1, color=RED, label='Peak Hours'),
    plt.Rectangle((0,0),1,1, color=ORANGE, label='Moderate'),
    plt.Rectangle((0,0),1,1, color='#CCCCCC', label='Low'),
], loc='upper left', fontsize=8)

# ── 2. Day-of-Week heatmap (orders × hour) ────────────────────
ax2 = fig.add_subplot(gs[0, 2])
days_order = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
heat = df.groupby(['day_of_week','hour']).size().unstack(fill_value=0).reindex(days_order)
im = ax2.imshow(heat.values, aspect='auto', cmap='YlOrRd', interpolation='nearest')
ax2.set_yticks(range(7)); ax2.set_yticklabels(days_order, fontsize=8)
ax2.set_xticks([0,6,12,18,23])
ax2.set_xticklabels(['0h','6h','12h','18h','23h'], fontsize=7)
ax2.set_title('🔥 Order Heatmap\n(Day × Hour)', fontweight='bold', fontsize=11, pad=6)
plt.colorbar(im, ax=ax2, fraction=0.035, label='Orders')

# ── 3. Cuisine Demand ─────────────────────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
cuisine_cnt = df.groupby('cuisine').size().sort_values(ascending=True)
ccolors = [CUISINE_COLORS.get(c, RED) for c in cuisine_cnt.index]
ax3.barh(cuisine_cnt.index, cuisine_cnt.values, color=ccolors, height=0.65, edgecolor=WHITE)
ax3.set_title('🍜 Cuisine Demand', fontweight='bold', fontsize=11, pad=6)
ax3.set_xlabel('Orders', fontsize=8); ax3.set_facecolor(WHITE)
for i, v in enumerate(cuisine_cnt.values):
    ax3.text(v + 5, i, str(v), va='center', fontsize=7.5, color=DARK)

# ── 4. Delivery Time vs Rating scatter ───────────────────────
ax4 = fig.add_subplot(gs[1, 1])
sample = df.sample(800, random_state=1)
sc = ax4.scatter(sample.delivery_time, sample.rating, alpha=0.35, s=18,
                 c=sample.rating, cmap='RdYlGn', vmin=1, vmax=5, edgecolors='none')
m, b = np.polyfit(df.delivery_time, df.rating, 1)
x_line = np.linspace(10, 90, 100)
ax4.plot(x_line, m*x_line + b, color=RED, linewidth=2, label=f'Trend (r={np.corrcoef(df.delivery_time,df.rating)[0,1]:.2f})')
ax4.set_xlabel('Delivery Time (min)', fontsize=9)
ax4.set_ylabel('Customer Rating', fontsize=9)
ax4.set_title('⏱️  Delivery Time vs Rating', fontweight='bold', fontsize=11, pad=6)
ax4.set_facecolor(WHITE); ax4.legend(fontsize=8)
plt.colorbar(sc, ax=ax4, fraction=0.035, label='Rating')

# ── 5. Avg delivery time by cuisine ──────────────────────────
ax5 = fig.add_subplot(gs[1, 2])
cuis_del = df.groupby('cuisine')['delivery_time'].mean().sort_values()
bar_colors = [ACCENT2 if v < cuis_del.median() else RED for v in cuis_del.values]
ax5.bar(range(len(cuis_del)), cuis_del.values, color=bar_colors, edgecolor=WHITE)
ax5.set_xticks(range(len(cuis_del)))
ax5.set_xticklabels(cuis_del.index, rotation=45, ha='right', fontsize=7.5)
ax5.axhline(cuis_del.mean(), color=ACCENT1, linestyle='--', linewidth=1.5, label=f'Mean: {cuis_del.mean():.1f} min')
ax5.set_title('🛵 Avg Delivery Time\nby Cuisine', fontweight='bold', fontsize=11, pad=6)
ax5.set_ylabel('Minutes', fontsize=8); ax5.set_facecolor(WHITE)
ax5.legend(fontsize=8)

# ── 6. Monthly Revenue trend ─────────────────────────────────
ax6 = fig.add_subplot(gs[2, :2])
month_order = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']
monthly = df.groupby('month')['order_value'].sum().reindex(month_order).dropna()
ax6.fill_between(range(len(monthly)), monthly.values, alpha=0.25, color=RED)
ax6.plot(range(len(monthly)), monthly.values, color=RED, linewidth=2.5, marker='o', markersize=6)
ax6.set_xticks(range(len(monthly)))
ax6.set_xticklabels([m[:3] for m in monthly.index], fontsize=9)
ax6.set_title('📈 Monthly Revenue Trend (₹)', fontweight='bold', fontsize=11, pad=6)
ax6.set_ylabel('Total Revenue (₹)', fontsize=9); ax6.set_facecolor(WHITE)
ax6.yaxis.grid(True, linestyle='--', alpha=0.4)

# ── 7. Rating distribution pie ───────────────────────────────
ax7 = fig.add_subplot(gs[2, 2])
bins = pd.cut(df.rating, bins=[0,2,3,4,4.5,5], labels=['1–2','2–3','3–4','4–4.5','4.5–5'])
rating_dist = bins.value_counts().sort_index()
wedge_colors = ['#E74C3C','#E67E22','#F1C40F','#2ECC71','#1ABC9C']
wedges, texts, auts = ax7.pie(rating_dist, labels=rating_dist.index, autopct='%1.1f%%',
                               colors=wedge_colors, startangle=90, pctdistance=0.75,
                               wedgeprops=dict(edgecolor=WHITE, linewidth=1.5))
for t in texts: t.set_fontsize(8)
for a in auts:  a.set_fontsize(7.5)
ax7.set_title('⭐ Rating Distribution', fontweight='bold', fontsize=11, pad=6)

plt.savefig('dashboard.png',
            dpi=150,
            bbox_inches='tight',
            facecolor=LIGHT)
plt.close()
print("Dashboard saved.")

# ═══════════════════════════════════════════════════════════════
# FIGURE 2 – BUSINESS RECOMMENDATIONS
# ═══════════════════════════════════════════════════════════════
fig2, axes = plt.subplots(2, 2, figsize=(18, 10), facecolor=LIGHT)
fig2.suptitle('📋  Business Insights & Recommendations', fontsize=18, fontweight='bold',
              color=DARK, y=0.97)

# A. Cuisine avg rating
ax = axes[0][0]
cuis_rat = df.groupby('cuisine')['rating'].mean().sort_values(ascending=False)
bar_c = [ACCENT2 if v >= cuis_rat.median() else RED for v in cuis_rat]
ax.bar(range(len(cuis_rat)), cuis_rat.values, color=bar_c, edgecolor=WHITE)
ax.set_xticks(range(len(cuis_rat)))
ax.set_xticklabels(cuis_rat.index, rotation=45, ha='right', fontsize=8)
ax.set_ylim(3.5, 4.5)
ax.axhline(cuis_rat.mean(), linestyle='--', color=ACCENT1, linewidth=1.5,
           label=f'Mean: {cuis_rat.mean():.2f}')
ax.set_title('Avg Rating by Cuisine', fontweight='bold', fontsize=12)
ax.set_ylabel('Rating', fontsize=9); ax.set_facecolor(WHITE); ax.legend(fontsize=8)

# B. Peak slot planning
ax = axes[0][1]
slot_map = {h: ('Breakfast(7-10)' if 7<=h<10 else
                'Lunch(11-14)'    if 11<=h<14 else
                'Snack(15-17)'    if 15<=h<17 else
                'Dinner(18-22)'   if 18<=h<22 else
                'Off-peak')       for h in range(24)}
df['slot'] = df['hour'].map(slot_map)
slot_rev = df.groupby('slot')['order_value'].sum().sort_values(ascending=False)
slot_ord = df.groupby('slot').size().reindex(slot_rev.index)
slot_colors = [RED, ORANGE, ACCENT1, ACCENT2, ACCENT3][:len(slot_rev)]
ax2b = ax.twinx()
ax.bar(range(len(slot_rev)), slot_rev.values/1000, color=slot_colors, alpha=0.8, label='Revenue (₹K)')
ax2b.plot(range(len(slot_rev)), slot_ord.values, 'ko--', linewidth=2, markersize=7, label='Orders')
ax.set_xticks(range(len(slot_rev)))
ax.set_xticklabels(slot_rev.index, rotation=15, fontsize=9)
ax.set_ylabel('Revenue (₹ thousands)', fontsize=9)
ax2b.set_ylabel('Orders', fontsize=9)
ax.set_title('Revenue & Orders by Time Slot', fontweight='bold', fontsize=12)
ax.set_facecolor(WHITE)
lines1, lbl1 = ax.get_legend_handles_labels()
lines2, lbl2 = ax2b.get_legend_handles_labels()
ax.legend(lines1 + lines2, lbl1 + lbl2, fontsize=8)

# C. Discount impact on order value
ax = axes[1][0]
disc_val = df.groupby('discount_pct')['order_value'].mean()
disc_cnt = df.groupby('discount_pct').size()
ax.bar(disc_val.index.astype(str).map(lambda x: x+'%'), disc_val.values,
       color=[ACCENT2, ACCENT1, ORANGE, RED], width=0.5, edgecolor=WHITE)
ax.set_title('Discount % vs Avg Order Value', fontweight='bold', fontsize=12)
ax.set_xlabel('Discount', fontsize=9); ax.set_ylabel('Avg Order Value (₹)', fontsize=9)
ax.set_facecolor(WHITE)
for i, (v, c) in enumerate(zip(disc_val.values, disc_cnt.values)):
    ax.text(i, v + 3, f'₹{v:.0f}\n(n={c})', ha='center', fontsize=8, color=DARK)

# D. Top 5 restaurants
ax = axes[1][1]
top5_rev = df.groupby('restaurant')['order_value'].sum().nlargest(5)
top5_rat = df.groupby('restaurant')['rating'].mean().reindex(top5_rev.index)
x = np.arange(len(top5_rev))
width = 0.35
b1 = ax.bar(x - width/2, top5_rev.values/1000, width, color=RED, label='Revenue (₹K)', alpha=0.85)
ax2c = ax.twinx()
b2 = ax2c.bar(x + width/2, top5_rat.values, width, color=ACCENT1, label='Avg Rating', alpha=0.85)
ax.set_xticks(x); ax.set_xticklabels(top5_rev.index, rotation=20, ha='right', fontsize=8)
ax.set_ylabel('Revenue (₹ thousands)', fontsize=9)
ax2c.set_ylabel('Avg Rating', fontsize=9); ax2c.set_ylim(3, 5)
ax.set_title('Top 5 Restaurants: Revenue vs Rating', fontweight='bold', fontsize=12)
ax.set_facecolor(WHITE)
ax.legend(loc='upper left', fontsize=8); ax2c.legend(loc='upper right', fontsize=8)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(r'C:\Users\Abhay\Documents\Zomato_analysis\dashboard.png',
            dpi=150,
            bbox_inches='tight',
            facecolor=LIGHT)
plt.close()
print("Insights chart saved.")
