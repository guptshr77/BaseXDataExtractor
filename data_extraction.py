from BaseXClient import BaseXClient
import xml.etree.ElementTree as ET
import pandas as pd
import re

# get csv for authors 
def get_authors(id_num):
    session = BaseXClient.Session('localhost', 1984, 'test', 'test')
    query_string = f"for $doc in collection('{database}') where contains(document-uri($doc), '{id_num}') return $doc//name"
    query = session.query(query_string)
    result = query.execute()

    names = result.split('\n')
    
    for name in names:
        name = name.strip()
        if not name:
            continue 
        if not name.startswith("<name") or not name.endswith("</name>"):
            # bad formated XML
            continue
        name = re.sub(r' xmlns="[^"]+"', '', name)
        root = ET.fromstring(name)
        if not list(root) and root.text:
            name_building = " ".join(root.itertext()).strip()
        else:
            name_building = " ".join(root.itertext()).strip()
            tags = ['given-names', 'surname']
            for tag in tags:
                elem = root.find(tag)
                if elem is not None and elem.text:
                    content = elem.text.strip()
                    if content:
                        context_ungrouped['label'].append(tag)
                        output = '[name] ' + content
                        context_ungrouped['text'].append(output)
                        name_building = name_building + content + " "

            if name_building:
                # grouped author
                grouped_output['label'].append('name')
                grouped_output['text'].append(name_building)

    query.close()
    session.close()

# get csv for affiliations 
def get_affiliation(id_num):
    session = BaseXClient.Session('localhost', 1984, 'test', 'test')
    
    query_string = f"for $doc in collection('{database}') where contains(document-uri($doc), '{id_num}') return $doc//aff"
    query = session.query(query_string)
    result = query.execute()

    affs = result.split('\n')
    
    for aff in affs:
        aff = aff.strip()
        if not aff:
            continue 
        if not aff.startswith("<aff") or not aff.endswith("</aff>"):
            # bad formated XML
            continue
        aff = re.sub(r' xmlns="[^"]+"', '', aff)
        root = ET.fromstring(aff)
        if not list(root) and root.text:
            aff_building = " ".join(root.itertext()).strip()
        else:
            aff_building = " ".join(root.itertext()).strip()
            tags = ['label', 'addr-line', 'sup', 'institution', 'country', 'email']
            
            for tag in tags:
                elem = root.find(tag)
                if elem is not None and elem.text:
                    content = elem.text.strip()
                    if content:
                        #Ungrouped label context
                        context_ungrouped['label'].append(tag)
                        output = '[aff] ' + content
                        context_ungrouped['text'].append(output)
                        aff_building = aff_building + content + " "
            
            if aff_building:
                # grouped affiliation
                grouped_output['label'].append('aff')
                grouped_output['text'].append(aff_building)

    query.close()
    session.close()

# get csv for citations
def get_citation(id_num):
    session = BaseXClient.Session('localhost', 1984, 'test', 'test')
    # try:
    query_string = f"for $doc in collection('{database}') where contains(document-uri($doc), '{id_num}') return $doc//element-citation"
    query = session.query(query_string)
    result = query.execute()
    namespaces = {'ns': 'publication-type="journal"'}

    # Split the result into individual XML documents
    start_tag = '<element-citation'
    end_tag = '</element-citation>'
    start_index = 0
    
    while True:
        start = result.find(start_tag, start_index)
        if start == -1:
            break
        
        end = result.find(end_tag, start + len(start_tag))
        if end == -1:
            break
        
        xml_doc = result[start:end + len(end_tag)]
        start_index = end + len(end_tag)

        root = ET.fromstring(xml_doc)
        temp = ""
        tags = [
            'person-group', 'source', 'year', 'publisher-loc', 'publisher-name',
            'lpage', 'article-title', 'volume', 'fpage', 'pub-id', 'comment',
            'collab', 'issue', 'conf-name', 'conf-date', 'conf-loc', 'month',
            'day', 'edition', 'date-in-citation', 'page-range', 'series', 'gov',
            'size', 'elocation-id', 'supplement', 'season', 'etal', 'patent',
            'name', 'ext-link', 'chapter-title', 'part-title'
        ]   
        for tag in tags:
            if tag == "person-group":
                person_group = root.find(".//person-group")
                if person_group is not None:
                    for person in person_group.findall(".//name"):
                        surname = person.find("surname")
                        given_names = person.find("given-names")

                        surname_text = surname.text.strip() if surname is not None and surname.text else ""
                        given_names_text = given_names.text.strip() if given_names is not None and given_names.text else ""

                        full_name = f"{given_names_text} {surname_text}".strip()
                        
                        if full_name:
                            # make one ungrouped without the context and one with context (surname alone vs with persongroup label)
                            context_ungrouped['label'].append('person-group[name[surname]]')
                            output = "[element-citation]" + surname_text
                            context_ungrouped['text'].append(output)
                            context_ungrouped['label'].append('person-group[name[given-names]]')
                            output = "[element-citation]" + given_names_text
                            context_ungrouped['text'].append(output)
                            temp += full_name
                            
            else:
                elem = root.find(f".//{tag}")
                if elem is not None:
                    value = elem.text.strip() if elem.text else ""
                    context_ungrouped['label'].append(tag)
                    output = '[element-citation] ' + value
                    context_ungrouped['text'].append(output)
                    temp += value + ' '

        if temp:
            grouped_output['label'].append('element-citation')
            grouped_output['text'].append(temp)
        else:
            break
    query.close()
    session.close()
    
#get csv for title
def get_title(id_num):
    session = BaseXClient.Session('localhost', 1984, 'test', 'test')

    query_string = f"for $doc in collection('{database}') where contains(document-uri($doc), '{id_num}') return $doc//title-group"
    query = session.query(query_string)
    result = query.execute()

    names = result.split('\n')
    
    for name in names:
        name = name.strip()
        if not name:
            continue 
        if not name.startswith("<title-group") or not name.endswith("</title-group>"):
            # bad formated XML
            continue
        name = re.sub(r' xmlns="[^"]+"', '', name)
        root = ET.fromstring(name)
        if not list(root) and root.text:
            title = " ".join(root.itertext()).strip()
        else:
            title = " ".join(root.itertext()).strip() 
            root = ET.fromstring(name)
            tags = ['article-title', 'alt-title', 'subtitle']
            for tag in tags:
                elem = root.find(tag)
                content = elem.text.strip() if elem is not None and elem.text else ""
                if content:
                    context_ungrouped['label'].append(tag)
                    output = '[title-group] ' + content
                    context_ungrouped['text'].append(output)
                    title = title + output + " "

            if title:
                # grouped title
                grouped_output['label'].append('title-group')
                grouped_output['text'].append(title)

    query.close()
    session.close()


def create_file():
    counter = 0
    with open('DocIds2.txt', 'r') as file:
        with open('incomplete_outputIds2.txt', 'a', encoding='utf-8') as ids:
            for line in file:
                id = line.strip()
                # if id and counter < 50:
                print(f"Processing ID: {id}")
                get_authors(id) 
                get_affiliation(id)
                get_citation(id)
                get_title(id)
                ids.write(id + '\n')
                    # counter += 1

    grouped_output_df = pd.DataFrame(grouped_output)
    grouped_output_df.dropna()
    grouped_output_df.drop_duplicates()
    grouped_output_df.to_csv('grouped2.csv', index=False, index_label=False)
    context_ungrouped_df = pd.DataFrame(context_ungrouped)
    context_ungrouped_df.dropna()
    context_ungrouped_df.drop_duplicates()
    context_ungrouped_df.drop_duplicates().to_csv("ungrouped_with_metadata2.csv", index=False)
    print("done")
    file.close()
    
grouped_output = {'label': [], 'text': []}
context_ungrouped = {'label': [], 'text': []}
database = "PMC002"
create_file()
