FROM node

WORKDIR /json-server

COPY . .

EXPOSE 3000

RUN npm install -g json-server

CMD json-server --watch db.json
