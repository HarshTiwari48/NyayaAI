import { Router } from "express";
import { sendChatMessage, getChatMessages } from "../controllers/chat.controller";
import optionalAuth from "../middlewares/optionalAuth.middleware";

import { aiRateLimiter } from "../middlewares/rateLimit.middleware";

import validate from "../middlewares/validate.middleware";
import { chatMessageSchema } from "../validators/chat.validator";

const router = Router();
console.log("🔥 CHAT ROUTER LOADED");

router.post(
  "/message",
  aiRateLimiter,
  optionalAuth,
  validate(chatMessageSchema),
  sendChatMessage
);

router.get(
  "/:threadId/messages",
  optionalAuth,
  getChatMessages
);

export default router;