# Research Spine — Process Intelligence Prompt Pack v0.1

This is a separate prompt pack from the existing Codex prompt pack.

## Purpose
Package a second research-spine bundle focused on AI-driven process improvement, manufacturing systems, cyber-physical operations, and PES business design.

This pack exists to support one of the five core business wings of PES.
It sits at the overlap between:
- PES business AI ideals
- manufacturing and industrial automation
- process improvement and Lean/Six Sigma style operational thinking
- LOOP as the governed intelligence/control architecture

## Why this pack is separate
The existing research-spine pack is architecture-heavy and LOOP-theory-first.
This pack is different.
It is:
- more commercially grounded
- more manufacturing-specific
- more focused on process intelligence as a PES service line
- more concerned with business models, pilot offers, integration patterns, and real plant-floor applicability

Do not merge this into the original pack.
Treat this as a parallel pack with its own scope and outputs.

## Output standard for every run
Each prompt in this pack should drive output that is useful to LOOP and PES specifically.
Every run should return:
1. a concise domain model
2. a plant-floor / business relevance map
3. implications for PES service design
4. implications for LOOP architecture or research doctrine
5. pilot opportunities or execution candidates
6. key risks, constraints, and false starts to avoid
7. recommended next actions

## Folder map
```plain text
/research_spine_process_intelligence/
  01_process_intelligence_foundations/
  02_ai_process_improvement_methods/
  03_brownfield_manufacturing_data_layer/
  04_operational_digital_twin_lite/
  05_predictive_maintenance_and_reliability/
  06_throughput_quality_energy_convergence/
  07_human_in_the_loop_operations_copilot/
  08_industrial_connectivity_and_integration/
  09_controls_aware_ai_architecture/
  10_pes_service_line_and_business_model/
  11_pilot_design_and_commercial_entry/
  12_governance_safety_and_trust/
```

---

## Prompt 01 — process_intelligence_foundations/
### Objective
Research the modern field of process intelligence for manufacturing and industrial operations.
Focus on:
- how process intelligence differs from generic analytics, dashboards, BI, MES, SCADA, and classic continuous improvement
- how Lean, Six Sigma, DMAIC, OEE, bottleneck analysis, takt time, downtime analysis, and line balancing relate to newer AI-assisted methods
- what the market currently means by process intelligence, operational intelligence, and smart manufacturing intelligence
- where the field is mature vs still hype-driven

### Then
1. define the cleanest operating definition of process intelligence for PES
2. map the domain to Malik’s real background in controls, motion, BAS, HVAC, troubleshooting, and plant support
3. identify where LOOP can act as the research and coordination backbone for this service line
4. identify the most credible non-hype entry points for PES

### Output
- domain definition
- terminology cleanup table
- mature vs hype map
- PES positioning statement
- recommended service-line framing

---

## Prompt 02 — ai_process_improvement_methods/
### Objective
Research how AI and machine learning are being applied to process improvement in manufacturing.
Focus on:
- anomaly detection
- bottleneck discovery
- cycle-time optimization
- throughput improvement
- defect prediction
- scheduling support
- root-cause analysis assistance
- optimization under real-world constraints

Do not stop at abstract use cases.
Compare where these methods actually outperform traditional process-improvement methods and where they fail.

### Then
1. compare classic process improvement vs AI-assisted process improvement
2. identify which use cases fit brownfield industrial environments best
3. identify which use cases are realistic for SMEs vs enterprise-only programs
4. propose a practical AI-assisted DMAIC model PES could use

### Output
- method comparison matrix
- use-case ranking by practicality
- SME vs enterprise fit table
- PES-ready AI-assisted DMAIC model
- recommended first 3 use cases

---

## Prompt 03 — brownfield_manufacturing_data_layer/
### Objective
Research brownfield manufacturing data acquisition and instrumentation strategy for AI/process-improvement use.
Focus on:
- using existing PLCs, drives, HMIs, historians, sensors, BAS, SCADA, and maintenance records
- data quality, timestamp integrity, tag structure, sampling issues, context loss, and historian gaps
- minimum viable data stacks for process intelligence
- how to build value before a full digital transformation exists

### Then
1. define the minimum brownfield data layer PES would need to support process-intelligence projects
2. separate must-have data from nice-to-have data
3. identify the most common brownfield blockers and how PES should diagnose them
4. map where LOOP can store coordination truth vs where Floor execution and edge data systems belong

### Output
- minimum viable data layer blueprint
- instrumentation gap checklist
- brownfield blocker map
- phased data-readiness model
- LOOP layer-fit implications

---

## Prompt 04 — operational_digital_twin_lite/
### Objective
Research practical digital twin approaches for process improvement in real factories.
Focus on:
- digital twin lite vs full enterprise digital twin
- what can realistically be mirrored for one line, one utility system, one cell, or one asset group
- what kinds of simulation, forecasting, and operator guidance are actually useful
- update frequency, model fidelity, and maintenance burden

### Then
1. define a PES-friendly operational digital twin lite offer
2. identify the best first twin candidates for PES-style work: utilities, HVAC/process air, pump/fan systems, drive-heavy lines, packaging, material handling, etc.
3. identify what data, logic, and interfaces are needed
4. map how LOOP could coordinate the knowledge twin side of this work

### Output
- twin-lite definition
- candidate system ranking
- implementation blueprint
- maintenance burden / ROI table
- LOOP knowledge-twin implications

---

## Prompt 05 — predictive_maintenance_and_reliability/
### Objective
Research predictive maintenance and reliability intelligence for industrial electrical/mechanical systems.
Focus on:
- motors, VFDs, fans, pumps, conveyors, HVAC/process utility equipment, actuators, thermal systems, and supporting sensors
- failure precursors
- data signals that are realistically available in brownfield plants
- maintenance workflow integration
- limits of predictive maintenance in low-data or low-discipline environments

### Then
1. identify which reliability-intelligence offerings fit PES best
2. distinguish between condition monitoring, reliability analytics, and true predictive maintenance
3. define a realistic pilot model PES could sell without overselling AI
4. identify where human technician judgment must remain primary

### Output
- reliability offering ladder
- signal-to-use-case matrix
- pilot model
- overclaim risk list
- human-vs-model boundary recommendations

---

## Prompt 06 — throughput_quality_energy_convergence/
### Objective
Research how throughput, quality, maintenance, and energy performance can be treated as one connected operating problem.
Focus on:
- the tradeoffs between speed, stability, quality, and energy
- how process drift, poor controls tuning, sequencing, and utility instability affect all four domains
- how advanced monitoring or AI can expose multi-domain improvement opportunities
- examples in industrial production and facility/process-support systems

### Then
1. define why PES should not sell these domains as isolated silos
2. propose a unified process-performance model PES can use in assessments
3. identify the strongest cross-domain metrics and operator views
4. identify where this converges with HVAC/BAS/energy retrofit expertise already inside PES

### Output
- unified performance model
- metric hierarchy
- cross-domain failure map
- PES differentiator statement
- top 5 convergence opportunities

---

## Prompt 07 — human_in_the_loop_operations_copilot/
### Objective
Research human-in-the-loop industrial operations copilots.
Focus on:
- operator guidance
- supervisor decision support
- maintenance triage support
- engineering support tools
- escalation design
- trust and usability in industrial environments

Avoid generic office copilots.
Stay focused on real operational settings where wrong advice has physical consequences.

### Then
1. define what an industrial operations copilot should and should not do for PES clients
2. distinguish decision support from automation and autonomy
3. identify the right user roles: operator, supervisor, maintenance tech, engineer, manager
4. define how LOOP could support copilot knowledge, traceability, and governed recommendations

### Output
- role-based copilot model
- support vs autonomy boundary map
- trust / adoption requirements
- LOOP integration model
- pilot recommendation

---

## Prompt 08 — industrial_connectivity_and_integration/
### Objective
Research the connectivity and integration layer required to support process-intelligence services.
Focus on:
- PLC, SCADA, historian, MES, CMMS, ERP-lite, BAS, MQTT, OPC UA, Modbus, REST/API bridges, and edge gateways
- interoperability pain in mixed-vendor plants
- safe connector strategy for brownfield environments
- event flows, change detection, and data contracts across operational systems

### Then
1. define the minimum integration architecture PES would need for early projects
2. identify the safest and most reusable connectivity patterns
3. identify integration anti-patterns that create brittle deployments
4. map how LOOP Connectors, Relay, Node, and Floor could coordinate this class of work

### Output
- integration reference architecture
- connector priority stack
- anti-pattern list
- deployment pattern recommendations
- LOOP-to-plant integration map

---

## Prompt 09 — controls_aware_ai_architecture/
### Objective
Research what makes an AI architecture controls-aware in industrial settings.
Focus on:
- separation between advisory logic and control logic
- real-time constraints
- fail-safe behavior
- supervisory layers vs deterministic control layers
- where optimization can safely live vs where it should never directly intervene
- interaction with PLCs, drives, BAS, and edge systems

### Then
1. define the architecture boundaries PES must respect to stay credible and safe
2. identify where AI can advise, where it can tune, and where it should never directly command
3. map this to LOOP’s Node / Container / Floor model and execution-surface concept
4. propose a controls-aware reference architecture for PES-led projects

### Output
- controls-aware boundary model
- advisory/tuning/control split
- safe architecture diagram in text
- LOOP mapping
- implementation guardrails

---

## Prompt 10 — pes_service_line_and_business_model/
### Objective
Research and design the PES business model for this service line.
Focus on:
- service-line structure
- assessment offers
- pilot offers
- recurring support models
- deliverables
- pricing logic
- packaging for SMEs vs mid-market clients
- strategic fit inside the wider PES business

This is not just a marketing prompt.
It must produce a durable business-design model.

### Then
1. define the cleanest service ladder for PES process intelligence
2. distinguish diagnostic work, pilot work, implementation work, and recurring support
3. identify which offers should be fixed-scope vs T&M vs retainer
4. define how this wing fits beside PES’s other core business wings

### Output
- service ladder
- offer architecture
- pricing-model recommendations
- capability/dependency map
- strategic fit memo

---

## Prompt 11 — pilot_design_and_commercial_entry/
### Objective
Research how PES should enter this market commercially.
Focus on:
- ideal first customer profiles
- easiest first wins
- brownfield pilot design
- proof-of-value structure
- sales framing
- objection handling
- what evidence decision-makers need before expanding scope

### Then
1. define the best first beachheads for PES
2. propose 3 pilot packages with clear scope, deliverables, proof points, and upgrade paths
3. define how to frame this without sounding like vague AI consulting
4. identify commercial mistakes likely to kill trust early

### Output
- ICP map
- 3 pilot packages
- commercial-entry strategy
- objection map
- trust-preserving sales language

---

## Prompt 12 — governance_safety_and_trust/
### Objective
Research governance, safety, trust, and accountability requirements for AI-assisted industrial process improvement.
Focus on:
- explainability requirements for operational recommendations
- human approval boundaries
- auditability and receipts
- cybersecurity and operational risk
- data governance
- liability and trust barriers in industrial adoption

### Then
1. define the minimum governance model PES should require before deploying anything beyond passive analysis
2. identify which LOOP doctrines already support this and which need extension
3. propose a trust model for recommendations, approvals, and execution boundaries
4. identify red-line cases PES should refuse

### Output
- governance minimums
- trust / approval model
- refusal-boundary list
- LOOP doctrine implications
- deployment readiness checklist

---

## Packaging note
When reused later, this pack should be exportable as:
- one markdown pack
- optional split files by prompt folder
- optional research-run entries in the Research Runs database

## Naming note
This artifact is a separate operator pack.
Do not overwrite or merge with:
- `LOOP Research Spine — Codex Prompt Pack v0.1`
- any future revised version of that original pack
