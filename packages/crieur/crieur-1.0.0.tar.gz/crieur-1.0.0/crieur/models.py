from dataclasses import dataclass
from typing import Optional

from dataclass_wizard import DatePattern, DumpMeta, YAMLWizard
from slugify import slugify
from yaml.composer import ComposerError


@dataclass
class Numero(YAMLWizard):
    _id: str
    name: str
    description: str
    metadata: str
    articles: list

    def configure_articles(self, yaml_path):
        # Preserves abstract_fr key (vs. abstract-fr) when converting to_yaml()
        DumpMeta(key_transform="SNAKE").bind_to(Article)

        loaded_articles = []
        for article in self.articles:
            article_folder = (
                yaml_path.parent
                / f"{article['article']['title']}-{article['article']['_id']}"
            )
            article_yaml_path = article_folder / f"{article['article']['title']}.yaml"
            try:
                loaded_article = Article.from_yaml_file(article_yaml_path)
            except ComposerError:
                loaded_article = Article.from_yaml(
                    article_yaml_path.read_text().split("---")[1]
                )
            loaded_article.content_md = (
                article_folder / f"{article['article']['title']}.md"
            ).read_text()
            loaded_article.images_path = (
                article_folder / "images"
                if (article_folder / "images").exists()
                else None
            )
            loaded_article.numero = self
            loaded_articles.append(loaded_article)
        self.articles = loaded_articles


@dataclass
class Article(YAMLWizard):
    id: str
    title: str
    title_f: str
    date: Optional[DatePattern["%Y/%m/%d"]]  # noqa: F722
    subtitle: str = ""
    subtitle_f: str = ""
    content_md: str = ""
    authors: list = None
    abstract: list = None
    keywords: list = None


def configure_numero(yaml_path):
    # Preserves abstract_fr key (vs. abstract-fr) when converting to_yaml()
    DumpMeta(key_transform="SNAKE").bind_to(Numero)

    try:
        numero = Numero.from_yaml_file(yaml_path)
    except ComposerError:
        numero = Numero.from_yaml(yaml_path.read_text().split("---")[1])

    numero.configure_articles(yaml_path)
    return numero


@dataclass
class Keyword:
    slug: str
    name: str
    articles: list

    def __eq__(self, other):
        return self.slug == other.slug

    def __lt__(self, other: "Keyword"):
        if not isinstance(other, Keyword):
            return NotImplemented
        len_self = len(self.articles)
        len_other = len(other.articles)
        if len_self == len_other:
            return self.slug > other.slug
        return len_self < len_other


def collect_keywords(numeros):
    keywords = {}
    for numero in numeros:
        for article in numero.articles:
            article_keywords = []
            for kwds in article.keywords:
                if kwds.get("list") and kwds.get("lang") == "fr":  # TODO: en?
                    for keyword in kwds.get("list", "").split(", "):
                        keyword_slug = slugify(keyword)
                        if keyword_slug in keywords:
                            keywords[keyword_slug].articles.append(article)
                            kw = keywords[keyword_slug]
                        else:
                            kw = Keyword(
                                slug=keyword_slug, name=keyword, articles=[article]
                            )
                            keywords[keyword_slug] = kw
                        article_keywords.append(kw)
            article.keywords = article_keywords
    return dict(sorted(keywords.items(), key=lambda item: item[1], reverse=True))
