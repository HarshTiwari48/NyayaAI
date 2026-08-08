import { NextFunction, Request, Response } from "express";
import jwt from "jsonwebtoken";
import { env } from "../config/env";
import ApiError from "../utils/ApiError";
import { AuthTokenPayload } from "../types/auth";


export interface AuthRequest extends Request {
  userId?: string;
}

const authMiddleware = (
  req: AuthRequest,
  res: Response,
  next: NextFunction
) => {
  const token = req.cookies.accessToken;

  if (!token) {
    throw new ApiError(401, "Authentication required");
  }

  try {
    const decoded = jwt.verify(
      token,
      env.JWT_ACCESS_SECRET
    ) as AuthTokenPayload;

    req.userId = decoded.userId;

    next();
  } catch {
    throw new ApiError(401, "Invalid or expired access token");
  }
};

export default authMiddleware;