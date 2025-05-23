git fetch origin main

# Compara o último commit local com o remoto
LOCAL=$(git rev-parse main)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "Atualizando s3-bridge"
    git pull

    # Removendo imagem docker
    docker stop flask-s3
    docker rm flask-s3
    docker rmi flask-s3

    docker build -t flask-s3 .
    docker run --name flask-s3 -p 5000:5000 --restart always flask-s3

    echo "Deploy do s3-bridge concluído"
fi