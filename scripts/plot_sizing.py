"""Plot native sizing outputs without reimplementing the force model."""
from fractions import Fraction
from io import BytesIO
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def sizing_figure(report):
    cases = json.loads(report)["checks"]
    values = [{v["name"]: v["value"] for v in c["values"]} for c in cases]
    if not values or any(c["status"] != "holds" for c in cases):
        raise ValueError("Sizing study has invalid computations")

    def numbers(name):
        return [float(Fraction(v[name].split()[0])) for v in values]

    labels = [json.loads(v["caseLabel"]).replace(" / ", " /\n") for v in values]
    x = list(range(len(values)))
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
    axes = axes.ravel()
    for key, label, marker, color in [
        ("minimumSailArea", "Drive minimum (fixed foils)", "^", "#176a9b"),
        ("maximumHeelSailArea", "Heel ceiling", "v", "#a45a17"),
        ("candidateSailArea", "Candidate area", "o", "#333333"),
    ]:
        y = numbers(key)
        if key == "minimumSailArea":
            y = [value if v["driveSolutionExists"] == "true" else float("nan") for value, v in zip(y, values)]
        axes[0].scatter(x, y, marker=marker, color=color, label=label, s=45)
    for i, v in enumerate(values):
        if v["driveSolutionExists"] != "true":
            axes[0].annotate("No drive root", (i, 0.02), rotation=90, fontsize=8, ha="center")
    axes[0].set(ylabel="Sail area (m²)", title="Drive demand versus heel capacity")
    for ax, stem, title in [(axes[1], "Keel", "Keel side-force capacity"), (axes[2], "Rudder", "Rudder trim + yaw reserve")]:
        ax.scatter(x, numbers("minimum" + stem + "Area"), marker="^", color="#176a9b", label="Demand area", s=45)
        ax.scatter(x, numbers("candidate" + stem + "Area"), color="#333333", label="Candidate area", s=40)
        ax.set(ylabel="Planform area (m², log scale)", title=title, yscale="log")
    axes[3].scatter(x, numbers("minimumBallastMass"), marker="^", color="#176a9b", label="Heel demand", s=45)
    axes[3].scatter(x, numbers("candidateBallastMass"), color="#333333", label="Candidate ballast", s=40)
    axes[3].set(ylabel="Ballast mass (kg)", title="Ballast demand at declared heel")
    for ax in axes:
        ax.set_xticks(x, labels, rotation=25, ha="right", fontsize=8)
        ax.grid(alpha=0.2)
        ax.legend(fontsize=8, frameon=False)
    fig.suptitle("Coupled sail, keel and rudder sizing — synthetic scenarios", fontsize=15)
    fig.text(0.5, 0.015, "Native SysML results. Fixed coefficients and geometry; no measured resistance, foil performance or stability evidence.\n"
             "The low-speed point is a steering stress probe, not a predicted sailing equilibrium.", ha="center", fontsize=9)
    fig.tight_layout(rect=(0, 0.07, 1, 0.96))
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=170, metadata={"Software": "SV Blue Dog — native SysML results"})
    plt.close(fig)
    return buffer.getvalue()
