# HealthGuide AI — 2-to-3 Minute Hackathon Demo Script
**Event:** UnivaBio 2026 Hackathon  
**Target Audience:** Hackathon Judges & Clinical Evaluators  
**Presenters:** Full-Stack & Safety Engineering Team  

---

## Demo Overview (Total Duration: 2 mins 45 secs)
- **0:00 – 0:30:** Problem Statement & Value Proposition
- **0:30 – 1:15:** Scenario 1: The Emergency Invariant (Priority Override)
- **1:15 – 1:55:** Scenario 2: Routine Symptoms & Curated Evidence
- **1:55 – 2:25:** Bilingual Tamil Support & Privacy Guarantee
- **2:25 – 2:45:** Architectural Wrap-up & Q&A Transition

---

### Segment 1: The Problem (0:00 – 0:30)
> **Speaker:**  
> "Judges, consider what happens when someone feels unwell late at night. They either Google their symptoms and panic over worst-case cancers, or they ask a generic AI chatbot that hallucinates a fake percentage or dangerous advice.  
>  
> Today, we present **HealthGuide AI**. Our tagline is simple: *Understand symptoms. Recognize warning signs. Take safer next steps.*  
>  
> Unlike conventional chatbots, HealthGuide AI is built on a **deterministic safety core**. It is strictly an educational tool designed to prevent clinical delays while never pretending to be a doctor."

---

### Segment 2: Scenario 1 — The Emergency Red Flag (0:30 – 1:15)
> **Action:** *Click the 'Demo 1: Emergency Red Flag' preset button.*  
>  
> **Speaker:**  
> "Let’s look at our first fictional scenario: A patient experiencing severe crushing chest pressure spreading to their left arm. Notice the user self-selected 'Mild' or 'Critical' severity.  
>  
> We click **'Review & Verify'**, inspect our input, and submit.  
>  
> Look at the result: The system immediately flags an **EMERGENCY** tier.  
>  
> Crucially, our safety engine enforced the **Zero-Downgrade Invariant**: even if an external LLM was connected or the user selected mild discomfort, the deterministic safety engine intercepted the cardiovascular warning sign, bypassed non-emergency analysis, suppressed home self-care remedies that might cause dangerous delays, and surfaced direct telephone hotlines for **112, 108, and 911** alongside clear emergency actions."

---

### Segment 3: Scenario 2 — Routine Symptoms & Verified Knowledge (1:15 – 1:55)
> **Action:** *Click 'Check Another Symptom', then click 'Demo 2: Routine Discomfort'.*  
>  
> **Speaker:**  
> "Now let's examine a routine case: A student with a dull tension headache after extended screen time.  
>  
> Notice our result:  
> 1. It classifies this as **'Low-Risk Routine Profile • Self-Care & Monitoring'**.  
> 2. It highlights **What the system noticed** without declaring a medical diagnosis.  
> 3. It offers vetted educational insights mapped directly to **MedlinePlus** and the **NHS**.  
> 4. Notice what is absent: **Zero fabricated statistics.** You won't see 'You have an 87% chance of condition X'.  
> 5. It provides safe, low-risk self-care suggestions: hydration, resting in a dimly lit room, and temperature tracking."

---

### Segment 4: Bilingual Support & Privacy (1:55 – 2:25)
> **Action:** *Click the 'தமிழ்' language toggle button in the top navigation bar.*  
>  
> **Speaker:**  
> "Healthcare access requires linguistic accessibility. In one click, the entire platform switches to natural, authentic **Tamil**.  
>  
> All triage questions, safety disclaimers, emergency hotlines, and curated educational recommendations are presented in clear Tamil.  
>  
> Furthermore, from a security standpoint, HealthGuide AI enforces **Privacy by Design**:  
> - We never ask for names, phone numbers, or dates of birth.  
> - We store nothing in a database.  
> - Our FastAPI backend includes automated middleware that scrubs and masks raw symptoms from all server access logs."

---

### Segment 5: Conclusion (2:25 – 2:45)
> **Speaker:**  
> "In summary: HealthGuide AI combines modern React and FastAPI engineering with audited deterministic safety rules and bilingual public health knowledge.  
>  
> All 21 automated safety, translation, and privacy tests run and pass out-of-the-box on Windows PowerShell.  
>  
> Thank you! We welcome your questions."
