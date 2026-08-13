import mongoose, { Document, Schema } from "mongoose";

export interface IDocument extends Document {
  userId: mongoose.Types.ObjectId;
  threadId: string;
  fileName: string;
  fileType: string;
  createdAt: Date;
}

const documentSchema = new Schema<IDocument>(
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
      index: true,
    },

    fileName: {
      type: String,
      required: true,
      trim: true,
    },

    fileType: {
      type: String,
      required: true,
    },
  },
  {
    timestamps: true,
  }
);

const DocumentModel = mongoose.model<IDocument>(
  "Document",
  documentSchema
);

export default DocumentModel;