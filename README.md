# 🇮🇳 Indian Language Translator

## ✨ Features

-   **Multi-Language Support**: Translate text into 12+ major Indian languages.
-   **Simple Interface**: A clean, two-column layout for easy input and clear results.
-   **Secure API Key Handling**: Uses a `.env` file to keep your OpenAI API key safe and out of the source code.
-   **Efficient**: Caches translation results to avoid redundant API calls and improve speed.
-   **Easy to Use**: Includes a "Clear All" button to quickly reset the text fields.

---

## 🛑 Before You Start: Setting Up Your API Key

This application requires an OpenAI API key to function. To protect your key, we will store it in a local environment file that is **never** uploaded to Git.

**This is a critical step.** The application will not work without it.

1.  **Create the `.env` file:**
    In the main directory of the project (the same folder where `main.py` is located), create a new file and name it exactly `.env`

2.  **Add Your API Key:**
    Open the `.env` file and add the following line, replacing `your_secret_api_key_goes_here` with your actual OpenAI API key:

    ```
    OPENAI_API_KEY="your_secret_api_key_goes_here"
    ```

3.  **Save the file.** The `.gitignore` file included in this project is already configured to ignore `.env`, so you don't have to worry about accidentally committing it.

---

## 🚀 How to Run Locally

Follow these steps in your computer's terminal to get the application running.

**1. Clone the Repository (If you are using Git):**
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
2. Create and Activate a Virtual Environment (Recommended):This keeps your project's dependencies isolated.# For Mac/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
3. Install the Required Libraries:The requirements.txt file lists all the necessary Python packages.pip install -r requirements.txt
4. Run the Streamlit App:This command will start the local web server and open the application in your browser.streamlit run main.py
You should now see the Indian Language Translator running in a new browser tab!📂 Project Structure.
├── .gitignore          # Tells Git which files to ignore (like .env)
├── main.py             # The main Python script for the Streamlit app
├── requirements.txt    # Lists the project's Python dependencies
├── README.md           # You are here!
└── .env                # Your local file for storing secret keys (not committed)
