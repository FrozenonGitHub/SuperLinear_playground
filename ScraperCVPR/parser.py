from bs4 import BeautifulSoup

# Load the raw HTML
with open('cvpr2024_raw.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all papers
papers = []
for paper in soup.find_all('dt', class_='ptitle'):
    paper_title = paper.find('a').text.strip()
    paper_link = paper.find('a')['href']
    authors = []

    # Move to the corresponding dd element for authors
    sibling_dd = paper.find_next_sibling('dd')
    if sibling_dd:
        forms = sibling_dd.find_all('form')
        for form in forms:
            author_name = form.find('input', {'name': 'query_author'})['value']
            authors.append(author_name)

    papers.append({
        'title': paper_title,
        'link': paper_link,
        'authors': authors,
    })

# Print the parsed data
for paper in papers:
    print(f"Title: {paper['title']}")
    print(f"Link: {paper['link']}")
    print(f"Authors: {', '.join(paper['authors'])}")
    print()
