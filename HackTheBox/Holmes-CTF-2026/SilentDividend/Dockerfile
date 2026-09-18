FROM node:22-alpine

WORKDIR /app

COPY flag.js .

RUN npm init -y
RUN npm install ethers

CMD ["node", "flag.js"]