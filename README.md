# CVM Extractor 

**🚀 Live App: [https://cvm-fundos2.onrender.com/](https://cvm-fundos2.onrender.com/)**

<img width="851" height="442" alt="image" src="https://github.com/user-attachments/assets/769d17e6-ed9e-4864-9790-126204211880" />


#### Description:

**CVM Intelligence** is a Flask-based web application designed to democratize access to high-frequency financial data from the Brazilian Securities and Exchange Commission (CVM). Specifically, the software automates the retrieval, extraction, and visualization of the *Composição e Diversificação das Aplicações* (CDA) documents, which detail the portfolio assets of investment funds in Brazil.

The project addresses a specific problem in the Brazilian financial open-data ecosystem: accessibility. While the CVM provides this data publicly, it is stored in complex directory structures, compressed in ZIP archives, and formatted in non-standard CSVs (using ISO-8859-1 encoding and semicolon separators). For a typical financial analyst or student, manually downloading, unzipping, and parsing these files for every query is inefficient. CVM Intelligence solves this by providing a web interface that simplefies the entire ETL (Extract, Transform, Load).

### Project Structure and Files

The project is organized as a standard Flask application:

* **`app.py`**: This is the core controller of the application. It initializes the Flask instance and defines the routes. The `CVMExtractor` class contains the business logic for connecting to the CVM `dados.cvm.gov.br` server, handling HTTP requests with proper user-agent headers to avoid blocking, downloading binary streams into memory (using `io.BytesIO` to avoid unnecessary disk I/O), and parsing specific files from within ZIP archives using `pandas`.
* **`templates/index.html`**: The landing page uses a form styled with Bootstrap and custom CSS to resemble a professional financial tool. It includes an "Asset Glossary" that educates the user on the specific CVM XML block structure (e.g., Block 1 for Government Bonds, Block 4 for Stocks). It also implements a JavaScript-based status notification system to provide feedback during long API requests.
* **`templates/view.html`**: The results dashboard. This template renders the processed dataframe. It integrates the `DataTables` library (with jQuery) to transform a static HTML table into an interactive dashboard featuring pagination, instant text search, column sorting, and horizontal scrolling. It also utilizes the `DataTables Buttons` extension to allow users to export the parsed data directly to CSV or Excel.
* **`requirements.txt`**: Lists the necessary dependencies (`Flask`, `pandas`, `requests`) to replicate the environment.

### Design Decisions and Technical Challenges

During the development of CVM Intelligence, several critical design decisions were made to ensure usability and performance.

#### 1. Architecture: From Desktop (Tkinter) to Web (Flask)
Initially, I prototyped this idea using a Python desktop GUI with Tkinter. However, I realized that a desktop app limits accessibility and requires local installation. A web architecture makes it accessible from any browser, and easier to deploy. This transition allowed me to utilize web technologies like Bootstrap for a superior UI and JavaScript for client-side interactivity.

#### 2. Handling Latency and User Experience
One of the main challenges was the latency of the government servers. Downloading a ZIP file and extracting it took several seconds. To mitigate this, I implemented a client-side JavaScript status box in `index.html`. When the form is submitted, the DOM is updated to show a loading spinner and a sequence of messages ("Connecting...", "Downloading...", "Rendering..."). This keeps the user informed about the backend state.

#### 3. Performance Optimization: Server-side vs. Client-side
The CVM CSV files can contain tens of thousands of rows. Attempting to render 50,000 HTML table rows (`<tr>`) caused the browser to crash or lag significantly due to DOM overload. I solved this using a hybrid approach:
* **Server-Side:** I utilized `df.head(100)` in `app.py` to limit the initial HTML payload, ensuring the page loads instantly.
* **Client-Side:** I implemented `DataTables` with `scrollX: true`. This handles horizontal scrolling for the wide financial datasets without breaking the page layout.
* **Export Capability:** Realizing that analysts often need the full dataset, I added the `Buttons` extension. This allows the user to view a sample on the web but download the complete structured data to Excel for deep analysis.

### Acknowledgements and Use of AI

In accordance with the CS50x policy on the use of AI tools, I state that I utilized **Google Gemini** to assist in the development of this project. The AI was used in the following:

* **Debugging:** Helping to identify syntax errors in the `DataTables` JavaScript configuration and the correct parameters for Pandas' `to_html` method.
  
* **Refactoring:** Assisting in the translation of the original codebase from Portuguese to English and converting my legacy Tkinter logic into Flask routes.
  
* **Documentation:** Translating drafts for this README file and the project description.

The core logic regarding the CVM data structure, the choice of libraries, and the architectural shift from desktop to web were my own decisions.
