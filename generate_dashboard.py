#!/usr/bin/env python3
"""
ZYTO Wellness Dashboard Generator
Transforms cryptic ZYTO PDF data into a beautiful spa-like experience.
"""

import argparse
import json
import math

# ─── Sample data for demonstration (synthetic — no real scan) ───
# All biomarker values below are round synthetic numbers (multiples of 10)
# chosen so the computed demo balance score lands at 72.

BIOMARKERS = {
    # Organs
    "organs": {
        "Adrenal Glands": 30.00,
        "Spleen": -30.00,
        "Stomach": 30.00,
        "Uterus": -20.00,
        "Small Intestine": -30.00,
        "Kidneys": -30.00,
        "Pancreas": 20.00,
        "Parathyroid Gland": 10.00,
        "Thymus": 0.00,
        "Pineal Gland": -10.00,
        "Pituitary Gland": 10.00,
        "Arteries/Veins": 10.00,
        "Skin": -10.00,
        "Gallbladder": 20.00,
        "Hypothalamus": -10.00,
        "Mammary Glands": 30.00,
        "Urinary Bladder": 10.00,
        "Central Nervous System": -10.00,
        "Joints/Connective Tissue": -20.00,
        "Liver": -20.00,
        "Ovary": -20.00,
        "Thyroid": 20.00,
        "Peripheral Nervous System": 0.00,
        "Lung": -10.00,
        "Large Intestine": 0.00,
        "Heart": -20.00,
        "Eyes": 0.00,
        "Lymphatic System": 0.00,
    },
    # Emotions
    "emotions": {
        "Jealous": 30.00,
        "Complacency": -20.00,
        "Tense": -30.00,
        "Envy": 30.00,
        "Fear": 20.00,
        "Grief": -10.00,
        "Exhausted": 20.00,
        "Hate": -30.00,
        "Greed": -20.00,
        "Resentful": 20.00,
        "Lonely": -20.00,
        "Mistrustful": 0.00,
        "Worry": 10.00,
        "Hopeless": -10.00,
        "Guilty": 10.00,
        "Helpless": 30.00,
    },
    # Neurotransmitters
    "neurotransmitters": {
        "L-Dopa": -30.00,
        "Phenylethylamine": 30.00,
        "Orthomethyl Serotonin": -20.00,
        "L-Glutamine": 10.00,
        "Taurine": 20.00,
        "Acetylcholine Chloride": -10.00,
        "Vit B-6 (Pyridoxine)": 20.00,
        "Dopamine": -20.00,
        "Serotonin": -30.00,
        "GABA": 30.00,
        "Norepinephrine": -20.00,
        "Malvin": 10.00,
        "L-Glutamic Acid": -10.00,
        "Nitric Oxide": -30.00,
        "Tryptophan": 10.00,
        "A-Endorphin": 20.00,
        "Kryptopyrrole": 0.00,
    },
    # TCM Meridians
    "tcm_meridians": {
        "Governing Meridian": 30.00,
        "Gall Bladder Meridian": 20.00,
        "Urinary Bladder Meridian": 10.00,
        "Triple Warmer Meridian": -30.00,
        "Small Intestine Meridian": -10.00,
        "Stomach Meridian": 30.00,
        "Heart Meridian": -20.00,
        "Pericardium Meridian": 30.00,
        "Kidney Meridian": 10.00,
        "Conception Meridian": -30.00,
        "Spleen Meridian": 20.00,
        "Liver Meridian": -20.00,
        "Lung Meridian": -20.00,
        "Large Intestine Meridian": 0.00,
    },
    # Vertebrae
    "vertebrae": {
        "C1": 30.00, "C2": 20.00, "C3": 10.00, "C4": -20.00, "C5": -10.00,
        "C6": 10.00, "C7": -10.00, "TH 1": -30.00, "TH 2": -20.00, "TH 3": -10.00,
        "TH 4": -30.00, "TH 5": 20.00, "TH 6": 10.00, "TH 7": 30.00, "TH 8": -20.00,
        "TH 9": -10.00, "TH 10": -30.00, "TH 11": 10.00, "TH 12": 20.00,
        "L1": 20.00, "L2": 30.00, "L3": 0.00, "L4": -30.00, "L5": -30.00,
        "S1": -20.00, "S2": 10.00, "S3": 0.00, "S4": -10.00, "S5": 0.00,
        "Coccyx": 20.00,
    },
    # Teeth
    "teeth": {
        "T 01 / 8+": 30.00, "T 02 / 7+": -20.00, "T 03 / 6+": 10.00, "T 04 / 5+": -30.00,
        "T 05 / 4+": 30.00, "T 06 / 3+": -10.00, "T 07 / 2+": 20.00, "T 08 / 1+": 30.00,
        "T 09 / +1": -20.00, "T 10 / +2": -20.00, "T 11 / +3": 10.00, "T 12 / +4": -30.00,
        "T 13 / +5": -30.00, "T 14 / +6": -10.00, "T 15 / +7": 20.00, "T 16 / +8": 30.00,
        "T 17 / -8": -20.00, "T 18 / -7": 10.00, "T 19 / -6": 0.00, "T 20 / -5": -30.00,
        "T 21 / -4": 30.00, "T 22 / -3": 20.00, "T 23 / -2": -10.00, "T 24 / -1": 30.00,
        "T 25 / 1-": -20.00, "T 26 / 2-": 20.00, "T 27 / 3-": 10.00, "T 28 / 4-": -30.00,
        "T 29 / 5-": -30.00, "T 30 / 6-": 20.00, "T 31 / 7-": -10.00, "T 32 / 8-": 0.00,
    },
    # EAV Points (top ones)
    "eav_points": {
        "GV-23-1a*": 30.00, "LV-1a*": 30.00, "CI-8d*": -30.00, "ST-9": -30.00,
        "ST-44b*": 20.00, "GB-43b*": -20.00, "UB-66b*": 30.00, "TW-20": -30.00,
        "SP-1aL*": 20.00, "LU-10c*": 10.00, "SM-1bL*": -20.00, "UB-65": -10.00,
        "SM-1bR*": 0.00,
    },
}

BALANCERS = [
    {"name": "Omega-3 Fish Oil", "category": "Nutrition", "impact": 30, "dose": "1 capsule 2x/day"},
    {"name": "Magnesium Glycinate", "category": "Minerals", "impact": 20, "dose": "1 capsule 1x/day"},
    {"name": "Vitamin D3 + K2", "category": "Vitamins", "impact": 15, "dose": "1 capsule 1x/day"},
    {"name": "Probiotic Blend", "category": "Digestion", "impact": 10, "dose": "1 capsule 1x/day"},
    {"name": "B-Complex", "category": "Vitamins", "impact": 8, "dose": "1 capsule 1x/day"},
    {"name": "Ashwagandha", "category": "Stress Support", "impact": 5, "dose": "1 capsule 1x/day"},
    {"name": "Turmeric (Curcumin)", "category": "Antioxidants", "impact": 3, "dose": "1 capsule 1x/day"},
    {"name": "Daily Affirmation Practice", "category": "Mental Wellness", "impact": 2, "dose": "Daily practice"},
]

SERVICES = [
    {"name": "Flotation Therapy", "score": 30.00},
    {"name": "Reiki", "score": 25.00},
    {"name": "EVOX Sessions", "score": 20.00},
    {"name": "Aura Healing", "score": 18.00},
    {"name": "Rife Machine", "score": 15.00},
]

RANGE = 8.20

parser = argparse.ArgumentParser(description="Generate the ZYTO demo dashboard HTML from the synthetic sample dataset.")
parser.add_argument("--output", default="dashboard.html",
                    help="Output HTML path (default: dashboard.html in the current directory).")
args = parser.parse_args()


def normalize_score(value, range_val=RANGE):
    """Convert a ZYTO biomarker value to a 0-100 wellness score.
    In-range = 100. Further from range = lower score.
    """
    deviation = abs(value) - range_val
    if deviation <= 0:
        return 100.0
    # Each unit beyond range costs ~2.5 points, capped at 0
    score = 100 - (deviation * 2.5)
    return max(0, min(100, score))


def compute_category_score(biomarkers_dict):
    """Average normalized score across a category."""
    if not biomarkers_dict:
        return 50
    scores = [normalize_score(v) for v in biomarkers_dict.values()]
    return round(sum(scores) / len(scores))


def compute_balance_score():
    """Overall balance across all biomarkers."""
    all_values = []
    for category in BIOMARKERS.values():
        all_values.extend(category.values())
    scores = [normalize_score(v) for v in all_values]
    return round(sum(scores) / len(scores))


# ─── Dashboard Category Mapping ───

categories = {
    "Energy": {
        "biomarkers": {
            **{k: v for k, v in BIOMARKERS["organs"].items() if k in ["Adrenal Glands", "Thyroid", "Heart", "Lungs"]},
            **{k: v for k, v in BIOMARKERS["neurotransmitters"].items() if k in ["Dopamine", "Serotonin", "Norepinephrine", "L-Dopa", "Phenylethylamine"]},
            **{k: v for k, v in BIOMARKERS["emotions"].items() if k in ["Exhausted", "Fear", "Grief"]},
        },
        "description": "Demonstration category computed from synthetic sample biomarkers. This text exists to exercise the dashboard layout."
    },
    "Heavy Metals": {
        "biomarkers": {
            **{k: v for k, v in BIOMARKERS["organs"].items() if k in ["Liver", "Kidneys", "Lymphatic System", "Skin"]},
            **{k: v for k, v in BIOMARKERS["neurotransmitters"].items() if k in ["Taurine", "L-Glutamine"]},
        },
        "description": "Demonstration category computed from synthetic sample biomarkers. This text exists to exercise the dashboard layout."
    },
    "Inflammation": {
        "biomarkers": {
            **{k: v for k, v in BIOMARKERS["organs"].items() if k in ["Stomach", "Spleen", "Small Intestine", "Joints/Connective Tissue", "Gallbladder"]},
            **{k: v for k, v in BIOMARKERS["tcm_meridians"].items() if k in ["Liver Meridian", "Spleen Meridian", "Triple Warmer Meridian"]},
        },
        "description": "Demonstration category computed from synthetic sample biomarkers. This text exists to exercise the dashboard layout."
    },
    "Nutrition": {
        "biomarkers": {
            **{k: v for k, v in BIOMARKERS["organs"].items() if k in ["Pancreas", "Stomach", "Small Intestine", "Liver", "Gallbladder"]},
            **{k: v for k, v in BIOMARKERS["neurotransmitters"].items() if k in ["Vit B-6 (Pyridoxine)", "L-Glutamine", "Tryptophan"]},
        },
        "description": "Demonstration category computed from synthetic sample biomarkers. This text exists to exercise the dashboard layout."
    },
    "Mental Wellness": {
        "biomarkers": {
            **{k: v for k, v in BIOMARKERS["emotions"].items()},  # all emotions
            **{k: v for k, v in BIOMARKERS["neurotransmitters"].items() if k in ["Serotonin", "Dopamine", "GABA", "Acetylcholine Chloride", "A-Endorphin"]},
            **{k: v for k, v in BIOMARKERS["organs"].items() if k in ["Pineal Gland", "Pituitary Gland", "Central Nervous System", "Hypothalamus"]},
        },
        "description": "Demonstration category computed from synthetic sample biomarkers. This text exists to exercise the dashboard layout."
    },
    "Detoxification": {
        "biomarkers": {
            **{k: v for k, v in BIOMARKERS["organs"].items() if k in ["Liver", "Kidneys", "Lymphatic System", "Large Intestine", "Skin", "Lungs"]},
            **{k: v for k, v in BIOMARKERS["tcm_meridians"].items() if k in ["Liver Meridian", "Kidney Meridian", "Large Intestine Meridian"]},
        },
        "description": "Demonstration category computed from synthetic sample biomarkers. This text exists to exercise the dashboard layout."
    },
}

# Compute all scores
dashboard_data = {}
for cat_name, cat_info in categories.items():
    score = compute_category_score(cat_info["biomarkers"])
    dashboard_data[cat_name] = {
        "score": score,
        "description": cat_info["description"],
        "biomarkers": cat_info["biomarkers"]
    }

balance_score = compute_balance_score()

# ─── Top stressors (out-of-range biomarkers with highest deviation) ───
all_biomarkers_flat = {}
for cat_name, cat_dict in BIOMARKERS.items():
    for k, v in cat_dict.items():
        all_biomarkers_flat[f"{cat_name}: {k}"] = v

top_stressors = sorted(
    [(k, v) for k, v in all_biomarkers_flat.items() if abs(v) > RANGE],
    key=lambda x: abs(x[1]),
    reverse=True
)[:8]

# ─── Generate HTML ───

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ZYTO Wellness Assessment — Sample Client</title>
<style>
  :root {
    --bg: #0b0c10;
    --bg-card: #111318;
    --text: #e0e6ed;
    --text-dim: #7a8599;
    --accent: #00d4ff;
    --accent-glow: rgba(0, 212, 255, 0.15);
    --positive: #00d4ff;
    --negative: #ff6b6b;
    --neutral: #feca57;
    --bar-bg: #1a1d24;
    --border: #1f232c;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    min-height: 100vh;
    overflow-x: hidden;
  }
  .container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 40px 30px;
  }
  header {
    text-align: center;
    margin-bottom: 50px;
    animation: fadeInDown 1s ease;
  }
  header h1 {
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 8px;
  }
  header h2 {
    font-size: 28px;
    font-weight: 300;
    color: var(--text);
    letter-spacing: 1px;
  }
  header .date {
    font-size: 13px;
    color: var(--text-dim);
    margin-top: 10px;
  }
  .dashboard {
    display: grid;
    grid-template-columns: 320px 1fr 380px;
    gap: 30px;
    align-items: start;
  }
  @media (max-width: 1200px) {
    .dashboard { grid-template-columns: 1fr; }
  }
  .card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px;
    animation: fadeInUp 0.8s ease both;
  }
  .card h3 {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 20px;
  }
  /* Body Visualization */
  .body-viz {
    position: relative;
    height: 480px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .body-svg {
    height: 100%;
    filter: drop-shadow(0 0 20px var(--accent-glow));
  }
  .body-svg path {
    fill: none;
    stroke: var(--accent);
    stroke-width: 1.5;
    opacity: 0.6;
  }
  .hotspot {
    position: absolute;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--negative);
    box-shadow: 0 0 12px var(--negative);
    animation: pulse 2s infinite;
    cursor: pointer;
  }
  .hotspot::after {
    content: attr(data-label);
    position: absolute;
    left: 18px;
    top: -6px;
    font-size: 11px;
    color: var(--text-dim);
    white-space: nowrap;
    opacity: 0;
    transition: opacity 0.3s;
  }
  .hotspot:hover::after { opacity: 1; }
  @keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 0.8; }
    50% { transform: scale(1.4); opacity: 0.4; }
  }
  /* Balance Score */
  .score-circle {
    width: 160px;
    height: 160px;
    margin: 0 auto 20px;
    position: relative;
  }
  .score-circle svg {
    transform: rotate(-90deg);
  }
  .score-circle .track {
    fill: none;
    stroke: var(--bar-bg);
    stroke-width: 8;
  }
  .score-circle .progress {
    fill: none;
    stroke: var(--accent);
    stroke-width: 8;
    stroke-linecap: round;
    transition: stroke-dashoffset 2s ease;
  }
  .score-value {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
  }
  .score-value .number {
    font-size: 48px;
    font-weight: 200;
    color: var(--accent);
    line-height: 1;
  }
  .score-value .label {
    font-size: 12px;
    color: var(--text-dim);
    margin-top: 4px;
    letter-spacing: 1px;
  }
  .balance-status {
    text-align: center;
    font-size: 16px;
    color: var(--text);
    margin-bottom: 12px;
  }
  .balance-desc {
    text-align: center;
    font-size: 13px;
    color: var(--text-dim);
    line-height: 1.7;
    max-width: 280px;
    margin: 0 auto;
  }
  /* Category Bars */
  .category {
    margin-bottom: 22px;
  }
  .category:last-child { margin-bottom: 0; }
  .cat-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 8px;
  }
  .cat-name {
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }
  .cat-score {
    font-size: 14px;
    font-weight: 600;
    color: var(--accent);
  }
  .cat-bar {
    height: 6px;
    background: var(--bar-bg);
    border-radius: 3px;
    overflow: hidden;
    position: relative;
  }
  .cat-fill {
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, var(--accent) 0%, #00a8cc 100%);
    transition: width 1.5s ease;
    position: relative;
  }
  .cat-fill::after {
    content: '';
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    width: 20px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15));
  }
  .cat-fill.low {
    background: linear-gradient(90deg, var(--negative) 0%, #ff8e8e 100%);
  }
  .cat-fill.medium {
    background: linear-gradient(90deg, var(--neutral) 0%, #ffd93d 100%);
  }
  /* Stressors */
  .stressor-list {
    list-style: none;
  }
  .stressor-list li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid var(--border);
    font-size: 13px;
  }
  .stressor-list li:last-child { border-bottom: none; }
  .stressor-name { color: var(--text); }
  .stressor-val {
    font-family: 'SF Mono', Monaco, monospace;
    font-size: 12px;
    padding: 2px 8px;
    border-radius: 4px;
    background: rgba(255, 107, 107, 0.1);
    color: var(--negative);
  }
  /* Recommendations */
  .rec-list {
    list-style: none;
  }
  .rec-list li {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid var(--border);
  }
  .rec-list li:last-child { border-bottom: none; }
  .rec-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: var(--accent-glow);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
  }
  .rec-content {
    flex: 1;
  }
  .rec-title {
    font-size: 13px;
    font-weight: 500;
    color: var(--text);
    margin-bottom: 2px;
  }
  .rec-meta {
    font-size: 11px;
    color: var(--text-dim);
  }
  .rec-impact {
    font-size: 11px;
    color: var(--accent);
    font-weight: 500;
    margin-top: 2px;
  }
  /* Services */
  .service-list {
    list-style: none;
  }
  .service-list li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid var(--border);
    font-size: 13px;
  }
  .service-list li:last-child { border-bottom: none; }
  .service-score {
    font-family: 'SF Mono', Monaco, monospace;
    font-size: 12px;
    color: var(--accent);
  }
  /* Disclaimer */
  .disclaimer {
    text-align: center;
    font-size: 11px;
    color: var(--text-dim);
    line-height: 1.6;
    max-width: 800px;
    margin: 40px auto 0;
    padding: 20px;
    border-top: 1px solid var(--border);
  }
  /* Animations */
  @keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
  }
  @keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .stagger-1 { animation-delay: 0.1s; }
  .stagger-2 { animation-delay: 0.2s; }
  .stagger-3 { animation-delay: 0.3s; }
  .stagger-4 { animation-delay: 0.4s; }
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>ZYTO Wellness Assessment</h1>
    <h2>Full Body Scan — 360° Biofeedback Profile</h2>
    <div class="date">Sample Client — January 15, 2025 (synthetic demonstration data)</div>
  </header>

  <div class="dashboard">
    <!-- Left Column: Body Visualization -->
    <div class="card stagger-1">
      <h3>Stress Map</h3>
      <div class="body-viz">
        <svg class="body-svg" viewBox="0 0 200 480" xmlns="http://www.w3.org/2000/svg">
          <!-- Simplified human body outline -->
          <path d="M100 15 C85 15 75 25 75 38 C75 48 82 55 90 58 L90 68 L60 78 L55 140 L70 145 L75 100 L80 100 L82 220 L78 280 L70 330 L85 335 L90 290 L95 290 L95 460 L105 460 L105 290 L110 290 L115 335 L130 330 L122 280 L118 220 L120 100 L125 100 L130 145 L145 140 L140 78 L110 68 L110 58 C118 55 125 48 125 38 C125 25 115 15 100 15Z"/>
          <!-- Spine line -->
          <path d="M100 58 L100 280" stroke-dasharray="4,4" opacity="0.3"/>
          <!-- Arms -->
          <path d="M60 78 L35 120 M140 78 L165 120"/>
        </svg>
        <!-- Hotspots positioned roughly over organs -->
        <div class="hotspot" style="left:55%; top:14%;" data-label="Adrenal Glands"></div>
        <div class="hotspot" style="left:45%; top:22%;" data-label="Stomach"></div>
        <div class="hotspot" style="left:52%; top:28%;" data-label="Small Intestine"></div>
        <div class="hotspot" style="left:48%; top:32%;" data-label="Kidneys"></div>
        <div class="hotspot" style="left:50%; top:38%;" data-label="Uterus"></div>
        <div class="hotspot" style="left:42%; top:42%;" data-label="Spleen"></div>
        <div class="hotspot" style="left:38%; top:48%;" data-label="Liver"></div>
        <div class="hotspot" style="left:62%; top:50%;" data-label="Pancreas"></div>
      </div>
    </div>

    <!-- Center Column: Score + Categories -->
    <div>
      <div class="card stagger-2" style="margin-bottom: 30px;">
        <h3>Scan Results</h3>
        <div class="score-circle">
          <svg width="160" height="160" viewBox="0 0 160 160">
            <circle class="track" cx="80" cy="80" r="70"/>
            <circle class="progress" cx="80" cy="80" r="70"
                    stroke-dasharray="440"
                    stroke-dashoffset="440"
                    id="balance-circle"/>
          </svg>
          <div class="score-value">
            <div class="number" id="balance-number">0</div>
            <div class="label">Balance Score</div>
          </div>
        </div>
        <div class="balance-status" id="balance-status">Analyzing...</div>
        <div class="balance-desc" id="balance-desc"></div>
      </div>

      <div class="card stagger-3">
        <h3>Category Breakdown</h3>
        <div id="categories">
          <!-- Categories injected by JS -->
        </div>
      </div>
    </div>

    <!-- Right Column: Stressors + Recommendations -->
    <div>
      <div class="card stagger-2" style="margin-bottom: 30px;">
        <h3>Priority Stressors</h3>
        <ul class="stressor-list" id="stressors">
          <!-- Injected by JS -->
        </ul>
      </div>

      <div class="card stagger-3" style="margin-bottom: 30px;">
        <h3>Recommended Balancers</h3>
        <ul class="rec-list" id="balancers">
          <!-- Injected by JS -->
        </ul>
      </div>

      <div class="card stagger-4">
        <h3>Suggested Services</h3>
        <ul class="service-list" id="services">
          <!-- Injected by JS -->
        </ul>
      </div>
    </div>
  </div>

  <div class="disclaimer">
    This scan is not a medical diagnosis and is not intended to diagnose, treat, cure, or prevent any disease.
    Results are for wellness purposes only. The ZYTO Hand Cradle is FDA-cleared for galvanic skin response measurement.
    ZYTO software has not undergone FDA review for effectiveness.
  </div>
</div>

<script>
const dashboardData = {{DASHBOARD_DATA_JSON}};
const balancers = {{BALANCERS_JSON}};
const services = {{SERVICES_JSON}};
const topStressors = {{STRESSORS_JSON}};

// Animate balance score
function animateValue(id, start, end, duration) {
  const obj = document.getElementById(id);
  const range = end - start;
  const minTimer = 50;
  let stepTime = Math.abs(Math.floor(duration / range));
  stepTime = Math.max(stepTime, minTimer);
  let startTime = new Date().getTime();
  let endTime = startTime + duration;
  let timer;

  function run() {
    let now = new Date().getTime();
    let remaining = Math.max((endTime - now) / duration, 0);
    let value = Math.round(end - (remaining * range));
    obj.innerHTML = value;
    if (value == end) clearInterval(timer);
  }
  timer = setInterval(run, stepTime);
  run();
}

// Set balance circle
const balanceScore = dashboardData.balanceScore;
const circumference = 440;
const offset = circumference - (balanceScore / 100) * circumference;
setTimeout(() => {
  document.getElementById('balance-circle').style.strokeDashoffset = offset;
  animateValue('balance-number', 0, balanceScore, 1500);
}, 300);

// Balance status text
const statusEl = document.getElementById('balance-status');
const descEl = document.getElementById('balance-desc');
if (balanceScore >= 80) {
  statusEl.textContent = 'Good Balance';
  descEl.textContent = 'Your body is showing signs of balance and adaptation. Keep nourishing your body and mind.';
} else if (balanceScore >= 60) {
  statusEl.textContent = 'Moderate Stress';
  descEl.textContent = 'Your biofeedback profile indicates areas of energetic stress that would benefit from targeted support.';
} else {
  statusEl.textContent = 'Significant Stress';
  descEl.textContent = 'Multiple systems are signaling stress. Prioritize rest, nutrition, and the recommended balancers below.';
}

// Render categories
const catContainer = document.getElementById('categories');
const catOrder = ['Energy', 'Heavy Metals', 'Inflammation', 'Nutrition', 'Mental Wellness', 'Detoxification'];
catOrder.forEach((name, i) => {
  const data = dashboardData.categories[name];
  const score = data.score;
  let fillClass = '';
  if (score < 60) fillClass = 'low';
  else if (score < 75) fillClass = 'medium';

  const div = document.createElement('div');
  div.className = 'category';
  div.innerHTML = `
    <div class="cat-header">
      <span class="cat-name">${name}</span>
      <span class="cat-score">${score}</span>
    </div>
    <div class="cat-bar">
      <div class="cat-fill ${fillClass}" style="width: 0%;" data-width="${score}%"></div>
    </div>
  `;
  catContainer.appendChild(div);

  // Animate bars
  setTimeout(() => {
    div.querySelector('.cat-fill').style.width = score + '%';
  }, 500 + i * 150);
});

// Render stressors
const stressorList = document.getElementById('stressors');
topStressors.forEach(([name, val]) => {
  const li = document.createElement('li');
  li.innerHTML = `<span class="stressor-name">${name.replace(/^[^:]+: /, '')}</span><span class="stressor-val">${val > 0 ? '+' : ''}${val.toFixed(2)}</span>`;
  stressorList.appendChild(li);
});

// Render balancers
const balancerList = document.getElementById('balancers');
const icons = {
  'Nutrition': '', 'Immunity': '', 'Minerals': '',
  'Antioxidants': '', 'Digestion': '', 'Mental Wellness': ''
};
balancers.slice(0, 5).forEach(b => {
  const li = document.createElement('li');
  li.innerHTML = `
    <div class="rec-icon">${icons[b.category] || ''}</div>
    <div class="rec-content">
      <div class="rec-title">${b.name}</div>
      <div class="rec-meta">${b.category} • ${b.dose}</div>
      <div class="rec-impact">+${b.impact} biomarkers brought into range</div>
    </div>
  `;
  balancerList.appendChild(li);
});

// Render services
const serviceList = document.getElementById('services');
services.forEach(s => {
  const li = document.createElement('li');
  li.innerHTML = `<span>${s.name}</span><span class="service-score">${s.score.toFixed(2)}</span>`;
  serviceList.appendChild(li);
});
</script>
</body>
</html>
"""

# Prepare JSON data
output_data = {
    "balanceScore": balance_score,
    "categories": {
        name: {"score": info["score"], "description": info["description"]}
        for name, info in dashboard_data.items()
    }
}

json_data = json.dumps(output_data)
json_balancers = json.dumps(BALANCERS)
json_services = json.dumps(SERVICES)
json_stressors = json.dumps(top_stressors)

html = HTML_TEMPLATE.replace("{{DASHBOARD_DATA_JSON}}", json_data)
html = html.replace("{{BALANCERS_JSON}}", json_balancers)
html = html.replace("{{SERVICES_JSON}}", json_services)
html = html.replace("{{STRESSORS_JSON}}", json_stressors)

output_path = args.output
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Dashboard generated: {output_path}")
print(f"\nComputed Scores:")
print(f"   Balance Score: {balance_score}")
for name in ["Energy", "Heavy Metals", "Inflammation", "Nutrition", "Mental Wellness", "Detoxification"]:
    print(f"   {name}: {dashboard_data[name]['score']}")
print(f"\nTop Stressors:")
for name, val in top_stressors[:5]:
    print(f"   {name}: {val:+.2f}")
print(f"\nTop Balancers:")
for b in BALANCERS[:3]:
    print(f"   {b['name']} (+{b['impact']} biomarkers)")
