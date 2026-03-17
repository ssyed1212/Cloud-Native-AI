FROM node:20-alpine

WORKDIR /srv/frontend

# frontend constraints: derive node requirements from lab5/lab5-frontend/package.json
COPY lab5/lab5-frontend/package.json lab5/lab5-frontend/package-lock.json ./

RUN npm ci

COPY lab5/lab5-frontend/ ./

RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start", "--", "-p", "3000", "-H", "0.0.0.0"]
