"use client"

import { useFormContext, FieldPath, FieldValues } from "react-hook-form";
import { 
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "../ui/form";
import { Textarea } from "../ui/textarea";
import { TextareaHTMLAttributes } from "react";

type TextareaProps<S extends FieldValues> = {
    fieldTitle: string,
    nameInSchema: FieldPath<S>,
    className?: string,
} & TextareaHTMLAttributes<HTMLTextAreaElement>;

export function TextAreaWithLabel<S extends FieldValues>({
    fieldTitle, nameInSchema, className, ...props
}: TextareaProps<S>) {
    const form = useFormContext();

    return (
        <FormField
            control={form.control}
            name={nameInSchema}
            render={({ field }) => (
                <FormItem>

                    <FormLabel
                        className="text-xs sm:text-base mb-2"
                        htmlFor={nameInSchema}
                    >
                        {fieldTitle}
                    </FormLabel>

                    <FormControl>

                        <Textarea
                            {...field}
                            {...props}
                            id={nameInSchema}
                            className={`dark:disabled:text-yellow-300 disabled:text-green-500 disabled:opacity-50 ${className}`}
                        />

                    </FormControl>

                    <FormMessage />
                </FormItem>
            )}
        />
    )
}
