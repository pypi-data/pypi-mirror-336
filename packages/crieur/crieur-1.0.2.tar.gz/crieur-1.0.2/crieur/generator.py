import locale
import shutil
from pathlib import Path

import mistune
from jinja2 import Environment as Env
from jinja2 import FileSystemLoader
from slugify import slugify

from .utils import neighborhood

locale.setlocale(locale.LC_ALL, "")
environment = Env(loader=FileSystemLoader(str(Path(__file__).parent / "templates")))


def slugify_(value):
    return slugify(value)


environment.filters["slugify"] = slugify_

md = mistune.create_markdown(plugins=["footnotes", "superscript"])


def markdown(value):
    return md(value) if value else ""


environment.filters["markdown"] = markdown


def generate_html(title, numeros, keywords, target_path):
    common_params = {
        "numeros": numeros,
        "keywords": keywords,
        "title": title,
    }

    template_homepage = environment.get_template("homepage.html")
    content = template_homepage.render(**common_params)
    target_path.mkdir(parents=True, exist_ok=True)
    (target_path / "index.html").write_text(content)

    for numero in numeros:
        template_numero = environment.get_template("numero.html")
        content = template_numero.render(numero=numero, **common_params)
        numero_folder = target_path / "numero" / numero.name
        numero_folder.mkdir(parents=True, exist_ok=True)
        (numero_folder / "index.html").write_text(content)

        template_article = environment.get_template("article.html")
        for index, previous, article, next_ in neighborhood(numero.articles):
            content = template_article.render(
                article=article,
                numero=numero,
                previous_situation=previous,
                next_situation=next_,
                **common_params,
            )
            article_folder = numero_folder / "article" / article.id
            article_folder.mkdir(parents=True, exist_ok=True)
            (article_folder / "index.html").write_text(content)
            if article.images_path:
                shutil.copytree(
                    article.images_path, article_folder / "images", dirs_exist_ok=True
                )

    for slug, keyword in keywords.items():
        template_keyword = environment.get_template("keyword.html")
        content = template_keyword.render(keyword=keyword, **common_params)
        keyword_folder = target_path / "mot-clef" / keyword.slug
        keyword_folder.mkdir(parents=True, exist_ok=True)
        (keyword_folder / "index.html").write_text(content)
