# Frontend Dockerfile for PRODUCTION/DEPLOY (Railway, etc)
FROM node:18-slim

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install --production

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
