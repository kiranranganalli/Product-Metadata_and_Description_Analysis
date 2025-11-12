# Visual Intelligence for Logistics  
### *Automatic Product Metadata and Weight Estimation using Multimodal AI*

---

## 🧠 Abstract  
This project introduces a multimodal AI framework that automates **product metadata extraction and weight estimation** directly from images.  
By combining **computer vision**, **OCR**, and **language reasoning models**, the system identifies product details, extracts visible textual cues (e.g., “Net Weight: 250g”), and approximates missing weights using **OpenAI’s vision capabilities**.

The platform supports **logistics and e-commerce intelligence**, helping estimate packaging weights for categories where structured metadata is unavailable.  
It also integrates **database deduplication** to avoid redundant storage and dynamically computes **category-level weight averages** for scalable analysis.

---

## 📸 Project Gallery  

<img width="1470" height="789" alt="Home Page" src="https://github.com/user-attachments/assets/573412e3-1ce8-4aaf-bace-c3f35daa79d6" />
<img width="1470" height="789" alt="Extracted" src="https://github.com/user-attachments/assets/ed06893b-1a1a-4cd0-8fcb-83c580998dfb" />
<img width="1470" height="789" alt="Existed" src="https://github.com/user-attachments/assets/76b6659b-6ca9-43c8-854a-74edd411e5f4" />


---

## 📘 Table of Contents  
1. [Introduction](#introduction)  
2. [Motivation](#motivation)  
3. [Research Problem & Objectives](#research-problem--objectives)  
4. [System Architecture](#system-architecture)  
5. [Data Flow & Components](#data-flow--components)  
6. [Model Design & Algorithms](#model-design--algorithms)  
7. [Database & Deduplication Logic](#database--deduplication-logic)  
8. [Evaluation & Analytics](#evaluation--analytics)  
9. [Future Work](#future-work)  
10. [References](#references)  

---

## 1. Introduction  

In large-scale logistics systems, accurate **product weight estimation** plays a critical role in shipping optimization, load balancing, and warehouse cost modeling.  
However, most e-commerce listings contain incomplete or inaccurate metadata — especially weight and dimensions.  

This project builds a **research-driven multimodal pipeline** that:
- Extracts product attributes directly from visual input.
- Predicts approximate weight when metadata is missing.
- Aggregates data at the category level for statistical logistics modeling.  

It integrates **Streamlit** (frontend), **FastAPI** (backend), **SQLAlchemy** (data persistence), and **OpenAI’s multimodal models** to deliver an intelligent visual understanding system.

---

## 2. Motivation  

Modern supply chains depend heavily on accurate **SKU-level product weight data** for routing and fulfillment.  
When product catalogs lack standardized metadata, operational efficiency drops due to manual verification and estimation.  

Key challenges include:
- Missing or inconsistent weight labels.  
- Duplicate product entries across sources.  
- Poor OCR readability for images with dense packaging design.  

This project proposes an AI-assisted approach that learns to reason about **visual scale, packaging cues, and textual indicators**, providing approximate weights to fill in missing metadata.  

---

## 3. Research Problem & Objectives  

### Research Questions  
1. How can multimodal AI be used to infer missing physical attributes (like weight) from visual and textual cues?  
2. What accuracy can be achieved in weight estimation using visual reasoning without explicit ground-truth labels?  
3. Can deduplication and category-level averaging improve dataset consistency for logistics prediction?

### Objectives  
- Develop a **robust OCR + Vision-Language model** pipeline.  
- Build an **automated deduplication system** for product registration.  
- Compute **dynamic category-wise weight averages**.  
- Integrate **OpenAI-based reasoning** for approximate weight inference.

---

## 4. System Architecture  

### 🔹 Overview  

The system is modular, consisting of four key components:
1. **Frontend (Streamlit)** — User uploads product image(s) and views extracted details.  
2. **Backend (FastAPI)** — Orchestrates image processing, extraction, and inference.  
3. **Database Layer (SQLAlchemy)** — Stores structured product metadata and weight averages.  
4. **AI Layer (OpenAI Vision + OCR)** — Performs text extraction and visual weight approximation.

**Flow:**  
`User Upload → OCR → Metadata Parsing → Weight Detection → AI Approximation → DB Storage → Category Analytics`

---

## 5. Data Flow & Components  

### 🧾 Step 1: Image Upload  
- Users upload product images through the Streamlit UI.  
- Uploaded images are sent to the backend via API call.  

### 🔍 Step 2: OCR Extraction  
- Extracts visible text such as *“500ml”*, *“2kg”*, *“Net Wt: 200g”*.  
- Tools used: `pytesseract` / `easyocr`.  
- Text is parsed into structured key-value pairs.  

### ⚙️ Step 3: Metadata Structuring  
- Extracted text is cleaned and tokenized.  
- Regular expressions detect numeric + unit combinations (`250 g`, `0.5 L`, `2 kg`).  
- Category is derived via heuristic or filename context.  

### 🤖 Step 4: OpenAI Vision Reasoning  
If no explicit weight is found, the system sends the image to an OpenAI vision model with a prompt like:
> “Estimate the approximate weight of this product in grams, considering packaging type and visible scale.”

The response is parsed, validated, and stored with confidence scoring.

### 🧮 Step 5: Weight Averaging  
For each category (e.g., Shampoo, Snack, Beverage), the system computes:
\[
\text{Category Average Weight} = \frac{\sum_{i=1}^{n} w_i}{n}
\]

This aids future approximations when multiple missing entries occur.

---

## 6. Model Design & Algorithms  

### 🧩 OCR + Text Extraction  
```python
import pytesseract
text = pytesseract.image_to_string(image)
weights = re.findall(r'\d+\.?\d*\s?(g|kg|ml|l)', text.lower())
