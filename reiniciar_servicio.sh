git pull origin main
git submodule update --remote
docker compose down
docker compose up --build -d
cd ~/XPERTIA/Reverse-Proxy-xpert-IA
docker compose down
docker compose up --build -d
