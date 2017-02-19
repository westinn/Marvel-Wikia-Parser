import urllib
from lxml import html
import requests


class MarvelParser:
    """
        allComicsURL = the initial URL of the character/comics to parse through

        yearToStart  = the year from which to select comic series from.
                        Select only series that start after yearToStart.
    """

    def __init__(self, year_to_start=0, all_comics_url='http://marvel.wikia.com/wiki/Spider-Man_Comic_Books'):
        """
            Construct parser that grabs all comics found at all_comics_url that start on or after year_to_start.

            If all_comics_url isn't passed it will parse Spider-Man comics
            If year_to_start isn't passed it will use 0 as default
        """
        self.year_to_start = year_to_start
        self.all_comics_url = all_comics_url

    # issueName, issueNum, seriesName, releaseDate, issueID, seriesID, imageURL
    def save_issue_data(self, issue_url):
        """
            Write an issues data as a csv file

            example:

            issueName,issueNum,seriesName,releaseDate,image,issueID,seriesID
            The Hunger: Part 1 of 5,1,The Spectacular Spider-Man Vol 2,"September, 2003",1,1
            The Hunger: Part 2 of 5,2,The Spectacular Spider-Man Vol 2,"September, 2003",2,1
        """

        print(issue_url)

        page = requests.get(issue_url)
        tree = html.fromstring(page.content)

        issueName = tree.xpath(
            # '//*[@id="mw-content-text"]/table[1]/tr/td/div/table/tr/th/div/b/a'
            # '//*[@id="mw-content-text"]/table[1]/tr[1]/td/div/table/tr[1]/th/div/b/a')[0].strip()
            '//*[@id="mw-content-text"]/table[1]/tr[1]/td/div/table/tr[1]/th/div/b/a/text()')[0].strip()
        seriesName = tree.xpath(
            '//*[@id="mw-content-text"]/table[1]/tr[1]/td/div/div[2]/div[1]/a/text()')[0].strip()

        imageURL = tree.xpath(
            '//*[@id="templateimage"]/div/div/a/img/@src')[0]
        imageURL = imageURL[:imageURL.find('.jpg') + 4].strip()

        issueNum = tree.xpath(
            '//*[@id="mw-content-text"]/table[1]/tr[1]/td/div/div[2]/div[1]/text()')[0]
        issueNum = issueNum[issueNum.find('#') + 1:].strip()

        releaseDate = tree.xpath(
            '//*[@id="mw-content-text"]/table[1]/tr[1]/td/div/div[2]/div[2]/a/text()')
        if len(releaseDate) == 0:
            releaseDate = tree.xpath('//*[@id="mw-content-text"]/table[1]/tr[1]/td/div/div[2]/div[2]/div[4]/a/text()')
        elif len(releaseDate) == 0:
            releaseDate = tree.xpath('//*[@id="mw-content-text"]/table[1]/tr[1]/td/div/div[2]/div[2]/div[4]/text()')
        else:
            releaseDate = releaseDate[0].strip() + ', ' + releaseDate[1].strip()
        print(releaseDate)
        releaseDate.strip()

        print(releaseDate)
        entry = [issueName, issueNum, seriesName, releaseDate, imageURL]
        print(entry)

    # write to character.csv
    # charName, typeOfChar, earthID, issueID, charID
    def save_character_data(self, data, columns, here):
        """
            Write a character data as a csv file

            example:

            "Name","Race","Homeworld","Affiliation"
            "C-3 PO","Droid","Unknown","rebels"
            "Chewbacca","Wookie","Kashyyyk","rebels"
            "Darth Vader","Human","Unknown","empire"
            "Han Solo","Human","Corellia","rebels"
        """
        # For each parameter,
        #    save it in the proper column

    def parse_series_data(self):
        """
            Grabs a comic series's data and calls another function to write the data to an excel spreadsheet
        """

        # Go to a series URL
        # For every issue in the series,
        #   click it and parse all data of that issue
        #   save it as a list
        #   pass all data in that issues page to save_series_data funtcion

        valid_series_urls = self.grab_series_url()

        for series_url in valid_series_urls:
            page = requests.get(series_url)
            tree = html.fromstring(page.content)

            home_url = 'http://marvel.wikia.com'
            issue_url_endings = tree.xpath('//*[contains(@id,"gallery")]/div[*]/div[*]/div/b/a/@href')
            issue_urls = [home_url + issue for issue in issue_url_endings]
            [self.save_issue_data(issue_url) for issue_url in issue_urls]

    def grab_series_url(self):
        """
            Returns a list of URLs (list of comic book series) to look in and grab data from.

            Grabs the series that start after this MarvelParsers yearToStart year.
        """

        # For every comic visible at the given link
        #   look for series that start on or after year_to_start
        #   add that series URL to the list
        # return that valid_series_urls

        page = requests.get(self.all_comics_url)
        tree = html.fromstring(page.content)

        home_url = 'http://marvel.wikia.com'
        series_start_dates = tree.xpath('//*[@id="gallery-0"]/div[*]/div[2]/center/i/a[1]/text()')
        series_start_dates = list(map(int, series_start_dates))
        series_urls = tree.xpath('//*[@id="gallery-0"]/div[*]/div[*]/center[i/a[1]/@href]/b/a/@href')

        valid_series_urls = [home_url + comic for index, comic in enumerate(series_urls)
                             if series_start_dates[index] >= self.year_to_start]

        return valid_series_urls

    def parse(self):
        self.parse_series_data()


# =====================================================================================================================


#   Executable
# =====================================================================================================================

if __name__ == "__main__":
    # default = MarvelParser()
    # print("Default:\n")
    # default.grab_series_url()

    twok = MarvelParser(2000)
    print("2000+:\n")
    twok.parse()
