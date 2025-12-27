# AsimovLeadCaptor

![Project Logo](logo.png)

**A complete lead capture and WhatsApp automation system with a cyberpunk interface.**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org) [![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org) [![WhatsApp](https://img.shields.io/badge/WhatsApp-Bot-25D366.svg)](https://whatsapp.com) [![AI](https://img.shields.io/badge/AI-Powered-purple.svg)](https://openrouter.ai) [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Overview

AsimovLeadCaptor is a full-stack automation tool designed to capture leads from Google Maps and dispatch personalized WhatsApp messages. It leverages AI for message generation and features a futuristic terminal-based UI for a unique user experience.

## 🚀 Quick Start

### Prerequisites
- **Python 3.7+**
- **Node.js 18+**
- A valid **WhatsApp** account
- API Keys for **AI Services** (OpenRouter, DALL-E, etc.)

### Installation & Execution

1. **Clone the repository:**
   bash
   git clone https://github.com/yourusername/AsimovLeadCaptor.git
   cd AsimovLeadCaptor
   

2. **Install Dependencies:**
   bash
   # Python dependencies
   pip install -r requirements.txt

   # Node.js dependencies
   npm install
   

3. **Configure Environment:**
   Create a `.env` file or edit `config.json` with your API keys and settings.

4. **Run the Application:**
   
   **Windows:**
   cmd
   start_asimov.bat
   
   
   **Linux/Mac:**
   bash
   python app.py
   

## 🎮 Usage

Upon launching, you will be presented with a main menu:

1. **🚀 Full System:** Runs both the Lead Generator and WhatsApp Dispatcher.
2. **🎯 Lead Generator Only:** Extracts data from Google Maps.
3. **📱 WhatsApp Dispatcher Only:** Manages message sending and session.
4. **⚙️ Settings & Status:** Configure API keys and check system status.

### Workflow

1. Select **[1] Full System** or **[2] Lead Generator**.
2. Enter your search criteria (Niche, Location).
3. The system scrapes Google Maps and saves leads to a database/CSV.
4. Select **[3] WhatsApp Dispatcher**.
5. Connect your WhatsApp via QR Code scan.
6. Start the campaign to send AI-generated messages to your leads.

## 🤖 AI Integration

The system integrates with LLMs to:
- **Personalize Messages:** Unique intros for every lead based on their business type.
- **Generate Context:** Analyze lead data to create relevant hooks.
- **Image Generation (Optional):** Use DALL-E to generate personalized images for messages.

## ⚙️ Configuration

Key configuration files:
- `config.json`: Main settings (timeout, delays, file paths).
- `.env`: Secure storage for API keys and tokens.

## 📊 Features

- **Lead Capture:**
  - Google Maps scraping with filters.
  - Data validation and cleaning.
  - Export to Excel/CSV.

- **WhatsApp Automation:**
  - Multi-session support.
  - Auto-reconnection.
  - Real-time statistics dashboard.

- **Interface:**
  - Cyberpunk / Terminal aesthetic.
  - Interactive menu system.

## 🔒 Disclaimer

*Automating WhatsApp usage is against their Terms of Service. Use this tool responsibly and at your own risk. This project is for educational purposes.*

## 📄 License

MIT License. See `LICENSE` file for details.