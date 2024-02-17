# Programmatically Filling out a PDF

This is an example of how to programmatically fill out a PDF using pypdf.

I found the guide for [interacting with PDF
forms](https://pypdf.readthedocs.io/en/stable/user/forms.html) in pypdf
somewhat sparse. As such I wrote this application note to help others get
started with using the library.

# Setup and Run

In terminal install dependencies:
```zsh
python -m pip install -r requirements.txt
```

Run worked example script as follows:
```
mkdir output
python prepopulate.py

# Will populate output folder with filled pdfs.
```
