"use client"

import { useFormContext } from "react-hook-form";
import { 
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "../ui/form";
import { Input } from "../ui/input";
import { InputHTMLAttributes } from "react";

type InputProps<S> = {
    fieldTitle: string,
    nameInSchema: keyof S & string,
    className?: string,
} & InputHTMLAttributes<HTMLInputElement>;

export function InputWithLabel<S>({
    fieldTitle, nameInSchema, className, ...props
}: InputProps<S>) {
    const form = useFormContext();

    return (
        <FormField
            control={form.control}
            name={nameInSchema}
            render={({ field }) => (
                <FormItem>
                    <FormLabel
                        className="text-base"
                        htmlFor={nameInSchema}
                    >
                        {fieldTitle}
                    </FormLabel>

                    <FormControl>
                        <Input
                            id={nameInSchema}
                            className={`w-full max-w-xs dark:disabled:text-yellow-300 disabled:text-green-500 disabled:opacity-50 ${className}`}
                            {...props}
                            {...field}
                        />
                    </FormControl>

                    <FormMessage />
                </FormItem>
            )}
        />
    );
}