import { roboto_mono } from "@/app/fonts";
import { EditUserForm } from "./EditUserForm";
import { UsersService, UserInfo } from "@/api/client";

export default async function EditUserPage() {
    const userData: UserInfo = {
        id: 0,
        username: "crusader",
        email: "emy@gmail.com",
        created: new Date(),
        country: "NG",

    }

    return (
        <div
            className={`${roboto_mono.className} p-5 rounded-md shadow-lg dark:shadow-white dark:shadow-md m-10`}
        >
            <h3 className={`font-extrabold text-2xl mb-3`}>Edit User</h3>
            <div className="flex flex-col-reverse sm:flex-row justify-between">
                <EditUserForm user={userData} />
            </div>
        </div>
    );
}
