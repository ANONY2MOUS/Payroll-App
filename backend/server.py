from fastapi import FastAPI
from reportlab.pdfgen import canvas

app = FastAPI()

employees = []

@app.get("/")
def home():
    return {"message": "Payroll app running"}

@app.post("/add_employee")
def add_employee(name: str, salary: float):
    employees.append({
        "name": name,
        "salary": salary
    })
    return {"message": "Employee added"}

@app.get("/run_payroll")
def run_payroll():
    results = []

    for emp in employees:
        base = emp["salary"]
        per_day = base / 30
        earned = per_day * 26

        overtime = 5 * (per_day / 8)

        gross = earned + overtime
        pf = gross * 0.12
        esi = gross * 0.0075
        net = gross - pf - esi

        data = {
            "name": emp["name"],
            "net": round(net, 2)
        }

        generate_payslip(emp["name"], net)

        results.append(data)

    return results


def generate_payslip(name, net):
    file = f"{name}.pdf"
    c = canvas.Canvas(file)

    c.drawString(100, 750, f"Payslip: {name}")
    c.drawString(100, 700, f"Net Salary: {net}")

    c.save()
