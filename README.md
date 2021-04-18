# CPT-3 - Automated Documentation and Summary of Doctor-Patient Conversations


## Features

- Record conversation in the browser, upload as file, or paste a transcribed conversation
- Automatic speech-to-text conversion
- Extract symptoms, diagnosis, and treatment of the conversation
- Export summary to .csv
- Retrieve ICD-10 codes for symptoms


## Installation

```
git clone https://github.com/kechtel/CPT-3
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m flask run
```