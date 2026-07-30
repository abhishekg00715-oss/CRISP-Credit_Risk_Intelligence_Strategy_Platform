# 1. Purpose

The Business Rules Catalogue documents the business decision rules currently implemented by the CRISP(Credit Risk Intelligence & Strategy Platform). These rules are intended for demonstration purposes and provide transparency into how customer assessments are derived during the MVP phases.
The rules are not institution-specific underwriting policies and should be regarded as configurable reference implementations.

# 2. Business Rules Overview 

|Rule ID|	Rule Name|	Description	|Current Threshold|	Source|	Phase | Used by | Current Implementation pattern |
|--------|-------|----------------|-----------|-------|------|-------|-------------|
|BR-001	|Credit Score Classification|	Categorizes customer creditworthiness using bureau score.|	≥750 Excellent, 700–749 Good, 650–699 Fair, <650 Poor|	Demonstration Rule	|Phase 2|Customer Agent| Hard coded Python|
|BR-02 |Credit Utilization Assessment|Categorizes the customer's credit limit utilization|<30% Low, 30–50% Moderate, >50% High| Demonstration Rule	|Phase 2|Customer Agent| Hard coded Python|
|BR-03 |DTI Assessment|Categorizes Customer's Debt to Income ratio |<20% Low, 20–35% Moderate, >35% High| Demonstration Rule	|Phase 2|Customer Agent| Hard coded Python|
|BR-04 |Payment History |Categorizes Customer's Payment history into different levels |0 late payments = Excellent, 1–2 = Moderate, >2 = Poor| Demonstration Rule	|Phase 2|Customer Agent| Hard coded Python|
|BR-05 |Fraud Flag |Categorizes Customer potential to lead into Fraud |Fraud = High Risk, No Fraud = Clear| Demonstration Rule	|Phase 2|Customer Agent| Hard coded Python|
|BR-06 |Overall Customer Risk Assessment |This provides an overall rating to the customer profile | a)If Fraud Indicator = High Risk, Overall Rating= High Risk b)If Credit Score = Poor,Overall Rating= High Risk  c) Two or more High/ Poor assessments ,Overall Rating= High Risk  d) One High/ Poor or two Moderate assessments Moderate Risk,Overall Rating= Moderate Risk  e) Otherwise ,Overall Rating = Low Risk | Demonstration Rule	|Phase 2|Customer Agent| Hard coded Python|


# Assumptions

- Assessment thresholds are illustrative and not based on a specific bank's credit policy.
- Customer data is synthetically generated for demonstration purposes.

# Future Enhancements

In Future Rollouts there are posssibilities to include a capability for users to update the Business Rules without changing the code.
