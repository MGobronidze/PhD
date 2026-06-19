"""
ფიგურა 1 — გრაფი G: θ-ციკლი κ-სიმძლავრის ხისტი ხეებით
[10] ყიფიანის თეორემის საილუსტრაციო ნახაზი

ციკლის სიგრძე: θ  (სასრული, წინასწარ დასახელებული)
ხეების სიმძლავრე: κ
ავტომორფიზმთა ჯგუფი: |Aut(G)| = θ
გრაფის სიმძლავრე: |G| = κ
"""

import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np

# ფერები
CYCLE_NODE_COLOR = "#7F77DD"
TREE_NODE_COLOR  = "#1D9E75"
EDGE_COLOR       = "#888780"
TREE_EDGE_COLOR  = "#B4B2A9"
DASHED_COLOR     = "#534AB7"   # წყვეტილი წიბოს ფერი (მუქი იისფერი)
BG_COLOR         = "#FFFFFF"
TEXT_COLOR       = "#2C2C2A"
SUBTITLE_COLOR   = "#5F5E5A"

fig, ax = plt.subplots(figsize=(10, 9))
ax.set_aspect("equal")
ax.axis("off")
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

# ---- ციკლის კვანძები -------------------------------------------------------
# ვიზუალურად 6 კვანძი, ბოლო წიბო წყვეტილია → „ნებისმიერი θ"
N = 6
cx, cy = 0.0, 0.0
R = 1.6
cycle_nodes = [
    (cx + R * math.sin(2 * math.pi * i / N),
     cy + R * math.cos(2 * math.pi * i / N))
    for i in range(N)
]

# კვანძების ეტიკეტები: v₁, v₂, ..., vₙ₋₁, vθ
subscripts = ["₁", "₂", "₃", "₄", "₅"]
labels = [f"v{subscripts[i]}" for i in range(N - 1)] + ["vθ"]

# ---- ციკლის წიბოები --------------------------------------------------------
# ბოლო წიბო (vθ → v₁) — წყვეტილი, სამი წერტილიანი
DASHED_EDGE_IDX = N - 2   # i=5: v₆(=vθ) → v₁

for i in range(N):
    x0, y0 = cycle_nodes[i]
    x1, y1 = cycle_nodes[(i + 1) % N]

    if i == DASHED_EDGE_IDX:
        # წყვეტილი წიბო — "..." სიმბოლოებით შუაში
        # ვხატავთ ორ მოკლე მყარ სეგმენტს + „..." შუაში
        t = 0.32   # რამდენი ნაწილი მყარია თითო მხრიდან
        mx0 = x0 + t * (x1 - x0)
        my0 = y0 + t * (y1 - y0)
        mx1 = x0 + (1 - t) * (x1 - x0)
        my1 = y0 + (1 - t) * (y1 - y0)

        ax.plot([x0, mx0], [y0, my0],
                color=DASHED_COLOR, lw=1.8, zorder=2, solid_capstyle="round")
        ax.plot([mx1, x1], [my1, y1],
                color=DASHED_COLOR, lw=1.8, zorder=2, solid_capstyle="round")

        # სამი წერტილი შუაში
        mid_x = (x0 + x1) / 2
        mid_y = (y0 + y1) / 2
        # წერტილები წყვეტის მიმართულებით
        dx_u = (x1 - x0) / math.hypot(x1 - x0, y1 - y0)
        dy_u = (y1 - y0) / math.hypot(x1 - x0, y1 - y0)
        for offset in [-0.13, 0.0, 0.13]:
            ax.plot(mid_x + offset * dx_u, mid_y + offset * dy_u,
                    "o", color=DASHED_COLOR, markersize=4, zorder=3)
    else:
        ax.plot([x0, x1], [y0, y1],
                color=EDGE_COLOR, lw=1.6, zorder=1, solid_capstyle="round")

# ---- ხისტი ხის გამოსახვა --------------------------------------------------
def draw_rigid_tree(ax, root_x, root_y, direction_angle_deg, scale=0.38):
    ang = math.radians(direction_angle_deg)

    def pt(r, a):
        return root_x + r * math.cos(a), root_y + r * math.sin(a)

    # პარამეტრი: დაპატარავებული მწვანე წვეროების რადიუსი
    node_r = 0.06

    c1 = pt(scale, ang)
    ax.plot([root_x, c1[0]], [root_y, c1[1]],
            color=TREE_EDGE_COLOR, lw=1.0, zorder=1)

    c1a = (c1[0] + scale * 0.55 * math.cos(ang + 0.55),
           c1[1] + scale * 0.55 * math.sin(ang + 0.55))
    c1b = (c1[0] + scale * 0.55 * math.cos(ang - 0.55),
           c1[1] + scale * 0.55 * math.sin(ang - 0.55))
    ax.plot([c1[0], c1a[0]], [c1[1], c1a[1]],
            color=TREE_EDGE_COLOR, lw=0.7, zorder=1)
    ax.plot([c1[0], c1b[0]], [c1[1], c1b[1]],
            color=TREE_EDGE_COLOR, lw=0.7, zorder=1)

    for delta in [0.55, -0.3]:
        leaf_ang = ang + 0.55 + delta * 0.8
        lx = c1a[0] + scale * 0.40 * math.cos(leaf_ang)
        ly = c1a[1] + scale * 0.40 * math.sin(leaf_ang)
        ax.plot([c1a[0], lx], [c1a[1], ly],
                color=TREE_EDGE_COLOR, lw=0.5, zorder=1)
        ax.add_patch(plt.Circle((lx, ly), node_r * 0.75,
                                color=TREE_NODE_COLOR, zorder=3,
                                linewidth=0.5, ec=TREE_NODE_COLOR))

    leaf_ang2 = ang - 0.55 - 0.5
    lx2 = c1b[0] + scale * 0.40 * math.cos(leaf_ang2)
    ly2 = c1b[1] + scale * 0.40 * math.sin(leaf_ang2)
    ax.plot([c1b[0], lx2], [c1b[1], ly2],
            color=TREE_EDGE_COLOR, lw=0.5, zorder=1)
    ax.add_patch(plt.Circle((lx2, ly2), node_r * 0.75,
                             color=TREE_NODE_COLOR, zorder=3,
                             linewidth=0.5, ec=TREE_NODE_COLOR))

    for c in [c1, c1a, c1b]:
        ax.add_patch(plt.Circle(c, node_r, color=TREE_NODE_COLOR, zorder=3,
                                linewidth=0.7, ec="#085041"))
    return c1

# ---- ხეები ციკლის კვანძებზე ------------------------------------------------
tree_label_offsets = []
for i, (vx, vy) in enumerate(cycle_nodes):
    dx, dy = vx - cx, vy - cy
    out_angle = math.degrees(math.atan2(dy, dx))
    draw_rigid_tree(ax, vx, vy, direction_angle_deg=out_angle, scale=0.38)
    tree_label_offsets.append((vx + 0.78 * dx / R, vy + 0.78 * dy / R))

# ---- ციკლის კვანძები (ზედა ფენა) ------------------------------------------
# პარამეტრი: დაპატარავებული იისფერი წვეროების რადიუსი და ტექსტი
for i, (vx, vy) in enumerate(cycle_nodes):
    ax.add_patch(plt.Circle((vx, vy), 0.11, color=CYCLE_NODE_COLOR,
                             zorder=5, linewidth=1.2, ec="#3C3489"))
    ax.text(vx, vy, labels[i], ha="center", va="center",
            fontsize=6.5, color="white", fontweight="bold", zorder=6,
            fontfamily="DejaVu Sans")

# ---- ხეების ეტიკეტები T_κ --------------------------------------------------
for i, (lx, ly) in enumerate(tree_label_offsets):
    ax.text(lx, ly, r"$T_\kappa$",
            ha="center", va="center", fontsize=9,
            color=SUBTITLE_COLOR, zorder=7,
            bbox=dict(boxstyle="round,pad=0.2", fc=BG_COLOR, ec="none", alpha=0.88))

# ---- შუა წარწერა -----------------------------------------------------------
ax.text(cx, cy + 0.28, r"$\theta$-ციკლი", ha="center", va="center",
        fontsize=11, color=SUBTITLE_COLOR, style="italic")
ax.text(cx, cy - 0.05, r"$|\mathrm{Aut}(G)| = \theta$",
        ha="center", va="center", fontsize=10, color=SUBTITLE_COLOR)
ax.text(cx, cy - 0.35, r"$|G| = \kappa$",
        ha="center", va="center", fontsize=10, color=SUBTITLE_COLOR)

# ---- წყვეტის ანოტაცია წაშლილია თქვენი მოთხოვნით ----

# ---- ლეგენდა ----------------------------------------------------------------
legend_elements = [
    mpatches.Patch(facecolor=CYCLE_NODE_COLOR, edgecolor="#3C3489",
                   label=r"ციკლის წვერო $v_i$"),
    mpatches.Patch(facecolor=TREE_NODE_COLOR, edgecolor="#085041",
                   label=r"$T_\kappa$-ხისტი ხის წვერო ($|T_\kappa|=\kappa$)"),
    mpatches.Patch(facecolor=EDGE_COLOR,
                   label=r"ციკლის წიბო"),
    mpatches.Patch(facecolor=DASHED_COLOR,
                   label=r"გამოტოვებული წიბოები ($\theta$ სასრულია)"),
]
ax.legend(handles=legend_elements, loc="lower center",
          bbox_to_anchor=(0.5, -0.07), ncol=2,
          fontsize=8, frameon=True, framealpha=0.92,
          handlelength=1.4, handleheight=0.9)

# ---- სათაური ----------------------------------------------------------------
ax.set_title(
    r"ფიგურა 1 — გრაფი $G$: სასრული $\theta$-ციკლი, $\kappa$-სიმძლავრის ხისტი ხეებით"
    + "\n"
    + r"$|\mathrm{Aut}(G)| = \theta$,  $|G| = \kappa$   [ყიფიანი, 10]",
    fontsize=11.5, color=TEXT_COLOR, pad=20
)

ax.set_xlim(-2.85, 2.85)
ax.set_ylim(-2.85, 2.85)

plt.tight_layout()

# გზა გასწორებულია ლოკალურ დირექტორიაზე
plt.savefig("rigid_tree_cycle.png", dpi=180, bbox_inches="tight", facecolor=BG_COLOR)
plt.show()

print("შენახულია: rigid_tree_cycle.png")