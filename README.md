# Due Date Calculator

A Python package that calculates issue due dates based on working hours in an issue tracking system.

## 📌 Features
- Considers working hours **(9 AM - 5 PM, Monday to Friday)**
- **Skips weekends** (Saturday & Sunday)
- **Supports multi-day calculations**
- **Uses Poetry for dependency management and packaging**

---

## 🚀 Installation & Setup

### **1. Clone the Repository**
```sh
git clone https://github.com/sunnyar/due-date-calculator.git
cd due-date-calculator
```

### **2. Activate Virtual Environment**
```sh
python3 -m venv .venv
source .venv/bin/activate
```

### **3. Install Dependencies**
```sh
pip install poetry
poetry install
```

### **4. Usage**
```sh
poetry run due-date-calc
```
or

```python
from due_date_calculator import DueDateCalculator
import datetime

# Create a calculator instance
calculator = DueDateCalculator()

# Calculate a due date
submit_date = datetime.datetime(2025, 3, 12, 14, 12)  # Wednesday 2:12 PM
turnaround_hours = 16

due_date = calculator.calculate_due_date(submit_date, turnaround_hours)
print(f"Due date: {due_date}")  # Should be Friday 2:12 PM
```

### **5. Running Tests**
To run unit tests, use:

```sh
pytest
```

### **6. Formatting**
```sh
black .
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude .venv
```