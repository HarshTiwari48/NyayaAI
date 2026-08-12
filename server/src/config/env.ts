import dotenv from "dotenv";

dotenv.config();

const requiredEnvVariables = [
  "NODE_ENV",
  "PORT",
  "MONGODB_URI",
  "JWT_ACCESS_SECRET",
  "JWT_REFRESH_SECRET",
  "ACCESS_TOKEN_EXPIRY",
  "REFRESH_TOKEN_EXPIRY",
  "FASTAPI_URL",
  "CLIENT_URL",
] as const;

for (const key of requiredEnvVariables) {
  if (!process.env[key]) {
    throw new Error(`Missing required environment variable: ${key}`);
  }
}

export const env = {
  NODE_ENV: process.env.NODE_ENV!,
  PORT: Number(process.env.PORT),
  MONGODB_URI: process.env.MONGODB_URI!,
  JWT_ACCESS_SECRET: process.env.JWT_ACCESS_SECRET!,
  JWT_REFRESH_SECRET: process.env.JWT_REFRESH_SECRET!,
  ACCESS_TOKEN_EXPIRY: process.env.ACCESS_TOKEN_EXPIRY!,
  REFRESH_TOKEN_EXPIRY: process.env.REFRESH_TOKEN_EXPIRY!,
  FASTAPI_URL: process.env.FASTAPI_URL!,
  CLIENT_URL: process.env.CLIENT_URL!,
} as const;