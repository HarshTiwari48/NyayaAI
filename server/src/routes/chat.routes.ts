import { Router } from "express";
import { sendChatMessage, getChatMessages } from "../controllers/chat.controller";
import optionalAuth from "../middlewares/optionalAuth.middleware";

const router = Router();
console.log("🔥 CHAT ROUTER LOADED");

router.post(
  "/message",
  optionalAuth,
  sendChatMessage
);

router.get(
  "/:threadId/messages",
  optionalAuth,
  getChatMessages
);

export default router;