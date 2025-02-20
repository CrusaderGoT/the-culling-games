"use client";

import {
    zCreateCt,
    zCreateCtApp,
    zCreatePlayer
} from "@/api/client/zod.gen";
import { InputWithLabel } from "@/components/inputs/InputWithLabel";
import { SelectWithLabel } from "@/components/inputs/SelectWithLabel";
import { TextAreaWithLabel } from "@/components/inputs/TextAreaWithLabel";
import { Button } from "@/components/ui/button";
import { Form } from "@/components/ui/form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

export function CreatePlayerForm() {
    const createPlayerFormSchema = z.object({
        player: zCreatePlayer,
        cursed_technique: zCreateCt,
        applications: z.array(zCreateCtApp).max(5).min(5),
    });

    type createPlayerFormType = z.infer<typeof createPlayerFormSchema>;

    const defaultValues: createPlayerFormType = {
        player: {
            name: "",
            age: 18,
            gender: "non-binary",
            role: ""
        },
        cursed_technique: {
            name: "",
            definition: "",
        },
        applications: [
            {application: ""},
            {application: ""},
            {application: ""},
            {application: ""},
            {application: ""},
        ]
    }

    

    const form = useForm<createPlayerFormType>({
        resolver: zodResolver(createPlayerFormSchema),
        mode: "onBlur",
        defaultValues
    });

    function onSubmit(data: createPlayerFormType) {
        console.log(data);
    }

    return (
        <div className="sm:px-8 p-4 min-w-[50%] border rounded-md">
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)}>
                    <div className="flex flex-col gap-4 max-w-lsm">
                        <div className="flex flex-col md:flex-row gap-2">
                            {/** for player */}
                            <InputWithLabel<createPlayerFormType>
                                nameInSchema="player.name"
                                fieldTitle="Player Name"
                            />
                            <InputWithLabel<createPlayerFormType>
                                nameInSchema="player.role"
                                fieldTitle="Role"
                            />
                            <InputWithLabel<createPlayerFormType>
                                nameInSchema="player.age"
                                fieldTitle="Age"
                                type="number"
                            />
                            <SelectWithLabel<createPlayerFormType>
                                nameInSchema="player.gender"
                                fieldTitle="Gender"
                                data={[{ id: "male", description: "Male" }]}
                            />
                        </div>


                        <div>
                            {/** for cursed technique */}
                            <InputWithLabel<createPlayerFormType>
                                nameInSchema="cursed_technique.name"
                                fieldTitle="Cursed Technique Name"
                            />
                            <TextAreaWithLabel<createPlayerFormType>
                                nameInSchema="cursed_technique.definition"
                                fieldTitle="CT Definition"
                            />
                        </div>
                        <div>
                            {/** for applications */}
                            <TextAreaWithLabel<createPlayerFormType>
                                nameInSchema="applications.0.application"
                                fieldTitle="Technique Application 1"
                            />
                            <TextAreaWithLabel<createPlayerFormType>
                                nameInSchema="applications.1.application"
                                fieldTitle="Technique Application 2"
                            />
                            <TextAreaWithLabel<createPlayerFormType>
                                nameInSchema="applications.2.application"
                                fieldTitle="Technique Application 3"
                            />
                            <TextAreaWithLabel<createPlayerFormType>
                                nameInSchema="applications.3.application"
                                fieldTitle="Technique Application 4"
                            />
                            <TextAreaWithLabel<createPlayerFormType>
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
