FROM node:20-alpine

WORKDIR /app

# Copy package files first
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy rest of frontend
COPY . .

# Build app
RUN npm run build

# Serve using Vite preview
EXPOSE 5173

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0"]