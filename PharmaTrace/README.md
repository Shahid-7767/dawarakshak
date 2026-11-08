# PharmaTrace – Blockchain-Based Fake Medicine Detection

## 1. Project Overview

PharmaTrace is a blockchain-based medicine verification system designed to help identify counterfeit medicines and improve transparency in the pharmaceutical supply chain.

The system uses QR codes and blockchain technology to help users verify medicine information and track its movement through the supply chain.

## 2. Problem Statement

Fake medicines are a serious threat to public health. Traditional medicine supply chains can make it difficult to verify whether a medicine is genuine or counterfeit.

PharmaTrace aims to address this problem by providing a transparent and verifiable medicine-tracking system.

## 3. Proposed Solution

PharmaTrace provides a digital verification process:

1. A manufacturer registers medicine information.
2. A unique QR code is generated for the medicine.
3. Medicine information is recorded in the blockchain.
4. Distributors and pharmacies update supply-chain information.
5. Users scan the QR code to verify the medicine details.
6. The system checks the recorded information to identify suspicious or invalid records.

## 4. Key Features

- QR-code-based medicine identification.
- Blockchain-based record management.
- Medicine supply-chain tracking.
- Medicine information verification.
- Flask-based web application.
- Validator and consensus simulation.

*Note: Update this feature list as each feature becomes fully implemented and tested.*

## 5. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application |
| Blockchain | Secure record management |
| QR Code | Medicine identification |
| HTML and CSS | User interface |
| Database | Storing application information |
| Git and GitHub | Version control |

## 6. Project Structure

```text
PharmaTrace/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── blockchain/
│   ├── block.py
│   ├── chain.py
│   ├── consensus.py
│   └── validators.py
│
├── database/
├── modules/
├── static/
│   ├── qr/
│   └── style.css
│
├── templates/
└── tests/
```

## 7. Installation and Execution

### Step 1: Clone the repository

```bash
git clone https://github.com/Shahid-7767/dawarakshak.git
```

### Step 2: Open the project folder

```bash
cd dawarakshak/PharmaTrace
```

### Step 3: Create a virtual environment

```bash
python -m venv .venv
```

### Step 4: Activate the environment (Windows)

```powershell
.venv\Scripts\activate
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the application

```bash
python app.py
```

### Step 7: Open the application

Visit the following address in your browser:

```text
http://127.0.0.1:5000
```

## 8. Expected Benefits

- Helps users verify medicine information.
- Improves transparency in the pharmaceutical supply chain.
- Makes medicine records easier to track.
- Helps identify suspicious medicine records.
- Demonstrates the use of blockchain in healthcare.

## 9. Future Enhancements

- Mobile application for medicine verification.
- Integration with real pharmaceutical supply chains.
- Improved QR-code verification.
- Advanced blockchain consensus mechanisms.
- Role-based access for manufacturers, distributors, pharmacies and regulators.

## 10. Project Information

**Project Name:** PharmaTrace  
**Project Domain:** Blockchain and Healthcare  
**Programming Language:** Python  
**Application Framework:** Flask  
**Repository:** https://github.com/Shahid-7767/dawarakshak

---

*PharmaTrace – Building Trust in Every Medicine.*