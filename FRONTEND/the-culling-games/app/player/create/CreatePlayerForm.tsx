"use client";

import { BodyCreatePlayer, UserInfo } from "@/api/client";
import { zCreateCt, zCreateCtApp, zCreatePlayer } from "@/api/client/zod.gen";
import { DisplayResponseMessage } from "@/components/DisplayServerResponse";
import { InputForm } from "@/components/inputs/InputForm";
import { SelectForm } from "@/components/inputs/SelectWithLabel";
import { TextAreaForm } from "@/components/inputs/TextAreaWithLabel";
import { Button } from "@/components/ui/button";
import { Form } from "@/components/ui/form";
import { GENDERS } from "@/constants/GENDERS";
import { useCreatePlayerMutation } from "@/lib/custom-hooks/player-mutations";
import { accessToken } from "@/lib/custom-hooks/user-mutations";
import { zodResolver } from "@hookform/resolvers/zod";
import { InfoIcon, LoaderCircle } from "lucide-react";
import { useForm } from "react-hook-form";
import { z } from "zod";

type CreatePlayerProp = {
    user: UserInfo;
};

export function CreatePlayerForm({ user }: CreatePlayerProp) {
    const createPlayerFormSchema = z.object({
        player: zCreatePlayer,
        cursed_technique: zCreateCt,
        applications: z.array(zCreateCtApp).max(5).min(5),
    });

    const defaultValues: BodyCreatePlayer = {
        player: {
            name: "",
            age: 18,
            gender: "non-binary",
            role: "",
        },
        cursed_technique: {
            name: "",
            definition: "",
        },
        applications: [
            { name: "", application: "" },
            { name: "", application: "" },
            { name: "", application: "" },
            { name: "", application: "" },
            { name: "", application: "" },
        ],
    };

    const form = useForm<BodyCreatePlayer>({
        resolver: zodResolver(createPlayerFormSchema),
        mode: "onBlur",
        defaultValues,
    });

    const {
        mutate,
        isPending: isCreatingPlayer,
        error: createPlayerError,
        isSuccess: createPlayerSuccess,
    } = useCreatePlayerMutation(accessToken());

    function onSubmit(data: BodyCreatePlayer) {
        mutate({
            body: { ...data },
            path: { user: user.id },
        });
    }

    return (
        <div className="px-4 py-6 sm:py-10 sm:px-8 min-w-[50%] rounded-xl bg-primary-foreground/80">
            {isCreatingPlayer && (
                <div className="w-full max-w-xs flex justify-center items-center text-xs font-semibold">
                    <LoaderCircle className="animate-spin max-h-full ml-2 text-lime-300 w-[12px]" />

                    <span className="text-blue-400">
                        Creating your Player...
                    </span>
                </div>
            )}
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)}>
                    <div className="flex flex-col gap-4">
                        <div className="flex flex-col md:flex-row gap-2 border hover:border-green-600 px-3 py-4 rounded-lg relative md:justify-between">
                            <h2 className="text-sm absolute -inset-y-2.5 backdrop-blur h-fit w-fit font-semibold px-1 text-green-600 rounded-lg">
                                Player Info
                            </h2>
                            {/** for player */}
                            <InputForm<BodyCreatePlayer>
                                nameInSchema="player.name"
                                fieldTitle="Player Name"
                                includeTip
                                TooltipIcon={InfoIcon}
                                tooltipContent="This is the name of your Player"
                            />
                            <InputForm<BodyCreatePlayer>
                                nameInSchema="player.role"
                                fieldTitle="Role"
                                includeTip
                                TooltipIcon={InfoIcon}
                                tooltipContent="This is the role or occupation of your Player. e.g, Doctor, Curse User, Sorcerer, Curse, etc..."
                            />
                            <InputForm<BodyCreatePlayer>
                                nameInSchema="player.age"
                                fieldTitle="Age"
                                type="number"
                                includeTip
                                TooltipIcon={InfoIcon}
                                tooltipContent="This is the age of your Player. Must be in the range of 10 yrs old to 102 yrs old."
                            />
                            <SelectForm<BodyCreatePlayer>
                                nameInSchema="player.gender"
                                fieldTitle="Gender"
                                data={GENDERS}
                                includeTip
                                TooltipIcon={InfoIcon}
                                tooltipContent="This is the player's gender."
                            />
                        </div>

                        <div className="flex flex-col gap-3 border hover:border-green-500 px-3 py-4 rounded-lg relative">
                            {/** for cursed technique */}
                            <h2 className="text-sm absolute -inset-y-2.5 backdrop-blur h-fit w-fit font-semibold px-1 text-green-500 rounded-lg">
                                Cursed Technique Overview
                            </h2>
                            <InputForm<BodyCreatePlayer>
                                nameInSchema="cursed_technique.name"
                                fieldTitle="Cursed Technique Name"
                                includeTip
                                TooltipIcon={InfoIcon}
                                tooltipContent="This is the name of your player's cursed technique. Not the same as its subsets/applications. e.g, Shadow Manipulation, Infinity, etc..."
                            />
                            <TextAreaForm<BodyCreatePlayer>
                                nameInSchema="cursed_technique.definition"
                                fieldTitle="Cursed Technique Definition"
                                includeTip
                                TooltipIcon={InfoIcon}
                                tooltipContent="This is the overview of the player's cursed technique. Do not write the different ways they apply it here."
                                className="resize-none h-32 text-left tracking-wide"
                            />
                        </div>

                        <div className="flex flex-col gap-4 border hover:border-green-400 px-3 py-4 rounded-lg relative">
                            {/** for applications */}
                            <h2 className="text-sm absolute -inset-y-2.5 backdrop-blur h-fit w-fit font-semibold px-1 text-green-400 rounded-lg">
                                Your Five (5) Applications
                            </h2>
                            <div className="flex flex-col gap-1">
                                <InputForm<BodyCreatePlayer>
                                    nameInSchema="applications.0.name"
                                    fieldTitle="Name (1)"
                                    includeTip
                                    TooltipIcon={InfoIcon}
                                    tooltipContent="This is the name of an application/subset of the player's CT. e.g, Demon Dogs, Red, etc."
                                />
                                <TextAreaForm<BodyCreatePlayer>
                                    nameInSchema="applications.0.application"
                                    fieldTitle="Application (2)"
                                    includeTip
                                    TooltipIcon={InfoIcon}
                                    tooltipContent="This is the detail of how the application is used/performed, including what it does."
                                    className="resize-none h-44 text-left tracking-wide"
                                />
                            </div>

                            <div className="flex flex-col gap-1">
                                <InputForm<BodyCreatePlayer>
                                    nameInSchema="applications.1.name"
                                    fieldTitle="Name (2)"
                                    includeTip
                                    TooltipIcon={InfoIcon}
                                    tooltipContent="This is the name of an application/subset of the player's CT. e.g, Demon Dogs, Red, etc."
                                />
                                <TextAreaForm<BodyCreatePlayer>
                                    nameInSchema="applications.1.application"
                                    fieldTitle="Application (2)"
                                    includeTip
                                    TooltipIcon={InfoIcon}
                                    tooltipContent="This is the detail of how the application is used/performed, including what it does."
                                    className="resize-none h-44 text-left tracking-wide"
                                />
                            </div>

                            <div className="flex flex-col gap-1">
                                <InputForm<BodyCreatePlayer>
                                    nameInSchema="applications.2.name"
                                    fieldTitle="Name (3)"
                                    includeTip
                                    TooltipIcon={InfoIcon}
                                    tooltipContent="This is the name of an application/subset of the player's CT. e.g, Demon Dogs, Red, etc."
                                />
                                <TextAreaForm<BodyCreatePlayer>
                                    nameInSchema="applications.2.application"
                                    fieldTitle="Application (3)"
                                    includeTip
                                    TooltipIcon={InfoIcon}
                                    tooltipContent="This is the detail of how the application is used/performed, including what it does."
                                    className="resize-none h-44 text-left tracking-wide"
                                />
                            </div>

                            <div className="flex flex-col gap-1">
                                <InputForm<BodyCreatePlayer>
                                    nameInSchema="applications.3.name"
                                    fieldTitle="Name (4)"
                                    includeTip
                                    TooltipIcon={InfoIcon}
                                    tooltipContent="This is the name of an application/subset of the player's CT. e.g, Demon Dogs, Red, etc."
                                />
                                <TextAreaForm<BodyCreatePlayer>
                                    nameInSchema="applications.3.application"
                                    fieldTitle="Application (4)"
                                    includeTip
                                    TooltipIcon={InfoIcon}
                                    tooltipContent="This is the detail of how the application is used/performed, including what it does."
                                    className="resize-none h-44 text-left tracking-wide"
                                />
                            </div>

                            <div className="flex flex-col gap-1">
                                <InputForm<BodyCreatePlayer>
                                    nameInSchema="applications.4.name"
                                    fieldTitle="Name (5)"
                                    includeTip
                                    TooltipIcon={InfoIcon}
                                    tooltipContent="This is the name of an application/subset of the player's CT. e.g, Demon Dogs, Red, etc."
                                />
                                <TextAreaForm<BodyCreatePlayer>
                                    nameInSchema="applications.4.application"
                                    fieldTitle="Application (5)"
                                    includeTip
                                    TooltipIcon={InfoIcon}
                                    tooltipContent="This is the detail of how the application is used/performed, including what it does."
                                    className="resize-none h-44 text-left tracking-wide"
                                />
                            </div>

                            {createPlayerError && (
                                <div className="max-w-md self-end my-1 max-h-max">
                                    <DisplayResponseMessage
                                        error={createPlayerError}
                                    />
                                </div>
                            )}
                        </div>

                        <div className="self-end">
                            {/** submit buttons */}
                            <Button
                                type="submit"
                                disabled={isCreatingPlayer || createPlayerSuccess}
                            >
                                Create Player
                            </Button>
                        </div>
                    </div>
                </form>
            </Form>
        </div>
    );
}
