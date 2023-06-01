# 🚩 Plotolo

### A full-stack Python framework for creating interactive web applications from Jupyter Notebooks.

Experiments for serving Jupyter Notebook files through Tornado websockets as an interactive web application.

---

# How it works 🤷🏽
#### ~ Streamlit + Jupyter Notebook:

- The client connects through websocket
- The server reads and compiles the Notebook's source code and executes it cell by cell
- The Notebook calls widgets
- The widgets send their states to the client through the server
- The client displays the widgets as UI components
- The client sends the input to the server on user interactions
- The server partially re-executes the Notebook with the new input

+1 Works embedded inside Jupyter without running a server

<img src="https://github.com/GergoMiklos/plotolo/assets/70636477/6c79a9d0-7e5d-4a7b-9b23-83733ed36a86" width="395">
<img src="https://github.com/GergoMiklos/plotolo/assets/70636477/30936dc6-8d74-476f-b001-8821b530b106" width="395">
<img src="https://github.com/GergoMiklos/plotolo/assets/70636477/0cb1cd37-8607-46db-adeb-f936cae0b2cf" width="800">

---

# Project structure

This project is a monorepo containing the following:
- **backend (lib)**: Tornado Web Server + IPython widgets
- **frontend**: Next.js Web Application
- **widget(s)**: React Component Library

<img src="https://github.com/GergoMiklos/plotolo/assets/70636477/f7c02d30-b1e8-4b7f-b533-811fa25dc212" width="800">

---

# How to run 🏃🏽

_Currently only the dev mode is supported._

Prerequisites:
- Python >= 3.9 + PiP
- Node.js >= 18.0

---

### Install dependencies:
```bash
pip install -r requirements.txt
cd ./frontend
npm install
```

---

### Embedded mode from a Notebook:
Use an existing example or create a new Notebook:
```bash
cd ./examples
jupyter notebook
```

---

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

---

Start widget storybook:
```bash
cd ./widget
npm run storybook
```
Then go to [http://localhost:6006](http://localhost:6006)
