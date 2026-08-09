import { Router } from "express";

import {
  register,
  login,
  refresh,
  me,
  logout,
} from "../controllers/auth.controller";

import validate from "../middlewares/validate.middleware";
import { authRateLimiter } from "../middlewares/rateLimit.middleware";

import {
  registerSchema,
  loginSchema,
} from "../validators/auth.validator";

import authMiddleware from "../middlewares/auth.middleware";

console.log("🔥 AUTH ROUTER LOADED");

const router = Router();


router.get("/test", (_, res) => {
  res.json({
    message: "Auth router is working",
  });
});

router.post(
  "/register",
  authRateLimiter,
  validate(registerSchema),
  register
);

router.post(
  "/login",
  authRateLimiter,
  validate(loginSchema),
  login
);

router.get("/me", authMiddleware, me);

router.post("/refresh", authRateLimiter, refresh);

router.post("/logout", authMiddleware, logout);

export default router;