import { HttpValidationError, ValidationError } from "@/api/client";
import { zValidationError } from "@/api/client/zod.gen";
import { isString } from "util";
import { isArrayBuffer } from "util/types";
import { z } from "zod";

type ResultProps = {
    error?: HttpValidationError;
    success?: string;
};

const MessageBox = ({
    type,
    content,
}: {
    type: "success" | "error";
    content: string;
}) => (
    <div
        className={`bg-accent px-4 py-2 rounded-lg max-w-xs max-h-max text-xs md:text-base my-1 ${
            type === "error" ? "text-red-500" : ""
        }`}
    >
        {type === "success" ? "🎉" : "❌"} {content}
    </div>
);

export function DisplayResponseMessage({ error, success }: ResultProps) {
    return (
        <>
            {(typeof error?.detail === "string") && (
                <MessageBox type="error" content={error.detail} />
            ) }

            {(typeof error?.detail === "object") && (
                error.detail.map((e, ind) => (
                    <MessageBox key={ind} type="error" content={e.msg} />
                ))
            )}
        </>
    );
}
