"use client";

import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

import {
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";

import { LucideIcon } from "lucide-react";
import { FieldPath, FieldValues, useFormContext } from "react-hook-form";
import { TooltipPopover } from "../TooltipPopover";

type DataObj = {
    id: string;
    description: string;
};

type SelectProps<S extends FieldValues> = {
    data: DataObj[];
    fieldTitle: string;
    nameInSchema: FieldPath<S>;
    className?: string;
    includeTip?: boolean;
    TooltipComponent?: React.ElementType;
    TooltipIcon?: LucideIcon;
    tooltipContent?: string;
    triggerText?: string;
};

export function SelectForm<S extends FieldValues>({
    data,
    fieldTitle,
    nameInSchema,
    className,
    includeTip = false,
    TooltipComponent,
    TooltipIcon,
    tooltipContent = "",
    triggerText,
}: SelectProps<S>) {
    const form = useFormContext();

    return (
        <FormField
            control={form.control}
            name={nameInSchema}
            render={({ field }) => (
                <FormItem>
                    <FormLabel className="text-xs sm:text-base">
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

                    <Select
                        {...field}
                        onValueChange={field.onChange}
                        defaultValue={field.value}
                    >
                        <FormControl>
                            <SelectTrigger
                                id={nameInSchema}
                                className={`w-full max-w-xs ${className}`}
                            >
                                <SelectValue placeholder="Select" />
                            </SelectTrigger>
                        </FormControl>

                        <SelectContent>
                            {data.map((item) => (
                                <SelectItem
                                    key={`${nameInSchema}_${item.id}`}
                                    value={item.id}
                                >
                                    {item.description}
                                </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>

                    <FormMessage className="overflow-y-scroll overflow-x- max-h-10 sm:max-w-sm max-w-xs text-wrap" />
                </FormItem>
            )}
        />
    );
}
