"use client";

import { type BodyEditPlayer, type PlayerInfo } from "@/api/client";
import { zBodyEditPlayer } from "@/api/client/zod.gen";
import { InputWithLabel } from "@/components/inputs/InputWithLabel";
import { SelectWithLabel } from "@/components/inputs/SelectWithLabel";
import { TextAreaWithLabel } from "@/components/inputs/TextAreaWithLabel";
import { Button } from "@/components/ui/button";
import { Form } from "@/components/ui/form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";

type EditPlayerProps = {
    player: PlayerInfo
}
export function EditPlayerForm({ player: currentPlayer }: EditPlayerProps) {
    const defaultValues: BodyEditPlayer = {
        player: {
            name: currentPlayer.name,
            age: currentPlayer.age,
            role: currentPlayer.role,
            gender: currentPlayer.gender,
        },
        cursed_technique: currentPlayer.cursed_technique,
        applications: currentPlayer.cursed_technique.applications
    };

    const form = useForm<BodyEditPlayer>({
        mode: "onBlur",
        resolver: zodResolver(zBodyEditPlayer),
        defaultValues: defaultValues,
    });

    function onSubmit(data: BodyEditPlayer) {
        console.log(data);
    }

    return (
        <div className="sm:px-8 p-4 min-w-[50%] border rounded-md">
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)}>
                    <div className="flex flex-col gap-4 max-w-lsm">
                        <div className="flex flex-col md:flex-row gap-2">
                            {/** for player */}
                            <InputWithLabel<BodyEditPlayer>
                                nameInSchema="player.name"
                                fieldTitle="Player Name"
                            />
                            <InputWithLabel<BodyEditPlayer>
                                nameInSchema="player.role"
                                fieldTitle="Role"
                            />
                            <InputWithLabel<BodyEditPlayer>
                                nameInSchema="player.age"
                                fieldTitle="Age"
                            />
                            <SelectWithLabel<BodyEditPlayer>
                                nameInSchema="player.gender"
                                fieldTitle="Gender"
                                data={[{id: "male", description: "Male"}]}
                            />
                        </div>

                        <div>
                            {/** for cursed technique */}
                            <InputWithLabel<BodyEditPlayer>
                                nameInSchema="cursed_technique.name"
                                fieldTitle="Cursed Technique Name"
                            />
                            <TextAreaWithLabel<BodyEditPlayer>
                                nameInSchema="cursed_technique.definition"
                                fieldTitle="CT Definition"
                            />
                        </div>
                        <div>
                            {/** for applications */}
                            <TextAreaWithLabel<BodyEditPlayer>
                                nameInSchema="applications.0.application"
                                fieldTitle="Technique Application 1"
                            />
                            <TextAreaWithLabel<BodyEditPlayer>
                                nameInSchema="applications.1.application"
                                fieldTitle="Technique Application 2"
                            />
                            <TextAreaWithLabel<BodyEditPlayer>
                                nameInSchema="applications.2.application"
                                fieldTitle="Technique Application 3"
                            />
                            <TextAreaWithLabel<BodyEditPlayer>
                                nameInSchema="applications.3.application"
                                fieldTitle="Technique Application 4"
                            />
                            <TextAreaWithLabel<BodyEditPlayer>
                                nameInSchema="applications.4.application"
                                fieldTitle="Technique Application 5"
                            />
                        </div>

                        <div className="self-end">
                            {/** submit buttons */}
                            <Button type="submit">Edit Player</Button>
                        </div>
                    </div>
                </form>
            </Form>
        </div>
    );
}
