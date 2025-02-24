"use client";

import { currentUserOptions } from "@/api/client/@tanstack/react-query.gen";
import { Button } from "@/components/ui/button";
import { useQuery } from "@tanstack/react-query";
import { LoaderCircle } from "lucide-react";
import { useRouter } from "next/navigation";
import { CreatePlayerForm } from "./CreatePlayerForm";

export default function CreatePlayerPage() {
    const router = useRouter();
    // get access token
    const token = localStorage.getItem("access_token");
    // check if player exists for this user, and if user exist
    const {
        data: currentUser,
        error,
        isPending,
        isFetching,
        isSuccess,
        refetch,
    } = useQuery({
        ...currentUserOptions({
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }),
    });
    return (
        <div className="m-6">
            {(isPending || isFetching) && (
                <div className="w-full h-dvh grid place-content-center fixed inset-0">
                    <div className="flex gap-1">
                        <LoaderCircle className="animate-spin" /> Loading...
                    </div>
                </div>
            )}

            {error && (
                <div className="w-full h-dvh grid place-content-center fixed inset-0">
                    {error.message && error instanceof Error && (
                        <div className="flex flex-col items-center">
                            <p>
                                {error.message}, make sure you have good
                                internet connection.
                            </p>
                            <Button
                                className="max-w-xs w-full"
                                onClick={() => refetch()}
                            >
                                Retry
                            </Button>
                        </div>
                    )}

                    {error.detail && (
                        <div className="flex flex-col items-center">
                            <p>{error.detail}</p>
                            <Button
                                onClick={(e) => {
                                    e.currentTarget.disabled;
                                    router.push("/user/login");
                                }}
                                className="max-w-xs w-full"
                            >
                                Login
                            </Button>
                        </div>
                    )}

                    {typeof error === "string" && (
                        <div className="flex flex-col items-center">
                            <p>{error}</p>
                            <Button
                                className="max-w-xs w-full"
                                onClick={(e) => {
                                    e.currentTarget.disabled;
                                    router.push("/player/edit");
                                }}
                            >
                                Edit Player
                            </Button>
                        </div>
                    )}
                </div>
            )}

            {currentUser && isSuccess ? (
                !currentUser.player ? (
                    <div className="flex flex-col">
                        <h2 className="text-lg font-bold self-center">
                            Create Your Player Here
                        </h2>
                        <CreatePlayerForm user={currentUser} />
                    </div>
                ) : (
                    !isFetching && (
                        <div className="w-full h-dvh grid place-content-center fixed inset-0">
                            <p>Already Have a Player</p>
                            <Button onClick={() => router.push("/player/edit")}>
                                Edit Player
                            </Button>
                        </div>
                    )
                )
            ) : null}
        </div>
    );
}
