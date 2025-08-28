import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

SAVE_FOLDER = "Payslips"
os.makedirs(SAVE_FOLDER, exist_ok=True)

st.title("💼 Payslip Generator (Template Style)")

# Employee Input
employeeName = st.text_input("Employee Name")
pin = st.text_input("PIN")
designation = st.text_input("Designation")
joiningDate = st.date_input("Joining Date")
salary = st.number_input("Basic Salary", value=0)
allowance = st.number_input("Allowance", value=0)
transport = st.number_input("Transport Deduction", value=0)
tax = st.number_input("Tax Deduction", value=0)
otherDeductions = st.number_input("Other Deductions", value=0)
payslipMonth = st.text_input("Payslip Month (e.g., August 2025)")

if st.button("Generate Payslip"):
    if not all([employeeName, pin, designation, payslipMonth]):
        st.error("Please fill all required fields")
    else:
        # Salary calculations
        basic_comp = round(0.5 * salary)
        house_rent = round(0.3 * salary)
        medical = round(0.1 * salary)
        conveyance = round(0.1 * salary)
        totalDeductions = transport + tax + otherDeductions
        netSalary = salary + allowance - totalDeductions

        # Create PDF
        pdf = FPDF('P', 'mm', 'A4')
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Header
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Company Name", ln=True, align="C")
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Payslip for {payslipMonth}", ln=True, align="C")
        pdf.ln(5)

        # Employee Info Table
        pdf.set_font("Arial", "", 12)
        pdf.cell(50, 8, "Employee Name:", border=0)
        pdf.cell(0, 8, employeeName, ln=True)
        pdf.cell(50, 8, "PIN:", border=0)
        pdf.cell(0, 8, pin, ln=True)
        pdf.cell(50, 8, "Designation:", border=0)
        pdf.cell(0, 8, designation, ln=True)
        pdf.cell(50, 8, "Joining Date:", border=0)
        pdf.cell(0, 8, str(joiningDate), ln=True)
        pdf.ln(5)

        # Earnings Table
        pdf.set_font("Arial", "B", 12)
        pdf.cell(95, 8, "Earnings", border=1, align="C")
        pdf.cell(95, 8, "Amount (BDT)", border=1, ln=True, align="C")

        pdf.set_font("Arial", "", 12)
        earnings = {
            "Basic": basic_comp,
            "House Rent": house_rent,
            "Medical": medical,
            "Conveyance": conveyance,
            "Allowance": allowance
        }
        for key, val in earnings.items():
            pdf.cell(95, 8, key, border=1)
            pdf.cell(95, 8, f"{val:,.2f}", border=1, ln=True)

        pdf.ln(5)

        # Deductions Table
        pdf.set_font("Arial", "B", 12)
        pdf.cell(95, 8, "Deductions", border=1, align="C")
        pdf.cell(95, 8, "Amount (BDT)", border=1, ln=True, align="C")

        pdf.set_font("Arial", "", 12)
        deductions = {
            "Transport": transport,
            "Tax": tax,
            "Other": otherDeductions,
            "Total Deductions": totalDeductions
        }
        for key, val in deductions.items():
            pdf.cell(95, 8, key, border=1)
            pdf.cell(95, 8, f"{val:,.2f}", border=1, ln=True)

        pdf.ln(10)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Net Salary: BDT {netSalary:,.2f}", ln=True, align="C")

        # Save PDF
        filename_pdf = os.path.join(SAVE_FOLDER, f"Payslip_{employeeName}_{payslipMonth}.pdf")
        pdf.output(filename_pdf)

        st.success("Payslip generated successfully! 🎉")
        with open(filename_pdf, "rb") as f:
            st.download_button("💾 Download Payslip PDF", f, file_name=os.path.basename(filename_pdf))
