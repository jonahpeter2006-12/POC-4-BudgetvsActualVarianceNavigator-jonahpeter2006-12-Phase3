FROM node:22-alpine

WORKDIR /app

COPY package*.json ./

RUN --mount=type=cache,target=/root/.npm \
    npm ci --prefer-offline --fetch-retries=5 --fetch-retry-mintimeout=20000 --fetch-retry-maxtimeout=120000 --fetch-timeout=300000 --maxsockets=5

COPY . .

ARG NEXT_PUBLIC_API_URL=http://localhost:8002
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

RUN npm run build

EXPOSE 3000

CMD ["sh", "-c", "npm run start -- -H 0.0.0.0 -p ${PORT:-3000}"]
