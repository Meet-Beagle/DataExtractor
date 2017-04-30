"""
Class to extract useful information from an HTML document. Right now, I implemented only the ability to extract information
 from the EMBO webpage of conferences

"""

from bs4 import BeautifulSoup
import json

__author__ = "Karsten"
__date__ = "2017-04-30"

class DataExtractor:

    def __init__(self, file_contents, remove_characters = ('\n', '\xa0'), end_of_line_char = '|', data_types=('conference', 'location', 'date')):
        self.file_contents = file_contents # todo make this into property
        # todo use file_contents property to dynamically construct the BeautifulSoup object
        self.remove_characters = remove_characters
        self.end_of_line_char = end_of_line_char
        self.soup = BeautifulSoup(file_contents, 'html.parser')

    @staticmethod
    def export(filename, *data):
        # todo add append mode
        # todo use George's json class to save the data to a json file
        conferences, locations, dates = data[0]
        keys = [''.join((c.lower(),l.lower(),d.lower())) for c,l,d in zip(conferences, locations, dates)]

        assert len(conferences) == len(locations) == len(dates)

        n_entries = len(conferences)
        database = dict( zip(keys, zip(conferences, locations, dates)) )
        print(database)
        with open(filename, mode='a') as file:
            json.dump(database, file)

    @classmethod
    def run_example(cls):
        file_contents = open('mock_webpage.html').read()
        data = DataExtractor(file_contents).perform_extraction()
        DataExtractor.export('mock_file.json', data)

    def _get_data_(self, html_class, html_structure='span'):
        return [el.get_text() for el in self.soup.find_all(html_structure, class_=html_class)]

    def _get_dates_(self):
        return [el.split(self.end_of_line_char)[0] for el in self._get_data_(html_class='date')]

    def _get_locations_(self):
        return [el.split(self.end_of_line_char)[1] for el in self._get_data_(html_class='date')]

    def _get_conferences_(self):
        return self._get_data_(html_class='event-title')

    def _remove_characters_(self, data: list):
        """
        Removes selected characters from the extracted data.
        :return: 
        """
        return [el.translate({ord(c): None for c in self.remove_characters}) for el in data]


    def perform_extraction(self):
        return self._get_conferences_(), self._get_dates_(), self._get_locations_()

if __name__ == '__main__':
    DataExtractor.run_example()

