import requests

from api.config import BOOK_ENDPOINT


class Book:
    def __init__(self, isbn: int) -> None:
        self.isbn = isbn
        self.publisher = None
        self.publish_date = None
        self.title = None
        self.price = None
        self.pages = None
        self.c_code = None
        self.category_code = None
        self.has_image = None
        self.authors = None
        self.subjects = None
    
    def search(self):
        params = {
            "isbn": self.isbn
        }
        response = requests.get(BOOK_ENDPOINT, params=params)
        book_info_dict = response.json()[0]
        self.extract_info(book_info_dict)

    def extract_info(self, data: dict):
        self.title = data["onix"]["DescriptiveDetail"]["TitleDetail"]["TitleElement"]["TitleText"]["content"]

        self.authors = data["onix"]["DescriptiveDetail"]["Contributor"]
        self.authors = [author["PersonName"]["content"] for author in self.authors]
        self.authors = ["".join(author.split()) for author in self.authors]

        self.pages = data["onix"]["DescriptiveDetail"]["Extent"][0]["ExtentValue"]

        for i, j in enumerate(data["onix"]["DescriptiveDetail"]["Subject"]):
            if i == 0:
                self.c_code = j["SubjectCode"]
            elif i == 1:
                self.category_code = j["SubjectCode"]
            elif i == 2:
                self.subjects = j["SubjectHeadingText"]
                self.subjects = self.subjects.split(" ")
                self.subjects = [subject for subject in self.subjects]

        try:
            self.has_image = data["onix"]["CollateralDetail"]["SupportingResource"][0]["ResourceVersion"][0]["ResourceLink"]
            self.has_image = True
        except:
            print('book image not found')
            self.has_image = False

        self.publisher = data["onix"]["PublishingDetail"]["Imprint"]["ImprintName"]
        self.publish_date = data["onix"]["PublishingDetail"]["PublishingDate"][0]["Date"]

        self.price = data["onix"]["ProductSupply"]["SupplyDetail"]["Price"][0]["PriceAmount"]

        self.cover = data["summary"]["cover"]