"""
Configuration Module
Handles application configuration and constants
"""

from datetime import datetime, timedelta


# Default prompt configurations
DEFAULT_PROMPTS = {
    'categorization': """Analyze the email content and categorize it into exactly one of the following: Important, Newsletter, Spam, To-Do, Project. 
"To-Do" emails must include a direct request requiring user action. 
"Important" is for high-stakes communication from leadership or clients.
Return ONLY the category name.""",
    
    'actionExtraction': """Extract actionable tasks from the email. 
Return a JSON object with a key "tasks" containing an array of objects. 
Each object must have: "task" (string description), "deadline" (string or null), and "priority" (High/Medium/Low).
If no tasks, return an empty array.""",
    
    'autoReply': """Draft a polite, professional reply based on the sender's tone. 
If it is a meeting request, ask for an agenda if missing. 
If it is a task assignment, acknowledge receipt and estimated completion time.
Keep it concise.""",
    
    'customAnalyzers': []
}


# Mock inbox data
def get_mock_inbox():
    """Generate mock inbox with relative timestamps"""
    return [
        {
            'id': '1',
            'sender': 'sarah.manager@company.com',
            'subject': 'Urgent: Q3 Report Review',
            'timestamp': (datetime.now() - timedelta(hours=3)).isoformat(),
            'body': 'Hi Team, I need everyone to review the attached Q3 financial report by EOD tomorrow. It is crucial for the board meeting on Monday. Please highlight any discrepancies.',
            'isRead': False,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': '2',
            'sender': 'legal.team@enterprise-corp.com',
            'subject': 'URGENT: Data Breach Incident Response - Action Required Within 24 Hours',
            'timestamp': (datetime.now() - timedelta(hours=5)).isoformat(),
            'body': '''CONFIDENTIAL - ATTORNEY-CLIENT PRIVILEGE

Dear Security and Compliance Team,

This is an urgent notification regarding a potential data breach incident that was detected at 3:47 AM EST today. Our security monitoring systems identified unauthorized access attempts to our customer database containing approximately 2.3 million records.

IMMEDIATE ACTIONS REQUIRED:

1. INCIDENT RESPONSE TEAM ACTIVATION (By 2 PM Today):
   - Convene emergency meeting with: CISO, Legal, PR, Engineering leads
   - Conference bridge: +1-555-0199, Code: 847293
   - Location: War Room B, 3rd Floor

2. FORENSIC INVESTIGATION (Complete by EOD):
   - Preserve all server logs from November 20-23
   - Engage third-party forensics firm (contact: forensics@cyberresponse.com)
   - DO NOT modify any affected systems
   - Document chain of custody for all evidence

3. REGULATORY COMPLIANCE (48 Hour Window):
   - Prepare breach notification letters per GDPR Article 33
   - Contact list: EU Data Protection Authority, California AG Office
   - Estimated affected users: 847,392 EU residents, 1,453,201 US residents
   - Customer notification emails must be drafted and approved by legal

4. TECHNICAL REMEDIATION:
   - Patch vulnerability in authentication service (CVE-2025-18473)
   - Reset all API keys and OAuth tokens
   - Enable additional MFA requirements
   - Contact: security@company.com for remediation scripts

5. STAKEHOLDER COMMUNICATION:
   - Board notification: Draft presentation by 5 PM today
   - Investor relations: Hold statement until legal review complete
   - Customer support: Prepare FAQ document and train support staff

CRITICAL TIMELINE:
- T+0 (Now): Containment phase
- T+4 hours: Impact assessment complete
- T+24 hours: Regulatory notification filed
- T+72 hours: Customer communications sent
- T+7 days: Full incident report to board

LEGAL IMPLICATIONS:
- Potential GDPR fines: €20M or 4% of annual revenue
- Class action lawsuit risk: HIGH
- SEC disclosure requirements apply
- Attorney work product - treat as confidential

Please confirm receipt and attendance at emergency meeting by replying to this email within 1 hour.

Contact 24/7 hotline for questions: +1-555-SECURITY

Regards,
Jennifer Martinez
Chief Legal Officer & General Counsel
Enterprise Corp | Legal Department
Direct: +1-555-0147 | Emergency: +1-555-9999''',
            'isRead': False,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': '3',
            'sender': 'alex.dev@company.com',
            'subject': 'Sync on Project Titan?',
            'timestamp': (datetime.now() - timedelta(days=1, hours=7)).isoformat(),
            'body': "Hey, are you free to sync regarding the API migration? I'm stuck on the authentication flow. Let's meet tomorrow at 2 PM if possible.",
            'isRead': True,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': '4',
            'sender': 'investment.committee@globalventures.capital',
            'subject': 'Series B Term Sheet - Final Review Before Partner Meeting',
            'timestamp': (datetime.now() - timedelta(days=1, hours=10)).isoformat(),
            'body': '''Dear Founding Team,

Following our extensive due diligence process and multiple discussions with your leadership team, our investment committee has prepared the final term sheet for your Series B funding round. This represents a significant milestone, and we're excited about the potential partnership.

INVESTMENT TERMS SUMMARY:

Investment Amount: $45,000,000
Pre-money Valuation: $180,000,000
Post-money Valuation: $225,000,000
Security Type: Series B Preferred Stock
Price per Share: $8.75

INVESTOR RIGHTS & PROVISIONS:

1. Board Composition:
   - Total seats: 7 (Current: 5)
   - Investor seats: 2 (Global Ventures representatives)
   - Founder seats: 3
   - Independent seats: 2
   - Board observer rights for Series A lead

2. Liquidation Preference:
   - 1x non-participating preferred
   - Pro-rata participation rights in future rounds
   - Standard anti-dilution protection (weighted average)

3. Protective Provisions:
   - Approval required for: M&A transactions over $5M, new debt over $10M
   - Change in business direction
   - Amendments to charter or bylaws affecting Series B rights
   - Approval of annual budget and deviations >20%

4. Vesting & Restrictions:
   - Founder shares: 4-year vesting with 1-year cliff (25% accelerated on acquisition)
   - Employee option pool: Increase to 15% post-money (currently 10%)
   - Right of first refusal on secondary sales
   - Co-sale rights for investors

5. Information Rights:
   - Monthly financials within 15 days of month-end
   - Quarterly board meetings with detailed reporting
   - Annual audited statements within 90 days of fiscal year-end
   - Weekly operational metrics dashboard access

6. Milestones & Performance Targets (18-month period):
   - ARR growth: $15M → $45M (3x multiple)
   - Customer acquisition: 500 enterprise clients
   - Net revenue retention: >120%
   - Gross margin improvement: 35% → 55%
   - Achieve EBITDA breakeven by Q4 2026

ADDITIONAL PROVISIONS:

Use of Proceeds (Approved Allocation):
- Product development & engineering: $18M (40%)
- Sales & marketing expansion: $15.75M (35%)
- International market entry (EMEA): $6.75M (15%)
- Working capital & operations: $4.5M (10%)

Investor Participation Rights:
- Pro-rata rights in future financings
- Most favored nation clause
- Standard redemption rights (year 7+)

Closing Conditions:
- Satisfactory completion of final legal due diligence
- Key employee retention agreements signed
- Updated cap table and stockholder consents
- Resolution of outstanding IP assignments
- D&O insurance policy ($15M minimum coverage)

NEXT STEPS & TIMELINE:

Monday, Nov 25: Partner meeting vote (internal)
Tuesday, Nov 26: Term sheet delivery with markup deadline
Friday, Nov 29: Final term sheet agreement
Week of Dec 2: Begin definitive documentation
Week of Dec 9: Legal due diligence complete
December 18: Target closing date

REQUIRED ACTIONS FROM YOUR TEAM:

1. Executive Review (By Wednesday):
   - CEO, CFO, General Counsel review all terms
   - Prepare questions/concerns for Thursday call
   - Engage your corporate counsel for review

2. Financial Documentation (By Friday):
   - Updated 3-year financial projections
   - Detailed cap table with all convertible instruments
   - List of all material contracts and commitments
   - Updated org chart and hiring plan

3. Legal Preparation (Next Week):
   - Engage merger & acquisition counsel
   - Prepare disclosure schedules
   - Review all IP assignments and contractor agreements
   - Employee stock option plan documentation

4. Stakeholder Management:
   - Existing investor consent and pro-rata elections
   - Board approval meeting scheduled
   - Key employee communications plan

CONFIDENTIALITY REMINDER:

This term sheet and all related discussions remain strictly confidential under our NDA dated October 15, 2025. Do not disclose terms to employees, advisors, or third parties without prior written consent. Any leaks could jeopardize the transaction.

CALL SCHEDULED:

We've scheduled a comprehensive review call for Thursday, November 28 at 2:00 PM EST. Please ensure all key decision-makers can attend:
- Zoom link: [redacted]
- Duration: 2 hours
- Agenda: Term-by-term review, Q&A, negotiation discussion

Please confirm your team's attendance and send any preliminary questions by Wednesday EOD.

We're thrilled about the opportunity to partner with you in this next phase of growth. Your vision for transforming the industry aligns perfectly with our investment thesis, and we're committed to being value-added partners beyond just capital.

Best regards,

Michael Chen, CFA
Managing Partner, Enterprise Technology
Global Ventures Capital
mchen@globalventures.capital | Direct: +1-555-0182
225 Sand Hill Road, Menlo Park, CA 94025

CC: Sarah Williams (Investment Principal), David Kumar (Legal Counsel)''',
            'isRead': False,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': '5',
            'sender': 'ceo@company.com',
            'subject': 'Company All-Hands',
            'timestamp': (datetime.now() - timedelta(days=2, hours=14)).isoformat(),
            'body': 'Team, we will have an all-hands meeting next Friday at 10 AM to discuss the annual roadmap. Attendance is mandatory.',
            'isRead': True,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': '6',
            'sender': 'clinical.trials@pharmaresearch.edu',
            'subject': 'Phase III Clinical Trial Results & FDA Submission Timeline - Protocol Amendment Required',
            'timestamp': (datetime.now() - timedelta(hours=2)).isoformat(),
            'body': '''Dear Principal Investigators and Research Coordinators,

I am writing to share the preliminary results from our Phase III clinical trial (Study ID: PRX-2025-847) for the novel Alzheimer's treatment compound, along with critical next steps for our FDA New Drug Application (NDA) submission.

TRIAL RESULTS SUMMARY (Interim Analysis - 18 Months):

Study Design:
- Randomized, double-blind, placebo-controlled multicenter trial
- N = 2,847 patients (1,423 treatment, 1,424 placebo)
- 67 sites across US, Canada, and EU
- Primary endpoint: Change in ADAS-Cog cognitive assessment at 18 months

Primary Efficacy Results:
✓ Treatment group showed 3.2-point improvement vs placebo (p < 0.001)
✓ Statistically significant difference achieved (confidence level: 99.7%)
✓ Effect size: Cohen's d = 0.68 (medium-large effect)
✓ Clinical significance threshold exceeded (>2.5 point difference)

Secondary Endpoints:
✓ Activities of Daily Living (ADL): 18% improvement vs placebo (p = 0.003)
✓ Caregiver Global Impression: 42% rated "much improved" (vs 12% placebo)
✓ Brain imaging (amyloid PET): 31% reduction in plaque burden
✓ Quality of life measures: Significant improvement across all domains

Safety Profile:
- Serious adverse events: 8.3% (treatment) vs 7.9% (placebo) - not significant
- Most common side effects: Mild nausea (12%), headache (8%), fatigue (6%)
- No unexpected safety signals
- Discontinuation rate: 11.2% (comparable to placebo 10.8%)
- Two deaths in treatment arm (deemed unrelated after adjudication)

REGULATORY PATHWAY & FDA SUBMISSION:

Current Status: Breakthrough Therapy Designation (awarded June 2024)
Target NDA Submission: April 2026
Expected FDA Review: Priority Review (6-month timeline)
Potential Approval: Q4 2026

Required Actions for NDA Submission:

1. COMPLETE CLINICAL DATA PACKAGE (Deadline: January 31, 2026):
   
   A. Final Study Report Components:
      - Integrate 24-month follow-up data (additional 6 months needed)
      - Complete statistical analysis with multiple imputation for missing data
      - Subgroup analyses: Age, gender, APOE4 status, disease severity
      - Site-by-site efficacy analysis for consistency
      
   B. Safety Database Lock:
      - All adverse events reported and coded (MedDRA terminology)
      - Serious adverse event narratives (87 cases require detailed write-ups)
      - Laboratory data integration (>125,000 lab values)
      - ECG analysis (potential QT prolongation signal requires review)
      
   C. Regulatory Documents:
      - Module 2.5: Clinical Overview (150+ pages)
      - Module 2.7: Clinical Summary (250+ pages)
      - Module 5: Individual study reports (>2,000 pages)

2. PROTOCOL AMENDMENT - IMMEDIATE ACTION REQUIRED:

   Background: FDA has requested additional data on long-term cognitive benefits

   Amendment Changes:
   - Extend study duration: 18 months → 36 months
   - Add open-label extension phase for all participants
   - Include additional biomarker assessments
   - Enhanced MRI imaging protocol (volumetric analysis)
   
   Implementation Timeline:
   - IRB submissions: All 67 sites by December 15
   - Patient consent updates: Begin December 20
   - First patient in extension phase: January 15, 2026
   
   Site Coordinator Actions Required:
   □ Review protocol amendment document (sent separately)
   □ Schedule IRB submission meetings
   □ Prepare patient communication materials
   □ Update study binders and source documents
   □ Retrain site staff on new procedures (virtual training: Dec 10)

3. MANUFACTURING & CHEMISTRY CONTROLS (CMC):
   
   - Scale-up production validation (3 batches minimum)
   - Stability data through 24 months (ongoing)
   - Impurity profile characterization
   - Container-closure system validation
   - Manufacturing site inspection readiness
   
   Partner: Global BioPharma Manufacturing (contact: cmc@globalbio.com)

4. POST-MARKETING COMMITMENTS:
   
   FDA will likely require:
   - Phase IV pediatric study (under PREA legislation)
   - 5-year post-approval safety study (N = 10,000)
   - Real-world evidence collection via registry
   - Medication guide and REMS program development

FINANCIAL & BUSINESS IMPLICATIONS:

Development Costs (Remaining):
- Extension phase clinical operations: $42M
- FDA submission preparation: $8M
- Manufacturing scale-up: $35M
- Post-approval commitments: $67M
- Total additional investment: $152M

Revenue Projections (Post-Approval):
- Year 1: $280M (US market only)
- Year 3: $1.2B (US + EU)
- Peak sales: $3.8B annually
- Patent protection: Through 2041

Market Analysis:
- Target patient population: 6.2M in US, 15M globally
- Current competitor drugs: Limited efficacy, same side effect profile
- Pricing strategy: $36,000/year (competitive with existing therapies)
- Reimbursement: Medicare coverage expected, private insurance TBD

UPCOMING MEETINGS & MILESTONES:

Dec 5: FDA Type C Meeting (discuss NDA submission strategy)
Dec 10: Site coordinator training webinar (2-3 PM EST, mandatory)
Dec 15: All IRB submissions due
Jan 8: Data Safety Monitoring Board review
Jan 15: Extension phase enrollment begins
Jan 31: Clinical data package complete
Feb 15: Pre-NDA meeting with FDA
Apr 30: NDA submission target

IMMEDIATE ACTION ITEMS:

FOR PRINCIPAL INVESTIGATORS:
1. Review interim results and safety data (detailed report attached)
2. Approve protocol amendment by Dec 1
3. Attend FDA strategy meeting Dec 5 (travel arrangements sent separately)
4. Sign off on final study report sections (assigned by site)

FOR SITE COORDINATORS:
1. Begin IRB submission preparation immediately
2. Identify patients eligible for extension phase
3. Schedule patient discussion visits
4. Complete protocol amendment training module
5. Update informed consent documents

FOR REGULATORY AFFAIRS TEAM:
1. Draft briefing book for FDA meeting
2. Prepare responses to anticipated FDA questions
3. Coordinate with CMC team on manufacturing sections
4. Begin outlining REMS program structure

FOR DATA MANAGEMENT:
1. Lock 18-month database by December 10
2. Generate final analysis datasets
3. Complete data quality checks
4. Archive all source documents

CONFIDENTIALITY NOTE:

These results remain confidential until official publication. Manuscript submitted to New England Journal of Medicine (under peer review). Embargo until publication - estimated March 2026.

Any disclosure, including at conferences or to colleagues not involved in the study, is prohibited and could jeopardize regulatory approval.

QUESTIONS & SUPPORT:

- Clinical questions: Dr. Amanda Richardson (arichardson@pharmaresearch.edu)
- Regulatory questions: Robert Chen (rchen@regulatory.pharmaresearch.edu)
- Data questions: Statistics team (stats@pharmaresearch.edu)
- Site operations: Julia Martinez (jmartinez@clinops.pharmaresearch.edu)

Emergency hotline (24/7): +1-555-TRIAL1

Thank you for your continued dedication to this groundbreaking research. We are on the cusp of delivering a transformative therapy to millions of patients suffering from Alzheimer's disease.

Sincerely,

Dr. Elizabeth Morgan, MD, PhD
Chief Medical Officer & Study Chair
Department of Neurology | Pharma Research Institute
elizabeth.morgan@pharmaresearch.edu | Office: +1-555-0198

Attachments (12):
- Interim_Results_Statistical_Report.pdf (247 pages)
- Safety_Analysis_Tables.xlsx
- Protocol_Amendment_v4.0_Redline.pdf
- FDA_Meeting_Briefing_Book_Draft.pdf
- Site_Coordinator_Training_Materials.pptx''',
            'isRead': False,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': '7',
            'sender': 'procurement@aerospace-defense.mil',
            'subject': 'RFP Response Submission - $2.4B Defense Contract - Final Clarifications Required',
            'timestamp': (datetime.now() - timedelta(hours=8)).isoformat(),
            'body': '''DEPARTMENT OF DEFENSE - PROCUREMENT DIVISION
CONTRACT OPPORTUNITY: FA8625-25-R-6482
CLASSIFICATION: UNCLASSIFIED // FOR OFFICIAL USE ONLY

TO: All Qualified Bidders
FROM: Defense Procurement Office, Aerospace Systems Division
RE: Request for Proposal - Next-Generation Satellite Communication System

Dear Contractor Representatives,

This communication addresses the upcoming RFP submission deadline for the Next-Generation Tactical Satellite Communication System (NG-SATCOM) program. Based on vendor questions received during the pre-proposal conference, we are providing critical clarifications that will impact your technical and cost proposals.

PROGRAM OVERVIEW:

Contract Value: $2.4 Billion (base + options)
Contract Type: Cost-Plus-Fixed-Fee with Award Fee
Period of Performance: 84 months (7 years)
  - Base Period: 36 months (Development & Prototype)
  - Option Period 1: 24 months (Production - 15 units)
  - Option Period 2: 24 months (Production - 25 additional units)

Contract Structure:
- CPFF for development phase: $890M
- Firm Fixed Price for production units: $1,510M
- Award fee pool: 8% of cost ($71.2M available)

TECHNICAL REQUIREMENTS CLARIFICATIONS:

System Performance Specifications (Updated):

1. Communications Payload:
   - Frequency bands: Ka-band (30-40 GHz), EHF (44 GHz)
   - Data rate: Minimum 10 Gbps aggregate throughput
   - Coverage: Global with emphasis on INDOPACOM region
   - Anti-jam capability: 60 dB protection margin
   - COMSEC: NSA Type 1 encryption required
   - Beam steering: Electronic (no mechanical gimbal)
   - Latency: <150ms for tactical communications

2. Spacecraft Bus Requirements:
   - Design life: 15 years on-orbit (10 year warranty)
   - Launch compatibility: Multiple launch vehicles (Falcon Heavy, Atlas V, Vulcan)
   - Radiation tolerance: 100 krad total ionizing dose
   - Propulsion: Electric for orbit maintenance, chemical for emergency maneuvers
   - Power generation: Solar arrays >15kW EOL
   - Pointing accuracy: 0.01 degrees (3-sigma)

3. Ground Segment:
   - 4 primary ground stations (CONUS locations TBD)
   - 2 alternate stations (OCONUS - Europe and Pacific)
   - Network operations center with 24/7 operations capability
   - Cybersecurity: Compliance with NIST 800-53 Rev 5 High baseline
   - Integration with existing DSN infrastructure

4. NEW REQUIREMENT - Resilience & Protection:
   - Maneuver capability to evade kinetic threats
   - Hardening against directed energy weapons
   - Autonomous collision avoidance (conjunction assessment)
   - Redundant command & control pathways
   - Cyber intrusion detection and response system

PROPOSAL SUBMISSION REQUIREMENTS:

Volume I - Technical Proposal (Page limit: 250 pages)

Section A: Technical Approach (100 pages max)
- System architecture and design concept
- Trade studies and rationale for design choices
- Technology readiness assessment (TRL for all critical components)
- Integration and test approach
- Risk management and mitigation strategies

Section B: Management Approach (75 pages max)
- Program management structure and staffing
- Integrated Master Schedule (IMS) with critical path analysis
- Subcontractor management plan
- Facilities and equipment available
- Quality assurance program
- Cybersecurity program plan

Section C: Past Performance (50 pages max)
- 5 most relevant contracts (last 7 years)
- Focus on: satellite development, communications payloads, ground systems
- Customer references with POC information
- Metrics: Cost, schedule, technical performance

Section D: Small Business Participation (25 pages max)
- Small business subcontracting plan (35% goal)
- Veteran-owned small business emphasis
- HUBZone business participation
- Mentor-protégé program involvement

Volume II - Cost Proposal (No page limit)

Section A: Cost/Price Breakdown
- WBS-based cost estimate (Level 4 minimum)
- Labor rates by category with escalation factors
- Materials and subcontractor costs (competitive quotes required if >$1M)
- ODCs: Travel, equipment, facilities
- Fee/profit calculation and rationale

Section B: Basis of Estimate
- Ground rules and assumptions
- Cost estimating methodology
- Risk-adjusted costs (integration with technical risks)
- Historical cost data from similar programs
- Learning curve assumptions for production units

Section C: Supporting Schedules
- Cost phasing by government fiscal year
- Spending plan (monthly through development)
- Funding requirements for government-furnished equipment
- Working capital requirements

Volume III - Contractual Documents
- Completed representations and certifications
- Signed proposal letter
- Cost accounting standards disclosure
- Facility security clearance documentation (FCL required: Top Secret)
- DCAA-approved accounting system documentation

EVALUATION CRITERIA (Weighted):

Technical Approach: 40 points
- Innovation and technical merit (15)
- Risk and feasibility (15)
- Test and integration approach (10)

Management Approach: 25 points
- Program management capability (10)
- Staffing and key personnel (8)
- Schedule realism (7)

Past Performance: 20 points
- Relevance of experience (12)
- Customer satisfaction (8)

Cost/Price: 15 points
- Price reasonableness (8)
- Cost realism (7)

CRITICAL CLARIFICATIONS FROM PRE-PROPOSAL CONFERENCE:

Q1: Government Furnished Equipment (GFE)
A: The following items will be provided as GFE:
   - Encryption devices (KG-250X units) - 8 units
   - Test equipment for EMI/EMC testing (loan basis)
   - Launch services NOT included in GFE (contractor responsible)

Q2: Foreign National Access
A: This program requires ITAR compliance. Foreign nationals from NATO countries may be approved with proper licenses. Pacing items (propulsion, encryption) require US person only access.

Q3: Facility Requirements
A: Contractor must have:
   - Class 10,000 cleanroom (minimum 5,000 sq ft)
   - Thermal vacuum chamber (>4 meter diameter)
   - Anechoic chamber for RF testing
   - SCIF for classified work (Top Secret level)
   Or demonstrate access through partnership/lease

Q4: Key Personnel Requirements (Updated):
   - Program Manager: 15+ years aerospace/defense PM experience, active TS clearance
   - Chief Engineer: PhD in EE/Aerospace, 20+ years satellite development
   - Cybersecurity Lead: CISSP certified, satellite cybersecurity experience
   - All key personnel must be dedicated 100% to program (no other assignments)
   - Resumes required with proposal (does not count against page limit)

Q5: Protests and Debriefs
A: This procurement will use alternative dispute resolution procedures. Debriefs provided only to competitive range offerors. Protests follow FAR 33.1 procedures.

SUBMISSION INSTRUCTIONS:

Electronic Submission Required (no paper copies accepted):
- Portal: https://dibnet.dod.mil (CAC authentication required)
- File format: PDF/A-1b only
- Maximum file size per volume: 50 MB
- Virus scan all files before upload
- Submit at least 24 hours before deadline to allow for technical issues

Submission Deadline: December 15, 2025, 2:00 PM Eastern Standard Time

Late submissions will NOT be considered under any circumstances.

QUESTIONS AND CLARIFICATIONS:

Submit questions via email to: procurement.satcom@aerospace-defense.mil
Subject line: "NG-SATCOM RFP Question - [Your Company Name]"

Question cutoff date: November 30, 2025, 12:00 PM EST
Responses posted: December 5, 2025 (amendment issued)

All questions and answers will be published (anonymized) for all offerors.

PRE-AWARD ACTIVITIES:

Competitive Range: Announced February 1, 2026
Oral Presentations: February 10-20, 2026 (3 days each offeror)
   - Format: Technical deep-dive with live demonstration
   - Location: Pentagon, Arlington, VA
   - Attendees: Max 15 people from contractor
   
Final Proposal Revision: March 1, 2026 (if requested)
Award Decision: April 30, 2026 (estimated)
Contract Start: June 1, 2026

ORGANIZATIONAL CONFLICTS OF INTEREST:

Contractors currently supporting the government in:
- Systems engineering and technical assistance (SETA) roles
- Advisory and assistance services
- Related satellite communications programs

Must submit OCI mitigation plan. Failure to disclose OCIs may result in disqualification.

REQUIRED CERTIFICATIONS:

□ Cybersecurity Maturity Model Certification (CMMC Level 3)
□ ISO 9001:2015 Quality Management System
□ AS9100D Aerospace Quality Management
□ NIST 800-171 compliance (self-attestation)
□ Facility Clearance (Top Secret)
□ Cost Accounting Standards (CAS) disclosure

All certifications must be current and provided with proposal.

IMPORTANT DATES SUMMARY:

Nov 30: Question cutoff
Dec 5: Government responses published
Dec 15: Proposal submission deadline (2 PM EST)
Feb 1: Competitive range announcement
Feb 10-20: Oral presentations
Mar 1: Final proposal revisions due (if requested)
Apr 30: Award decision
Jun 1: Contract start date

POINT OF CONTACT:

Primary: Colonel James Mitchell, USAF
         Program Manager, NG-SATCOM
         Email: james.mitchell@aerospace-defense.mil
         Phone: +1-555-0199 (DSN: 555-0199)

Contracting Officer: Ms. Patricia Anderson
                     Email: patricia.anderson@dla.mil
                     Phone: +1-555-0177

Security: Mr. Robert Chang (FSO)
          Email: security.clearances@aerospace-defense.mil
          Phone: +1-555-0165

FINAL REMINDERS:

1. This is a full and open competition - all qualified contractors encouraged to propose
2. Teaming arrangements permitted and encouraged (prime-sub relationships)
3. Award will be made to offeror providing best value to government
4. Debriefings provided only to offerors in competitive range
5. This program is essential to national security - treat all information accordingly

We look forward to receiving your innovative and competitive proposals.

Very respectfully,

PATRICIA L. ANDERSON, GS-14
Contracting Officer
Defense Procurement Office - Aerospace Systems Division
Department of Defense
patricia.anderson@dla.mil

DISTRIBUTION: All registered bidders (47 companies)
CLASSIFICATION: UNCLASSIFIED // FOR OFFICIAL USE ONLY
CONTROLS: Export Controlled Information - ITAR/EAR Applicable''',
            'isRead': False,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': '8',
            'sender': 'hr@company.com',
            'subject': 'Action Required: Complete Annual Performance Review',
            'timestamp': (datetime.now() - timedelta(hours=12)).isoformat(),
            'body': 'Please complete your self-assessment for the annual performance review by December 1st. The form link is attached. This is mandatory for all employees.',
            'isRead': False,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': '9',
            'sender': 'client@bigcorp.com',
            'subject': 'RE: Project Deadline Extension Request',
            'timestamp': (datetime.now() - timedelta(days=1, hours=3)).isoformat(),
            'body': 'Thank you for the update. We can approve a 1-week extension, but please ensure the deliverables are complete by December 10th. Let us know if you need any resources.',
            'isRead': True,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': '10',
            'sender': 'academic.affairs@university.edu',
            'subject': 'PhD Dissertation Defense - Committee Feedback & Major Revisions Required Before Final Defense',
            'timestamp': (datetime.now() - timedelta(days=1, hours=6)).isoformat(),
            'body': '''Dear Marcus,

Following your preliminary dissertation defense on November 20th, the committee has convened to provide comprehensive feedback on your work titled "Machine Learning Approaches for Early Detection of Neurodegenerative Diseases: A Multi-Modal Neuroimaging Study."

First, congratulations on reaching this significant milestone. Your research demonstrates considerable originality and has clear potential for impact in both clinical neuroscience and computational medicine. However, the committee has identified several substantive issues that must be addressed before we can approve the final defense.

COMMITTEE EVALUATION SUMMARY:

Overall Assessment: Conditional Pass (Major Revisions Required)
Estimated Time to Address: 4-6 months

Chair: Dr. Elizabeth Chen (Neuroscience) - Recommend major revisions
Member: Dr. Robert Martinez (Computer Science) - Recommend major revisions  
Member: Dr. Sarah Johnson (Biostatistics) - Recommend moderate revisions
Member: Dr. James Wong (Clinical Neurology) - Recommend major revisions
External Examiner: Dr. Amanda Richardson (MIT) - Written evaluation attached

MAJOR ISSUES REQUIRING ATTENTION:

1. METHODOLOGICAL CONCERNS (Critical - Must Address):

A. Sample Size and Statistical Power:
   Your current study includes 247 patients (183 with disease, 64 controls). Dr. Johnson's power analysis indicates this is insufficient for the number of features (n=1,847) in your ML models. 

   Required Actions:
   - Perform formal power calculation using G*Power
   - Address the p >> n problem (predictors exceed samples)
   - Consider feature selection/dimensionality reduction (PCA, LASSO)
   - Justify sample size or acknowledge as limitation
   - Alternative: Collaborate with Alzheimer's Disease Neuroimaging Initiative (ADNI) for additional data
   
   Timeline Impact: 2-3 months if using public datasets

B. Cross-Validation Methodology:
   Current approach: 80/20 train-test split with 5-fold CV
   Issue: Data leakage in preprocessing pipeline - feature scaling performed before split
   
   Required Actions:
   - Rerun entire analysis with proper pipeline (preprocessing within CV folds)
   - Implement nested cross-validation for hyperparameter tuning
   - Report performance metrics with confidence intervals
   - Address class imbalance (SMOTE or weighted loss functions)
   
   Chapter 3 must be substantially rewritten with corrected results

C. Multi-Modal Integration:
   You combine MRI, PET, and genomic data but lack theoretical justification for fusion method.
   
   Required Actions:
   - Literature review of fusion approaches (early, late, hybrid)
   - Comparative analysis of different fusion strategies
   - Justify chosen approach with ablation studies
   - New section needed in Chapter 4 (15-20 pages)

2. THEORETICAL FRAMEWORK (Significant Concerns):

A. Literature Review (Chapter 2):
   - Missing key recent papers (2024-2025) in deep learning for neuroimaging
   - Insufficient coverage of interpretability methods (crucial for clinical adoption)
   - Need stronger theoretical foundation for why ML improves over traditional biomarkers
   
   Required Actions:
   - Expand lit review by ~25 pages
   - Add section on explainable AI (XAI) methods
   - Include systematic review table of recent studies
   - References: Update from 127 to estimated 180+ citations

B. Clinical Relevance and Translational Potential:
   Dr. Wong notes that clinical utility is mentioned but not rigorously evaluated.
   
   Required Actions:
   - Add cost-effectiveness analysis section
   - Discuss implementation barriers in clinical settings
   - Compare to current clinical diagnostic criteria
   - Include clinician perspectives (interviews with 3-5 neurologists)
   - New Chapter 6: "Clinical Translation and Implementation" (30-35 pages)

3. RESULTS AND INTERPRETATION:

A. Model Performance Claims:
   Current: "Achieved 94.3% accuracy in predicting conversion to dementia"
   Issue: Accuracy alone is misleading with imbalanced classes
   
   Required Actions:
   - Report comprehensive metrics: sensitivity, specificity, PPV, NPV, AUC-ROC, AUC-PR
   - Confusion matrices for all models
   - Calibration plots and reliability curves
   - Comparison to clinical baselines (not just chance)
   - Statistical significance testing between models (McNemar's test)

B. Feature Importance Analysis:
   Current analysis identifies important features but lacks biological interpretation
   
   Required Actions:
   - Map ML features back to neuroanatomical regions
   - Validate findings against known pathophysiology
   - Use SHAP values or LIME for model interpretability
   - Collaborate with neurologist for clinical interpretation

C. Generalization and External Validation:
   All experiments on single-center data (Stanford Memory Clinic)
   
   Required Actions:
   - Test on external dataset (ADNI, OASIS, or another institution)
   - Discuss generalization limitations extensively
   - Plan for future multi-center validation
   - If external validation not feasible: Major limitation to discuss

4. WRITING AND PRESENTATION:

A. Dissertation Structure:
   Current: 187 pages (excluding appendices)
   Committee consensus: Needs expansion to 250-300 pages to address above issues
   
   Chapter-by-Chapter Recommendations:
   - Chapter 1 (Introduction): Adequate, minor revisions (5 pages)
   - Chapter 2 (Literature Review): Major expansion needed (add 25 pages)
   - Chapter 3 (Methods): Rewrite with corrected methodology (rewrite 30 pages)
   - Chapter 4 (Multi-Modal Fusion): New content needed (add 20 pages)
   - Chapter 5 (Results): Expand with comprehensive metrics (add 15 pages)
   - Chapter 6 (Clinical Translation): NEW CHAPTER REQUIRED (30-35 pages)
   - Chapter 7 (Discussion): Expand limitations and future work (add 10 pages)
   - Chapter 8 (Conclusions): Minor revisions (2 pages)

B. Figures and Tables:
   - Figure quality: Improve resolution of brain imaging figures (Figures 3.2, 4.1, 5.3)
   - Add figures: ROC curves, calibration plots, feature importance plots
   - Table formatting: Inconsistent across chapters - standardize
   - All figures need permission statements if adapted from other sources

C. Writing Quality:
   - Generally good, but technical terminology inconsistently defined
   - Some sections too technical for neuroscience audience, others too simplistic for CS audience
   - Balance needed - dissertation should be accessible to both disciplines
   - Recommended: Professional editing service for final draft

5. ETHICAL AND REGULATORY COMPLIANCE:

A. IRB Approval:
   - Current IRB approval expires January 15, 2026
   - Modification required if adding external datasets
   - Action: Submit IRB modification or renewal by December 1st

B. Data Sharing and Reproducibility:
   - Committee requires code and data availability statement
   - Action: Prepare GitHub repository with cleaned code
   - Action: Anonymize patient data per HIPAA requirements
   - Action: Write detailed README for reproducibility

C. Patient Consent Forms:
   - Verify all participants consented to data use in research publications
   - Action: Audit consent forms with Clinical Research Coordinator

REQUIRED REVISIONS TIMELINE:

December 1-31, 2025:
- Correct cross-validation methodology
- Rerun all analyses with proper pipeline
- Begin literature review expansion

January 1-February 28, 2026:
- Complete multi-modal fusion analysis
- Write new clinical translation chapter
- Comprehensive results tables and figures
- External validation (if feasible)

March 1-31, 2026:
- Finalize all chapters
- Professional editing
- Committee member reviews of specific sections

April 1-15, 2026:
- Submit complete revised dissertation
- Committee review (2 weeks)

May 1, 2026:
- Final defense (if approved)
- Target graduation: May 2026 commencement

MEETING SCHEDULE:

1. Progress Check-In: January 15, 2026
   - Review methodology corrections
   - Discuss external dataset options
   - 1-hour Zoom meeting with full committee

2. Chapter Review: March 1, 2026
   - Submit draft Chapters 3, 4, 6 for preliminary review
   - Individual meetings with committee members

3. Final Draft Review: April 15, 2026
   - Full dissertation due
   - Committee vote on readiness for final defense

FINANCIAL SUPPORT:

Your graduate fellowship has been extended through June 2026 (pending final defense completion). However, this is the final extension available. Failure to defend by June 30, 2026 may impact your funding status.

Teaching assistantship available for Spring 2026 semester if additional support needed:
- Course: Introduction to Computational Neuroscience (NEURO 101)
- Hours: 15 hours/week
- Stipend: Additional $3,500/semester

RESOURCES AND SUPPORT:

1. Statistical Consulting:
   - Dr. Sarah Johnson available for consultation
   - Office hours: Thursdays 2-4 PM (Stats Building, Room 304)
   - Schedule via: stats.consulting@university.edu

2. Writing Center:
   - Graduate writing workshops every Monday
   - One-on-one consultations available
   - Dissertation writing bootcamp: January 15-17 (highly recommended)

3. Computational Resources:
   - HPC cluster access extended through June 2026
   - GPUs available (Tesla V100) - submit request via portal
   - Storage quota increased to 5TB

4. Research Collaboration:
   - Dr. Wong can facilitate access to additional patient data
   - MIT collaboration possible through Dr. Richardson
   - Consider joint lab meeting presentation to get additional feedback

PUBLICATION STRATEGY:

Given the major revisions, recommend focusing solely on dissertation until defense. Post-defense, prioritize publications:

Target Journals:
1. Primary findings: Nature Neuroscience or NeuroImage (high impact)
2. Methodological paper: Medical Image Analysis
3. Clinical translation: JAMA Neurology or Alzheimer's & Dementia

Estimated timeline for publications: 6-12 months post-defense

POSITIVE HIGHLIGHTS FROM YOUR DEFENSE:

Despite the required revisions, the committee wants to emphasize several strengths:

✓ Novel application of attention mechanisms to multi-modal fusion
✓ Impressive programming skills and technical implementation
✓ Clear presentation style and ability to answer questions
✓ Strong foundation in both neuroscience and machine learning
✓ Potential for significant clinical impact

The required revisions are substantial but definitely achievable. Many successful PhD students go through similar revision processes. This is not a reflection of inadequacy but rather the rigor expected for doctoral-level research.

NEXT STEPS:

1. Read this email thoroughly and note all action items
2. Review individual committee member reports (attached separately)
3. Schedule meeting with me (your advisor) within 1 week to discuss strategy
4. Create detailed revision plan with timeline
5. Set up recurring meetings (bi-weekly) to track progress

I am confident you can address these issues successfully. Please don't hesitate to reach out with questions or concerns. Remember, revision is a normal part of the PhD process, and addressing these critiques will ultimately make your research much stronger.

Let's schedule a meeting next week to create a concrete action plan.

Best regards,

Dr. Elizabeth Chen, PhD
Professor of Neuroscience
Director, Computational Neuroscience Lab
PhD Committee Chair
Department of Neuroscience
University Institute
elizabeth.chen@university.edu
Office: +1-555-0189
Office Hours: Tuesdays 1-3 PM, Thursdays 10 AM-12 PM

Attachments:
- Individual_Committee_Reports.pdf (23 pages)
- External_Examiner_Evaluation_DrRichardson.pdf (8 pages)
- Revised_Timeline_Template.xlsx
- Statistical_Power_Analysis_DrJohnardson.pdf
- Recommended_Reading_List.pdf (47 papers)''',
            'isRead': False,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': '11',
            'sender': 'security@company.com',
            'subject': 'Critical: Security Patch Required',
            'timestamp': (datetime.now() - timedelta(hours=4)).isoformat(),
            'body': 'A critical security vulnerability has been identified in our systems. All team members must install the security patch by 5 PM today. Instructions are attached.',
            'isRead': False,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': '12',
            'sender': 'pr.crisis@global-brands.com',
            'subject': 'URGENT: Social Media Crisis Response - Viral Negative Campaign Requires Immediate Action',
            'timestamp': (datetime.now() - timedelta(days=2)).isoformat(),
            'body': '''CONFIDENTIAL - CRISIS MANAGEMENT TEAM ONLY

CRISIS ALERT LEVEL: RED (Highest Priority)
ESTIMATED BRAND DAMAGE: $15-30M in lost revenue
SOCIAL MEDIA REACH: 47M impressions in 18 hours

Dear Crisis Response Team,

This email confirms our emergency call at 6:00 AM this morning regarding the rapidly escalating social media crisis affecting our flagship product line. What began as a single complaint has exploded into a coordinated campaign that threatens significant brand damage.

INCIDENT SUMMARY:

Timeline:
- Nov 21, 11:42 PM: Initial TikTok video posted by @influencer_mom (2.3M followers)
- Nov 22, 8:15 AM: Video goes viral (12M views in 8 hours)
- Nov 22, 3:30 PM: Picked up by major news outlets (CNN, Fox, BBC)
- Nov 22, 6:00 PM: #BoycottGlobalBrands trending #2 on Twitter/X (340K tweets)
- Nov 23, Current: 47M total social media impressions, 89% negative sentiment

Original Complaint:
"HealthyKids Organic Snacks" product line allegedly contains unlisted allergens. Influencer's child had severe allergic reaction (hospitalized). Video shows packaging, medical bracelet, hospital wristband. Extremely emotional, authentic-seeming content.

Current Status:
- Twitter: #BoycottGlobalBrands, #AllergicReaction trending
- TikTok: 847 copycat videos, 34M combined views
- Instagram: 12,000+ stories sharing original video
- Facebook: 2,400 parent groups discussing, planning organized boycott
- Reddit: 47 threads across parenting/consumer advocacy subreddits
- News coverage: CNN, Fox News, BBC, BuzzFeed, Huffington Post

Celebrity Amplification:
- 3 celebrity parents shared with combined 28M followers
- 2 nutritionists posted critical analyses
- 1 pediatrician interviewed on Good Morning America

Stock Impact (as of market open):
- Share price down 7.3% ($890M market cap loss)
- Trading volume 4x normal
- Analyst downgrades expected

PRODUCT INVESTIGATION FINDINGS (Quality Assurance):

Lab Results (expedited overnight testing):
✓ Product samples from same batch: NO undeclared allergens found
✓ Manufacturing records: Proper cleaning procedures followed
✓ Supplier documentation: All ingredients properly declared
✓ Third-party lab confirmation: Product meets all FDA requirements

Conclusion: Product is NOT contaminated. Allergen disclosure is accurate and complete.

Alternative Explanations:
1. Child may have reacted to declared ingredient (not noticed by parent)
2. Cross-contamination from other food consumed that day
3. Unrelated medical condition coincidentally timed
4. Possibility of staged incident (though seems unlikely given hospital visit)

LEGAL ASSESSMENT:

Liability Exposure:
- Product liability claim: LOW risk (lab results exonerate product)
- Defamation risk: MODERATE (public statements must be carefully crafted)
- Securities implications: Shareholders may file if poor crisis response

Regulatory Concerns:
- FDA inquiry initiated: Response due within 5 business days
- State AG offices (CA, NY, TX): Monitoring situation
- FTC advertising compliance review possible

Insurance:
- Product liability insurance: $50M coverage
- Crisis management rider: $5M for PR costs
- D&O coverage: $25M for potential securities claims

RESPONSE STRATEGY (Approved by CEO):

Phase 1: IMMEDIATE (Next 6 hours):

1. Official Statement (Ready for Approval):
   Tone: Empathetic, transparent, science-based
   Key Messages:
   - Express genuine concern for child's health
   - Announce independent lab testing results
   - Reaffirm commitment to safety and transparency
   - Offer to pay medical bills regardless of cause
   - Invite independent third-party testing

2. Social Media Response:
   - Respond to top 100 most-viewed posts with consistent message
   - Activate brand ambassadors (47 influencers under contract)
   - Boosted posts with lab results and safety information
   - NO defensive tone - empathy first, facts second

3. Stakeholder Communications:
   - Investors: Conference call at 2 PM EST today
   - Employees: Company-wide email within 1 hour
   - Retailers: Direct calls to top 20 partners (Walmart, Target, Amazon, etc.)
   - Suppliers: Reassurance that business continues normally

Phase 2: SUSTAINED (Next 72 hours):

4. Media Outreach:
   - Exclusive interview: CEO on Good Morning America (requested for Monday)
   - Press conference: Tuesday 10 AM with Q&A
   - Op-ed placement: Washington Post or NY Times (draft attached)
   - Fact sheet distribution to 500+ journalists

5. Independent Verification:
   - Engage FDA-approved third-party lab (SGS or Eurofins)
   - Invite journalist observation of testing
   - Livestream factory inspection (transparency initiative)
   - Publish results publicly on website

6. Consumer Outreach:
   - Customer service hotline: 24/7 staffing (300 additional agents)
   - Email to 12M registered customers explaining situation
   - Refund offer: No questions asked, full refund + $50 goodwill credit
   - Medical bill coverage: For any customer reporting allergic reaction

Phase 3: RECOVERY (Next 30 days):

7. Brand Rehabilitation Campaign:
   - $10M advertising budget for "Transparency First" campaign
   - Partner with Children's Hospital on allergy awareness initiative
   - Enhanced allergen labeling (beyond FDA requirements)
   - QR codes on packages linking to complete ingredient sourcing

8. Policy Changes:
   - Implement real-time allergen testing in manufacturing
   - Create industry-leading allergen management protocol
   - Quarterly third-party safety audits (publish results publicly)
   - Advisory board of allergists and parents

9. Monitoring & Adjustment:
   - 24/7 social listening with 15-minute reporting
   - Daily sentiment analysis
   - Weekly brand health tracking
   - Monthly sales impact assessment

REQUIRED ACTIONS BY TEAM:

PR Team:
□ Finalize official statement (deadline: 2 hours)
□ Schedule CEO media interviews
□ Coordinate influencer outreach
□ Monitor social media continuously

Legal Team:
□ FDA response preparation
□ Review all public statements
□ Medical bill payment process
□ Investor relations legal review

Executive Team:
□ CEO: Record video message (authentic, empathetic)
□ CFO: Prepare financial impact assessment
□ COO: Factory inspection arrangements
□ Chief Medical Officer: Technical Q&A preparation

Customer Service:
□ Update scripts with approved talking points
□ Train 300 temporary agents (by EOD today)
□ Set up dedicated hotline number
□ Monitor call volume and sentiment

Quality Assurance:
□ Complete expanded product testing
□ Prepare technical documentation for FDA
□ Coordinate third-party lab engagement
□ Review all manufacturing processes

TALKING POINTS (Approved for All Spokespeople):

DO SAY:
✓ "The health and safety of children is our top priority"
✓ "Independent lab testing confirms no undeclared allergens"
✓ "We're paying medical bills to support this family"
✓ "We're inviting transparent third-party verification"
✓ "We're implementing additional safety measures beyond requirements"

DO NOT SAY:
✗ "The claim is false" (defensive)
✗ "The parent made a mistake" (accusatory)
✗ "This is an organized attack" (paranoid)
✗ "Our product is perfectly safe" (absolute claims)
✗ "This is hurting our business" (self-centered)

ESCALATION PROCEDURES:

Level 1 (Current): Crisis management team handles, CEO briefed hourly
Level 2: If trending remains #1 for 24+ hours, Board notification required
Level 3: If stock drops >15%, emergency Board meeting
Level 4: If criminal investigation or FDA recall, activate external crisis firm

WAR ROOM OPERATIONS:

Location: Executive Conference Room (Building A, 12th Floor)
Staffing: 24/7 coverage, 3 eight-hour shifts
Technology: 10 monitors tracking social media, news, stock price
Communication: Dedicated Slack channel (#crisis-response-nov2025)

Team Assignments:
- Social media monitoring: 6 people per shift
- Media relations: 4 people per shift
- Executive support: 2 people per shift
- Legal review: 1 person per shift on-call

BUDGET AUTHORIZATION:

Immediate spend authority (CEO approved):
- Crisis PR firm retainer: $500K
- Additional customer service staffing: $200K
- Advertising campaign acceleration: $2M
- Legal expenses: $300K
- Third-party testing: $100K
- Medical bill payments: $50K initial reserve
- Influencer activation: $400K

Total crisis response budget: $3.55M (with $10M campaign to follow)

METRICS & SUCCESS CRITERIA:

24-Hour Goals:
- Stop trending on Twitter within 24 hours
- Achieve 40% positive/neutral sentiment in news coverage
- Reduce customer service call volume by 50%
- No additional celebrity pile-on

72-Hour Goals:
- Stock price recovery to within 3% of pre-crisis levels
- Major media outlets cover lab results and company response
- Positive earned media placements (at least 5)
- Customer refund requests stabilize

30-Day Goals:
- Net sentiment positive (>55%)
- Sales decline less than 10%
- Brand favorability scores return to baseline
- No regulatory actions or fines

CONFIDENTIALITY REMINDER:

All information in this email and attachments is strictly confidential. Do not discuss outside crisis team. All media inquiries must be directed to PR team. Unauthorized statements could create legal liability.

NEXT STEPS:

1. Crisis team meeting: Every 4 hours until situation stabilizes
2. CEO decision on medical bill offer: Needed within 2 hours
3. Legal approval of statement: Within 1 hour
4. Execute Phase 1 response plan: Begin immediately

Please confirm receipt and your specific action items.

We will get through this with transparency, empathy, and decisive action.

Sarah Mitchell
VP of Communications & Public Relations
Global Brands Corporation
sarah.mitchell@global-brands.com
Mobile: +1-555-0193 (24/7 crisis line)
War Room Direct: +1-555-CRISIS1

CC: Crisis Management Team (23 members)
Attachments: Crisis_Response_Plan.pdf, Lab_Results.pdf, Legal_Analysis.pdf, Social_Listening_Report.pdf, Approved_Talking_Points.pdf, CEO_Video_Script.docx''',
            'isRead': False,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': '13',
            'sender': 'billing@stripe.com',
            'subject': 'Invoice for November 2025',
            'timestamp': (datetime.now() - timedelta(days=3)).isoformat(),
            'body': 'Your invoice for November is ready. Total amount: $249.99. Payment will be automatically processed on December 1st.',
            'isRead': True,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': '14',
            'sender': 'acquisitions@megacorp.com',
            'subject': 'Confidential: Merger & Acquisition Proposal - $850M Offer + Integration Plan',
            'timestamp': (datetime.now() - timedelta(days=1, hours=15)).isoformat(),
            'body': '''ATTORNEY-CLIENT PRIVILEGED - CONFIDENTIAL
DO NOT FORWARD OR DISCUSS OUTSIDE DESIGNATED RECIPIENTS

Dear Board of Directors and Executive Leadership Team,

Following three months of confidential discussions and comprehensive due diligence, MegaCorp Industries is pleased to present a formal acquisition proposal for YourCompany, Inc. This represents a strategic opportunity that we believe will create significant value for shareholders, employees, and customers of both organizations.

TRANSACTION OVERVIEW:

Offer Structure: All-Cash Transaction
Purchase Price: $850,000,000 ($67.50 per share)
Premium: 42% over current stock price ($47.50)
  - 52% over 30-day VWAP
  - 65% over 52-week low
  - 12% above all-time high

Payment Terms:
- 90% cash at closing ($765M)
- 10% earnout based on performance milestones ($85M potential)
- Earnout period: 24 months post-closing
- Earnout triggers: Revenue and EBITDA targets (details attached)

Transaction Type: Merger (stock-for-cash via merger sub)
Closing Timeline: 180 days from definitive agreement
Expected Close: Q2 2026

STRATEGIC RATIONALE:

For YourCompany:
✓ Immediate liquidity event for shareholders (42% premium)
✓ Access to MegaCorp's global distribution (150 countries)
✓ Technology investment ($200M committed over 3 years)
✓ Retain brand identity and operational autonomy (first 2 years)
✓ Career growth opportunities for employees in larger organization

For MegaCorp:
✓ Acquire leading AI technology and 47 patents
✓ Enter high-growth SaaS market segment ($12B TAM, 25% CAGR)
✓ Add 12,500 enterprise customers to cross-sell existing products
✓ Talent acquisition: 850 engineers and data scientists
✓ Geographic expansion into Asia-Pacific markets

Synergy Analysis:
- Revenue synergies: $45M annually by year 3
- Cost synergies: $28M annually (economies of scale, vendor consolidation)
- Total synergy value: $73M annual run-rate
- One-time integration costs: $95M

VALUATION ANALYSIS:

Comparable Public Companies:
- Median EV/Revenue multiple: 8.2x (YourCompany implied value: $738M)
- Median EV/EBITDA multiple: 24.5x (YourCompany implied value: $710M)
- Our offer: 9.4x revenue, 29.3x EBITDA (premium valuation)

Comparable Transactions (Last 24 months):
- 12 SaaS acquisitions in relevant sector
- Median premium: 35% (our offer: 42%)
- Median EV/Revenue: 7.8x (our offer: 9.4x)
- Our offer in 85th percentile of comp set

DCF Analysis:
- Present value of cash flows (10-year projection): $690M
- Terminal value (perpetuity growth 3%): $420M
- Enterprise value: $1,110M
- Net debt adjustment: ($180M)
- Equity value: $930M
- Our offer: $850M (91% of DCF value, conservative)

TRANSACTION TERMS & CONDITIONS:

Purchase Agreement Highlights:

1. Representations & Warranties:
   - Standard business reps (organization, capitalization, financials)
   - Technology & IP reps (ownership, no infringement, etc.)
   - 18-month survival period (24 months for fundamental reps)
   - Liability cap: 25% of purchase price ($212.5M)
   - Deductible ("basket"): $8.5M (1% of purchase price)

2. Material Adverse Effect (MAE) Definition:
   - Customary carve-outs for economic conditions, industry changes
   - Specific definition: >15% revenue decline OR >20% EBITDA decline
   - Measured over consecutive 90-day period
   - Buyer may terminate if MAE occurs pre-closing

3. Covenants:
   - Ordinary course of business operations
   - No extraordinary transactions without buyer consent
   - Monthly financial reporting
   - Cooperation with regulatory filings
   - No shop clause (cannot solicit alternative buyers)

4. Conditions to Closing:
   □ Shareholder approval (majority required)
   □ HSR antitrust clearance (30-day waiting period)
   □ No material adverse effect
   □ Representations and warranties substantially true
   □ Key employee retention agreements signed
   □ Third-party consents obtained (25 major customer contracts)

5. Termination Rights:
   - Either party: If closing doesn't occur within 180 days
   - Buyer: MAE, breach of reps/warranties, failure to obtain approvals
   - Seller: Superior proposal (subject to match right and breakup fee)
   - Reverse breakup fee: $42.5M (5% of deal value)
   - Seller breakup fee: $25.5M (3% of deal value)

EMPLOYEE MATTERS:

Executive Team:
- CEO: 2-year employment agreement, report to MegaCorp COO
  - Base: $850K, Bonus: 100% target ($850K), Equity: $5M RSUs
  - Retention bonus: $3M (50% at 1 year, 50% at 2 years)
  - Change of control: 2x base+bonus if terminated without cause

- CTO: 3-year employment agreement, join MegaCorp technology leadership
  - Base: $650K, Bonus: 80% target ($520K), Equity: $4M RSUs
  - Retention bonus: $2.5M vesting over 3 years
  
- CFO: Transition services (6 months), then severance
  - Severance: 18 months base + bonus + COBRA
  - Equity acceleration: 100% of unvested options/RSUs

- Other C-suite: Individual negotiations ongoing

Key Employees (Retention Critical):
- 47 identified "must keep" employees (engineers, product leaders, sales)
- Retention bonuses: $18M total pool
- Standard: 1.0x-1.5x base salary, paid 50% at close, 50% at 12 months
- Enhanced equity grants in MegaCorp stock
- Guaranteed roles for 18 months (no involuntary terminations)

General Workforce:
- All employees offered roles in combined company
- No layoffs planned for first 12 months (commitment in press release)
- Benefits harmonization: Better of either company's plans
- 401(k) match increase to MegaCorp's 6% (from current 4%)
- PTO: MegaCorp's unlimited policy (from YourCompany's 20 days)

Integration Planning:
- 100-day integration plan (detailed document attached)
- Day 1 readiness: IT systems, email, badges, communications
- Shared services migration: 6-12 months (HR, finance, legal)
- Product roadmap integration: Led by joint committee
- Customer communication strategy: Coordinated rollout

REGULATORY & APPROVAL PROCESS:

Antitrust (HSR):
- Filing required (transaction exceeds $119.5M threshold)
- Pre-merger notification to FTC and DOJ
- 30-day waiting period (likely no second request given market share)
- Combined market share: 12% (well below concern threshold)
- Legal opinion: <5% risk of challenge

Shareholder Approval:
- Requires majority of outstanding shares
- Current ownership: 42% institutional, 38% retail, 20% insider/employees
- Top 10 holders: 37% of shares (initial conversations positive)
- ISS/Glass Lewis likely to recommend "FOR" (substantial premium)
- Proxy materials: 4-6 weeks to prepare and distribute
- Shareholder meeting: 30-45 days after mailing

Third-Party Consents:
- Customer contracts: 25 require consent for change of control
  - Top 10 customers: $47M ARR, preliminary discussions positive
  - Strategy: Emphasize continuity and enhanced capabilities
- Debt agreements: $180M term loan requires consent (bank supportive)
- Real estate leases: 8 office leases require landlord consent (routine)

FINANCING & CLOSING MECHANICS:

Source of Funds:
- MegaCorp cash on hand: $400M
- New term loan (committed): $300M
- Revolving credit facility draw: $150M
- Total sources: $850M (fully committed, no financing contingency)

Debt Financing Terms:
- Term loan: $300M, 5-year maturity, L+275 bps (~7.75% all-in)
- Financial covenants: 3.5x leverage, 3.0x interest coverage
- Use of proceeds: Acquisition only
- Commitment letter attached (signed by 3 banks)

Closing Statement Adjustments:
- Working capital target: $25M (delivered at closing)
- Excess working capital: Dollar-for-dollar increase to purchase price
- Cash/debt-free basis (all cash to seller, all debt remains with seller)
- Transaction expenses: Each party bears own (estimated $15M for seller)

Escrow Arrangements:
- Indemnity escrow: $42.5M (5% of purchase price)
- Released: $21.25M at 12 months, $21.25M at 18 months
- Claims against escrow for breaches of reps/warranties
- Unclaimed escrow released to sellers pro rata

POST-CLOSING INTEGRATION PLAN:

Organizational Structure:
- YourCompany becomes wholly-owned subsidiary
- Initial autonomy: Separate brand, P&L, operations
- Integration phases: Year 1 (standalone), Year 2 (partial), Year 3 (full)
- Reporting: CEO reports to MegaCorp COO (not CEO - maintains focus)

Technology Integration:
- Product roadmaps remain separate for 18 months
- Backend infrastructure migration: 24-month timeline
- API integration: Begin at month 6
- Unified data platform: Month 12-24
- Investment: $200M over 3 years (MegaCorp commitment)

Go-To-Market:
- Sales teams remain separate (avoid disruption)
- Cross-training: Month 6-12
- Joint selling motions: Month 12+
- Comp plans: No changes for 12 months
- Customer segmentation: Enterprise (MegaCorp), Mid-market (YourCompany)

Culture Integration:
- Culture assessment: Pre-close (completed)
- Values alignment: High compatibility (both tech-focused, innovation-driven)
- Change management: Dedicated team, town halls, leadership visibility
- Employee survey: Monthly pulse checks during first year

TIMELINE & NEXT STEPS:

Week 1-2 (Dec 1-15):
□ Board review and approval of proposal
□ CEO/CFO due diligence questions
□ Draft definitive merger agreement
□ Engage financial and legal advisors

Week 3-4 (Dec 16-31):
□ Negotiate definitive agreement
□ Finalize management retention agreements
□ Complete remaining due diligence items
□ Board approval of final terms

Month 2 (January):
□ Execute definitive merger agreement
□ File HSR pre-merger notification
□ Announce transaction (joint press release)
□ Investor presentation and analyst call

Month 3-4 (February-March):
□ Prepare and file proxy statement with SEC
□ Shareholder outreach and education
□ Obtain third-party consents
□ Integration planning (100-day plan)

Month 5 (April):
□ Shareholder meeting and vote
□ HSR clearance obtained
□ Closing conditions satisfied
□ Closing and funding

Month 6+ (May onward):
□ Day 1 integration execution
□ 100-day plan milestones
□ Synergy capture and tracking
□ Cultural integration initiatives

GOVERNANCE & DECISION RIGHTS:

Board Representation Post-Close:
- MegaCorp: 100% ownership, full board control
- Advisory board: 3 YourCompany board members (non-voting, 2-year term)
- Quarterly business reviews with MegaCorp board

Operating Authority:
- Budget approval: <$5M (CEO), >$5M (MegaCorp CFO approval)
- Hiring: <VP level (CEO), VP+ (MegaCorp HR approval)
- Product decisions: CEO authority (first 18 months)
- M&A: Any transaction requires MegaCorp board approval

Financial Reporting:
- Monthly P&L and cash flow reporting to MegaCorp
- Quarterly business review presentations
- Annual budget process (integrated with MegaCorp)
- Real-time dashboard access for key metrics

RISK FACTORS & MITIGATION:

Key Risks:
1. Customer churn during transition (15-20% typical)
   - Mitigation: Early customer communication, service guarantees, executive engagement

2. Employee attrition (25-30% typical in M&A)
   - Mitigation: Retention bonuses, clear career paths, cultural integration plan

3. Integration complexity and cost overruns
   - Mitigation: Dedicated integration team, phased approach, contingency budget

4. Regulatory delay or challenge
   - Mitigation: Pre-filing discussions with FTC, strong antitrust analysis, reverse breakup fee

5. Market conditions deteriorate (economic recession)
   - Mitigation: MAE clause, reverse breakup fee, committed financing

CONFIDENTIALITY & NEXT STEPS:

This proposal and all related discussions are strictly confidential and subject to the non-disclosure agreement executed on August 15, 2025. Do not discuss with anyone outside the board, executive team, and specifically authorized advisors.

Required Actions:
1. Board meeting to review proposal: December 1, 2025
2. Engage investment banker (if not already retained)
3. Engage M&A legal counsel (recommend Wilson Sonsini or Skadden)
4. Provide initial feedback by December 8, 2025
5. Schedule management presentation with MegaCorp board: Week of December 10

We are excited about this transaction and believe it represents a compelling opportunity for your shareholders, employees, and customers. We are committed to a smooth process and successful integration.

Please let us know your initial thoughts and proposed next steps.

Sincerely,

Michael Thompson
Chief Executive Officer
MegaCorp Industries, Inc.
michael.thompson@megacorp.com
Mobile: +1-555-0196 (direct line, confidential)

Jonathan Roberts
Chief Financial Officer & Head of Corporate Development
jonathan.roberts@megacorp.com
Mobile: +1-555-0197

Attachments (15):
- Merger_Agreement_Draft_v1.pdf (147 pages)
- Purchase_Price_Allocation.xlsx
- Synergy_Analysis_Detailed.pdf
- Integration_Plan_100Days.pdf
- Management_Retention_Agreements.pdf
- Financing_Commitment_Letter.pdf
- Regulatory_Analysis_Memo.pdf
- Customer_Transition_Plan.pdf''',
            'isRead': False,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': '15',
            'sender': 'orders@amazon.com',
            'subject': 'Your package will arrive today',
            'timestamp': (datetime.now() - timedelta(hours=6)).isoformat(),
            'body': 'Good news! Your order #123-4567890 will be delivered today between 2 PM - 6 PM. Track your package in real-time.',
            'isRead': False,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': '16',
            'sender': 'promo@spotify.com',
            'subject': 'Your 2024 Wrapped is here!',
            'timestamp': (datetime.now() - timedelta(hours=24)).isoformat(),
            'body': 'Your personalized 2024 Wrapped is ready! Discover your most played songs, artists, and genres. Share your story with friends.',
            'isRead': False,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': '17',
            'sender': 'legal@company.com',
            'subject': 'Updated Terms of Service - Action Required',
            'timestamp': (datetime.now() - timedelta(hours=18)).isoformat(),
            'body': 'We have updated our Terms of Service. Please review and acknowledge the changes by December 5th. Continued use implies acceptance.',
            'isRead': False,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': '18',
            'sender': 'events@techconf.com',
            'subject': 'Reminder: TechConf 2025 Early Bird Ends Tomorrow',
            'timestamp': (datetime.now() - timedelta(hours=9)).isoformat(),
            'body': 'Last chance to save $300 on TechConf 2025 tickets! Early bird pricing ends tomorrow at midnight. Register now to secure your spot.',
            'isRead': False,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': '19',
            'sender': 'devops@company.com',
            'subject': 'Scheduled Maintenance: Dec 1st 2-4 AM',
            'timestamp': (datetime.now() - timedelta(days=2, hours=5)).isoformat(),
            'body': 'Our systems will undergo scheduled maintenance on December 1st from 2 AM to 4 AM EST. All services will be unavailable during this time.',
            'isRead': True,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': '20',
            'sender': 'wins@lottery-spam.com',
            'subject': 'CONGRATULATIONS! You Won $1,000,000!!!',
            'timestamp': (datetime.now() - timedelta(hours=7)).isoformat(),
            'body': 'You have been randomly selected to receive $1,000,000! Click here to claim your prize now! This is not a scam!',
            'isRead': False,
            'category': 'Unprocessed',
            'actionItems': []
        }
    ]


# Gmail mock inbox (simulated connection)
def get_gmail_mock_inbox():
    """Generate Gmail-style mock inbox"""
    return [
        {
            'id': 'g1',
            'sender': 'alert@bank.com',
            'subject': 'Security Alert: New sign-in detected',
            'timestamp': datetime.now().isoformat(),
            'body': 'We detected a new sign-in to your account from a new device. If this was you, you can ignore this email.',
            'isRead': False,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': 'g2',
            'sender': 'recruiter@techjobs.com',
            'subject': 'Interview Request: Senior Frontend Engineer',
            'timestamp': (datetime.now() - timedelta(hours=1)).isoformat(),
            'body': 'Hi, we were impressed by your profile. Are you available for a 30-minute intro call this week? Please let us know your availability.',
            'isRead': True,
            'category': 'Unprocessed',
            'actionItems': []
        },
        {
            'id': 'g3',
            'sender': 'billing@aws.com',
            'subject': 'AWS Invoice Available',
            'timestamp': (datetime.now() - timedelta(days=1)).isoformat(),
            'body': 'Your AWS invoice for the previous month is now available. Total amount: $12.34. Please login to the console to view details.',
            'isRead': False,
            'category': 'Unprocessed',
            'actionItems': []
        }
    ]


# Backwards compatibility
MOCK_INBOX = get_mock_inbox()
GMAIL_MOCK_INBOX = get_gmail_mock_inbox()
