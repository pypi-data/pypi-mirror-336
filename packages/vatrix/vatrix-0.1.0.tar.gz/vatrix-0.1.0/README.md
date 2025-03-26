# vatrix
![Python](https://img.shields.io/badge/python-3.9-blue)  ![License](https://img.shields.io/badge/license-MIT-green) [![Last Commit](https://img.shields.io/github/last-commit/brianbatesactual/vatrix)](https://github.com/brianbatesactual/vatrix) [![Stars](https://img.shields.io/github/stars/brianbatesactual/vatrix?style=social)](https://github.com/brianbatesactual/vatrix)


# 🧠 Vatrix

**Vatrix** is an intelligent log processing and SBERT training tool. It converts structured logs into natural language events, useful for training sentence similarity models, SOC alert pipelines, and log summarization tools.

---

## 🚀 Features

- 🏗️ Modular template system powered by Jinja2
- 🧪 SBERT data generation and similarity scoring
- 🌊 Supports file mode, stdin stream mode, and CLI flags
- 📦 Exports training pairs to CSV
- 🪵 Flexible and colorful logging with log rotation

---

## 📦 Installation

```bash
git clone https://github.com/brianbatesactual/vatrix.git
cd vatrix
make setup
```
---

## 🛠️ Usage
```bash
vatrix --mode file \
       --render-mode all \
       --input data/input_logs.json \
       --output data/processed_logs.csv \
       --unmatched data/unmatched_logs.json \
       --generate-sbert-data \
       --log-level DEBUG \
       --log-file logs/vatrix_debug.log
```
Run with default file input:
```bash
make run
```
Stream logs from stdin:
```bash
make stream
```
Generate SBERT training pairs:
```bash
make retrain
```
---

## 🧠 Example

---

## 🧪 Testing
```bash
make test
```
---

## 📁 Logs

All logs are saved to the logs/ directory with daily rotation.

---

## 🧼 Cleanup
```bash
make clean    # Clean temp data
make nuke     # Wipe and rebuild virtualenv
```
---

## 📚 License

MIT © Brian Bates