# Sample Prompts for Testing Data Extraction

Below are several sample prompts that you can use to test and evaluate the data-extraction capabilities of your local model (`phi-3.1-mini-128k-instruct`).

Each prompt demonstrates a different type of extraction task.

You can adapt or expand them based on your specific use case.

---

### 1. Extracting Email Addresses
**Prompt:**
```
Extract all email addresses from the text below. Provide the emails in a JSON list.

Text:
"Hello David, please reach out to sarah.jones@example.com and support@mycompany.org. 
Also, don’t forget to CC marketing-team@website.co.uk."
```
**Expected Output (Example):**
```
[
  "sarah.jones@example.com",
  "support@mycompany.org",
  "marketing-team@website.co.uk"
]
```

---

### 2. Extracting Phone Numbers
**Prompt:**
```
Read the text and extract any phone numbers. Return them as a list of strings.

Text:
"Contact our customer service at 1-800-555-1234 or our local office at (555) 999-8888. 
You can also reach us internationally at +44 20 7946 0000."
```
**Expected Output (Example):**
```
[
  "1-800-555-1234",
  "(555) 999-8888",
  "+44 20 7946 0000"
]
```

---

### 3. Extracting Named Entities (People, Places, Organizations)
**Prompt:**
```
Please identify and list all named entities in the text, categorized into "PERSON", "ORG", and "LOCATION".

Text:
"Barack Obama served as the 44th President of the United States.
He was born in Honolulu, Hawaii, and studied at Columbia University."
```
**Expected Output (Example):**
```
{
  "PERSON": ["Barack Obama"],
  "ORG": ["Columbia University"],
  "LOCATION": ["United States", "Honolulu", "Hawaii"]
}
```

---

### 4. Structured Data from a Product Description
**Prompt:**
```
Extract the product's name, manufacturer, price, and key features from the following description. 
Return your answer as valid JSON.

Text:
"The new SmartWatch X by TechTime offers a 1.8-inch display, heart rate monitoring, 
and GPS tracking. Priced at $199.99, this watch is water-resistant up to 50 meters 
and comes with a 1-year warranty."
```
**Expected Output (Example):**
```
{
  "product_name": "SmartWatch X",
  "manufacturer": "TechTime",
  "price": 199.99,
  "features": [
    "1.8-inch display",
    "heart rate monitoring",
    "GPS tracking",
    "water-resistant up to 50 meters",
    "1-year warranty"
  ]
}
```

---

### 5. Extracting Multiple Fields from a Resume or CV
**Prompt:**
```
From the resume below, extract the following fields:
- Full Name
- Email
- Phone Number
- Education Background
- Work Experience (list each role with "title", "company", and "dates")

Text:
"Name: Alex Johnson
Email: alex.johnson@domain.com
Phone: 123-456-7890
Education: B.Sc. in Computer Science, University of Example (2015-2019)
Work Experience:
   Software Engineer at TechCorp (2020 - 2022)
   Senior Developer at CodeFlow Inc (2022 - Present)"
```
**Expected Output (Example):**
```
{
  "full_name": "Alex Johnson",
  "email": "alex.johnson@domain.com",
  "phone_number": "123-456-7890",
  "education": [
    {
      "degree": "B.Sc. in Computer Science",
      "institution": "University of Example",
      "year_range": "2015-2019"
    }
  ],
  "work_experience": [
    {
      "title": "Software Engineer",
      "company": "TechCorp",
      "dates": "2020 - 2022"
    },
    {
      "title": "Senior Developer",
      "company": "CodeFlow Inc",
      "dates": "2022 - Present"
    }
  ]
}
```

---

### 6. Parsing Invoice Details
**Prompt:**
```
You are given an invoice. Extract the invoice number, date, bill-to name, total amount, 
and itemized details (each item’s description, quantity, and price) and return them 
in JSON format.

Text:
"Invoice #INV-2025, Date: 03/25/2025
Bill To: Jane Doe
Items:
  - Consulting Services, 8 hours, $75/hr
  - Software License, 1 unit, $300
Total: $900"
```
**Expected Output (Example):**
```
{
  "invoice_number": "INV-2025",
  "invoice_date": "03/25/2025",
  "bill_to": "Jane Doe",
  "total_amount": 900,
  "items": [
    {
      "description": "Consulting Services",
      "quantity": 8,
      "unit_price": 75
    },
    {
      "description": "Software License",
      "quantity": 1,
      "unit_price": 300
    }
  ]
}
```

---

### 7. Extracting Research References (Titles, Authors, Year)
**Prompt:**
```
Extract all reference entries from the text below, providing the following fields 
for each reference: "title", "authors", and "year".

Text:
"[1] Smith, J. and Doe, A. (2021). Advances in Neural Networks. Journal of AI Research
[2] Chan, E. (2020). Modern Data Pipelines. Data Engineering Today
[3] Johnson, M., Lee, C., and Zhao, W. (2022). Robotic Process Automation. Robotics International"
```
**Expected Output (Example):**
```
[
  {
    "title": "Advances in Neural Networks",
    "authors": ["Smith, J.", "Doe, A."],
    "year": 2021
  },
  {
    "title": "Modern Data Pipelines",
    "authors": ["Chan, E."],
    "year": 2020
  },
  {
    "title": "Robotic Process Automation",
    "authors": ["Johnson, M.", "Lee, C.", "Zhao, W."],
    "year": 2022
  }
]
```

---

### 8. Customer Feedback Sentiment & Keywords
**Prompt:**
```
From the customer feedback below, extract:
- The overall sentiment (positive, negative, or neutral)
- The main keywords or topics mentioned

Text:
"I loved the quick customer service, but the product quality was disappointing. 
The delivery was also delayed by a week."
```
**Expected Output (Example):**
```
{
  "sentiment": "mixed",
  "keywords": ["customer service", "product quality", "delivery"]
}
```

---

## Tips for Testing

- **Vary the formatting and style** of your test text (e.g., bullet points, multiple lines, messy spacing) to see how robustly the model extracts the data.
- **Change the output format** (JSON, CSV, bullet-list) to see how well the model follows your instructions about structure.
- **Mix multiple data types** in the same prompt (like phone numbers, URLs, and emails in a single text passage) to test the model’s ability to extract more than one type of entity at once.
- **Include distractors or incomplete data** to test the model’s error handling and see how it responds when expected fields are missing.

By trying these prompts, you can evaluate how well your local `phi-3.1-mini-128k-instruct` model handles various data-extraction tasks and follows structured-output instructions. Good luck with your testing!