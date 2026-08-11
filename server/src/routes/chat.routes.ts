import { Router } from "express";
import { sendChatMessage } from "../controllers/chat.controller";
import optionalAuth from "../middlewares/optionalAuth.middleware";

const router = Router();

router.post("/message", optionalAuth, sendChatMessage);

export default router;