import io
import zipfile
import requests
import pandas as pd
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = "cvm_secret_key" 

class CVMExtractor:
    def __init__(self):
        self.base_url = 'https://dados.cvm.gov.br/dados/FI/DOC/CDA/DADOS/{}cda_fi_{}{}.zip'

    def get_data_as_df(self, year, month=None, block_id=None):
        
        #URL example since 2023
        #https://dados.cvm.gov.br/dados/FI/DOC/CDA/DADOS/cda_fi_202506.zip
        if int(year) >= 2023:
            url = self.base_url.format("",year, month)
        
        #URL example pre 2023
       #https://dados.cvm.gov.br/dados/FI/DOC/CDA/DADOS/HIST/cda_fi_2022.zip
        elif int(year) < 2023:
            url = self.base_url.format("HIST/", year,"")
        
        
        headers = {'User-Aent': 'Mozilla/5.0'}
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None, f"CVM Error: Status {response.status_code}"

        block_filter = f'BLC_{block_id}'
        
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            file_list = zip_ref.namelist()
            target = [f for f in file_list if block_filter in f]
            
            if not target:
                return None, f"Block {block_id} not found for this date."

            # Read the first found file directly into a DataFrame
            with zip_ref.open(target[0]) as csv_file:
                # CVM files typically use ';' as a separator
                df = pd.read_csv(csv_file, sep=';', encoding='iso-8859-1')
                return df,
                
                one

extractor = CVMExtractor()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        year = request.form.get("ano")
        month = request.form.get("mes")
        block_id = request.form.get("bloco")

        df, error = extractor.get_data_as_df(year, month, block_id)
        
        if error:
            flash(error)
            return render_template("index.html")


        table_html = df.head(100).to_html(classes='table table-hover', table_id='cvmTable', index=False)
        return render_template("view.html", table=table_html, year=year, month=month, block=block_id)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)