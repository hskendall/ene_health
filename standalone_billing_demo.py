#!/usr/bin/env python3
"""
Standalone Demo for EneHealths Billing and Insurance Reimbursement Agents

This script demonstrates the functionality of the BillingAgent and 
InsuranceReimbursementAgent without any external dependencies.
"""

import json
import datetime
import uuid
from typing import Dict, List, Optional, Tuple, Any


class BillingAgent:
    """
    Agent responsible for handling billing operations for EneHealths mental health services.
    """
    
    def __init__(self):
        """Initialize the BillingAgent with billing configurations."""
        self.cpt_codes = self._load_cpt_codes()
        self.payment_methods = ["credit_card", "debit_card", "insurance", "bank_transfer"]
        self.transactions = []
        self.invoices = []
        
    def _load_cpt_codes(self) -> Dict[str, Dict[str, Any]]:
        """Load default CPT codes for mental health services."""
        return {
            "90791": {
                "description": "Psychiatric diagnostic evaluation",
                "rate": 150.00,
                "duration_minutes": 50
            },
            "90832": {
                "description": "Psychotherapy, 30 minutes",
                "rate": 65.00,
                "duration_minutes": 30
            },
            "90834": {
                "description": "Psychotherapy, 45 minutes",
                "rate": 85.00,
                "duration_minutes": 45
            },
            "90837": {
                "description": "Psychotherapy, 60 minutes",
                "rate": 130.00,
                "duration_minutes": 60
            },
            "90853": {
                "description": "Group psychotherapy",
                "rate": 50.00,
                "duration_minutes": 90
            },
            "96127": {
                "description": "Brief emotional/behavioral assessment",
                "rate": 25.00,
                "duration_minutes": 15
            }
        }
    
    def verify_cpt_code(self, code: str) -> Tuple[bool, Dict[str, Any]]:
        """Verify if a CPT code is valid and return its details."""
        if code in self.cpt_codes:
            return True, self.cpt_codes[code]
        return False, {}
    
    def calculate_service_cost(self, cpt_code: str, units: int = 1, 
                              modifiers: Optional[List[str]] = None) -> Dict[str, Any]:
        """Calculate the cost of a service based on CPT code and modifiers."""
        is_valid, code_details = self.verify_cpt_code(cpt_code)
        
        if not is_valid:
            return {
                "success": False,
                "error": f"Invalid CPT code: {cpt_code}",
                "total_cost": 0.0
            }
        
        base_rate = code_details["rate"]
        total_cost = base_rate * units
        
        # Apply modifiers if any
        if modifiers:
            if "22" in modifiers:  # Increased procedural service
                total_cost *= 1.5
            if "52" in modifiers:  # Reduced service
                total_cost *= 0.5
        
        return {
            "success": True,
            "service": code_details["description"],
            "base_rate": base_rate,
            "units": units,
            "modifiers": modifiers or [],
            "total_cost": total_cost,
            "duration_minutes": code_details["duration_minutes"] * units
        }
    
    def process_payment(self, patient_id: str, amount: float, 
                       payment_method: str, service_details: Dict[str, Any]) -> Dict[str, Any]:
        """Process a payment for services rendered."""
        if payment_method not in self.payment_methods:
            return {
                "success": False,
                "error": f"Invalid payment method: {payment_method}",
                "transaction_id": None
            }
        
        # Generate transaction ID
        transaction_id = f"TXN-{len(self.transactions) + 1}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        transaction = {
            "transaction_id": transaction_id,
            "patient_id": patient_id,
            "amount": amount,
            "payment_method": payment_method,
            "service_details": service_details,
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "completed"
        }
        
        self.transactions.append(transaction)
        
        return {
            "success": True,
            "transaction_id": transaction_id,
            "amount": amount,
            "timestamp": transaction["timestamp"]
        }
    
    def generate_invoice(self, patient_id: str, services: List[Dict[str, Any]], 
                        payment_status: str = "unpaid") -> Dict[str, Any]:
        """Generate an invoice for services provided to a patient."""
        # Calculate total amount
        total_amount = sum(service.get("total_cost", 0) for service in services)
        
        # Generate invoice ID
        invoice_id = f"INV-{len(self.invoices) + 1}-{datetime.datetime.now().strftime('%Y%m%d')}"
        
        invoice = {
            "invoice_id": invoice_id,
            "patient_id": patient_id,
            "services": services,
            "total_amount": total_amount,
            "issue_date": datetime.datetime.now().isoformat(),
            "due_date": (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat(),
            "payment_status": payment_status
        }
        
        self.invoices.append(invoice)
        
        return invoice
    
    def get_patient_billing_history(self, patient_id: str) -> Dict[str, Any]:
        """Retrieve billing history for a specific patient."""
        transactions = [t for t in self.transactions if t["patient_id"] == patient_id]
        invoices = [i for i in self.invoices if i["patient_id"] == patient_id]
        
        return {
            "patient_id": patient_id,
            "transactions": transactions,
            "invoices": invoices,
            "total_paid": sum(t["amount"] for t in transactions),
            "outstanding_balance": sum(i["total_amount"] for i in invoices 
                                     if i["payment_status"] == "unpaid")
        }


class InsuranceReimbursementAgent:
    """
    Agent responsible for handling insurance reimbursement operations for EneHealths.
    """
    
    def __init__(self):
        """Initialize the InsuranceReimbursementAgent with insurance configurations."""
        self.insurance_providers = self._load_insurance_providers()
        self.claims = []
        self.reimbursements = []
        
    def _load_insurance_providers(self) -> Dict[str, Dict[str, Any]]:
        """Load default insurance provider information."""
        return {
            "blue_cross": {
                "name": "Blue Cross Blue Shield",
                "contact": "1-800-123-4567",
                "website": "https://www.bluecross.com",
                "coverage": {
                    "90791": 0.80,  # Coverage percentage for diagnostic evaluation
                    "90832": 0.70,  # Coverage for 30-min therapy
                    "90834": 0.70,  # Coverage for 45-min therapy
                    "90837": 0.70,  # Coverage for 60-min therapy
                    "90853": 0.80,  # Coverage for group therapy
                    "96127": 0.90   # Coverage for assessment
                },
                "requires_preauth": ["90791"]
            },
            "aetna": {
                "name": "Aetna",
                "contact": "1-800-987-6543",
                "website": "https://www.aetna.com",
                "coverage": {
                    "90791": 0.75,
                    "90832": 0.75,
                    "90834": 0.75,
                    "90837": 0.75,
                    "90853": 0.85,
                    "96127": 0.85
                },
                "requires_preauth": ["90791", "90837"]
            },
            "united": {
                "name": "UnitedHealthcare",
                "contact": "1-800-456-7890",
                "website": "https://www.unitedhealthcare.com",
                "coverage": {
                    "90791": 0.70,
                    "90832": 0.70,
                    "90834": 0.70,
                    "90837": 0.70,
                    "90853": 0.80,
                    "96127": 0.80
                },
                "requires_preauth": []
            }
        }
    
    def verify_coverage(self, insurance_id: str, provider_code: str, 
                       cpt_code: str) -> Dict[str, Any]:
        """Verify insurance coverage for a specific service."""
        if provider_code not in self.insurance_providers:
            return {
                "verified": False,
                "error": f"Unknown insurance provider: {provider_code}",
                "coverage_percentage": 0.0
            }
        
        provider = self.insurance_providers[provider_code]
        
        if cpt_code not in provider["coverage"]:
            return {
                "verified": False,
                "error": f"Service not covered: {cpt_code}",
                "coverage_percentage": 0.0
            }
        
        coverage_percentage = provider["coverage"][cpt_code]
        requires_preauth = cpt_code in provider["requires_preauth"]
        
        return {
            "verified": True,
            "insurance_id": insurance_id,
            "provider": provider["name"],
            "cpt_code": cpt_code,
            "coverage_percentage": coverage_percentage,
            "requires_preauthorization": requires_preauth,
            "estimated_patient_responsibility": 1.0 - coverage_percentage
        }
    
    def submit_claim(self, patient_info: Dict[str, Any], provider_info: Dict[str, Any],
                    service_info: Dict[str, Any], insurance_info: Dict[str, Any]) -> Dict[str, Any]:
        """Submit an insurance claim for reimbursement."""
        # Verify coverage first
        coverage = self.verify_coverage(
            insurance_info.get("insurance_id", ""),
            insurance_info.get("provider_code", ""),
            service_info.get("cpt_code", "")
        )
        
        if not coverage["verified"]:
            return {
                "success": False,
                "error": coverage.get("error", "Coverage verification failed"),
                "claim_id": None
            }
        
        # Generate claim ID
        claim_id = f"CLM-{str(uuid.uuid4())[:8]}"
        
        # Create claim record
        claim = {
            "claim_id": claim_id,
            "patient_info": patient_info,
            "provider_info": provider_info,
            "service_info": service_info,
            "insurance_info": insurance_info,
            "coverage_details": coverage,
            "submission_date": datetime.datetime.now().isoformat(),
            "status": "submitted",
            "status_history": [
                {
                    "status": "submitted",
                    "timestamp": datetime.datetime.now().isoformat(),
                    "notes": "Initial claim submission"
                }
            ]
        }
        
        self.claims.append(claim)
        
        return {
            "success": True,
            "claim_id": claim_id,
            "submission_date": claim["submission_date"],
            "status": claim["status"],
            "estimated_reimbursement": service_info.get("total_cost", 0) * coverage["coverage_percentage"]
        }
    
    def check_claim_status(self, claim_id: str) -> Dict[str, Any]:
        """Check the status of a submitted claim."""
        for claim in self.claims:
            if claim["claim_id"] == claim_id:
                return {
                    "success": True,
                    "claim_id": claim_id,
                    "status": claim["status"],
                    "status_history": claim["status_history"],
                    "submission_date": claim["submission_date"]
                }
        
        return {
            "success": False,
            "error": f"Claim not found: {claim_id}"
        }
    
    def update_claim_status(self, claim_id: str, new_status: str, notes: str = "") -> Dict[str, Any]:
        """Update the status of a claim."""
        for claim in self.claims:
            if claim["claim_id"] == claim_id:
                claim["status"] = new_status
                status_update = {
                    "status": new_status,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "notes": notes
                }
                claim["status_history"].append(status_update)
                
                return {
                    "success": True,
                    "claim_id": claim_id,
                    "status": new_status,
                    "updated_at": status_update["timestamp"]
                }
        
        return {
            "success": False,
            "error": f"Claim not found: {claim_id}"
        }
    
    def process_reimbursement(self, claim_id: str, amount: float) -> Dict[str, Any]:
        """Process a reimbursement for an approved claim."""
        # Find the claim
        claim = None
        for c in self.claims:
            if c["claim_id"] == claim_id:
                claim = c
                break
        
        if not claim:
            return {
                "success": False,
                "error": f"Claim not found: {claim_id}"
            }
        
        if claim["status"] not in ["approved", "partially_approved"]:
            return {
                "success": False,
                "error": f"Claim not in approved status: {claim['status']}"
            }
        
        # Generate reimbursement ID
        reimbursement_id = f"REIMB-{str(uuid.uuid4())[:8]}"
        
        # Create reimbursement record
        reimbursement = {
            "reimbursement_id": reimbursement_id,
            "claim_id": claim_id,
            "amount": amount,
            "payment_date": datetime.datetime.now().isoformat(),
            "patient_info": claim["patient_info"],
            "insurance_info": claim["insurance_info"],
            "service_info": claim["service_info"]
        }
        
        self.reimbursements.append(reimbursement)
        
        # Update claim status
        self.update_claim_status(
            claim_id, 
            "reimbursed", 
            f"Reimbursement processed: ${amount:.2f}"
        )
        
        return {
            "success": True,
            "reimbursement_id": reimbursement_id,
            "claim_id": claim_id,
            "amount": amount,
            "payment_date": reimbursement["payment_date"]
        }


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
    
    # Update claim status
    print("\n--- Claim Status Update ---")
    update = insurance_agent.update_claim_status(
        claim_id=claim['claim_id'],
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
        claim_id=claim['claim_id'],
        amount=91.00  # 70% of $130.00
    )
    
    print(f"Reimbursement successful: {reimbursement['success']}")
    print(f"Reimbursement ID: {reimbursement['reimbursement_id']}")
    print(f"Claim ID: {reimbursement['claim_id']}")
    print(f"Amount: ${reimbursement['amount']:.2f}")
    print(f"Payment Date: {reimbursement['payment_date']}")


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