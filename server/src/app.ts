import express from "express";
import cors from "cors";
import cookieParser from "cookie-parser";

import { env } from "./config/env";
import errorHandler from "./middlewares/error.middleware";


const app = express();

app.use(
  cors({
    origin: env.CLIENT_URL,
    credentials: true,
  })
);

app.use(express.json());

app.use(express.urlencoded({ extended: true }));

app.use(cookieParser());

app.get("/health", (_, res) => {
  res.status(200).json({
    success: true,
    message: "Server is running",
  });
});


app.use(errorHandler);


export default app;