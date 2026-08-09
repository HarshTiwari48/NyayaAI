import User from "../models/User.model";
import ApiError from "../utils/ApiError";
import { hashPassword, comparePassword } from "../utils/password";
import {
  generateAccessToken,
  generateRefreshToken,
  verifyRefreshToken,
} from "../utils/jwt";


interface RegisterData {
  name: string;
  email: string;
  password: string;
  avatar?: string;
}

export const registerUser = async (data: RegisterData) => {
  const { name, email, password, avatar } = data;

  const existingUser = await User.findOne({ email });

  if (existingUser) {
    throw new ApiError(409, "User with this email already exists");
  }

  const hashedPassword = await hashPassword(password);

  const user = await User.create({
    name,
    email,
    password: hashedPassword,
    avatar,
  });

  const accessToken = generateAccessToken(user._id.toString());
  const refreshToken = generateRefreshToken(user._id.toString());
  const refreshTokenHash = await hashPassword(refreshToken);

  user.refreshTokenHash = refreshTokenHash;
  await user.save();

  return {
    user: {
      id: user._id,
      name: user.name,
      email: user.email,
      avatar: user.avatar,
    },
    accessToken,
    refreshToken,
  };
};

export const loginUser = async (
  email: string,
  password: string
) => {
  const user = await User.findOne({ email });

  if (!user) {
    throw new ApiError(401, "Invalid email or password");
  }

  const isPasswordCorrect = await comparePassword(
    password,
    user.password
  );

  if (!isPasswordCorrect) {
    throw new ApiError(401, "Invalid email or password");
  }

  const accessToken = generateAccessToken(user._id.toString());
  const refreshToken = generateRefreshToken(user._id.toString());

  const refreshTokenHash = await hashPassword(refreshToken);

  user.refreshTokenHash = refreshTokenHash; 
  await user.save();

  return {
    user: {
      id: user._id,
      name: user.name,
      email: user.email,
      avatar: user.avatar,
    },
    accessToken,
    refreshToken,
  };
};

export const getCurrentUser = async (userId: string) => {
  const user = await User.findById(userId).select(
    "-password"
  );

  if (!user) {
    throw new ApiError(404, "User not found");
  }

  return user;
};

export const refreshAccessToken = async (refreshToken: string) => {
  let userId: string;

  try {
    userId = verifyRefreshToken(refreshToken);
  } catch {
    throw new ApiError(401, "Invalid or expired refresh token");
  }

  const user = await User.findById(userId);

  if (!user || !user.refreshTokenHash) {
    throw new ApiError(401, "Invalid refresh token");
  }

  const isValid = await comparePassword(
    refreshToken,
    user.refreshTokenHash
  );

  if (!isValid) {
    throw new ApiError(401, "Invalid refresh token");
  }

  const newAccessToken = generateAccessToken(user._id.toString());
  const newRefreshToken = generateRefreshToken(user._id.toString());

  const newRefreshTokenHash = await hashPassword(newRefreshToken);

  user.refreshTokenHash = newRefreshTokenHash;
  await user.save();

  return {
    accessToken: newAccessToken,
    refreshToken: newRefreshToken,
  };
};


export const logoutUser = async (userId: string) => {
  const user = await User.findById(userId);

  if (!user) {
    throw new ApiError(404, "User not found");
  }

  user.refreshTokenHash = null;
  await user.save();
};