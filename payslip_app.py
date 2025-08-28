# Filename: payslip_app.py
import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="Payslip Generator", page_icon="💰")
st.title("💼 Payslip Generator")

# Payslip Form
with st.form("payslip_form"):
    st.subheader("Employee Details")
    name = st.text_input("Employee Name")
    emp_id = st.text_input("Employee ID")
    designation = st.text_input("Designation")
    
    st.subheader("Salary Components")
    basic = st.number_input("Basic Pay", value=0)
    house_rent = st.number_input("House Rent Allowance", value=0)
    medical = st.number_input("Medical Allowance", value=0)
    conveyance = st.number_input("Conveyance Allowance", value=0)
    bonus = st.number_input("Festival Bonus", value=0)
    
    st.subheader("Deductions")
    tax = st.number_input("Tax Deduction", value=0)
    loan = st.number_input("Loan Deduction", value=0)
    
    submitted = st.form_submit_button("Generate Payslip")

# Function to generate PDF
def create_payslip_pdf(name, emp_id, designation, basic, house_rent, medical, conveyance, bonus, tax, loan):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "Payslip", ln=True, align="C")
    
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    
    # Employee Info
    pdf.cell(0, 8, f"Name: {name}", ln=True)
    pdf.cell(0, 8, f"Employee ID: {emp_id}", ln=True)
    pdf.cell(0, 8, f"Designation: {designation}", ln=True)
    
    pdf.ln(10)
    
    # Earnings
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Earnings", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Basic Pay: BDT {basic:,.2f}", ln=True)
    pdf.cell(0, 8, f"House Rent: BDT {house_rent:,.2f}", ln=True)
    pdf.cell(0, 8, f"Medical Allowance: BDT {medical:,.2f}", ln=True)
    pdf.cell(0, 8, f"Conveyance Allowance: BDT {conveyance:,.2f}", ln=True)
    pdf.cell(0, 8, f"Festival Bonus: BDT {bonus:,.2f}", ln=True)
    
    pdf.ln(5)
    
    # Deductions
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Deductions", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Tax: BDT {tax:,.2f}", ln=True)
    pdf.cell(0, 8, f"Loan: BDT {loan:,.2f}", ln=True)
    
    pdf.ln(10)
    
    # Net Salary
    net_salary = basic + house_rent + medical + conveyance + bonus - tax - loan
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Net Salary: BDT {net_salary:,.2f}", ln=True)
    
    # Save PDF
    filename = f"{emp_id}_payslip.pdf"
    pdf.output(filename)
    return filename

# Generate PDF if submitted
if submitted:
    if name and emp_id:
        filename = create_payslip_pdf(
            name, emp_id, designation, basic, house_rent, medical, conveyance, bonus, tax, loan
        )
        st.success("Payslip generated successfully! 🎉")
        
        # Download button
        with open(filename, "rb") as f:
            st.download_button("💾 Download Payslip PDF", f, file_name=filename)
    else:
        st.error("Please enter at least Employee Name and ID.")
