# 📱 WhatsApp Sender and Management Tool

A Python-based desktop application to automate the sending of WhatsApp messages and manage related tasks through an admin panel. This tool is ideal for businesses or individuals needing efficient communication with clients, whether for marketing, support, reminders, or notifications.

---

## 🔧 Overview

This project consists of two main components:

* **Message Sender**: Automates the delivery of WhatsApp messages via scheduled or manual input.
* **Admin Interface**: A GUI-based control panel for managing users, messages, logs, and configurations.

---

## 🗃️ Features

* Send custom or scheduled WhatsApp messages
* Manage recipients and message templates
* View message history and logs
* Simple, user-friendly admin panel (built with PyQt5 or Tkinter)
* Integrated SQL database for data storage
* Support for packaging into standalone executables (via PyInstaller)
* Virtual environment support for isolated dependencies

---

## 🛠️ Technical Details

* **Language**: Python
* **Database**: SQL (MySQL or SQLite compatible)
* **GUI Framework**: PyQt5 or Tkinter
* **Packaging Tool**: PyInstaller

The provided `.sql` file creates the necessary tables for managing messages, users, and logs. This allows for easy deployment on compatible systems and supports scalability.

---

## 🔐 Security Notice

* Avoid storing plain text passwords (e.g., in `sender passw.txt`)
* Use environment variables or encrypted secrets for storing sensitive data
* This tool is **not affiliated with WhatsApp** and must be used in accordance with WhatsApp’s Terms of Service

---

## 📚 Intended Use

This tool is designed for **educational and practical applications** in automating WhatsApp communications. It provides a solid foundation for learning or extending toward a production-ready messaging system. Possible extensions include:

* Contact import/export (CSV, Excel)
* Integration with cloud services (e.g., Firebase, AWS)
* Task scheduling and background processing

---

## 👨‍💻 Developer Notes

The codebase is modular and easy to adapt. Whether you're looking to automate a personal messaging workflow or build a client outreach tool, this project gives you the tools to get started with Python-based WhatsApp automation.

---

## ⚠️ Disclaimer

This tool is an independent project. It is **not developed, endorsed, or supported by WhatsApp Inc.** All users are responsible for complying with the relevant laws and platform rules.
