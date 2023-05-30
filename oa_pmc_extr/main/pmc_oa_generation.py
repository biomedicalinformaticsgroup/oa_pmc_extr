import wget
from bs4 import BeautifulSoup
import os
from datetime import date
import time
import tarfile
import re
import unicodedata
import glob

def xml_clean_soup(soup):
    # here is a list of tags that i want to remove before i extract the text
    # these include links, scripts, supplemnetal tags, references, tables, authors
    tag_remove_list = ['ref-list',
                       'supplementary-material',
                       'bibliography',
                       'tex-math',
                       'inline-formula',
                       'table',
                       'tbody',
                       'table-wrap',
                       'ack',
                       'fig',
                       'table-wrap-foot',
                       'surname',
                       'given-names',
                       'name',
                       'xref',
                       'element-citation',
                       'sup',
                       'td',
                       'tr',
                       'string-name',
                       'familyname',
                       'givennames',
                       'mixed-citation',
                       'author',
                       'aff',
                       'ext-link',
                       'link',
                       'pub-id',
                       'year',
                       'issue',
                       'th',
                       'floats-group',
                       'back',
                       'front',
                       'licensep',
                       'license',
                       'permissions',
                       'article-meta',
                       'url',
                       'uri',
                       'label',
                       'person-group'
                      ]
    # find all the tags matching any name in the list
    tags = soup.find_all(tag_remove_list)
    # loop through each tag and apply the decompose function to remove them from the soup
    for tag in tags:
        tag.decompose()
    return soup

def get_ab(soup):
    # set the defaul abstract value to None. 
    ab = ''
    # This list can be the options to look for abstract tags
    for tag in ['abstract','<dc:description>','<prism:description>']:
        # check for the tag's presence and then try and extrac the text.
        search_result = soup.find(tag)
        if search_result:
            ab = search_result.get_text(separator = u' ')
            if type(ab) == list:
                ab = ' '.join(ab)
            # if text is extracted then no need to try the other options.
            break
    return ab

def xml_body_p_parse(soup, abstract):
    # we'll save each paragraph to a holding list then join at the end
    p_text = []
    # keeping the abstract at the begining depending on the input
    p_text.append(abstract)
    # search the soup object for body tag
    body = soup.find('body')
    # if a body tag is found then find the main article tags
    if body:
        main = body.find_all(['article','component','main'])
        if main:
            # work though each of these tags if present and look for p tags
            for tag in main:
                ps = tag.find_all('p')
                if ps:
                    # for every p tag, extract the plain text, stripping the whitespace and making one long string
                    p_text.extend([p.text.strip() for p in ps if p.text.strip() not in p_text])
            # join each p element with a space 
            p_text = ' '.join(map(str,p_text))
        else:
            # when there is no body tag then the XML is not useful.
            p_text = ''
    else:
        # when there is no body tag then the XML is not useful.
        p_text = ''
    # ensure the p_text is a simplified string format even if the parsing fails    
    if p_text == [] or p_text == '' or p_text == ' ':
        p_text = ''
    return p_text

def pmc_oa_generation(path = './'): 
    #taking today date to create the output directory
    path = str(path + str(f"/pmc_oabulk_output"))
    try:
        os.mkdir(path)
    except:
        pass
    try:
        os.mkdir(f"{path}/unzip_files")
    except:
        pass
    try:
        os.mkdir(f"{path}/unzip_files/txt")
    except:
        pass
    try:
        os.mkdir(f"{path}/unzip_files/xml")
    except:
        pass
    try:
        os.mkdir(f"{path}/zip_files")
    except:
        pass
    try:
        os.mkdir(f"{path}/zip_files/txt")
    except:
        pass
    try:
        os.mkdir(f"{path}/zip_files/xml")
    except:
        pass
    try:
        os.mkdir(f"{path}/parsed_files")
    except:
        pass
    try:
        os.mkdir(f"{path}/parsed_files/txt")
    except:
        pass
    try:
        os.mkdir(f"{path}/parsed_files/xml")
    except:
        pass
    #loading the two ftp addresses where the files for the OA set are kept
    url = [
            'https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_noncomm/txt/',
            'https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_comm/txt/',
            'https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_other/txt/',
            'https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_noncomm/xml/',
            'https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_comm/xml/',
            'https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_other/xml/'
            ]
    #the code is going to extract every file for each parent link
    for j in range(len(url)):
        #downloading the page where the links to each files are stored
        print(f'Retrieving link: {url[j]}')
        print('\n')
        filename = wget.download(url[j], out=f'./{path}')
        #loadind the page
        soup = BeautifulSoup(open(f'{path}/download.wget'), features="lxml")
        #extracting the links to each of the files
        links = soup.find_all('a')
        links = links[1:]
        base_url = url[j]
        complete_links = []
        for i in range(len(links)):
            if links[i].attrs['href'] == 'https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_noncomm/' or links[i].attrs['href'] == 'https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_comm/' or links[i].attrs['href'] == 'https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_other/' or links[i].attrs['href'] == 'https://www.hhs.gov/vulnerability-disclosure-policy/index.html':
                pass
            else:
                complete_links.append(str(base_url) + str(links[i].attrs['href']))
        for i in range(len(complete_links)):
            try:
                #downlodaing the files in the pre-defines directory
                print(f' Retrieving link: {complete_links[i]}')
                print('\n')
                if '/txt/' in complete_links[i]:
                    filename = wget.download(complete_links[i], out=f"{path}/zip_files/txt")
                elif '/xml/' in complete_links[i]:
                    filename = wget.download(complete_links[i], out=f"{path}/zip_files/xml")
                #providing 1 second sleep to the server to be polite
                time.sleep(1)
            except:
                #if faillure to access the link, we still provide the one second to be polite and avoid being blocked
                time.sleep(1)
                #re-downlodaing the files in the pre-defines directory
                try:
                    failed_file = glob.glob(f'{path}/*.tmp')
                    for k in range(len(failed_file)):
                        os.remove(f'{failed_file[k]}')
                    print(f' Retrying to retrieve link: {complete_links[i]}')
                    print('\n')
                    if '/txt/' in complete_links[i]:
                        filename = wget.download(complete_links[i], out=f"{path}/zip_files/txt")
                    elif '/xml/' in complete_links[i]:
                        filename = wget.download(complete_links[i], out=f"{path}/zip_files/xml")
                    #providing 1 second sleep to the server to be polite
                    time.sleep(1)
                except:
                    failed_file = glob.glob(f'{path}/*.tmp')
                    for k in range(len(failed_file)):
                        print(f' Failed to retreive {failed_file[k]}')
                        os.remove(f'{failed_file[k]}')
                    time.sleep(1)
        os.remove(f'{path}/download.wget')
    print('\n')
    print('Retrieval process completed')
    #extracting all the files from the previously downloaded pre-defined directory
    for file in os.listdir(f"{path}/zip_files/txt"):   # get the list of files
        if '.tar.gz' in str(file): # if it is a zipfile, extract it
            # open file
            unzip_file = tarfile.open(str(f"{path}/zip_files/txt/") + str(file))
            # extracting file
            unzip_file.extractall(f"{path}/unzip_files/txt")
            unzip_file.close()
    print('\n')
    print('Unzip txt subdirectory process completed')
    
    for file in os.listdir(f"{path}/zip_files/xml"):   # get the list of files
        if '.tar.gz' in str(file): # if it is a zipfile, extract it
            # open file
            unzip_file = tarfile.open(str(f"{path}/zip_files/xml/") + str(file))
            # extracting file
            unzip_file.extractall(f"{path}/unzip_files/xml")
            unzip_file.close()
    print('\n')
    print('Unzip xml subdirectory process completed')

    #Extracting the absolute path to all the files
    file_to_create = glob.glob(f"{path}/unzip_files/txt/*")
    list_to_parse = []
    for i in range(len(file_to_create)):
        try:
            os.mkdir(file_to_create[i])
        except:
            pass
        list_to_parse.append(file_to_create[i].split('/')[-1])
    for i in range(len(list_to_parse)):
        list_to_extract = glob.glob(f"{path}/unzip_files/txt/{list_to_parse[i]}/*.txt")
        print(f'Parsing {list_to_parse[i]} .txt')
        for j in range(len(list_to_extract)):
            try:
                f = open(list_to_extract[j], "r")
                text = f.read().encode('utf-8', 'ignore').decode()
                f.close()
                curent_list = text.split('\n')
                lower = 0
                upper = len(curent_list)
                for j in range(len(curent_list)):
                    if curent_list[j] == '==== Body':
                        lower = j+1
                    if curent_list[j] == '==== Refs':
                        upper = j-1
                curent_text = str(' '.join(curent_list[lower:upper]))
                curent_text = unicodedata.normalize("NFKD", curent_text)
                curent_text = curent_text.replace('\t', ' ')
                try:
                    curent_text = curent_text.replace('\\u', ' ')
                except:
                    pass
                r = open(f"{path}/parsed_files/txt/{list_to_parse[i]}/{list_to_extract[j].split('/')[-1].split('.')[0]}.txt", "w+")
                r.write(str(curent_text))
                r.close()
            except:
                    pass
        
    file_to_create = glob.glob(f"{path}/unzip_files/xml/*")
    list_to_parse = []
    for i in range(len(file_to_create)):
        try:
            os.mkdir(file_to_create[i])
        except:
            pass
        list_to_parse.append(file_to_create[i].split('/')[-1])
    for i in range(len(list_to_parse)):
        list_to_extract = glob.glob(f"{path}/unzip_files/xml/{list_to_parse[i]}/*.xml")
        print(f'Parsing {list_to_parse[i]} .xml')
        for j in range(len(list_to_extract)):
            try:
                with open(f"{list_to_extract[j]}", "r") as f:
                    # Read each line in the file, readlines() returns a list of lines
                    content = f.readlines()
                # Combine the lines in the list into a string
                content = "".join(content)
                f.close()
                soup = BeautifulSoup(content, features = 'lxml')
                soup = xml_clean_soup(soup)
                ab = get_ab(soup)
                p_text = xml_body_p_parse(soup, ab)
                if p_text != '':
                    r = open(f"{path}/parsed_files/xml/{list_to_parse[i]}/{list_to_extract[j].split('/')[-1].split('.')[0]}.txt", "w+")
                    r.write(str(p_text.replace('\n', '')))
                    r.close()
            except:
                    pass

    print('\n')
    print('Generation of the files for the parsed text completed')
    print('\n')
    print('Process completed')