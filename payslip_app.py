import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os

# Folder to save payslips
SAVE_FOLDER = "Payslips"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Streamlit UI
st.title("💼 Payslip Generator")

with st.form("payslip_form"):
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
    
    submitted = st.form_submit_button("Generate Payslip")

# Generate Payslip
if submitted:
    # Salary components
    basic = round(0.5 * salary)
    houseRent = round(0.3 * salary)
    medical = round(0.1 * salary)
    conveyance = round(0.1 * salary)
    
    # Total deductions
    totalDeductions = transport + tax + otherDeductions
    
    # Net salary
    netSalary = salary + allowance - totalDeductions

    # Log data to CSV
    df = pd.DataFrame([{
        "Timestamp": datetime.now(),
        "Employee Name": employeeName,
        "PIN": pin,
        "Designation": designation,
        "Joining Date": joiningDate,
        "Salary": salary,
        "Allowance": allowance,
        "Transport": transport,
        "Tax": tax,
        "Other Deductions": otherDeductions,
        "Total Deductions": totalDeductions,
        "Net Salary": netSalary,
        "Basic": basic,
        "House Rent": houseRent,
        "Medical": medical,
        "Conveyance": conveyance,
        "Payslip Month": payslipMonth
    }])
    
    log_file = "payslip_log.csv"
    if os.path.exists(log_file):
        df.to_csv(log_file, mode='a', header=False, index=False)
    else:
        df.to_csv(log_file, index=False)
    
    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Payslip", ln=True, align="C")
    
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.cell(0, 8, f"Employee Name: {employeeName}", ln=True)
    pdf.cell(0, 8, f"PIN: {pin}", ln=True)
    pdf.cell(0, 8, f"Designation: {designation}", ln=True)
    pdf.cell(0, 8, f"Joining Date: {joiningDate}", ln=True)
    pdf.cell(0, 8, f"Payslip Month: {payslipMonth}", ln=True)
    
    pdf.ln(5)
    pdf.cell(0, 8, f"Basic: BDT {basic:,.2f}", ln=True)
    pdf.cell(0, 8, f"House Rent: BDT {houseRent:,.2f}", ln=True)
    pdf.cell(0, 8, f"Medical: BDT {medical:,.2f}", ln=True)
    pdf.cell(0, 8, f"Conveyance: BDT {conveyance:,.2f}", ln=True)
    pdf.cell(0, 8, f"Allowance: BDT {allowance:,.2f}", ln=True)
    
    pdf.ln(5)
    pdf.cell(0, 8, f"Transport Deduction: BDT {transport:,.2f}", ln=True)
    pdf.cell(0, 8, f"Tax Deduction: BDT {tax:,.2f}", ln=True)
    pdf.cell(0, 8, f"Other Deductions: BDT {otherDeductions:,.2f}", ln=True)
    pdf.cell(0, 8, f"Total Deductions: BDT {totalDeductions:,.2f}", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Net Salary: BDT {netSalary:,.2f}", ln=True)
    
    # Save PDF
    pdf_file = os.path.join(SAVE_FOLDER, f"Payslip_{employeeName}_{payslipMonth}.pdf")
    pdf.output(pdf_file)
    
    st.success("Payslip generated successfully! 🎉")
    with open(pdf_file, "rb") as f:
        st.download_button("💾 Download Payslip PDF", f, file_name=os.path.basename(pdf_file))
