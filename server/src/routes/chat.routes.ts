import { Router } from "express";
import { sendChatMessage } from "../controllers/chat.controller";
import optionalAuth from "../middlewares/optionalAuth.middleware";

const router = Router();
console.log("🔥 CHAT ROUTER LOADED");

router.post(
  "/message",
  optionalAuth,
  sendChatMessage
);

export default router;