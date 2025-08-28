import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

# Folder to save generated payslips
SAVE_FOLDER = "Payslips"
os.makedirs(SAVE_FOLDER, exist_ok=True)

st.title("💼 Payslip Generator (PDF Template)")

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
        pdf.set_font("Arial", "B", 18)
        pdf.cell(0, 10, "Payslip", ln=True, align="C")

        pdf.set_font("Arial", "", 12)
        pdf.ln(10)

        # Employee Info
        pdf.cell(0, 8, f"Employee Name: {employeeName}", ln=True)
        pdf.cell(0, 8, f"PIN: {pin}", ln=True)
        pdf.cell(0, 8, f"Designation: {designation}", ln=True)
        pdf.cell(0, 8, f"Joining Date: {joiningDate}", ln=True)
        pdf.cell(0, 8, f"Payslip Month: {payslipMonth}", ln=True)

        pdf.ln(5)

        # Earnings
        pdf.cell(0, 8, f"Basic: BDT {basic_comp:,.2f}", ln=True)
        pdf.cell(0, 8, f"House Rent: BDT {house_rent:,.2f}", ln=True)
        pdf.cell(0, 8, f"Medical: BDT {medical:,.2f}", ln=True)
        pdf.cell(0, 8, f"Conveyance: BDT {conveyance:,.2f}", ln=True)
        pdf.cell(0, 8, f"Allowance: BDT {allowance:,.2f}", ln=True)

        pdf.ln(5)

        # Deductions
        pdf.cell(0, 8, f"Transport Deduction: BDT {transport:,.2f}", ln=True)
        pdf.cell(0, 8, f"Tax Deduction: BDT {tax:,.2f}", ln=True)
        pdf.cell(0, 8, f"Other Deductions: BDT {otherDeductions:,.2f}", ln=True)
        pdf.cell(0, 8, f"Total Deductions: BDT {totalDeductions:,.2f}", ln=True)

        pdf.ln(10)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Net Salary: BDT {netSalary:,.2f}", ln=True)

        # Save PDF
        filename_pdf = os.path.join(SAVE_FOLDER, f"Payslip_{employeeName}_{payslipMonth}.pdf")
        pdf.output(filename_pdf)

        st.success("Payslip generated successfully! 🎉")
        with open(filename_pdf, "rb") as f:
            st.download_button("💾 Download Payslip PDF", f, file_name=os.path.basename(filename_pdf))
