sudo apt install git
git clone https://github.com/carlosMoragon/ing_sw_TruthPaper.git
cd ing_sw_TruthPaper
git branch pruebaIntegracion
git checkout pruebaIntegracion
git config --global user.email "cmoragoncorella@gmail.com"
git config --global user.name "carlos"
git pull origin pruebaIntegracion
sudo apt  install docker.io 
docker build -t flaskapp .
