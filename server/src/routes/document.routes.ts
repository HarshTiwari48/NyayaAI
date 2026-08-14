import { Router } from "express";
import { analyzeDocumentController,
    getThreadDocumentsController,
    deleteDocumentController,
 } from "../controllers/document.controller";
import optionalAuth from "../middlewares/optionalAuth.middleware";
import upload from "../middlewares/upload.middleware";

import { aiRateLimiter } from "../middlewares/rateLimit.middleware";

import validate from "../middlewares/validate.middleware";
import { documentQuerySchema } from "../validators/document.validator";

const router = Router();

router.post(
  "/analyze",
  aiRateLimiter,
  optionalAuth,
  validate(documentQuerySchema),
  upload.single("file"),
  analyzeDocumentController
);

router.get(
  "/:threadId",
  optionalAuth,
  getThreadDocumentsController
);

router.delete(
  "/:documentId",
  optionalAuth,
  deleteDocumentController
);


export default router;