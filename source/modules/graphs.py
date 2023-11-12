#Clase que genera gráficos, al principio solo de pruebas para la entrega
import matplotlib.pyplot as plt #pip install matplotlib
from typing import List
from modules import classes as cl
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
import nltk
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
    plt.show()

''' Misma función pero colorea si es de distinto owner
    for new in news:
        try:
            category = new.get_category()
            owner = new.get_owner()

            if category in categories:
                categories[category] += 1
            else:
                categories[category] = 1

            if owner not in owners:
                owners[owner] = len(owners)  # Asignar un número único a cada owner

        except Exception as e:
            print(f"Error al obtener la categoría o el propietario de la noticia: {e}")

    # Obtener categorías y cantidades
    categories = dict(sorted(categories.items(), key=lambda item: item[1], reverse=True))
    categories_names = list(categories.keys())
    counts = list(categories.values())

    # Obtener owners y sus números asociados
    owners_colors = {owner: f'C{num}' for owner, num in owners.items()}

    # Generar gráfico
    fig, ax = plt.subplots()
    for category, count in zip(categories_names, counts):
        owner = owners_colors[news[0].get_owner()]  # Tomar el owner del primer elemento
        ax.bar(category, count, color=owner, label=f'{category} ({count})')

    # Personalizar el gráfico
    plt.title("Número de noticias por categoría")
    plt.xlabel("Categoría")
    plt.ylabel("Número de noticias")
    plt.xticks(rotation=45)
    plt.legend(title="Propietario")
    plt.tight_layout()

    # Mostrar el gráfico
    plt.show()
'''

stop_words_es = set(stopwords.words('spanish'))
#Nube de palabras por categoría
def wordcloud_per_category(news: List[cl.News], requested_category):
    # Obtener lista de "stop words"
    stop_words = set(STOPWORDS)

    # Crear un diccionario para almacenar el contenido por categoría
    content_by_category = {}

    # Agrupar el contenido por categoría
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

    # Generar nubes de palabras por categoría
    for category, content in content_by_category.items():
        if category == requested_category:
            # Eliminar stop words en español del contenido
            filtered_content = ' '.join(word for word in content.split() if word.lower() not in stop_words_es)

            # Generar la nube de palabras
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(filtered_content)

            # Mostrar la nube de palabras
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

# Función que dada una categoría si esta pertenece a una categoría general, devuelve esta
def get_general_categories(categories: List[str]) -> List[str]:
    result = []

    category_mapping = {
        'General': ['general', 'Tiempo'],
        'Economía': ['Economía', 'España'],
        'España': ['España', 'Andalucía', 'Elecciones', 'Espejo Público', 'Cataluña', 'Valencia', 'Madrid'],
        'Deportes': ['Ciclismo', 'Deportes Jugones', 'Motor Fórmula 1', 'Baloncesto', 'Tenis', 'Motor', 'Tecnología', 'Fútbol'],
        'Salud': ['Salud', 'Bienestar'],
        'Internacional': ['Guerra Ucrania', 'Mundo', 'Europa', 'Internacional'],
        'Ciencia y Tecnología': ['Ciencia y tecnología', 'Ciencia'],
        'Viral': ['Viral', '¿Cómo, qué, cuándo?', 'Virales'],
        'Programas': ['Programas', 'Series'],
        'Sociedad': ['Loterías y sorteos', 'Cultura', 'Sociedad', 'Loterías']
    }

    for category in categories:
        found = False
        for general_category, specific_categories in category_mapping.items():
            if category in specific_categories:
                result.append(general_category)
                found = True
                break
        if not found:
            result.append(None)  # Si no se encuentra una categoría general, se agrega None a la lista resultante

    return result

# Funcion que dada una categoria general, devuelve una lista con las categorias especificas
def get_specific_categories(general_category: str) -> List[str]:
    category_mapping = {
        'General': ['general', 'Tiempo'],
        'Economía': ['Economía', 'España'],
        'España': ['España', 'Andalucía', 'Elecciones', 'Espejo Público', 'Cataluña', 'Valencia', 'Madrid'],
        'Deportes': ['Ciclismo', 'Deportes Jugones', 'Motor Fórmula 1', 'Baloncesto', 'Tenis', 'Motor', 'Tecnología', 'Fútbol'],
        'Salud': ['Salud', 'Bienestar'],
        'Internacional': ['Guerra Ucrania', 'Mundo', 'Europa', 'Internacional'],
        'Ciencia y Tecnología': ['Ciencia y tecnología', 'Ciencia'],
        'Viral': ['Viral', '¿Cómo, qué, cuándo?', 'Virales'],
        'Programas': ['Programas', 'Series'],
        'Sociedad': ['Loterías y sorteos', 'Cultura', 'Sociedad', 'Loterías']
    }

    specific_categories = category_mapping.get(general_category, [])

    return specific_categories

# Ejemplo de uso
general_category = 'Deportes'
specific_categories_list = get_specific_categories(general_category)






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