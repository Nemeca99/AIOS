from flask import Flask, request, render_template_string, jsonify
import os
import datetime
import sys

# Add the UML Calculator core path
sys.path.append(r'd:\UML Calculator\UML_Core')
from uml_core import parse_uml, eval_uml, eval_recursive_compress, letter_to_number, number_to_letter

# Base52 encoding function for web calculator compatibility
def base52_encode(n):
    """Convert integer to base52 letter encoding for UML mode display."""
    if n <= 0:
        return '0'
    return number_to_letter(n)

# Commented out LLM-related imports and variables
# import requests
# LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"
# LMSTUDIO_MODEL = "deepseek/deepseek-r1-0528-qwen3-8b"
# OLLAMA_URL = "http://localhost:11434/api/generate"
# MODEL = "llama3"
SUMMARIES_DIR = os.path.join("Memory", "Codex_Summaries")

# Load Codex context from all summary .md files
def load_codex_context():
    codex_context = ""
    if os.path.isdir(SUMMARIES_DIR):
        summary_files = [f for f in os.listdir(SUMMARIES_DIR) if f.endswith(".md")]
        summary_files.sort()
        for fname in summary_files:
            fpath = os.path.join(SUMMARIES_DIR, fname)
            try:
                with open(fpath, encoding="utf-8") as f:
                    codex_context += f"\n\n# {fname}\n" + f.read()
            except OSError as e:
                codex_context += f"\n[Warning: Could not read {fname}: {e}]\n"
    return codex_context

def get_manual_codex_preload():
    """Returns the persistent Codex context for UML and Notion, as in the CLI calculator."""
    return '''
# === UML (Universal Mathematical Language) Preload ===
# Always interpret the acronym UML as "Universal Mathematical Language" (not Unified Modeling Language, not Universal Model Language).
# UML is a symbolic, recursive, and universal notation for expressing mathematical, logical, and philosophical concepts.
# In this Codex, UML is the language of symbolic math, recursion, and compressed meaning.
# When a user asks about UML, always:
#   - Treat it as Universal Mathematical Language.
#   - Provide foundational concepts, symbolic logic, and examples in Codex style.
#   - Use UML to answer symbolic, recursive, or mathematical queries, showing step-by-step logic if possible.
#   - If a user asks for a UML diagram, provide a symbolic or equation-based representation, not a software diagram.
# Example: In UML, a recursive function is a symbolic loop; a system is a set of nested, self-referential equations.
# Example: To express the factorial function in UML:  n! = n × (n-1)!  with base case 0! = 1.
# ...
# === Notion: UML Section 1 – Dimensional Operators & Syntax ===
# UML Operator Table:
#   Addition:        [A,B][A,B]         → A + B
#   Subtraction:     {A,B} {A,B\\}       → A - B
#   Multiplication:  >A,B<<A,B<         → A × B
#   Division:        <A,B><A,B>         → A ÷ B
#   Exponentiation:  n[A,B]^n[A,B]      → A^n + B^n
#   Root:            >\\/[N]<>\\/[N]<     → Nth root
#   Logarithm:       ?(A,B)?(A,B)       → log_A B
#   Factorial:       !A!A               → A!
#   Modulo:          %[A,B]             → A mod B
# ...
'''

app = Flask(__name__)

HTML = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Codex Calculator</title>
    <link href="/bootstrap-5.3.6-dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
    <style>
      body {
        font-family: 'Share Tech Mono', 'Fira Mono', 'Montserrat', Arial, sans-serif;
        background: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%);
        min-height: 100vh;
        color: #23272f;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
      }
      .header-bar {
        width: 100vw;
        background: linear-gradient(90deg, #6366f1 0%, #3b82f6 100%);
        color: #fff;
        font-family: 'Share Tech Mono', monospace;
        font-size: 2rem;
        font-weight: bold;
        letter-spacing: 0.04em;
        text-align: center;
        padding: 0.7em 0 0.5em 0;
        margin-bottom: 2em;
        box-shadow: 0 2px 12px #6366f133;
        border-bottom-left-radius: 1.2em;
        border-bottom-right-radius: 1.2em;
        transition: box-shadow 0.2s;
      }
      .calc-panel {
        background: rgba(255,255,255,0.25);
        backdrop-filter: blur(8px);
        border-radius: 2em;
        box-shadow: 0 8px 32px 0 #6366f133, 0 1.5px 6px #6366f122;
        border: 1.5px solid #e0e7ff;
        padding: 2.2em 1.7em 1.7em 1.7em;
        margin-bottom: 1em;
        position: relative;
        animation: panelFadeIn 0.7s;
        display: flex;
        flex-direction: column;
        align-items: center;
        transition: box-shadow 0.2s, background 0.2s;
        width: 100%;
        max-width: 480px;
      }
      @keyframes panelFadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: none; }
      }
      .calc-title {
        font-family: 'Share Tech Mono', monospace;
        color: #6366f1;
        font-size: 1.5em;
        margin-bottom: 1.2em;
        text-align: center;
        letter-spacing: 0.03em;
      }
      .calc-screen-row {
        width: 100%;
        display: flex;
        justify-content: center;
        margin-bottom: 1.2em;
      }
      #calc-screen {
        width: 100%;
        max-width: 340px;
        font-size: 2em;
        text-align: right;
        padding: 0.7em 1em;
        background: rgba(255,255,255,0.7);
        border: none;
        border-radius: 1em;
        box-shadow: 0 4px 24px #b6c6f1cc, 0 1.5px 6px #6366f122;
        outline: none;
        color: #23272f;
        font-family: 'Share Tech Mono', monospace;
        transition: box-shadow 0.2s, background 0.2s;
        margin: 0 auto;
        display: block;
      }
      #calc-screen:focus {
        box-shadow: 0 0 0 3px #6366f1aa, 0 4px 24px #b6c6f1cc;
        background: #f0f7ff;
      }
      .virtual-keyboard-box {
        background: rgba(255,255,255,0.18);
        border-radius: 1.5em;
        box-shadow: 0 2px 12px #6366f122, 0 1.5px 6px #6366f122;
        padding: 0.7em 0.5em 0.7em 0.5em;
        margin-bottom: 1.2em;
        border: 1.5px solid #a5b4fc;
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        max-width: 320px;
      }
      .virtual-keyboard {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 0.5em;
        width: 100%;
        justify-items: center;
        background: none;
        box-shadow: none;
        padding: 0;
        margin: 0;
      }
      .vk-btn {
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.1em;
        background: rgba(255,255,255,0.85);
        border: none;
        color: #3b82f6;
        border-radius: 1em;
        padding: 0.7em 0;
        cursor: pointer;
        transition: background 0.18s, color 0.18s, box-shadow 0.18s, transform 0.09s;
        box-shadow: 0 2px 8px #b6c6f1cc, 0 1.5px 6px #6366f122;
        user-select: none;
        min-width: 2em;
        min-height: 2em;
        font-weight: 600;
        margin: 0.1em;
        outline: none;
        border-bottom: 3px solid #c7d2fe;
      }
      .vk-btn:active {
        background: #6366f1;
        color: #fff;
        transform: scale(0.97);
        box-shadow: 0 2px 16px #6366f144;
        border-bottom: 3px solid #6366f1;
      }
      .vk-btn:hover {
        background: #e0e7ff;
        color: #23272f;
        box-shadow: 0 4px 16px #6366f144;
      }
      .result {
        background: #f1f5f9;
        padding: 1.7em;
        border-radius: 1em;
        margin-bottom: 1.5em;
        white-space: pre-wrap;
        font-family: 'Fira Mono', monospace;
        font-size: 1.22em;
        box-shadow: 0 2px 8px #6366f122;
        position: relative;
        min-height: 4em;
      }
      .result button {
        position: absolute;
        top: 1.1em;
        right: 1.1em;
        font-size: 1em;
        padding: 0.4em 1.1em;
        border-radius: 0.5em;
        border: none;
        background: #6366f1;
        color: #fff;
        cursor: pointer;
        transition: background 0.2s;
      }
      .result button:hover {
        background: #3b82f6;
      }
      .history {
        background: rgba(255,255,255,0.18);
        border: 1.5px solid #a5b4fc;
        border-radius: 1em;
        padding: 1.3em;
        max-height: 180px;
        overflow-y: auto;
        font-size: 1.08em;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
        box-shadow: 0 1px 4px #6366f122;
        min-height: 3em;
        width: 100%;
        max-width: 340px;
        color: #23272f;
      }
      .history-item {
        padding: 0.3em 0.2em;
        border-radius: 0.5em;
        margin-bottom: 0.2em;
        cursor: pointer;
        transition: background 0.15s, color 0.15s;
      }
      .history-item:hover {
        background: #6366f1;
        color: #fff;
      }
      .calc-tabs {
        display: flex;
        justify-content: center;
        margin-bottom: 1.5em;
        gap: 0.5em;
      }
      .calc-tab {
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.1em;
        background: #e0e7ff;
        color: #3b82f6;
        border: none;
        border-radius: 1em 1em 0 0;
        padding: 0.7em 1.5em;
        cursor: pointer;
        transition: background 0.18s, color 0.18s;
        font-weight: 600;
        outline: none;
      }
      .calc-tab.active {
        background: #6366f1;
        color: #fff;
        box-shadow: 0 2px 8px #6366f144;
      }
      .calc-panel-section { display: none; }
      .calc-panel-section.active { display: block; }
      /* Distinct styles for each calculator */
      .basic-calc .calc-title { color: #6366f1; }
      .scientific-calc .calc-title { color: #10b981; }
      .graphing-calc .calc-title { color: #f59e42; }
      .base-calc .calc-title { color: #e11d48; }
      .symbolic-calc .calc-title { color: #a21caf; }
    </style>
</head>
<body class="bg-body-tertiary">
    <div class="header-bar">Codex Calculator Suite</div>
    <div class="container-fluid d-flex flex-row justify-content-center align-items-start" style="min-height:90vh;">
      <!-- Left panel: Fun facts, tips, or Codex branding -->
      <div class="d-none d-lg-flex flex-column align-items-end justify-content-start pe-4 pt-5" style="width:22vw; min-width:220px;">
        <div class="card shadow-sm mb-4 p-3 bg-info bg-opacity-25 border-0 rounded-4" style="max-width: 320px;">
          <div class="fw-bold text-primary mb-2">Did you know?</div>
          <div class="small">UML mode lets you see symbolic math in a universal language.<br><br>Try graphing <span class="text-success">sin(x);cos(x);x^2</span>!</div>
        </div>
        <div class="card shadow-sm p-3 bg-warning bg-opacity-25 border-0 rounded-4" style="max-width: 320px;">
          <div class="fw-bold text-warning mb-2">Tip</div>
          <div class="small">Use the <b>Base</b> dropdown to convert numbers to any base (2-52).<br>Click <b>History</b> to reuse calculations.</div>
        </div>
      </div>
      <!-- Center: Calculator with tabs -->
      <div class="calc-panel card shadow-lg p-4 bg-white bg-opacity-75 border-0 rounded-4 mx-2" style="min-width:340px;max-width:520px;width:100%;z-index:2;">
        <div class="calc-tabs">
          <button class="calc-tab active" id="tab-basic">Basic</button>
          <button class="calc-tab" id="tab-scientific">Scientific</button>
          <button class="calc-tab" id="tab-graphing">Graphing</button>
          <button class="calc-tab" id="tab-base">Base Converter</button>
          <button class="calc-tab" id="tab-symbolic">Symbolic/UML</button>
        </div>
        <!-- Basic Calculator Panel -->
        <div class="calc-panel-section basic-calc active" id="panel-basic">
          <div class="calc-title h4 text-center mb-3">Basic Calculator</div>
          <input type="text" id="basic-screen" class="form-control form-control-lg text-end fw-bold rounded-3 shadow-sm mb-2" placeholder="0" readonly />
          <div class="virtual-keyboard-box mb-2">
            <div class="virtual-keyboard" id="basic-keyboard">
              <!-- Basic keypad: 7 8 9 /, 4 5 6 *, 1 2 3 -, 0 . + =, C -->
              <button class="vk-btn" data-key="7">7</button>
              <button class="vk-btn" data-key="8">8</button>
              <button class="vk-btn" data-key="9">9</button>
              <button class="vk-btn" data-key="/">÷</button>
              <button class="vk-btn" data-key="4">4</button>
              <button class="vk-btn" data-key="5">5</button>
              <button class="vk-btn" data-key="6">6</button>
              <button class="vk-btn" data-key="*">×</button>
              <button class="vk-btn" data-key="1">1</button>
              <button class="vk-btn" data-key="2">2</button>
              <button class="vk-btn" data-key="3">3</button>
              <button class="vk-btn" data-key="-">-</button>
              <button class="vk-btn" data-key="0">0</button>
              <button class="vk-btn" data-key=".">.</button>
              <button class="vk-btn" data-key="+">+</button>
              <button class="vk-btn" data-key="=">=</button>
              <button class="vk-btn btn-outline-danger" data-key="C">C</button>
            </div>
          </div>
          <div class="history card bg-light bg-opacity-50 border-0 rounded-4 p-3 shadow-sm mt-3" id="basic-history-box"><b>History:</b><ul id="basic-history-list" class="list-unstyled mb-0"></ul></div>
        </div>
        <!-- Scientific Calculator Panel (stub) -->
        <div class="calc-panel-section scientific-calc" id="panel-scientific">
          <div class="calc-title h4 text-center mb-3">Scientific Calculator</div>
          <div class="text-center text-muted">Coming soon: advanced functions, trig, log, etc.</div>
        </div>
        <!-- Graphing Calculator Panel (existing UI moved here) -->
        <div class="calc-panel-section graphing-calc" id="panel-graphing">
          <div class="calc-title h4 text-center mb-3">Graphing Calculator</div>
          <!-- Output mode, base, and scientific row -->
          <div class="d-flex justify-content-between align-items-center mb-2">
            <div class="btn-group" role="group" aria-label="Output Mode">
              <button type="button" class="btn btn-outline-primary btn-sm" id="mode-standard">Standard</button>
              <button type="button" class="btn btn-outline-secondary btn-sm" id="mode-uml">UML</button>
            </div>
            <div class="input-group input-group-sm ms-2" style="width: 140px;">
              <span class="input-group-text">Base</span>
              <select class="form-select" id="base-select">
                {% for b in range(2, 53) %}
                  <option value="{{b}}">{{b}}</option>
                {% endfor %}
              </select>
              <button class="btn btn-outline-info" id="convert-base" type="button">Convert</button>
            </div>
          </div>
          <!-- Graphing screen -->
          <div class="calc-screen-row mb-2">
            <input type="text" id="calc-screen" name="calc_screen" class="form-control form-control-lg text-end fw-bold rounded-3 shadow-sm" placeholder="0" readonly style="font-size:2em; background:rgba(255,255,255,0.7); border:none;" />
          </div>
          <!-- Graphing function input and controls -->
          <div class="d-flex flex-column flex-md-row align-items-center mb-2 gap-2">
            <input type="text" id="function-input" class="form-control form-control-sm me-2" placeholder="f(x) = e.g. sin(x), x^2+3x-2;cos(x)" style="max-width:220px;">
            <button type="button" class="btn btn-outline-success btn-sm" id="graph-btn">Graph</button>
            <button type="button" class="btn btn-outline-info btn-sm" id="zoom-in">Zoom In</button>
            <button type="button" class="btn btn-outline-info btn-sm" id="zoom-out">Zoom Out</button>
            <button type="button" class="btn btn-outline-secondary btn-sm" id="reset-graph">Reset</button>
            <div class="btn-group ms-md-2" role="group" aria-label="Theme">
              <button type="button" class="btn btn-outline-dark btn-sm" id="theme-light">Light</button>
              <button type="button" class="btn btn-outline-dark btn-sm" id="theme-dark">Dark</button>
            </div>
          </div>
          <!-- Graphing calculator keypad (TI-84 style) -->
          <div class="row g-1 mb-2 justify-content-center">
            <div class="col-2"><button class="vk-btn btn btn-outline-dark w-100" data-key="2nd">2nd</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-dark w-100" data-key="mode">MODE</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-dark w-100" data-key="del">DEL</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-dark w-100" data-key="stat">STAT</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-dark w-100" data-key="on">ON</button></div>
          </div>
          <div class="row g-1 mb-2 justify-content-center">
            <div class="col-2"><button class="vk-btn btn btn-outline-primary w-100" data-key="sin">sin</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-primary w-100" data-key="cos">cos</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-primary w-100" data-key="tan">tan</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-primary w-100" data-key="^">^</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-primary w-100" data-key="√">√</button></div>
          </div>
          <div class="row g-1 mb-2 justify-content-center">
            <div class="col-2"><button class="vk-btn btn btn-outline-secondary w-100" data-key="7">7</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-secondary w-100" data-key="8">8</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-secondary w-100" data-key="9">9</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-primary w-100" data-key="/">÷</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-primary w-100" data-key="ln">ln</button></div>
          </div>
          <div class="row g-1 mb-2 justify-content-center">
            <div class="col-2"><button class="vk-btn btn btn-outline-secondary w-100" data-key="4">4</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-secondary w-100" data-key="5">5</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-secondary w-100" data-key="6">6</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-primary w-100" data-key="*">×</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-primary w-100" data-key="log">log</button></div>
          </div>
          <div class="row g-1 mb-2 justify-content-center">
            <div class="col-2"><button class="vk-btn btn btn-outline-secondary w-100" data-key="1">1</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-secondary w-100" data-key="2">2</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-secondary w-100" data-key="3">3</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-primary w-100" data-key="-">-</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-primary w-100" data-key="Ans">Ans</button></div>
          </div>
          <div class="row g-1 mb-2 justify-content-center">
            <div class="col-2"><button class="vk-btn btn btn-outline-secondary w-100" data-key="0">0</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-secondary w-100" data-key=".">.</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-primary w-100" data-key="+">+</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-primary w-100" data-key="=">=</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-danger w-100" data-key="AC">AC</button></div>
          </div>
          <div class="row g-1 mb-2 justify-content-center">
            <div class="col-2"><button class="vk-btn btn btn-outline-info w-100" data-key="π">π</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-info w-100" data-key="e">e</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-info w-100" data-key="!">!</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-info w-100" data-key="(">(</button></div>
            <div class="col-2"><button class="vk-btn btn btn-outline-info w-100" data-key=")">)</button></div>
          </div>
          <!-- Graph and steps -->
          <div id="graph" class="mt-3" style="width:100%;max-width:400px;height:320px;"></div>
          <div id="steps" class="mt-3 card p-3 bg-light bg-opacity-75 border-0 rounded-4 shadow-sm" style="display:none;"></div>
          <!-- History -->
          <div class="history card bg-light bg-opacity-50 border-0 rounded-4 p-3 shadow-sm mt-3" id="history-box"><b>History:</b><ul id="history-list" class="list-unstyled mb-0"></ul></div>
        </div>
        <!-- Base Converter Panel (stub) -->
        <div class="calc-panel-section base-calc" id="panel-base">
          <div class="calc-title h4 text-center mb-3">Base Converter</div>
          <div class="text-center text-muted">Coming soon: convert numbers between bases 2-52.</div>
        </div>
        <!-- Symbolic/UML Calculator Panel (stub) -->
        <div class="calc-panel-section symbolic-calc" id="panel-symbolic">
          <div class="calc-title h4 text-center mb-3">Symbolic/UML Calculator</div>
          <div class="text-center text-muted">Coming soon: symbolic math, UML expressions, and step-by-step logic.</div>
        </div>
      </div>
      <!-- Right panel: More info, branding, or fun -->
      <div class="d-none d-lg-flex flex-column align-items-start justify-content-start ps-4 pt-5" style="width:22vw; min-width:220px;">
        <div class="card shadow-sm mb-4 p-3 bg-success bg-opacity-25 border-0 rounded-4" style="max-width: 320px;">
          <div class="fw-bold text-success mb-2">Codex Graphing</div>
          <div class="small">Supports multi-function plots, zoom, and step-by-step breakdowns.<br>Try <span class="text-primary">x^3-2x;sin(x)</span>!</div>
        </div>
        <div class="card shadow-sm p-3 bg-secondary bg-opacity-25 border-0 rounded-4" style="max-width: 320px;">
          <div class="fw-bold text-secondary mb-2">About</div>
          <div class="small">This calculator is powered by Codex Symbolic Core and Plotly.js.<br>Switch themes, explore bases, and enjoy math!</div>
        </div>
      </div>
    </div>  <script>
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Calculator JavaScript loading...');
        // Tab switching logic
        const tabs = ['basic', 'scientific', 'graphing', 'base', 'symbolic'];
    tabs.forEach(tab => {
      document.getElementById('tab-' + tab).onclick = function() {
        tabs.forEach(t => {
          document.getElementById('tab-' + t).classList.remove('active');
          document.getElementById('panel-' + t).classList.remove('active');
        });
        this.classList.add('active');
        document.getElementById('panel-' + tab).classList.add('active');
      };
    });
    let screen = document.getElementById('calc-screen');
    let expr = '';
    let output_mode = 'standard';
    let memory = 0;
    let lastAns = '';
    document.getElementById('mode-standard').onclick = function() {
      output_mode = 'standard';
      this.classList.add('btn-primary');
      this.classList.remove('btn-outline-primary');
      document.getElementById('mode-uml').classList.remove('btn-primary');
      document.getElementById('mode-uml').classList.add('btn-outline-secondary');
    };
    document.getElementById('mode-uml').onclick = function() {
      output_mode = 'uml';
      this.classList.add('btn-primary');
      this.classList.remove('btn-outline-secondary');
      document.getElementById('mode-standard').classList.remove('btn-primary');
      document.getElementById('mode-standard').classList.add('btn-outline-primary');
    };
    document.getElementById('convert-base').onclick = function() {
      let base = parseInt(document.getElementById('base-select').value);
      let val = parseInt(screen.value);
      if (!isNaN(val) && base >= 2 && base <= 52) {
        screen.value = val.toString(base);
      }
    };
    function updateScreen(val) {
      screen.value = val || '0';
    }
    function clearScreen() {
      expr = '';
      updateScreen(expr);
    }
    function backspaceScreen() {
      expr = expr.slice(0, -1);
      updateScreen(expr);
    }
    function appendScreen(val) {
      expr += val;
      updateScreen(expr);
    }    function handleKey(key) {
      console.log('handleKey called with:', key);
      if (key === 'C' || key === 'AC') { clearScreen(); return; }
      if (key === '⌫') { backspaceScreen(); return; }
      if (key === '=') { submitCalc(); return; }
      if (key === 'Ans') { appendScreen(lastAns); return; }
      if (key === 'M+') { memory += parseFloat(screen.value)||0; return; }
      if (key === 'M-') { memory -= parseFloat(screen.value)||0; return; }
      if (key === 'MR') { appendScreen(memory.toString()); return; }
      if (key === 'MC') { memory = 0; return; }
      if (key === '+/-') {
        if (screen.value.startsWith('-')) {
          screen.value = screen.value.slice(1);
        } else {
          screen.value = '-' + screen.value;
        }
        expr = screen.value;
        return;
      }
      appendScreen(key);
    }
    function submitCalc() {
      fetch('/api/calc', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ expr: expr, output_mode: output_mode })
      })
      .then(res => res.json())
      .then data => {
        updateScreen(data.result);
        lastAns = data.result;
        expr = '';
        updateHistory(data.history);
        showSteps(screen.value, data.result);
      })
      .catch(() => updateScreen('Err'));
    }
    function updateHistory(historyArr) {
      let list = document.getElementById('history-list');
      list.innerHTML = '';
      historyArr.forEach(item => {
        let li = document.createElement('li');
        li.textContent = item;
        li.className = 'history-item';
        li.onclick = function() {
          expr = item.split('=')[0].replace(/\\[.*?\\]|UML:|\\d{4}-\\d{2}-\\d{2}.*?\\]/g, '').trim();
          updateScreen(expr);
        };
        list.appendChild(li);
      });    }
    const buttons = document.querySelectorAll('.vk-btn');
    console.log('Found', buttons.length, 'calculator buttons');
    buttons.forEach(btn => {
      btn.onclick = function() { 
        console.log('Button clicked:', this.getAttribute('data-key'));
        handleKey(this.getAttribute('data-key')); 
      };
    });
    // Keyboard support
    document.addEventListener('keydown', function(e) {
      if (e.key.match(/[0-9+\\-*/^%.()]/)) { appendScreen(e.key); }
      if (e.key === 'Enter') { submitCalc(); }
      if (e.key === 'Backspace') { backspaceScreen(); }
      if (e.key === 'Delete') { clearScreen(); }
    });
    // On page load, fetch history
    fetch('/api/calc', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({expr:'',output_mode:output_mode})})
      .then(res => res.json())
      .then(data => updateHistory(data.history));
    updateScreen(expr);

    // Graphing logic (multi-function, zoom, reset)
    let graphLayout = {margin:{t:30}, title:'y = f(x)', xaxis:{title:'x', range:[-20,20]}, yaxis:{title:'y', autorange:true}};
    let graphData = [];
    function plotFunctions() {
      let funcStr = document.getElementById('function-input').value.trim();
      if (!funcStr) return;
      let funcs = funcStr.split(';').map(f => f.trim()).filter(f => f);
      graphData = [];
      funcs.forEach((fstr, idx) => {
        let safeFunc = fstr.replace(/\\^/g, '**');
        let x = [], y = [];
        for (let i = graphLayout.xaxis.range[0]; i <= graphLayout.xaxis.range[1]; i += 0.1) {
          let xi = i;
          try {
            let yi = eval(safeFunc.replace(/x/g, '('+xi+')'));
            if (typeof yi === 'number' && isFinite(yi)) {
              x.push(xi);
              y.push(yi);
            }
          } catch (e) { x.push(xi); y.push(NaN); }
        }
        graphData.push({x, y, mode:'lines', line:{color:Plotly.d3.schemeCategory10[idx%10]}, name:fstr});
      });
      Plotly.newPlot('graph', graphData, graphLayout, {responsive:true});
    }
    document.getElementById('graph-btn').onclick = plotFunctions;
    document.getElementById('zoom-in').onclick = function() {
      let r = graphLayout.xaxis.range;
      let mid = (r[0]+r[1])/2;
      let span = (r[1]-r[0])/2.5;
      graphLayout.xaxis.range = [mid-span/2, mid+span/2];
      plotFunctions();
    };
    document.getElementById('zoom-out').onclick = function() {
      let r = graphLayout.xaxis.range;
      let mid = (r[0]+r[1])/2;
      let span = (r[1]-r[0])*2;
      graphLayout.xaxis.range = [mid-span/2, mid+span/2];
      plotFunctions();
    };
    document.getElementById('reset-graph').onclick = function() {
      graphLayout.xaxis.range = [-20,20];
      plotFunctions();
    };
    // Multi-step breakdown for expressions
    function showSteps(expr, result) {
      let stepsDiv = document.getElementById('steps');
      if (!expr || !result) { stepsDiv.style.display = 'none'; return; }
      // Simple breakdown: tokenize and show order of operations
      let steps = [];
      try {
        let tokens = expr.match(/([\\d.]+|[+\\-*/^()])/g) || [];
        let stack = [];
        let out = [];
        let prec = {'+':1,'-':1,'*':2,'/':2,'^':3};
        tokens.forEach(tok => {
          if (/\d/.test(tok)) out.push(tok);
          else if ('+-*/^'.includes(tok)) {
            while (stack.length && prec[stack[stack.length-1]]>=prec[tok]) out.push(stack.pop());
            stack.push(tok);
          } else if (tok==='(') stack.push(tok);
          else if (tok===')') { while(stack.length && stack[stack.length-1]!=='(') out.push(stack.pop()); stack.pop(); }
        });
        while(stack.length) out.push(stack.pop());
        steps.push('Postfix: ' + out.join(' '));
        steps.push('Result: ' + result);
      } catch(e) { steps.push('Could not parse steps.'); }
      stepsDiv.innerHTML = '<b>Step-by-step:</b><br>' + steps.map(s=>'<div>'+s+'</div>').join('');
      stepsDiv.style.display = '';
    }
    // Theme switcher
    document.getElementById('theme-light').onclick = function() {
      document.body.style.background = 'linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%)';
      document.body.style.color = '#23272f';
    };
    document.getElementById('theme-dark').onclick = function() {      document.body.style.background = 'linear-gradient(120deg, #23272f 0%, #6366f1 100%)';
      document.body.style.color = '#f1f5f9';
    };
    
    }); // End DOMContentLoaded
  </script>
</body>
</html>
'''

# Store calculation history in memory (per session)
history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global history
    result = ''
    step_by_step = ''
    num1 = request.form.get('num1', '') if request.method == 'POST' else ''
    num2 = request.form.get('num2', '') if request.method == 'POST' else ''
    operator = request.form.get('operator', 'add') if request.method == 'POST' else 'add'
    output_mode = request.form.get('output_mode', 'standard') if request.method == 'POST' else 'standard'
    calc = request.form.get('calc') if request.method == 'POST' else None
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if calc:
        try:
            n1 = float(num1) if num1 else 0
            n2 = float(num2) if num2 else 0
            symbolic_expr = ''
            if operator == 'add':
                symbolic_expr = f'[{base52_encode(int(n1))},{base52_encode(int(n2))}]' if output_mode == 'uml' else f'[{n1},{n2}]'
            elif operator == 'sub':
                symbolic_expr = f'{{{base52_encode(int(n1))},{base52_encode(int(n2))}}}' if output_mode == 'uml' else f'{{{n1},{n2}}}'
            elif operator == 'mul':
                symbolic_expr = f'><{base52_encode(int(n1))},{base52_encode(int(n2))}<' if output_mode == 'uml' else f'><{n1},{n2}<'
            elif operator == 'div':
                symbolic_expr = f'<{base52_encode(int(n1))},{base52_encode(int(n2))}>' if output_mode == 'uml' else f'<{n1},{n2}>'
            elif operator == 'exp':
                symbolic_expr = f'^{base52_encode(int(n1))},{base52_encode(int(n2))}' if output_mode == 'uml' else f'^{n1},{n2}'
            elif operator == 'root':
                symbolic_expr = f'/{base52_encode(int(n1))},{base52_encode(int(n2))}' if output_mode == 'uml' else f'/{n1},{n2}'
            elif operator == 'log':
                symbolic_expr = f'?({base52_encode(int(n1))},{base52_encode(int(n2))})' if output_mode == 'uml' else f'?({n1},{n2})'
            elif operator == 'fact':
                symbolic_expr = f'!{base52_encode(int(n1))}' if output_mode == 'uml' else f'!{int(n1)}'
            elif operator == 'mod':
                symbolic_expr = f'%({base52_encode(int(n1))},{base52_encode(int(n2))})' if output_mode == 'uml' else f'%({n1},{n2})'
            symbolic_result = parse_uml(symbolic_expr, symbolic=(output_mode=='uml'))
            if output_mode == 'uml':
                result = f"UML: {symbolic_expr} = {symbolic_result}"
            else:
                result = str(symbolic_result)
            history.append(f"[{timestamp}] {symbolic_expr} = {symbolic_result}")
        except (ValueError, ZeroDivisionError) as e:
            result = f'[Error] {e}'
        except Exception as e:
            result = f'[Error] {e}'
    history_display = '\n'.join(history[-10:])
    year = datetime.datetime.now().year
    return render_template_string(HTML, result=result, num1=num1, num2=num2, operator=operator, output_mode=output_mode, history=history_display, year=year, step_by_step=step_by_step)

# Add a new API endpoint for AJAX calculation
@app.route('/api/calc', methods=['POST'])
def api_calc():
    import re
    data = request.json or {}
    expr = data.get('expr', '')
    output_mode = data.get('output_mode', 'standard')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result = ''
    
    try:
        # Handle empty expression (for initial history load)
        if not expr.strip():
            return jsonify({'result': '', 'history': history[-10:]})
        
        # Try to evaluate using enhanced UML core
        if output_mode == 'uml':
            # Use the enhanced UML Calculator for UML mode
            result_val = eval_recursive_compress(expr)
            result = f"UML: {expr} = {result_val}"
        else:
            # For standard mode, try basic math first, then UML fallback
            try:
                # Try standard math evaluation
                result_val = eval(expr)
                result = str(result_val)
            except:
                # Fall back to UML parsing for complex expressions
                parsed = parse_uml(expr)
                result_val = eval_uml(parsed)
                result = str(result_val)
        
        history.append(f"[{timestamp}] {expr} = {result}")
        
    except Exception as e:
        result = f'Err: {str(e)}'
        
    return jsonify({'result': result, 'history': history[-10:]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
