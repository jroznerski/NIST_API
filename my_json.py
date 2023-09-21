#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json
import re


# In[2]:


with open('dane.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

df = pd.DataFrame(data)

vulnerabilities_list = []

vulnerabilities_info = df['vulnerabilities']

for vulnerability in vulnerabilities_info:
    cve_info = vulnerability['cve']
    cve_id = cve_info['id']
    descriptions = cve_info['descriptions']
    
    for desc in descriptions:
        lang = desc['lang']
        if lang == 'en': 
            description = desc['value'].replace('\n', '')
            references = cve_info.get('references', [])
            for reference in references:
                url = reference.get('url', '')
                vulnerabilities_list.append([cve_id, description, url])

vulnerabilities_df = pd.DataFrame(vulnerabilities_list, columns=['CVE-ID', 'Description', 'URL'])

vulnerabilities_df = vulnerabilities_df.dropna(how='any')

vulnerabilities_df.to_csv('vulnerabilities.csv', index=False)

print("Dane zapisane do pliku vulnerabilities.csv")


# In[3]:


df_app = pd.read_csv('aplikacje.csv', encoding='latin1')
df_app['Nazwa aplikacji'] = df_app['Nazwa aplikacji'].str.lower()
df_app.to_csv('aplikacje.csv', index=False)


# In[4]:


df_aplikacje = pd.read_csv('aplikacje.csv')
df_vulnerabilities = pd.read_csv('vulnerabilities.csv')

unikalne_wyrazy = df_aplikacje['Nazwa aplikacji'].unique()

pasujace_wyrazy = {}

for wyraz in unikalne_wyrazy:
    unikalne_wyrazy_esc = re.escape(wyraz)
    wyrazenie_regularne = fr'\b{unikalne_wyrazy_esc}\b'
    pasujace_indeksy = df_vulnerabilities[df_vulnerabilities['Description'].str.contains(wyrazenie_regularne, flags=re.IGNORECASE, na=False)].index.tolist()
    if pasujace_indeksy:
        pasujace_wyrazy[wyraz] = pasujace_indeksy

df_połączone = df_vulnerabilities[df_vulnerabilities.index.isin([indeks for indeksy in pasujace_wyrazy.values() for indeks in indeksy])]

df_połączone.to_csv('połączone.csv', index=False)

for wyraz, indeksy in pasujace_wyrazy.items():
    print(f"Powtarzający się tekst: {wyraz}")
    print(f"Indeksy: {indeksy}")

