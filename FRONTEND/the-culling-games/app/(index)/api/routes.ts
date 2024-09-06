// api routes for the index page
import { cookies } from "next/headers"
import { redirect } from "next/navigation"


export function checkLogin() {
    const tokenExist = cookies().get("token")
    if (tokenExist) {
        redirect('/dashboard');
    } else {
        redirect('/login');
    }
}
