import re
from bs4 import BeautifulSoup


class LiveScheduleScraper:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'lxml')

    def extract_commands_to_dict(self):
        commands_dict = {}
        commands = self.soup.find_all('a', class_='filter-item-event--20qx1S')
        for command in commands:
            name = command.span.text
            href = command.get('href')
            if self.is_valid_name(name=name):
                commands_dict[name] = href
        return commands_dict

    def is_valid_name(self, name):
        return '(' not in name and ')' not in name and not re.search('U\d\d', name)
