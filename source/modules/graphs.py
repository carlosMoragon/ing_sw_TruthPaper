#Clase que genera gráficos, al principio solo de pruebas para la entrega
import matplotlib.pyplot as plt #pip install matplotlib
import web_scrapping as ws
import classes as cl
from typing import List
import sys
sys.path.append('classes.py')
from classes import cl


noticias = []
noticias = ws.get_news()

#Número de noticias por fuente
#Número de noticias de una categoría categoría por fuente
#Palabras más comunes 
#Nube de palabras

#Número de noticias por fuente

def graph_news_per_source(news: List[cl.News]):
    #contar noticias por fuente
    sources = {}
    for new in news:
        source = new.get_source()
        if source in sources:
            sources[source] += 1
        else:
            sources[source] = 1
    
    # obtener fuentes y cantidades
    newspaper = list(sources.keys())
    count = list(sources.values())

    #generar gráfico
    sources = dict(sorted(sources.items(), key=lambda item: item[1], reverse=True))
    plt.bar(newspaper, count, color='green')
    plt.title("Número de noticias por fuente")
    plt.xlabel("Fuente")
    plt.ylabel("Número de noticias")
    plt.show()

      # Guardar el gráfico como una imagen
    plt.savefig('static/img/graphs/news_per_source.png')


if __name__ == '__main__':
    # Contar el número de noticias por fuente
    graph_news_per_source(noticias)

'''
@app.route('/charts')
def generate_charts():
    noticias = ws.get_news()
    graph_news_per_source(noticias)
    return render_template('charts.html')
  '''