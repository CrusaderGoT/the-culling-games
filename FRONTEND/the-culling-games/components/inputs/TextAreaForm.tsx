"use client";

import { LucideIcon } from "lucide-react";
import { TextareaHTMLAttributes } from "react";
import { FieldPath, FieldValues, useFormContext } from "react-hook-form";
import { TooltipPopover } from "../TooltipPopover";
import {
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "../ui/form";
import { Textarea } from "../ui/textarea";

type TextareaProps<S extends FieldValues> = {
    fieldTitle: string;
    nameInSchema: FieldPath<S>;
    className?: string;
    includeTip?: boolean;
    TooltipComponent?: React.ElementType;
    TooltipIcon?: LucideIcon;
    tooltipContent?: string;
    triggerText?: string;
} & TextareaHTMLAttributes<HTMLTextAreaElement>;

export function TextAreaForm<S extends FieldValues>({
    fieldTitle,
    nameInSchema,
    className,
    includeTip = false,
    TooltipComponent,
    TooltipIcon,
    tooltipContent = "",
    triggerText,
    ...props
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
    );
}
