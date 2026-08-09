import { Router } from "express";

import {
  register,
  login,
  refresh,
  me,
  logout,
} from "../controllers/auth.controller";

import validate from "../middlewares/validate.middleware";
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
  validate(registerSchema),
  register
);

router.post(
  "/login",
  validate(loginSchema),
  login
);

router.get("/me", authMiddleware, me);

router.post("/refresh", refresh);

router.post("/logout", authMiddleware, logout);

export default router;