"use client"

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

import { useFormContext } from "react-hook-form";


type DataObj = {
    id: string,
    description: string
}

type SelectProps<S> = {
    data: DataObj[]
    fieldTitle: string,
    nameInSchema: keyof S & string,
    className?: string,
}


export function SelectWithLabel<S>({
    data, fieldTitle, nameInSchema, className
}: SelectProps<S> ) {

    const form = useFormContext();

    return (
        <FormField
            control={form.control}
            name={nameInSchema}
            render={({ field }) => (
                <FormItem>

                    <FormLabel
                        className="text-base"
                    >
                        {fieldTitle}
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
                            {data.map(item => (
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