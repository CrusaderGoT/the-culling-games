"use client";

import { EditUserForm } from "./EditUserForm";
import { useQuery } from "@tanstack/react-query";
import { currentUserOptions } from "@/api/client/@tanstack/react-query.gen";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { CircleDashed } from "lucide-react";

export default function EditUserPage() {
    const router = useRouter();
    // get token
    const token = localStorage.getItem("access_token");
    // query the current user
    const {
        data: currentUser,
        error,
        isError,
        isSuccess,
        isFetching,
        isPaused,
        refetch,
    } = useQuery({
        ...currentUserOptions({
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }),
        retry: 3,
        refetchOnWindowFocus: false,
    });

    if (isError && error?.detail) {
        router.push("/user/login");
        toast(`Login: ${error.detail}`);
    } else if ((isError && error && !error?.detail) || isPaused) {
        // mostly likely no network connect or/and fetch failed
        return (
            <div>
                <div>
                    <p>
                        An Error Occured, make sure you have good internet
                        connection
                    </p>
                    <Button onClick={() => refetch()}>Retry</Button>
                </div>
            </div>
        );
    } else if (isSuccess && currentUser) {
        return (
            <div className="flex flex-col items-center justify-center">
                <EditUserForm user={currentUser} />
                <div className="border">
                    <div>Change Password</div>
                    <div>Forget Password</div>
                    <div>Delete User</div>
                </div>
            </div>
        );
    } else if (isFetching) {
        return (
            <div className="">
                <CircleDashed className="animate-spin" />
                <p>Loading current user</p>
            </div>
        );
    }
}
