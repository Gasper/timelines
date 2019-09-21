
# Manual setup of the Timeline web app. Assumes that docker network "timeline" exists.
#
# docker build -f Dockerfile --rm -t timeline_web .
# docker run -it --rm -p 8080:80 --net timeline --name timeline-web timeline_web

FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
COPY env.prod.js env.js 
RUN npm run build

FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]