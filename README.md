<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>🧩 Sudoku Solver GUI – Python Tkinter</title>
<style>
  body { font-family: Arial, sans-serif; line-height: 1.6; background: #fafafa; color: #333; max-width: 800px; margin: auto; padding: 20px; }
  h1, h2, h3 { color: #4a148c; }
  code { background: #eee; padding: 2px 4px; border-radius: 4px; }
  pre { background: #eee; padding: 10px; border-radius: 6px; overflow-x: auto; }
  ul { list-style-type: "🔹 "; margin-left: 1em; }
  img { display: block; margin: 20px auto; border: 1px solid #ccc; border-radius: 8px; max-width: 100%; }
</style>
</head>
<body>

<h1>🧩 Sudoku Solver GUI – Python Tkinter</h1>

<p>
A fully interactive Sudoku Solver desktop application built with Python and Tkinter.
Supports manual puzzle input, random puzzle generation, visual backtracking with animation, and instant solve functionality using multithreading.
</p>

<h2>🚀 Features</h2>
<ul>
  <li>🔢 Manual input with real-time validation (only digits 1–9 allowed)</li>
  <li>🎲 Random puzzle generation from a preloaded set</li>
  <li>🧠 Visual backtracking algorithm with step-by-step animation and color-coded cells</li>
  <li>⚡ Skip button to instantly solve without animation</li>
  <li>✋ Stop button to interrupt the solving process</li>
  <li>🎨 Clean, responsive, and user-friendly Tkinter-based UI</li>
</ul>

<h2>📷 Screenshot</h2>
<p>Example of the solver running step-by-step (green = guesses, red = backtracks):</p>
<img src="sudoku_screenshot.jpg" alt="Sudoku Solver GUI screenshot" />

<h2>🛠 How It Works</h2>
<p>
Uses a classic <strong>backtracking algorithm</strong> to fill missing cells.
The step-by-step solve mode runs on a separate thread to keep the GUI responsive, updating cells in real time.
Instant solve mode computes the solution without animation.
</p>

<h2>🎯 Learning Goals & Highlights</h2>
<ul>
  <li>Combine backend algorithms with GUI design</li>
  <li>Use of Python multithreading for responsiveness</li>
  <li>Input validation and user-friendly error messages</li>
  <li>Practical event-driven programming</li>
</ul>

<h2>📦 Requirements</h2>
<ul>
  <li>Python 3.x (recommended ≥ 3.6)</li>
  <li>Tkinter (usually comes pre-installed)</li>
</ul>

<h2>✏️ Project Motivation</h2>
<p>
To build a desktop app that makes abstract algorithms visible and interactive, while practicing UI development and multithreading.
</p>

<h2>💡 Possible Extensions</h2>
<ul>
  <li>Import/export puzzles as text or JSON</li>
  <li>Timer or solving statistics</li>
  <li>Difficulty rating detection</li>
  <li>Web version using Flask, or mobile version using Kivy</li>
</ul>
</body>
</html>
