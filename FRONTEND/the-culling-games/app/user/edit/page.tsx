import { roboto_mono } from "@/app/fonts";
import { EditUserForm } from "./EditUserForm";
import { UsersService } from "@/api/client";

export default async function EditUserPage() {
    try {
        const userResponse = await UsersService.currentUser();

        if (userResponse.data === undefined) {

            return <div>{userResponse.error?.detail}</div>;
        }

        return (
            <div
                className={`${roboto_mono.className} p-5 rounded-md shadow-lg dark:shadow-white dark:shadow-md m-10`}
            >
                <h3 className={`font-extrabold text-2xl mb-3`}>
                    Register to Play
                </h3>
                <div className="flex flex-col-reverse sm:flex-row justify-between">
                    <EditUserForm user={userResponse.data} />
                </div>
            </div>
        );
    } catch (e) {
        console.error(e)
        if (e instanceof Error) {
            throw e;
        }
    }
}
