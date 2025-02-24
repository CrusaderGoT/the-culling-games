"use client";

import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger,
} from "@/components/ui/tooltip";
import { InfoIcon, LucideIcon } from "lucide-react";

type TooltipProps = {
    TriggerComponent?: React.ElementType;
    TriggerIcon?: LucideIcon;
    triggerText?: string;
    content: string;
};

export function TooltipPopover({
    TriggerComponent,
    TriggerIcon,
    triggerText,
    content,
}: TooltipProps) {
    return (
        <TooltipProvider>
            <Tooltip>
                <TooltipTrigger asChild>
                    {TriggerComponent && TriggerIcon === undefined ? (
                        <TriggerComponent className="h-3 md:h-4 min-h-3 max-h-7">{triggerText}</TriggerComponent>
                    ) : TriggerIcon && TriggerComponent === undefined ? (
                        <div className="flex h-3 items-center">
                            <TriggerIcon className="h-3 md:h-4 min-h-3 max-h-7" /> <p className="text-xs">{triggerText}</p> 
                        </div>
                    ) : triggerText ? (
                        triggerText
                    ) : (
                        <InfoIcon />
                    )}
                </TooltipTrigger>
                <TooltipContent className="max-w-prose">
                    <p className="text-pretty text-popover ">{content}</p>
                </TooltipContent>
            </Tooltip>
        </TooltipProvider>
    );
}
