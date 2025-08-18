from urllib.parse import quote_plus

class ElComercioUrlBuilder:
    BASE_URL = "https://www.elcomercio.com"
    
    @classmethod
    def build_search_url(cls, search_term: str) -> str:
        encoded_term = quote_plus(search_term)
        return f"{cls.BASE_URL}/?s={encoded_term}"
    
    @classmethod
    def build_section_url(cls, section: str = "ultima-hora") -> str:
        return f"{cls.BASE_URL}/{section}/"