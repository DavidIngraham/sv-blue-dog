"""Plot native replay outputs; no engineering equations are duplicated here."""
from io import BytesIO
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    from .prepare_design_search import native_value
except ImportError:
    from prepare_design_search import native_value


def search_figure(audit, search):
    report = json.loads(audit)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True, gridspec_kw={"width_ratios":[3,1]})
    contract = search["contract"]
    for ax, check, (name, study) in zip(axes, report["checks"], search["studies"].items(), strict=True):
        values = {v["name"]: v["value"] for v in check["values"]}
        speeds = native_value(values["groundSpeeds"])
        labels = [f'{contract["winds"][i]} m/s\n{"headwind" if contract["windward"][i] else "tailwind"}' + ('\nfouled' if contract['foulingDrag'][i] > 1 else '') for i in study['best']['scenarioIndices']]
        ax.bar(range(len(speeds)), speeds, color="#b75a36", width=.65)
        ax.axhline(contract["min_ground_m_s"], color="#25776d", linestyle="--", label="Required upstream VMG")
        ax.axhline(0, color="#444444", linewidth=.8)
        ax.set_xticks(range(len(speeds)), labels, fontsize=8)
        ax.set_title("Shared design: full scenario set" if name == "full_envelope" else "Nominal study", fontsize=11)
        ax.grid(axis="y", alpha=.2)
        ax.set_axisbelow(True)
    axes[0].set_ylabel("Upstream ground VMG (m/s)")
    axes[0].legend(loc="upper left", fontsize=9)
    fig.suptitle("Coupled design search: balanced sailing does not yet achieve upstream progress", fontsize=12)
    fig.text(.5, .02, "Local optima with illustrative resistance and foil models; negative VMG means downstream drift.", ha="center", fontsize=9)
    fig.tight_layout(rect=(0,.065,1,.94))
    output=BytesIO()
    fig.savefig(output, format="png", dpi=150, metadata={"Software":"SV Blue Dog native SysML analysis"})
    plt.close(fig)
    return output.getvalue()
