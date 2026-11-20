from pathlib import Path

def test_employee_handbook_exists():
    path = Path("data/employee_handbook.txt")
    assert path.exists(), "Employee handbook is missing"

def test_annual_leave_policy():
    text = Path("data/employee_handbook.txt").read_text(encoding="utf-8-sig")
    assert "25 days" in text
    assert "5 unused days" in text

def test_remote_work_policy():
    text = Path("data/employee_handbook.txt").read_text(encoding="utf-8-sig")
    assert "3 days per week" in text

def test_expense_policy():
    text = Path("data/employee_handbook.txt").read_text(encoding="utf-8-sig")
    assert "GBP 500" in text
