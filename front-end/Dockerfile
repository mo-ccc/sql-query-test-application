FROM node:15.14.0-alpine as build
WORKDIR /app
ARG REACT_APP_HOST
ENV REACT_APP_HOST=$REACT_APP_HOST

# copy all the files
COPY . .
# intitializes yarn in directory
RUN yarn install 
# continuous builds ensure frontend is up to date
RUN yarn build

# nginx will be used as a web server
FROM nginx:stable-alpine 
COPY --from=build /app/build /usr/share/nginx/html
# even though port 80 is exposed here. in the compose 9090 will be exposed
EXPOSE 80 
CMD ["nginx", "-g", "daemon off;"]

