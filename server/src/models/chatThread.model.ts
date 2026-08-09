import mongoose, { Document, Schema } from "mongoose";

export interface IChatThread extends Document {
  userId: mongoose.Types.ObjectId;
  threadId: string;
  title: string;
  lastMessage?: string;
  createdAt: Date;
  updatedAt: Date;
}

const chatThreadSchema = new Schema<IChatThread>(
  {
    userId: {
      type: Schema.Types.ObjectId,
      ref: "User",
      required: true,
      index: true,
    },
    
    threadId: {
      type: String,
      required: true,
      unique: true,
      index: true,
    },

    title: {
      type: String,
      required: true,
      trim: true,
      maxlength: 100,
      default: "New Chat",
    },

    lastMessage: {
      type: String,
      trim: true,
      maxlength: 500,
      default: "",
    },
  },
  {
    timestamps: true,
  }
);

const ChatThread = mongoose.model<IChatThread>(
  "ChatThread",
  chatThreadSchema
);

export default ChatThread;