"use client";

import { LucideIcon } from "lucide-react";
import { InputHTMLAttributes } from "react";
import { FieldPath, FieldValues, useFormContext } from "react-hook-form";
import { TooltipPopover } from "../TooltipPopover";
import {
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "../ui/form";
import { Input } from "../ui/input";

type InputProps<S extends FieldValues> = {
    fieldTitle: string;
    nameInSchema: FieldPath<S>;
    className?: string;
    fieldInfo?: string;
    includeTip?: boolean;
    TooltipComponent?: React.ElementType;
    TooltipIcon?: LucideIcon;
    tooltipContent?: string;
    triggerText?: string;
} & InputHTMLAttributes<HTMLInputElement>;

export function InputForm<S extends FieldValues>({
    fieldTitle,
    nameInSchema,
    className,
    fieldInfo,
    includeTip = false,
    TooltipComponent,
    TooltipIcon,
    triggerText,
    tooltipContent = "input info",
    ...props
}: InputProps<S>) {
    const form = useFormContext();

    return (
        <FormField
            control={form.control}
            name={nameInSchema}
            render={({ field }) => (
                <FormItem>
                    <FormLabel
                        className="text-xs sm:text-base"
                        htmlFor={nameInSchema}
                    >
                        <div className="flex items-center gap-1">
                            <span>{fieldTitle}</span>
                            {includeTip && (
                                <TooltipPopover
                                    TriggerComponent={TooltipComponent}
                                    TriggerIcon={TooltipIcon}
                                    triggerText={triggerText}
                                    content={tooltipContent}
                                />
                            )}
                        </div>
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
