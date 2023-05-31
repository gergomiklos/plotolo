# 🚩 Plotolo

### A full-stack Python framework for creating interactive web applications from Jupyter Notebooks.

---

Experiments for serving Jupyter Notebook files through Tornado websockets as an interactive web application.


This project is a monorepo containing the following:
- **backend (lib)**: Tornado Web Server + IPython widgets
- **frontend**: Next.js Web Application
- **widget(s)**: React Component Library

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

---

# How to run 🏃🏽

_Currently only in dev mode_

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

Start widget Storybook:
```bash
cd ./widget
npm run storybook
```
Then go to [http://localhost:6006](http://localhost:6006)
