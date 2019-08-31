# Pull MongoDB image
docker pull mongo:latest

# Build Timeline API image
cd timeline_api/
docker build -f Dockerfile --rm -t timeline_api .
cd ..

# Build web application image
cd timeline
docker build -f Dockerfile --rm -t timeline_web .
cd ..