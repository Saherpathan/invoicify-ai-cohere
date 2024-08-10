# Invoicify-AI-Cohere

A Flask application that extracts invoice details from uploaded PDFs and images using `pdfplumber`, `pytesseract`, and the Cohere API for natural language processing. The extracted data is displayed in a user-friendly format and can be downloaded as JSON.

## Features

- **Upload PDF or Image Files**: Supports PDFs and images in PNG, JPG, JPEG formats.
- **AI-Powered Extraction**: Utilizes Cohere API to extract invoice details such as customer information, product details, and total amount.
- **User-Friendly Interface**: Simple and intuitive UI for uploading files and viewing results.
- **Downloadable JSON**: Extracted data can be downloaded as a JSON file.
- **Deployment Support**: Ready for deployment on Vercel.

## Getting Started

### Prerequisites

- Python 3.8+
- `pip` (Python package installer)
- [Cohere API key](https://cohere.ai/) (Add this to a `.env` file)

### Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/Saherpathan/invoicify-ai-cohere.git
    cd invoicify-ai-cohere
    ```

2. **Create a Virtual Environment and Activate It**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the Required Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add your Cohere API key:

    ```env
    COHERE_API_KEY=<your_cohere_api_key>
    ```

5. **Run the Flask Application Locally**

    ```bash
    python api_call.py
    ```

    The app will be accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Deployment

### Deploying to Vercel

1. **Install Vercel CLI**

    ```bash
    npm install -g vercel
    ```

2. **Deploy Your Application**

    ```bash
    vercel
    ```

   Follow the prompts to deploy. Vercel will provide you with a URL where your app is live.

### Environment Setup on Vercel

When deploying to Vercel, make sure to set the `COHERE_API_KEY` in the Environment Variables settings on the Vercel dashboard.

## Folder Structure

```bash
invoicify-ai-cohere/
│           
├── requirements.txt        # Python dependencies
├── vercel.json             # Vercel deployment configuration
├── .env                    # Environment variables 
├── /api                    # Main Flask application script
|   └── api_call.py
│   └──/templates
│       ├── index.html          # Home page for file uploads
│       └── result.html         # Result page displaying extracted details
├── /output                 # JSON outputs of extracted details
├── /uploads                # Uploaded files
└── README.md               # Project documentation
```

## Contributing

We welcome contributions to this project. To contribute:

1. **Fork the Repository**: Click the "Fork" button at the top right of this repository.

2. **Create a New Branch**:

    ```bash
    git checkout -b feature/your-feature-name
    ```

3. **Commit Your Changes**:

    ```bash
    git commit -m "Add your message here"
    ```

4. **Push to the Branch**:

    ```bash
    git push origin feature/your-feature-name
    ```

5. **Submit a Pull Request**: Open a pull request to the `main` branch with a description of your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please contact: [sahergpathan@gmail.com](mailto:sahergpathan@gmail.com)

