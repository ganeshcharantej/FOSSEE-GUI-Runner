# OpenModelica Simulation Runner

A Python-based Desktop GUI application built with PyQt6 to seamlessly execute compiled OpenModelica (`.exe` or Linux binaries) simulations with custom time parameters.

This project was developed as a screening task for FOSSEE.

## 📖 Methodology & OOP Implementation
The application is strictly designed following Object-Oriented Programming (OOP) paradigms and PEP8 coding standards:
- **Encapsulation:** The entire GUI and its logic are encapsulated within the `OpenModelicaRunner` class (inheriting from `QWidget`).
- **Validation Pipeline:** Uses a dedicated `validate_inputs()` method to strictly enforce the mathematical constraint (`0 <= start time < stop time < 5`) before attempting execution.
- **Subprocess Integration:** Utilizes Python's `subprocess` module to inject the `-override` flag dynamically into the compiled model, as per OpenModelica simulation flags documentation.

## 🛠️ Prerequisites
- **Python:** 3.6+
- **OS:** Windows 10/11 or Linux
- **Library:** PyQt6
- **Model:** A compiled OpenModelica executable (e.g., `TwoConnectedTanks.exe`) and its dependencies.

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <YOUR-GITHUB-REPO-URL>
   cd <YOUR-REPO-FOLDER># FOSSEE-GUI-Runner
