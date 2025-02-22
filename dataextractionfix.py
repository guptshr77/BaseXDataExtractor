from BaseXClient import BaseXClient
import xml.etree.ElementTree as ET
import pandas as pd


#get csv for title
def get_title(id_num):
    session = BaseXClient.Session('localhost', 1984, 'test', 'test')
    try:
        query_string = f"for $doc in collection('{database}') where contains(document-uri($doc), '{id_num}') return $doc//title-group"
        query = session.query(query_string)
        result = query.execute()

        names = result.split('\n')
        
        for name in names:
            try:
                root = ET.fromstring(name)

                article_title_elem = root.find('article-title')
                alt_title_elem = root.find('alt-title')

                article_title = article_title_elem.text.strip() if article_title_elem is not None else ""
                alt_title = alt_title_elem.text.strip() if alt_title_elem is not None else ""
                if article_title or alt_title:
                    # grouped title
                    title = f"{article_title}"
                    grouped_output['label'].append('title')
                    grouped_output['text'].append(title)
                    
                    if article_title:
                        #ungrouped title
                        context_ungrouped['label'].append('article-title')
                        output = '[title-group] ' + article_title
                        context_ungrouped['text'].append(output)
                        #ungrouped title non context
                        noncontext_ungrouped['label'].append('article-title')
                        noncontext_ungrouped['text'].append(article_title)
                    if alt_title:
                        #ungrouped title
                        context_ungrouped['label'].append('alt-title')
                        output = '[title-group] ' + alt_title
                        context_ungrouped['text'].append(output)
                        #ungrouped title non context
                        noncontext_ungrouped['label'].append('alt-title')
                        noncontext_ungrouped['text'].append(alt_title)
            except ET.ParseError as e:
                print(f"XML ParseError: {e}")
            except Exception as e:
                print(f"Error: {e}")
        query.close()
    except BaseXClient.Error as e:
        print(f"BaseXClient Error: {e}")
    finally:
        session.close()

def create_file():
    counter = 0
    try:
        with open('DocIds2.txt', 'r') as file:
            with open('incomplete_outputIds2.txt', 'a', encoding='utf-8') as ids:
                for line in file:
                    id = line.strip()
                    # if id and counter < 5:
                    print(f"Processing ID: {id}")
                    # get_authors(id) 
                    # get_affiliation(id)
                    get_citation(id)
                    # get_title(id)
                    ids.write(id + '\n')
                        # counter += 2
    except IOError as e:
        print(f"IOError: {e}")
    except Exception as e:
        print(f"Error: {e}")

    grouped_output_df = pd.DataFrame(grouped_output)
    grouped_output_df.dropna()
    grouped_output_df.drop_duplicates()
    grouped_output_df.to_csv('groupted_data2.csv', index=False, index_label=False)
    context_ungrouped_df = pd.DataFrame(context_ungrouped)
    context_ungrouped_df.dropna()
    context_ungrouped_df.drop_duplicates()
    context_ungrouped_df.drop_duplicates().to_csv("context_ungrouped2.csv", index=False)
    noncontext_ungrouped_df = pd.DataFrame(noncontext_ungrouped)
    noncontext_ungrouped_df.dropna()
    noncontext_ungrouped_df.drop_duplicates()
    noncontext_ungrouped_df.drop_duplicates().to_csv("noncontext_ungrouped2.csv", index=False)
    print("done")
    file.close()
    
grouped_output = {'label': [], 'text': []}
context_ungrouped = {'label': [], 'text': []}
noncontext_ungrouped = {'label': [], 'text': []}
database = "PMC002"
create_file()