#!/usr/bin/env python3
"""
Demo script for EneHealths Billing and Insurance Reimbursement Agents

This script demonstrates the functionality of the BillingAgent and 
InsuranceReimbursementAgent for EneHealths mental health services.
"""

from src.agents.billing_agent import BillingAgent
from src.agents.insurance_agent import InsuranceReimbursementAgent


def demonstrate_billing_agent():
    """Demonstrate BillingAgent functionality"""
    print("\n=== BILLING AGENT DEMO ===\n")
    
    # Initialize the billing agent
    billing_agent = BillingAgent()
    print("Billing Agent initialized with default CPT codes")
    
    # Verify CPT codes
    print("\n--- CPT Code Verification ---")
    valid_code = "90834"  # 45-minute psychotherapy
    invalid_code = "99999"
    
    is_valid, code_details = billing_agent.verify_cpt_code(valid_code)
    print(f"CPT Code {valid_code} valid: {is_valid}")
    if is_valid:
        print(f"Description: {code_details['description']}")
        print(f"Rate: ${code_details['rate']:.2f}")
        print(f"Duration: {code_details['duration_minutes']} minutes")
    
    is_valid, _ = billing_agent.verify_cpt_code(invalid_code)
    print(f"CPT Code {invalid_code} valid: {is_valid}")
    
    # Calculate service cost
    print("\n--- Service Cost Calculation ---")
    service_cost = billing_agent.calculate_service_cost("90837", units=1)
    print(f"Service: {service_cost['service']}")
    print(f"Base Rate: ${service_cost['base_rate']:.2f}")
    print(f"Units: {service_cost['units']}")
    print(f"Total Cost: ${service_cost['total_cost']:.2f}")
    print(f"Duration: {service_cost['duration_minutes']} minutes")
    
    # Process payment
    print("\n--- Payment Processing ---")
    patient_id = "PT12345"
    payment = billing_agent.process_payment(
        patient_id=patient_id,
        amount=service_cost['total_cost'],
        payment_method="credit_card",
        service_details=service_cost
    )
    
    print(f"Payment successful: {payment['success']}")
    print(f"Transaction ID: {payment['transaction_id']}")
    print(f"Amount: ${payment['amount']:.2f}")
    
    # Generate invoice
    print("\n--- Invoice Generation ---")
    services = [
        billing_agent.calculate_service_cost("90791"),  # Diagnostic evaluation
        billing_agent.calculate_service_cost("90837")   # 60-minute therapy
    ]
    
    invoice = billing_agent.generate_invoice(
        patient_id=patient_id,
        services=services,
        payment_status="unpaid"
    )
    
    print(f"Invoice ID: {invoice['invoice_id']}")
    print(f"Patient ID: {invoice['patient_id']}")
    print(f"Total Amount: ${invoice['total_amount']:.2f}")
    print(f"Issue Date: {invoice['issue_date']}")
    print(f"Due Date: {invoice['due_date']}")
    print(f"Payment Status: {invoice['payment_status']}")
    
    # Get patient billing history
    print("\n--- Patient Billing History ---")
    history = billing_agent.get_patient_billing_history(patient_id)
    print(f"Patient ID: {history['patient_id']}")
    print(f"Total Paid: ${history['total_paid']:.2f}")
    print(f"Outstanding Balance: ${history['outstanding_balance']:.2f}")
    print(f"Number of Transactions: {len(history['transactions'])}")
    print(f"Number of Invoices: {len(history['invoices'])}")


def demonstrate_insurance_agent():
    """Demonstrate InsuranceReimbursementAgent functionality"""
    print("\n=== INSURANCE REIMBURSEMENT AGENT DEMO ===\n")
    
    # Initialize the insurance agent
    insurance_agent = InsuranceReimbursementAgent()
    print("Insurance Reimbursement Agent initialized with default providers")
    
    # Verify coverage
    print("\n--- Insurance Coverage Verification ---")
    insurance_id = "INS98765"
    provider_code = "blue_cross"
    cpt_code = "90837"  # 60-minute therapy
    
    coverage = insurance_agent.verify_coverage(
        insurance_id=insurance_id,
        provider_code=provider_code,
        cpt_code=cpt_code
    )
    
    print(f"Coverage verified: {coverage['verified']}")
    print(f"Provider: {coverage['provider']}")
    print(f"CPT Code: {coverage['cpt_code']}")
    print(f"Coverage Percentage: {coverage['coverage_percentage'] * 100:.1f}%")
    print(f"Requires Preauthorization: {coverage['requires_preauthorization']}")
    print(f"Patient Responsibility: {coverage['estimated_patient_responsibility'] * 100:.1f}%")
    
    # Submit claim
    print("\n--- Claim Submission ---")
    patient_info = {
        "patient_id": "PT12345",
        "name": "Jane Doe",
        "dob": "1985-06-15"
    }
    
    provider_info = {
        "provider_id": "PROV789",
        "name": "Dr. Smith",
        "npi": "1234567890"
    }
    
    service_info = {
        "cpt_code": "90837",
        "service_date": "2023-09-15",
        "diagnosis_code": "F41.1",  # Generalized anxiety disorder
        "total_cost": 130.00
    }
    
    insurance_info = {
        "insurance_id": insurance_id,
        "provider_code": provider_code,
        "group_number": "GRP123456"
    }
    
    claim = insurance_agent.submit_claim(
        patient_info=patient_info,
        provider_info=provider_info,
        service_info=service_info,
        insurance_info=insurance_info
    )
    
    print(f"Claim submission successful: {claim['success']}")
    print(f"Claim ID: {claim['claim_id']}")
    print(f"Submission Date: {claim['submission_date']}")
    print(f"Status: {claim['status']}")
    print(f"Estimated Reimbursement: ${claim['estimated_reimbursement']:.2f}")
    
    # Check claim status
    print("\n--- Claim Status Check ---")
    claim_id = claim['claim_id']
    status = insurance_agent.check_claim_status(claim_id)
    
    print(f"Claim ID: {status['claim_id']}")
    print(f"Status: {status['status']}")
    print(f"Submission Date: {status['submission_date']}")
    
    # Update claim status
    print("\n--- Claim Status Update ---")
    update = insurance_agent.update_claim_status(
        claim_id=claim_id,
        new_status="approved",
        notes="Claim approved by insurance provider"
    )
    
    print(f"Status update successful: {update['success']}")
    print(f"Claim ID: {update['claim_id']}")
    print(f"New Status: {update['status']}")
    print(f"Updated At: {update['updated_at']}")
    
    # Process reimbursement
    print("\n--- Reimbursement Processing ---")
    reimbursement = insurance_agent.process_reimbursement(
        claim_id=claim_id,
        amount=91.00  # 70% of $130.00
    )
    
    print(f"Reimbursement successful: {reimbursement['success']}")
    print(f"Reimbursement ID: {reimbursement['reimbursement_id']}")
    print(f"Claim ID: {reimbursement['claim_id']}")
    print(f"Amount: ${reimbursement['amount']:.2f}")
    print(f"Payment Date: {reimbursement['payment_date']}")
    
    # Get patient claims
    print("\n--- Patient Claims ---")
    patient_id = "PT12345"
    patient_claims = insurance_agent.get_patient_claims(patient_id)
    
    print(f"Patient ID: {patient_claims['patient_id']}")
    print(f"Claims Count: {patient_claims['claims_count']}")


def demonstrate_integrated_workflow():
    """Demonstrate an integrated workflow between billing and insurance agents"""
    print("\n=== INTEGRATED WORKFLOW DEMO ===\n")
    
    # Initialize agents
    billing_agent = BillingAgent()
    insurance_agent = InsuranceReimbursementAgent()
    
    # Patient and service information
    patient_id = "PT54321"
    patient_name = "John Smith"
    insurance_id = "INS12345"
    provider_code = "aetna"
    cpt_code = "90834"  # 45-minute therapy
    
    # Step 1: Calculate service cost
    print("Step 1: Calculate service cost")
    service_cost = billing_agent.calculate_service_cost(cpt_code)
    print(f"Service: {service_cost['service']}")
    print(f"Total Cost: ${service_cost['total_cost']:.2f}")
    
    # Step 2: Verify insurance coverage
    print("\nStep 2: Verify insurance coverage")
    coverage = insurance_agent.verify_coverage(
        insurance_id=insurance_id,
        provider_code=provider_code,
        cpt_code=cpt_code
    )
    
    coverage_percentage = coverage['coverage_percentage']
    patient_responsibility = coverage['estimated_patient_responsibility']
    
    print(f"Coverage: {coverage_percentage * 100:.1f}%")
    print(f"Patient Responsibility: {patient_responsibility * 100:.1f}%")
    
    # Step 3: Calculate patient portion and insurance portion
    print("\nStep 3: Calculate payment portions")
    total_cost = service_cost['total_cost']
    insurance_portion = total_cost * coverage_percentage
    patient_portion = total_cost * patient_responsibility
    
    print(f"Total Cost: ${total_cost:.2f}")
    print(f"Insurance Portion: ${insurance_portion:.2f}")
    print(f"Patient Portion: ${patient_portion:.2f}")
    
    # Step 4: Process patient payment
    print("\nStep 4: Process patient payment")
    payment = billing_agent.process_payment(
        patient_id=patient_id,
        amount=patient_portion,
        payment_method="credit_card",
        service_details=service_cost
    )
    
    print(f"Patient Payment: ${payment['amount']:.2f}")
    print(f"Transaction ID: {payment['transaction_id']}")
    
    # Step 5: Submit insurance claim
    print("\nStep 5: Submit insurance claim")
    patient_info = {
        "patient_id": patient_id,
        "name": patient_name,
        "dob": "1980-03-20"
    }
    
    provider_info = {
        "provider_id": "PROV456",
        "name": "Dr. Johnson",
        "npi": "0987654321"
    }
    
    service_info = {
        "cpt_code": cpt_code,
        "service_date": "2023-09-20",
        "diagnosis_code": "F32.1",  # Major depressive disorder
        "total_cost": total_cost
    }
    
    insurance_info = {
        "insurance_id": insurance_id,
        "provider_code": provider_code,
        "group_number": "GRP654321"
    }
    
    claim = insurance_agent.submit_claim(
        patient_info=patient_info,
        provider_info=provider_info,
        service_info=service_info,
        insurance_info=insurance_info
    )
    
    print(f"Claim ID: {claim['claim_id']}")
    print(f"Estimated Reimbursement: ${claim['estimated_reimbursement']:.2f}")
    
    # Step 6: Update claim status (simulating insurance processing)
    print("\nStep 6: Update claim status (insurance processing)")
    insurance_agent.update_claim_status(
        claim_id=claim['claim_id'],
        new_status="approved",
        notes="Claim approved by insurance provider"
    )
    
    # Step 7: Process reimbursement
    print("\nStep 7: Process reimbursement")
    reimbursement = insurance_agent.process_reimbursement(
        claim_id=claim['claim_id'],
        amount=insurance_portion
    )
    
    print(f"Reimbursement ID: {reimbursement['reimbursement_id']}")
    print(f"Reimbursement Amount: ${reimbursement['amount']:.2f}")
    
    # Step 8: Generate invoice for record-keeping
    print("\nStep 8: Generate invoice for record-keeping")
    invoice = billing_agent.generate_invoice(
        patient_id=patient_id,
        services=[service_cost],
        payment_status="paid"
    )
    
    print(f"Invoice ID: {invoice['invoice_id']}")
    print(f"Total Amount: ${invoice['total_amount']:.2f}")
    print(f"Payment Status: {invoice['payment_status']}")
    
    print("\n=== WORKFLOW COMPLETE ===")


if __name__ == "__main__":
    print("EneHealths Billing and Insurance Reimbursement Agents Demo")
    print("=" * 60)
    
    demonstrate_billing_agent()
    demonstrate_insurance_agent()
    demonstrate_integrated_workflow()
    
    print("\nDemo completed successfully!")