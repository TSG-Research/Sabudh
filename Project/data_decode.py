from import_modules import*
data=bz2.open("D:\\Sabudh Practice\\enwiki-20170820-pages-articles.xml.bz2",'rb')
def decode_data():
    bytes_to_read=10000000 # 10 mb
    data_subset = data.readlines(bytes_to_read)
    new_data = [x.decode() for x in data_subset]
    data1 = ''.join(new_data)
    soup = bs(data1, 'lxml')
    titles = soup.find_all('text') # titles stores the text content 
    return titles