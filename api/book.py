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

    def search_subjects(self, subject_list: list) -> list:
        subject_list = subject_list.split(" ")
        if len(subject_list) == 1:
            subject_list = subject_list[0].split(";")
        return [subject for subject in subject_list]

    def remove_space(self, keyword: str) -> str:
        return "".join(keyword.split())

    def extract_info(self, data: dict):
        self.title = data["onix"]["DescriptiveDetail"]["TitleDetail"]["TitleElement"]["TitleText"]["content"]
        self.title = self.remove_space(self.title)

        self.authors = data["onix"]["DescriptiveDetail"]["Contributor"]
        self.authors = [author["PersonName"]["content"] for author in self.authors]
        self.authors = [self.remove_space(author) for author in self.authors]

        try:
            self.pages = data["onix"]["DescriptiveDetail"]["Extent"][0]["ExtentValue"]
        except KeyError:
            self.pages = 0

        try:
            subjects = data["onix"]["DescriptiveDetail"]["Subject"]
            for i, j in enumerate(subjects):
                try:
                    code = str(j["SubjectCode"])
                    print(code)
                    if (len(code) == 4):
                        self.c_code = j["SubjectCode"]
                    elif (len(code) == 2):
                        self.category_code = j["SubjectCode"]
                    else:
                        print("key Error")
                except KeyError:
                    self.subjects = j["SubjectHeadingText"]
                    self.subjects = self.search_subjects(self.subjects)
        except KeyError:
            pass


        try:
            self.has_image = bool(data["onix"]["CollateralDetail"]["SupportingResource"][0]["ResourceVersion"][0]["ResourceLink"])
        except KeyError:
            self.has_image = False

        self.publisher = data["onix"]["PublishingDetail"]["Imprint"]["ImprintName"]
        self.publisher = self.remove_space(self.publisher)
        self.publish_date = data["onix"]["PublishingDetail"]["PublishingDate"][0]["Date"] if data["onix"]["PublishingDetail"]["PublishingDate"][0]["Date"] else None

        try:
            self.price = data["onix"]["ProductSupply"]["SupplyDetail"]["Price"][0]["PriceAmount"]
        except KeyError:
            pass

        self.cover = data["summary"]["cover"]