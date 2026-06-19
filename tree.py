"""
ფიგურა 3 — გრაფი G: ცენტრალური წვერო μ-რაოდენობის ხისტი ხეებით
ყიფიანის თეორემის საილუსტრაციო ნახაზი (θ = 2^μ შემთხვევა)

ცენტრალური სტრუქტურა: ვარსკვლავისებრი (Star-like Hub)
ხეების რაოდენობა: μ
ავტომორფიზმთა ჯგუფის სიმძლავრე: |Aut(G)| = 2^μ
გრაფის სიმძლავრე: |G| = κ
"""

import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ფერები (წინა ფიგურების იდენტური სტილი ვიზუალური ერთიანობისთვის)
HUB_NODE_COLOR   = "#E74C3C"   # ცენტრალური წვეროს გამორჩეული ფერი (წითელი)
TREE_NODE_COLOR  = "#1D9E75"
EDGE_COLOR       = "#888780"
TREE_EDGE_COLOR  = "#B4B2A9"
DASHED_COLOR     = "#534AB7"
BG_COLOR         = "#FFFFFF"
TEXT_COLOR       = "#2C2C2A"
SUBTITLE_COLOR   = "#5F5E5A"

fig, ax = plt.subplots(figsize=(10, 9))
ax.set_aspect("equal")
ax.axis("off")
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

# ---- ცენტრის პარამეტრები --------------------------------------------------
cx, cy = 0.0, 0.0  # ცენტრალური წვეროს კოორდინატები
R_start = 0.8      # მანძილი ცენტრიდან ხეების დასაწყისამდე (სხივების სიგრძე)

# გამოვიყენოთ 5 სხივი საილუსტრაციოდ, სადაც ბოლო სეგმენტში იქნება წყვეტა
M = 6  
# განვათავსოთ სხივები წრეზე, მაგრამ დავტოვოთ ადგილი წყვეტისთვის (...)
angles = [2 * np.pi * i / (M - 0.4) for i in range(M - 1)]

# ---- ხისტი ხის გამოსახვის ფუნქცია (მიმართულების კუთხის გათვალისწინებით) ---
def draw_rigid_tree_radial(ax, root_x, root_y, angle_rad, scale=0.38):
    node_r = 0.06  # დაპატარავებული ნაზი წვეროები

    def pt(r, a):
        return root_x + r * math.cos(a), root_y + r * math.sin(a)

    c1 = pt(scale, angle_rad)
    ax.plot([root_x, c1[0]], [root_y, c1[1]], color=TREE_EDGE_COLOR, lw=1.0, zorder=1)

    c1a = (c1[0] + scale * 0.55 * math.cos(angle_rad + 0.55), c1[1] + scale * 0.55 * math.sin(angle_rad + 0.55))
    c1b = (c1[0] + scale * 0.55 * math.cos(angle_rad - 0.55), c1[1] + scale * 0.55 * math.sin(angle_rad - 0.55))
    ax.plot([c1[0], c1a[0]], [c1[1], c1a[1]], color=TREE_EDGE_COLOR, lw=0.7, zorder=1)
    ax.plot([c1[0], c1b[0]], [c1[1], c1b[1]], color=TREE_EDGE_COLOR, lw=0.7, zorder=1)

    for delta in [0.55, -0.3]:
        leaf_ang = angle_rad + 0.55 + delta * 0.8
        lx = c1a[0] + scale * 0.40 * math.cos(leaf_ang)
        ly = c1a[1] + scale * 0.40 * math.sin(leaf_ang)
        ax.plot([c1a[0], lx], [c1a[1], ly], color=TREE_EDGE_COLOR, lw=0.5, zorder=1)
        ax.add_patch(plt.Circle((lx, ly), node_r * 0.75, color=TREE_NODE_COLOR, zorder=3, linewidth=0.5))

    leaf_ang2 = angle_rad - 0.55 - 0.5
    lx2 = c1b[0] + scale * 0.40 * math.cos(leaf_ang2)
    ly2 = c1b[1] + scale * 0.40 * math.sin(leaf_ang2)
    ax.plot([c1b[0], lx2], [c1b[1], ly2], color=TREE_EDGE_COLOR, lw=0.5, zorder=1)
    ax.add_patch(plt.Circle((lx2, ly2), node_r * 0.75, color=TREE_NODE_COLOR, zorder=3, linewidth=0.5))

    for c in [c1, c1a, c1b]:
        ax.add_patch(plt.Circle(c, node_r, color=TREE_NODE_COLOR, zorder=3, linewidth=0.7, ec="#085041"))

# ---- სხივების და ხეების აგება -----------------------------------------------
for ang in angles:
    # ხის ძირის (დაწყების) წერტილი
    rx = cx + R_start * math.cos(ang)
    ry = cy + R_start * math.sin(ang)
    
    # ვავლებთ ძირითად დამაკავშირებელ წიბოს ცენტრიდან ხემდე
    ax.plot([cx, rx], [cy, ry], color=EDGE_COLOR, lw=1.6, zorder=1, solid_capstyle="round")
    
    # ვხატავთ რადიალურად მიმართულ ხეს ამ წერტილზე
    draw_rigid_tree_radial(ax, rx, ry, angle_rad=ang, scale=0.38)
    
    # T_κ ლეიბლი თითოეული ხის თავზე
    lbl_dist = R_start + 1.2
    ax.text(cx + lbl_dist * math.cos(ang), cy + lbl_dist * math.sin(ang), r"$T_\kappa$", 
            ha="center", va="center", fontsize=9, color=SUBTITLE_COLOR, zorder=7,
            bbox=dict(boxstyle="round,pad=0.2", fc=BG_COLOR, ec="none", alpha=0.88))

# ---- უსასრულობის / ნებისმიერი რაოდენობის გამოხატვა (წყვეტა) ------------------
# წყვეტას ვაკეთებთ ბოლო და პირველ ხეს შორის დარჩენილ თავისუფალ სივრცეში
mid_dashed_angle = (angles[0] + angles[-1]) / 2 + math.pi  # ოპოზიტური კუთხე
dash_x = cx + (R_start + 0.4) * math.cos(mid_dashed_angle)
dash_y = cy + (R_start + 0.4) * math.sin(mid_dashed_angle)

# ვსვამთ სამწერტილს, რომელიც გამოხატავს, რომ სულ μ ცალი ასეთი სხივია
ax.text(dash_x, dash_y, r"$\dots$", fontsize=24, rotation=math.degrees(mid_dashed_angle)-90,
        ha="center", va="center", color=DASHED_COLOR, fontweight="bold")

# ---- ცენტრალური წვეროს დასმა (ზედა ფენა) -------------------------------------
# ეს არის წვერო, რომელიც არ ეკუთვნის არცერთ ხეს
ax.add_patch(plt.Circle((cx, cy), 0.12, color=HUB_NODE_COLOR, zorder=5, linewidth=1.5, ec="#962D22"))
ax.text(cx, cy, r"$c_0$", ha="center", va="center", fontsize=7.5,
        color="white", fontweight="bold", zorder=6, fontfamily="DejaVu Sans")

# ---- საინფორმაციო ტექსტები ცენტრის ქვემოთ ------------------------------------
ax.text(cx, cy - 1.8, r"$\mu$ ცალი იზომორფული ხისტი ხე", ha="center", va="center", 
        fontsize=11, color=SUBTITLE_COLOR, style="italic")
ax.text(cx, cy - 2.1, r"$|\mathrm{Aut}(G)| = 2^\mu$", ha="center", va="center", 
        fontsize=10, color=SUBTITLE_COLOR, fontweight="bold")
ax.text(cx, cy - 2.35, r"$|G| = \kappa$", ha="center", va="center", 
        fontsize=10, color=SUBTITLE_COLOR)

# ---- ლეგენდა ----------------------------------------------------------------
legend_elements = [
    mpatches.Patch(facecolor=HUB_NODE_COLOR, edgecolor="#962D22", label=r"ცენტრალური წვერო $c_0$"),
    mpatches.Patch(facecolor=TREE_NODE_COLOR, edgecolor="#085041", label=r"$T_\kappa$-ხისტი ხის წვერო"),
    mpatches.Patch(facecolor=EDGE_COLOR, label=r"დამაკავშირებელი წიბო ცენტრთან"),
    mpatches.Patch(facecolor=DASHED_COLOR, label=r"სხივების ჯამური რაოდენობაა $\mu$"),
]
ax.legend(handles=legend_elements, loc="lower center", bbox_to_anchor=(0.5, -0.06), 
          ncol=2, fontsize=8, frameon=True, framealpha=0.92, handlelength=1.4)

# ---- სათაური ----------------------------------------------------------------
ax.set_title(
    r"ფიგურა 3 — გრაფი $G$: ცენტრალური წვერო $\mu$ რაოდენობის ხისტი ხეებით"
    + "\n"
    + r"$|\mathrm{Aut}(G)| = 2^\mu$,  $|G| = \kappa$   [ყიფიანი, 10]",
    fontsize=11.5, color=TEXT_COLOR, pad=20
)

# საზღვრების ოპტიმიზაცია რადიალური სტრუქტურისთვის
ax.set_xlim(-2.6, 2.6)
ax.set_ylim(-2.7, 2.6)

plt.tight_layout()

# შენახვა ლოკალურად
plt.savefig("rigid_tree_star.png", dpi=180, bbox_inches="tight", facecolor=BG_COLOR)
plt.show()

print("შენახულია: rigid_tree_star.png")