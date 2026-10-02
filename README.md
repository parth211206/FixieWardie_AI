# FixieWardie

> **Turning hostel maintenance complaints into risk-aware, actionable work orders.**

FixieWardie is an AI-assisted hostel maintenance and safety platform that analyzes **complaint descriptions, images, location information, and related incidents** to identify potential hazards, assess risk, and route maintenance requests to an appropriate technician.

The system is designed to address three common problems in accommodation maintenance:

* **Misclassification** — the selected complaint category may not reflect the actual hazard.
* **Attachment blindness** — important information contained in an uploaded image may be ignored.
* **Complaint isolation** — multiple complaints from the same area may actually represent one developing incident.

---

# 🚀 Project Overview

A normal complaint system may process:

```text
Category → Bathroom Leakage
```

FixieWardie looks beyond the selected category and analyzes the complete complaint:

```text
Complaint
    ↓
Text + Image Evidence
    ↓
AI Intake & Classification
    ↓
Hazard Detection
    ↓
Risk Assessment
    ↓
Incident Correlation
    ↓
Technician Routing
    ↓
Work Order
```

For example, a resident may report:

> "There is water leaking near the electrical switchboard and the lights are flickering."

Although the resident may select **Bathroom Leakage**, FixieWardie can identify the electrical context, detect relevant hazards, assess the risk, and route the issue toward an appropriate electrical technician.

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │   STUDENT FRONTEND  │
                         │     HTML / React    │
                         └──────────┬──────────┘
                                    │
                              POST /analyze
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    FASTAPI BACKEND  │
                         │   FIXIEWARDIE API   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    INTAKE AGENT     │
                         │                     │
                         │ Text Understanding  │
                         │ Classification      │
                         │ Hazard Extraction   │
                         │ Image Evidence      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     RISK ENGINE     │
                         │                     │
                         │ Hazard Normalizing  │
                         │ Risk Scoring        │
                         │ Severity            │
                         │ Incident Correlation│
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   ROUTING ENGINE    │
                         │                     │
                         │ Skill Matching      │
                         │ Availability        │
                         │ Location            │
                         │ Workload            │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     WORK ORDER      │
                         │      ASSIGNED       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                              TECHNICIAN
```

---

# ✨ Key Features

## 1. AI-Powered Complaint Intake

FixieWardie analyzes:

* Complaint description
* User-selected category
* Location
* Uploaded image
* Relevant contextual information

The Intake Agent can:

* Understand the actual issue
* Detect potential hazards
* Identify the appropriate maintenance category
* Determine the required technician skill
* Estimate initial severity

Example:

```json
{
  "normalized_issue": "Water leaking near an electrical switchboard causing lights to flicker.",
  "corrected_category": "Electrical",
  "category_overridden": true,
  "detected_hazards": [
    "Water leak near electrical switchboard",
    "Flickering lights indicating potential electrical fault"
  ],
  "required_skill": "Electrical",
  "initial_severity": "Critical"
}
```

---

# 🖼️ 2. Visual Evidence Analysis

Uploaded photographs can provide information that is missing from the complaint text.

The Evidence Analyzer checks:

* Whether an image was provided
* Whether the image is valid
* Image dimensions and format
* Visible conditions relevant to the complaint

The visual analysis is designed to identify **observable evidence without intentionally inventing conditions that cannot be seen**.

Example:

```text
Complaint Text
      +
Uploaded Image
      ↓
Visual Evidence
      ↓
Combined Understanding
```

FixieWardie can also operate when no image is provided.

---

# ⚠️ 3. Risk Assessment

The Risk Engine converts extracted hazards into a structured risk assessment.

The current prototype uses deterministic, rule-based scoring.

### Example category weights

| Category   | Prototype Score |
| ---------- | --------------: |
| Electrical |              35 |
| Fire       |              70 |
| Structural |              55 |
| Water      |              25 |
| Plumbing   |              20 |
| Security   |              40 |

### Example hazard weights

| Hazard                 | Prototype Score |
| ---------------------- | --------------: |
| Exposed wires          |              25 |
| Sparks                 |              30 |
| Electrical fire        |              35 |
| Electric shock         |              35 |
| Fire                   |              40 |
| Smoke                  |              30 |
| Water near electricity |              35 |
| Burning smell          |              25 |

Combination rules can increase the risk when hazards occur together.

For example:

```text
Water Leak + Electrical Equipment
              ↓
        Increased Risk
```

### Prototype severity thresholds

```text
0 – 24       LOW
25 – 49      MEDIUM
50 – 74      HIGH
75 – 100     CRITICAL
```

> **Note:** These numerical values are prototype heuristics and are not official electrical, fire, or occupational safety standards.

---

# 🔗 4. Hazard Normalization

Different components may describe the same hazard using different terminology.

For example:

```text
"Water leak near electrical switchboard"
                ↓
"water_near_electricity"
```

The hazard normalizer converts natural-language outputs into a common vocabulary that can be consumed reliably by downstream modules.

This allows independently developed components to communicate consistently.

---

# 🧠 5. Incident Correlation

FixieWardie is designed to avoid treating every maintenance complaint as an isolated event.

Multiple complaints from the same area can potentially represent a connected incident.

Example:

```text
Monday
Water near switchboard
        ↓
Wednesday
Flickering lights
        ↓
Thursday
Burning smell
        ↓
FixieWardie
        ↓
Related Incident
```

This helps identify patterns that may not be obvious when complaints are viewed individually.

---

# 👷 6. Intelligent Technician Routing

After identifying the required skill and risk level, the Routing Engine determines an appropriate technician using predefined constraints.

Routing considers:

* Required skill
* Technician availability
* Building/location
* Current workload

Example:

```text
Required Skill
     ↓
Electrical
     ↓
Available Technicians
     ↓
Location + Workload
     ↓
Suitable Technician
```

The current prototype contains sample technicians for demonstrating this workflow.

---

# 📋 7. Work Order Generation

After routing, FixieWardie creates an actionable work order.

Example:

```text
Work Order
────────────────────────────
Complaint: REQ-F561CCA8

Category: Electrical

Risk: HIGH / CRITICAL

Location:
Block A
Floor 2
Room 204

Status:
ASSIGNED

Technician:
Arjun
────────────────────────────
```

This allows the system to move from:

```text
"Something may be wrong"
```

to:

```text
"This issue has been analyzed and routed for maintenance."
```

---

# 🔄 End-to-End Workflow

When a student submits a complaint:

```text
1. Student submits complaint
             ↓
2. Frontend sends POST /analyze
             ↓
3. FastAPI receives the request
             ↓
4. Intake Agent analyzes text
             ↓
5. Image evidence is analyzed if available
             ↓
6. Hazards are extracted
             ↓
7. Hazards are normalized
             ↓
8. Risk Engine calculates risk
             ↓
9. Related incidents are considered
             ↓
10. Routing Engine finds a suitable technician
             ↓
11. Work order is generated
             ↓
12. Result is returned as JSON
             ↓
13. Frontend displays the result
```

---

# 🧩 AI vs Deterministic Components

FixieWardie intentionally separates AI interpretation from operational decision logic.

### AI-assisted components

* Complaint understanding
* Category interpretation
* Hazard extraction
* Image evidence analysis
* Initial issue interpretation

### Deterministic components

* Hazard normalization
* Risk scoring
* Severity thresholds
* Technician skill matching
* Availability checking
* Location matching
* Work-order state

This design makes important operational decisions more transparent and controllable.

---

# 💻 Technology Stack

### Frontend

* HTML
* React
* Tailwind CSS
* Lucide

### Backend

* Python
* FastAPI
* Uvicorn

### AI / Analysis

* AI-based text understanding
* Image evidence analysis
* Rule-based risk engine
* Deterministic technician routing

### Development

* Git
* GitHub
* REST API
* JSON

---

# 📁 Project Structure

The exact structure may evolve as the team integrates the branches, but the architecture is organized around:

```text
FixieWardie/
│
├── backend/
│   ├── app/
│   │   ├── api.py
│   │   ├── intake/
│   │   ├── risk/
│   │   ├── routing/
│   │   └── ...
│   │
│   └── ...
│
├── frontend/
│   └── ...
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# 🌿 Team Development

The project was developed as separate modules and then brought together into a complete integrated system through GitHub.

### Team Contributions

| Team Member        | Contribution                                |
| ------------------ | ------------------------------------------- |
| **You**            | **AI Intake & Complete System Integration** |
| **Vastab Sarkar**  | **Routing & Work Management**               |
| **Shivam**         | **Risk Assessment & Incident Correlation**  |
| **Vanshika Dewan** | **Frontend**                                |

### Development Flow

```text
Vastab Sarkar
      │
      └── Routing & Work Management
                │
Shivam           │
      │          └── Risk Assessment &
      │              Incident Correlation
      │
Vanshika Dewan
      │
      └── Frontend
                │
                ▼
       ┌─────────────────┐
       │ AI Intake       │
       │ + Integration   │
       │                 │
       │      You        │
       └────────┬────────┘
                │
                ▼
       Complete FixieWardie
             System
```

The modular architecture allows individual components to be developed and tested independently before being integrated into the complete FixieWardie workflow.

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd FixieWardie
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Create a local `.env` file if required:

```text
API_KEY=your_api_key_here
```

> Do not commit `.env` or API keys to GitHub.

---

# ▶️ Running the Backend

From the project directory:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then:

```bash
uvicorn backend.app.api:app --reload
```

The API will be available locally at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation can be accessed through:

```text
http://127.0.0.1:8000/docs
```

---

# 🌐 Running the Frontend

Open the frontend application according to the project's frontend setup.

The frontend communicates with the backend through:

```text
POST /analyze
```

The request contains the complaint information and optional image evidence.

The backend processes the request and returns the structured FixieWardie analysis to the frontend.

---

# 🧪 Example Demo

### Input

```text
Category:
Bathroom Leakage

Description:
There is water leaking near the electrical switchboard
and the lights are flickering.

Location:
Block A, Floor 2, Room 204
```

### Processing

```text
Bathroom Leakage
        ↓
AI analyzes description
        ↓
Electrical context detected
        ↓
Hazards extracted
        ↓
Risk assessed
        ↓
Required skill = Electrical
        ↓
Technician routing
        ↓
Work order
```

### Expected outcome

```text
Corrected Category:
Electrical

Detected Hazards:
- Water near electrical equipment
- Flickering lights

Risk:
Elevated / High / Critical depending on
the configured prototype rules

Required Skill:
Electrical

Work Order:
Created / Assigned
```

---

# 🔌 API

## `POST /analyze`

Analyzes a maintenance complaint.

### Input

```text
description
category
location
image (optional)
```

### Output

The response contains structured information covering the relevant stages of the pipeline, including:

```text
Intake
Risk
Incident information
Routing
Work order
```

The API is also available through FastAPI Swagger UI at:

```text
/docs
```

---

# 🛡️ Safety & Limitations

FixieWardie is a **prototype decision-support and maintenance-routing system**.

It should not be treated as:

* A certified electrical safety system
* A replacement for qualified technicians
* An emergency response service
* An official safety risk standard

The prototype risk scores are based on configurable rules and are intended to demonstrate the concept.

For consequential real-world safety situations, appropriate human oversight and qualified personnel remain necessary.

---

# 🔮 Future Improvements

Potential production extensions include:

* Persistent database for complaints and incidents
* Real-time technician availability
* Push/SMS/email notifications
* Complete historical incident tracking
* More advanced incident clustering
* Authentication and role-based access
* Maintenance dashboards
* Audit logs
* Real-time building/room mapping
* Integration with hostel management systems
* Human approval workflows for high-risk incidents
* Production-grade monitoring and analytics

---

# 🎯 Project Goal

FixieWardie aims to transform hostel maintenance from a simple:

```text
Complaint → Technician
```

workflow into:

```text
Complaint
    ↓
Understand
    ↓
Verify Evidence
    ↓
Identify Hazards
    ↓
Assess Risk
    ↓
Correlate Incidents
    ↓
Route Correctly
    ↓
Create Work Order
    ↓
Take Action
```

### Core Idea

> **FixieWardie converts unstructured hostel complaints and visual evidence into risk-aware incidents and actionable maintenance assignments.**

---

# 👥 Team

### FixieWardie — Agentic Risk Intelligence for Accommodation

| Member             | Role                                    |
| ------------------ | --------------------------------------- |
| **You**            | AI Intake & Complete System Integration |
| **Vastab Sarkar**  | Routing & Work Management               |
| **Shivam**         | Risk Assessment & Incident Correlation  |
| **Vanshika Dewan** | Frontend                                |

Developed as a collaborative modular prototype using AI, FastAPI, React, rule-based risk analysis, incident intelligence, and technician routing.

---

# 📄 License

This project is currently a prototype developed for educational and hackathon purposes.
