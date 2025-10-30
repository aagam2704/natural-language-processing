$env:JAVA_HOME='C:\Program Files\Android\Android Studio\jbr'
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
Set-Location 'C:\Users\Aagam\OneDrive\Desktop\big_data_project\Real-Time-Twitter-Sentiment-Analysis\Django-Dashboard'
. 'C:\Users\Aagam\OneDrive\Desktop\big_data_project\Real-Time-Twitter-Sentiment-Analysis\venv\Scripts\Activate.ps1'
python manage.py runserver
