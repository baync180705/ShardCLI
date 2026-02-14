# ⚡ Shard

> Your terminal, fluent in English.

Shard is an AI-powered natural language interface for your terminal.  
It converts plain English instructions into safe shell commands — analyzes risk — and executes them only after confirmation.

No more memorizing obscure flags.  
Just describe what you want.

---

## ✨ Features

- 🧠 Natural language → shell command generation
- 🛡️ Built-in risk engine (strict / default / relaxed policies)
- 🔍 Structured output validation (LLM-safe parsing)
- 🎨 Clean terminal UI (Rich + Typer)
- 💬 Interactive session mode
- ⚙️ Configurable safety levels

---

## 🚀 Example

```bash
shard "delete all node_modules folders recursively"

shard --policy strict "install nginx"

shard
>> check all files including hidden ones
>> compress this folder
>> exit
```

---

## 🛡️ Safety First

Shard never executes commands automatically.

Each generated command:

- Is analyzed by a deterministic risk engine  
- Is classified as **SAFE / WARN / BLOCK**  
- Requires explicit user confirmation  

Strict mode can block dangerous operations entirely.

---

## 🧩 Installation (GitHub Version)

Since Shard is not yet published to PyPI, install directly from source.

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/baync180705/ShardCLI.git
cd ShardCLI
```

### 2️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
# venv\Scripts\activate   # Windows
```

### 3️⃣ Install in Editable Mode

```bash
pip install -e .
```

This makes the `shard` command available globally inside your environment.

---

## 🔑 Setup API Key

Shard requires a Groq API key.

Export it as an environment variable:

```bash
export GROQ_API_KEY=your_groq_api_key_here
```

For Windows (PowerShell):

```powershell
setx GROQ_API_KEY "your_groq_api_key_here"
```

---

## 🧠 Usage

### One-shot Mode

```bash
shard "check all files in this folder including hidden ones"
```

### Interactive Mode

```bash
shard
```

Type commands interactively:

```text
>> delete build folder
>> list large files
>> exit
```

### Policy Levels

You can control safety strictness:

```bash
shard --policy strict "delete temp files"
```

Available policies:

- `strict` → Maximum protection  
- `default` → Balanced safety (default)  
- `relaxed` → Less restrictive  

### Show Explanation

```bash
shard --explain "compress this directory"
```

Displays the reasoning behind the generated command.

---

## 📦 Project Structure

```text
shardcli/
├── LICENSE
├── pyproject.toml
├── README.md
└── shardcli
    ├── config
    │   ├── config.py
    │   └── __init__.py
    ├── core
    │   ├── environment.py
    │   ├── executor.py
    │   ├── __init__.py
    │   ├── models.py
    │   └── orchestrator.py
    ├── engine
    │   ├── __init__.py
    │   ├── policy
    │   │   ├── base.py
    │   │   ├── default.py
    │   │   ├── __init__.py
    │   │   ├── relaxed.py
    │   │   └── strict.py
    │   ├── risk_engine.py
    │   └── risk_types.py
    ├── __init__.py
    ├── interface
    │   ├── cli.py
    │   └── __init__.py
    ├── llm
    │   ├── __init__.py
    │   ├── llm_client.py
    │   ├── models
    │   │   └── command_result.py
    │   ├── prompt_builder.py
    │   └── structured_output.py
    ├── main.py
    └── requirements.txt
```

---

## 🏗️ Architecture

Shard is built with clean separation of concerns:

- **LLM Layer** → Structured command generation  
- **Risk Engine** → Deterministic safety checks  
- **Policy System** → Configurable safety levels  
- **Orchestrator** → Coordinates workflow  
- **Executor** → Runs commands safely  
- **CLI Layer** → User interface only  

---

## ⚠️ Disclaimer

Shard executes real shell commands.

Always review generated commands before confirming execution.  
Use strict mode when in doubt.

---

## 🛠️ Development

Run locally:

```bash
python -m shardcli.main
```

Or via installed CLI:

```bash
shard --help
```

---

## 📄 License

MIT License

---

## 🌟 Why Shard?

Because your terminal should understand you —  
not the other way around.
