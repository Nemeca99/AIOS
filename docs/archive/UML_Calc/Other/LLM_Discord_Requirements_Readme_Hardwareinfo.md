# LLM, Discord, Requirements & Hardware Guide

---

## System Requirements & Hardware

- **OS:** Windows 11 Home 64-bit (Build 22000)
- **CPU:** Intel i7-11700F (8C/16T, 2.5GHz base)
- **RAM:** 32GB DDR4
- **GPU:** NVIDIA GeForce RTX 3060 Ti (8GB VRAM, 24GB total display memory)
- **Storage:**
  - C: 476GB SSD (Kingston)
  - D: 953GB HDD (WD)
  - E: 1.9TB HDD (Seagate)
  - F: 1TB SSD (Samsung)
  - G: 256GB NVMe (Toshiba)
- **Monitor:** Samsung U32J59x (3840x2160@60Hz)
- **Audio:** Turtle Beach Stealth 450, Realtek, NVIDIA HD Audio
- **Peripherals:** Logitech G710 Keyboard, G203 Mouse, Logi C615 HD Webcam

---

## Installation & Setup

1. **Install Python 3.10+**
2. **Install dependencies:**
   - `pip install -r requirements.txt`
   - `pip install -r discord_bot_requirements.txt`
   - `pip install psutil spacy`
   - `python -m spacy download en_core_web_sm`
3. **Run setup:**
   - `python utils/setup/setup_blackwall.py` or `pip install -e .`
4. **Start the bot:**
   - `python run_blackwall.py`
5. **Dashboard:**
   - `python dashboard/integrated_dashboard.py`
6. **Batch/Automated Runs:**
   - Use `nightrun.py`, `nightrun_bypass.py`, or .bat equivalents

---

## Discord Bot Integration

- Requires Discord bot token
- LM Studio must be running at http://localhost:1234
- Google Drive API credentials optional for memory backup
- See DISCORD_BOT_GUIDE.md for details (now merged here)

---

## Requirements Files

- `requirements.txt`: Core dependencies
- `discord_bot_requirements.txt`: Discord and Google API dependencies

---

## Troubleshooting & Notes

- For import errors, check directory structure and use direct imports
- For missing right hemisphere, use bypass scripts
- Logs and feedback in /logs/ and BLACKWALL_LOGS.md
- For architecture, see SYSTEMS_SUMMARY.md
- For build history, see Build_Change_Log.md

---

## LLM

curl <http://localhost:1234/v1/chat/completions> \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen/qwen3-14b",
    "messages": [
      { "role": "system", "content": "Always answer in rhymes. Today is Thursday" },
      { "role": "user", "content": "What day is it today?" }
    ],
    "temperature": 0.7,
    "max_tokens": -1,
    "stream": false
  }'

Model: qwen/qwen3-14b

File: Qwen3-14B-Q6_K.gguf

Format: GGUF

Quantization: Q6_K

Arch: qwen3

Size on disk: 12.12 GB

API Usage: This model's API identifier

qwen/qwen3-14b

✅ The local server is reachable at this address

<http://169.254.83.107:1234>
