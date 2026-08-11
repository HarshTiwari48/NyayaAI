console.log("🔥 APP.TS LOADED");


import express from "express";

import cors from "cors";
import cookieParser from "cookie-parser";

import { env } from "./config/env";


import authRoutes from "./routes/auth.routes";
import chatThreadRoutes from "./routes/chatThread.routes";
import chatRoutes from "./routes/chat.routes";



//middleware
import errorHandler from "./middlewares/error.middleware";

//routes

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


console.log("🔥 MOUNTING AUTH ROUTES");
app.use("/api/auth", authRoutes);
app.use("/api/threads", chatThreadRoutes);
app.use("/api/chat", chatRoutes);


app.get("/health", (_, res) => {
  res.status(200).json({
    success: true,
    message: "Server is running",
  });
});

app.get("/api/direct-test", (_, res) => {
  res.status(200).json({
    success: true,
    message: "Direct route works",
  });
});


app.use(errorHandler);


export default app;