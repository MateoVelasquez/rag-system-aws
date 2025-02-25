"""Service to get articles from Wikipedia."""
import wikipediaapi

from ..config import settings


class WikipediaService:
    """Retriever articles from Wikipedia."""
    def __init__(
            self,
            language: str = settings.WIKI_USER_LANGUAGE,
            user_agent: str = settings.WIKI_USER_AGENT
        ) -> None:
        """Init."""
        self.wiki_wiki = wikipediaapi.Wikipedia(user_agent, language=language)

    def fetch_article_by_name(self, article_name: str) -> list:
        """Download an article from Wikipedia using its API."""
        page = self.wiki_wiki.page(article_name)
        if not page.exists():
            msg = f'Page: {article_name} not exists.'
            raise ValueError(msg)
        return {"title": article_name, "content": page.text}
