import { NextFunction, Request, Response } from "express";
import jwt from "jsonwebtoken";
import { env } from "../config/env";
import { AuthTokenPayload } from "../types/auth";

export interface OptionalAuthRequest extends Request {
  userId?: string;
}

const optionalAuth = (
  req: OptionalAuthRequest,
  res: Response,
  next: NextFunction
) => {
  const token = req.cookies.accessToken;

  if (!token) {
    return next();
  }

  try {
    const decoded = jwt.verify(
      token,
      env.JWT_ACCESS_SECRET
    ) as AuthTokenPayload;

    req.userId = decoded.userId;
  } catch {
    // Invalid/expired token → treat as guest
  }

  next();
};

export default optionalAuth;