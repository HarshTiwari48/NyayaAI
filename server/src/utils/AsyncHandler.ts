import { Request, Response, NextFunction, RequestHandler } from "express";

const AsyncHandler = (
  requestHandler: RequestHandler
): RequestHandler => {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(requestHandler(req, res, next)).catch(next);
  };
};

export default AsyncHandler;