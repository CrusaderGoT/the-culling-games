"use client";

import { Gender, type BodyCreatePlayer } from "@/api/client";
import { zBodyCreatePlayer } from "@/api/client/zod.gen";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Form } from "@/components/ui/form";
import { InputWithLabel } from "@/components/inputs/InputWithLabel";
import { Button } from "@/components/ui/button";
import { TextAreaWithLabel } from "@/components/inputs/TextAreaWithLabel";
import { SelectWithLabel } from "@/components/inputs/SelectWithLabel";

export function PlayerForm() {
    const defaultValues: BodyCreatePlayer = {
        player: {
            name: "",
            age: undefined,
            role: undefined,
            gender: Gender.MALE,
        },
        cursed_technique: {
            name: "",
            definition: "",
        },
        applications: [
            { application: "" },
            { application: "" },
            { application: "" },
            { application: "" },
            { application: "" },
        ],
    };

    const form = useForm<BodyCreatePlayer>({
        resolver: zodResolver(zBodyCreatePlayer),
        defaultValues: defaultValues,
    });

    function onSubmit(data: BodyCreatePlayer) {
        console.log(data);
    }

    return (
        <div className="sm:px-8 p-4 min-w-[50%] border rounded-md">
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)}>
                    <div className="flex flex-col gap-4 max-w-lsm">
                        <div className="flex flex-col md:flex-row gap-2">
                            {/** for player */}
                            <InputWithLabel<BodyCreatePlayer>
                                nameInSchema="player.name"
                                fieldTitle="Player Name"
                            />
                            <InputWithLabel<BodyCreatePlayer>
                                nameInSchema="player.role"
                                fieldTitle="Role"
                            />
                            <InputWithLabel<BodyCreatePlayer>
                                nameInSchema="player.age"
                                fieldTitle="Age"
                            />
                            <SelectWithLabel<BodyCreatePlayer>
                                nameInSchema="player.gender"
                                fieldTitle="Gender"
                                data={[{id: "male", description: "Male"}]}
                            />
                        </div>

                        <div>
                            {/** for cursed technique */}
                            <InputWithLabel<BodyCreatePlayer>
                                nameInSchema="cursed_technique.name"
                                fieldTitle="Cursed Technique Name"
                            />
                            <TextAreaWithLabel<BodyCreatePlayer>
                                nameInSchema="cursed_technique.definition"
                                fieldTitle="CT Definition"
                            />
                        </div>
                        <div>
                            {/** for applications */}
                            <TextAreaWithLabel<BodyCreatePlayer>
                                nameInSchema="applications.0.application"
                                fieldTitle="Technique Application 1"
                            />
                            <TextAreaWithLabel<BodyCreatePlayer>
                                nameInSchema="applications.1.application"
                                fieldTitle="Technique Application 2"
                            />
                            <TextAreaWithLabel<BodyCreatePlayer>
                                nameInSchema="applications.2.application"
                                fieldTitle="Technique Application 3"
                            />
                            <TextAreaWithLabel<BodyCreatePlayer>
                                nameInSchema="applications.3.application"
                                fieldTitle="Technique Application 4"
                            />
                            <TextAreaWithLabel<BodyCreatePlayer>
                                nameInSchema="applications.4.application"
                                fieldTitle="Technique Application 5"
                            />
                        </div>

                        <div className="self-end">
                            {/** submit buttons */}
                            <Button type="submit">Create Player</Button>
                        </div>
                    </div>
                </form>
            </Form>
        </div>
    );
}
