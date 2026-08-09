import { Router } from "express";
import {
  createChatThread,
  getChatThreads,
  getChatThread,
} from "../controllers/chatThread.controller";
import optionalAuth from "../middlewares/optionalAuth.middleware";

const router = Router();

router.post("/", optionalAuth, createChatThread);

router.get("/", optionalAuth, getChatThreads);

router.get("/:threadId", optionalAuth, getChatThread);

export default router;