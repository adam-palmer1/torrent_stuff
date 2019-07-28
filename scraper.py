from bs4 import BeautifulSoup
import PTN

def scrape(t):
    entries = []
    soup = BeautifulSoup(t, 'html.parser')
    search = soup.find(id='searchResult')
    try:
        results = search.find_all('tr')
    except:
        return entries
    for result in results:
        entry = result.find('div', {"class":'detName'})
        if entry is None:
            continue
        try:
            entry_name = result.find('a', {'class':'detLink'})['title'].replace("Details for ", "")
            entries.append({
                'entry_name': entry_name,
                'entry_link':  result.find('a', {'title':'Download this torrent using magnet'})['href'],
                'entry_seeds': result.find_all('td', {'align':'right'})[0].text,
                'entry_leech': result.find_all('td', {'align':'right'})[1].text,
                'entry_info':  PTN.parse(entry_name)
            })
        except Exception as e:
            print("Parse error")
    return entries
