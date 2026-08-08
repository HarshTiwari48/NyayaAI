import { Request, Response } from "express";
import {
  loginUser,
  registerUser,
  getCurrentUser,
} from "../services/auth.service";
import ApiResponse from "../utils/ApiResponse";
import AsyncHandler from "../utils/AsyncHandler";
import { AuthRequest } from "../middlewares/auth.middleware";

const cookieOptions = {
  httpOnly: true,
  secure: false, // true in production with HTTPS
  sameSite: "lax" as const,
};

export const register = AsyncHandler(
  async (req: Request, res: Response) => {
    const { name, email, password, avatar } = req.body;

    const result = await registerUser({
      name,
      email,
      password,
      avatar,
    });

    res
      .cookie("accessToken", result.accessToken, {
        ...cookieOptions,
        maxAge: 15 * 60 * 1000,
      })
      .cookie("refreshToken", result.refreshToken, {
        ...cookieOptions,
        maxAge: 7 * 24 * 60 * 60 * 1000,
      })
      .status(201)
      .json(
        new ApiResponse(
          201,
          { user: result.user },
          "User registered successfully"
        )
      );
  }
);

export const login = AsyncHandler(
  async (req: Request, res: Response) => {
    const { email, password } = req.body;

    const result = await loginUser(email, password);

    res
      .cookie("accessToken", result.accessToken, {
        ...cookieOptions,
        maxAge: 15 * 60 * 1000,
      })
      .cookie("refreshToken", result.refreshToken, {
        ...cookieOptions,
        maxAge: 7 * 24 * 60 * 60 * 1000,
      })
      .status(200)
      .json(
        new ApiResponse(
          200,
          { user: result.user },
          "Login successful"
        )
      );
  }
);

export const me = AsyncHandler(
  async (req: AuthRequest, res: Response) => {
    const user = await getCurrentUser(req.userId!);

    res
      .status(200)
      .json(
        new ApiResponse(200, user, "User fetched successfully")
      );
  }
);