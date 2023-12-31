import matplotlib
import matplotlib.pyplot as plt #pip install matplotlib
from typing import List
from modules import classes as cl
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
import nltk
# import unidecode
nltk.download('stopwords')

#Número de noticias por fuente

def graph_news_per_source(news: List[cl.News ]):
   #contar noticias por fuente
    sources = {}
    for new in news:
        try:
            source = new.get_owner()
            if source in sources:
                sources[source] += 1
            else:
                sources[source] = 1
        except Exception as e:
            print(f"Error al obtener la fuente de la noticia: {e}")
    #Comprobación
    #for source, count in sources.items():
    #   print(f"{source}: {count} noticias")

    # obtener fuentes y cantidades
    newspapers = list(sources.keys())
    counts = list(sources.values())

    #generar gráfico
    sources = dict(sorted(sources.items(), key=lambda item: item[1], reverse=True))
    plt.bar(newspapers, counts, color='green')
    plt.title("Número de noticias por fuente")
    plt.xlabel("Fuente")
    plt.ylabel("Número de noticias")
    #plt.savefig('static/img/graphs/news_per_source.png') # PROBLEMA donde lo guardo
    plt.show()


# Función que genera un gráfico del número de noticias por categoría
def graph_news_per_category(news: List[cl.News]):
    # Contar noticias por categoría
    categories = {}
    for new in news:
        try:
            category = new.get_category()
            if category in categories:
                categories[category] += 1
            else:
                categories[category] = 1
        except Exception as e:
            print(f"Error al obtener la categoría de la noticia: {e}")

    for category, count in categories.items():
        print(f"{category}: {count} noticias")

    # Obtener categorías y cantidades
    category_list = list(categories.keys())
    counts = list(categories.values())

    # Generar gráfico
    categories = dict(sorted(categories.items(), key=lambda item: item[1], reverse=True))
    plt.bar(category_list, counts, color='blue')
    plt.title("Número de noticias por categoría")
    plt.xlabel("Categoría")
    plt.ylabel("Número de noticias")
    plt.xticks(rotation=90) # Rotar las etiquetas del eje x 90 grados
    plt.show()


stop_words_es = set(stopwords.words('spanish'))
def filter_words(text):
    return ' '.join(unidecode.unidecode(word) for word in text.split() if word.lower() not in stop_words_es)

#Nube de palabras por categoría
def wordcloud_per_category(news: List[cl.News], requested_category):
    content_by_category = {}

    for new in news:
        try:
            category = new.get_category()
            content = new.get_content()

            if category in content_by_category:
                content_by_category[category] += ' ' + content
            else:
                content_by_category[category] = content

        except Exception as e:
            print(f"Error al obtener la categoría o el contenido de la noticia: {e}")

    for category, content in content_by_category.items():
        if category == requested_category:
            filtered_content = ' '.join(word for word in content.split() if word.lower() not in stop_words_es)

            # Generar la nube de palabras
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color='white',
                collocations=False,
                # regexp=r"\w[\w'áéíóúüñ]*",
                contour_width=0,
                contour_color='black',
                max_words=200,
           ).generate(filter_words(filtered_content))

            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.title(f"Nube de Palabras para la Categoría: {category}")
            plt.axis('off')
            plt.show()



#Función que genera una lista con todas las categorias --> cambiar de lugar!
def get_categories(news: List[cl.News]):
    categories = set()  # Usamos un conjunto para evitar duplicados

    for new in news:
        try:
            category = new.get_category()
            categories.add(category)
        except Exception as e:
            print(f"Error al obtener la categoría de la noticia: {e}")

    return list(categories)

category_mapping = {
        'General': ['general', 'Tiempo'],
        'Economía': ['Economía', 'España'],
        'España': ['España', 'Andalucía', 'Elecciones', 'Espejo Público', 'Cataluña', 'Valencia', 'Madrid'],
        'Deportes': ['Ciclismo', 'Deportes Jugones', 'Motor Fórmula 1', 'Baloncesto', 'Tenis', 'Motor', 'Fútbol'],
        'Salud': ['Salud', 'Bienestar'],
        'Internacional': ['Guerra Ucrania', 'Mundo', 'Europa', 'Internacional'],
        'Ciencia y Tecnología': ['Ciencia y tecnología', 'Ciencia'],
        'Viral': ['Viral', '¿Cómo, qué, cuándo?', 'Virales'],
        'Programas': ['Programas', 'Series'],
        'Sociedad': ['Loterías y sorteos', 'Cultura', 'Sociedad', 'Loterías']
    }
# Función que dada una categoría si esta pertenece a una categoría general, devuelve esta
def get_general_categories(categories: List[str]) -> List[str]:
    global category_mapping
    result = []

    for category in categories:
        found = False
        for general_category, specific_categories in category_mapping.items():
            if category in specific_categories:
                result.append(general_category)
                found = True
                break
        if not found:
            result.append('General')  # Si no se encuentra una categoría general, se agrega None a la lista resultante

    return result

# Funcion que dada una categoria general, devuelve una lista con las categorias especificas
def get_specific_categories(general_category: str) -> List[str]:
    global category_mapping
    # dada la general_category devuelve una lista de categorias especificas
    specific_categories = category_mapping[general_category]
    return specific_categories

''''
# Ejemplo de uso
general_category = 'Deportes'
specific_categories_list = get_specific_categories(general_category)
'''


''' Categorias
General: [ 'general',  'Tiempo',]
Economía: ['Economía', 'España']
Espanna: ['España','Andalucía', 'Elecciones', 'Espejo Público',  'Cataluña', 'Valencia', 'Madrid']
Deportes : ['Ciclismo', 'Deportes Jugones', 'Motor Fórmula 1',  'Baloncesto', 'Tenis', 'Motor',  'Tecnología', 'Fútbol']
Salud: [ 'Salud',  'Bienestar']
Internacional: ['Guerra Ucrania', 'Mundo', 'Europa',  'Internacional']
Ciencia y Tecnología: [ 'Ciencia y tecnología',  'Ciencia']
Viral: ['Viral', '¿Cómo, qué, cuándo?',  'Virales']
Programas: ['Programas', 'Series' ]
Sociedad: ['Loterías y sorteos',  'Cultura',  'Sociedad',   'Loterías']
'''