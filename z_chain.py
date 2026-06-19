"""
ფიგურა 2 — გრაფი G: ორმხრივ უსასრულო ჯაჭვი κ-სიმძლავრის ხისტი ხეებით
ყიფიანის თეორემის საილუსტრაციო ნახაზი (θ = ℵ₀ შემთხვევა)

ჯაჭვის სიგრძე: θ = ℵ₀ (უსასრულო ჯაჭვი)
ხეების სიმძლავრე: κ
ავტომორფიზმთა ჯგუფი: |Aut(G)| = ℵ₀
გრაფის სიმძლავრე: |G| = κ
"""

import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ფერები (შენარჩუნებულია წინა ფიგურის სტილი)
PATH_NODE_COLOR  = "#7F77DD"
TREE_NODE_COLOR  = "#1D9E75"
EDGE_COLOR       = "#888780"
TREE_EDGE_COLOR  = "#B4B2A9"
DASHED_COLOR     = "#534AB7"
BG_COLOR         = "#FFFFFF"
TEXT_COLOR       = "#2C2C2A"
SUBTITLE_COLOR   = "#5F5E5A"

fig, ax = plt.subplots(figsize=(11, 7))
ax.set_aspect("equal")
ax.axis("off")
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

# ---- ჯაჭვის კვანძების პარამეტრები -----------------------------------------
# გამოვიყენოთ 5 ძირითადი წვერო საილუსტრაციოდ, განლაგებული ჰორიზონტალურად
num_nodes = 5
spacing = 1.6
start_x = - (num_nodes - 1) * spacing / 2
y_path = -1.0  # ჯაჭვის სიმაღლე

path_nodes = []
for i in range(num_nodes):
    path_nodes.append((start_x + i * spacing, y_path))

# კვანძების ეტიკეტები: ..., v_-2, v_-1, v_0, v_1, v_2, ...
labels = ["v₋₂", "v₋₁", "v₀", "v₁", "v₂"]

# ---- ჯაჭვის წიბოების დახატვა ----------------------------------------------
# ჩვეულებრივი შიდა წიბოები
for i in range(num_nodes - 1):
    ax.plot([path_nodes[i][0], path_nodes[i+1][0]], [y_path, y_path],
            color=EDGE_COLOR, lw=1.6, zorder=1, solid_capstyle="round")

# მარცხენა უსასრულო წყვეტა (...)
x_left_end = path_nodes[0][0]
ax.plot([x_left_end, x_left_end - spacing*0.5], [y_path, y_path],
        color=DASHED_COLOR, lw=1.8, linestyle="--", zorder=2)
ax.text(x_left_end - spacing*0.7, y_path, r"$\dots$", fontsize=24,
        ha="center", va="center", color=DASHED_COLOR, fontweight="bold")

# მარჯვენა უსასრულო წყვეტა (...)
x_right_end = path_nodes[-1][0]
ax.plot([x_right_end, x_right_end + spacing*0.5], [y_path, y_path],
        color=DASHED_COLOR, lw=1.8, linestyle="--", zorder=2)
ax.text(x_right_end + spacing*0.7, y_path, r"$\dots$", fontsize=24,
        ha="center", va="center", color=DASHED_COLOR, fontweight="bold")

# ---- ხისტი ხის გამოსახვის ფუნქცია (ვერტიკალურად ზემოთ) ---------------------
def draw_rigid_tree_up(ax, root_x, root_y, scale=0.45):
    # მიმართულება პირდაპირ ზემოთ (90 გრადუსი)
    ang = math.radians(90)
    node_r = 0.06  # დაპატარავებული წვეროები თქვენი თხოვნით

    def pt(r, a):
        return root_x + r * math.cos(a), root_y + r * math.sin(a)

    c1 = pt(scale, ang)
    ax.plot([root_x, c1[0]], [root_y, c1[1]], color=TREE_EDGE_COLOR, lw=1.0, zorder=1)

    c1a = (c1[0] + scale * 0.55 * math.cos(ang + 0.55), c1[1] + scale * 0.55 * math.sin(ang + 0.55))
    c1b = (c1[0] + scale * 0.55 * math.cos(ang - 0.55), c1[1] + scale * 0.55 * math.sin(ang - 0.55))
    ax.plot([c1[0], c1a[0]], [c1[1], c1a[1]], color=TREE_EDGE_COLOR, lw=0.7, zorder=1)
    ax.plot([c1[0], c1b[0]], [c1[1], c1b[1]], color=TREE_EDGE_COLOR, lw=0.7, zorder=1)

    for delta in [0.55, -0.3]:
        leaf_ang = ang + 0.55 + delta * 0.8
        lx = c1a[0] + scale * 0.40 * math.cos(leaf_ang)
        ly = c1a[1] + scale * 0.40 * math.sin(leaf_ang)
        ax.plot([c1a[0], lx], [c1a[1], ly], color=TREE_EDGE_COLOR, lw=0.5, zorder=1)
        ax.add_patch(plt.Circle((lx, ly), node_r * 0.75, color=TREE_NODE_COLOR, zorder=3, linewidth=0.5))

    leaf_ang2 = ang - 0.55 - 0.5
    lx2 = c1b[0] + scale * 0.40 * math.cos(leaf_ang2)
    ly2 = c1b[1] + scale * 0.40 * math.sin(leaf_ang2)
    ax.plot([c1b[0], lx2], [c1b[1], ly2], color=TREE_EDGE_COLOR, lw=0.5, zorder=1)
    ax.add_patch(plt.Circle((lx2, ly2), node_r * 0.75, color=TREE_NODE_COLOR, zorder=3, linewidth=0.5))

    for c in [c1, c1a, c1b]:
        ax.add_patch(plt.Circle(c, node_r, color=TREE_NODE_COLOR, zorder=3, linewidth=0.7, ec="#085041"))
    return c1

# ---- ხეების და ლეიბლების დასმა თითოეულ წვეროზე ------------------------------
for i, (vx, vy) in enumerate(path_nodes):
    # ვხატავთ ხეს
    draw_rigid_tree_up(ax, vx, vy, scale=0.45)
    
    # T_κ ეტიკეტი ხის თავზე
    ax.text(vx, vy + 1.2, r"$T_\kappa$", ha="center", va="center", fontsize=9,
            color=SUBTITLE_COLOR, zorder=7,
            bbox=dict(boxstyle="round,pad=0.2", fc=BG_COLOR, ec="none", alpha=0.88))

# ---- ჯაჭვის წვეროები (ზედა ფენა) -------------------------------------------
for i, (vx, vy) in enumerate(path_nodes):
    ax.add_patch(plt.Circle((vx, vy), 0.11, color=PATH_NODE_COLOR, zorder=5, linewidth=1.2, ec="#3C3489"))
    ax.text(vx, vy, labels[i], ha="center", va="center", fontsize=6.5,
            color="white", fontweight="bold", zorder=6, fontfamily="DejaVu Sans")

# ---- ქვედა საინფორმაციო ტექსტები --------------------------------------------
ax.text(0.0, y_path - 0.6, r"ორმხრივ უსასრულო ჯაჭვი ($\theta = \aleph_0$)", 
        ha="center", va="center", fontsize=11, color=SUBTITLE_COLOR, style="italic")
ax.text(0.0, y_path - 1.0, r"$|\mathrm{Aut}(G)| = \aleph_0$", 
        ha="center", va="center", fontsize=10, color=SUBTITLE_COLOR)
ax.text(0.0, y_path - 1.3, r"$|G| = \kappa$", 
        ha="center", va="center", fontsize=10, color=SUBTITLE_COLOR)

# ---- ლეგენდა ----------------------------------------------------------------
legend_elements = [
    mpatches.Patch(facecolor=PATH_NODE_COLOR, edgecolor="#3C3489", label=r"ჯაჭვის წვერო $v_i$"),
    mpatches.Patch(facecolor=TREE_NODE_COLOR, edgecolor="#085041", label=r"$T_\kappa$-ხისტი ხის წვერო ($|T_\kappa|=\kappa$)"),
    mpatches.Patch(facecolor=EDGE_COLOR, label=r"ჯაჭვის მყარი წიბო"),
    mpatches.Patch(facecolor=DASHED_COLOR, label=r"უსასრულო გაგრძელება ($\theta = \aleph_0$)"),
]
ax.legend(handles=legend_elements, loc="lower center", bbox_to_anchor=(0.5, -0.05), 
          ncol=2, fontsize=8, frameon=True, framealpha=0.92, handlelength=1.4)

# ---- სათაური ----------------------------------------------------------------
ax.set_title(
    r"ფიგურა 2 — გრაფი $G$: ორმხრივ უსასრულო ჯაჭვი, $\kappa$-სიმძლავრის ხისტი ხეებით"
    + "\n"
    + r"$|\mathrm{Aut}(G)| = \aleph_0$,  $|G| = \kappa$   [ყიფიანი, 10]",
    fontsize=11.5, color=TEXT_COLOR, pad=20
)

# ეკრანის ოპტიმალური საზღვრები ჰორიზონტალური სტრუქტურისთვის
ax.set_xlim(start_x - 1.5, abs(start_x) + 1.5)
ax.set_ylim(y_path - 1.8, y_path + 1.8)

plt.tight_layout()

# შენახვა ლოკალურად
plt.savefig("rigid_tree_path.png", dpi=180, bbox_inches="tight", facecolor=BG_COLOR)
plt.show()

print("შენახულია: rigid_tree_path.png")