# 🚩 Plotolo

### A full-stack Python framework for creating interactive web applications from Jupyter Notebooks.

Experiments for serving Jupyter Notebook files through Tornado websockets as an interactive web application.

# Guide

_todo_

# How it works 🤷🏽
#### (Streamlit + Jupyter Notebook) =:

- The client connects to the server through websocket.
- The server reads and compiles the Notebook's source code and executes it cell by cell.
- The Notebook's source code calls widget functions.
- The widgets are sent to the client through the server.
- The client displays the widgets as UI components.
- The client sends widget input to the server on user interactions.
- The server partially re-executes the Notebook with the new input.

- +1 Works embedded inside Jupyter without running a server using in-browser Javascript.

So it is basically Streamlit, but it
- does not rerun the whole script on inputs, only the given cells (imitating the normal data science flow: when I modify a cell, I rerun it with the following cells).
- can work without a server and display widgets inside the Notebook during development.

So it is better. 💩

Example flow:
---
<img src="https://github.com/GergoMiklos/plotolo/assets/70636477/6c79a9d0-7e5d-4a7b-9b23-83733ed36a86" width="350">
<img src="https://github.com/GergoMiklos/plotolo/assets/70636477/30936dc6-8d74-476f-b001-8821b530b106" width="350">

Architecture:
---
<img src="https://github.com/GergoMiklos/plotolo/assets/70636477/0cb1cd37-8607-46db-adeb-f936cae0b2cf" width="500">

# Project structure 🏗

This project is a monorepo containing the following:
- **backend (lib)**: Tornado Web Server + IPython widgets
- **frontend**: Next.js Web Application
- **widget(s)**: React Component Library

Detailed architecture:
---
<img src="https://github.com/GergoMiklos/plotolo/assets/70636477/f7c02d30-b1e8-4b7f-b533-811fa25dc212" width="800">

# How to run 🏃🏽

_Currently only the dev mode is supported._

Prerequisites:
- Python >= 3.9 + PiP
- Node.js >= 18.0

### Install dependencies:
```bash
pip install -r requirements.txt
cd ./frontend
npm install
```

### Embedded mode from a Notebook:
Use an existing example or create a new Notebook:
```bash
cd ./examples
jupyter notebook
```

### Standalone server mode:
Start backend:
```bash
python ./main.py
```
Start frontend:
```bash
cd ./frontend
npm run dev
```
Then go to [http://localhost:3000](http://localhost:3000)

Start widget storybook:
```bash
cd ./widget
npm run storybook
```
Then go to [http://localhost:6006](http://localhost:6006)
