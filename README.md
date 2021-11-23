# Arjuna: Generate Indonesian Poets and Poems using python base NLP model 

Arjuna is a NLP Project to generate poets and poems based on Bahasa language. This repository is sources that used at PyCon ID 2021 talks created by [@miqdude](https://github.com/miqdude) and [@veronicaads](https://github.com/veronicaads).

This repository consist two main folder: scraper and model. 

## Scraper 

This folder contains python script that used to do web scraping to https://www.kompas.id/kategori/sastra/ as dataset for the model.

You need to register to  https://www.kompas.id first before use this scraper to fill the email and password parameter.

```
python kompas_sastra_scraper.py --user_email xxxxx@email.com --password xxxxxxxxxx --depth 5
```

## Model



