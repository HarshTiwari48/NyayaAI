import { Router } from "express";
import { analyzeDocumentController } from "../controllers/document.controller";
import optionalAuth from "../middlewares/optionalAuth.middleware";
import upload from "../middlewares/upload.middleware";

const router = Router();

router.post(
  "/analyze",
  optionalAuth,
  upload.single("file"),
  analyzeDocumentController
);

export default router;