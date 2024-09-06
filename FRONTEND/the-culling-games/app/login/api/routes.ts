"use server"
import { cookies } from "next/headers";
import { revalidatePath } from "next/cache";
import { permanentRedirect, redirect } from "next/navigation";

export async function login(prevState: any, rawFormData: FormData) {
    // send login api call to fastapi
    // they have to be sent as form query format, because of the fastapi oauth
    const newFormQuery = new URLSearchParams();
    const password = rawFormData.get('password') as string;
    const username = rawFormData.get('username') as string;
    newFormQuery.append('username', username)
    newFormQuery.append('password', password)
    // send request to get token
    const res = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers : {
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: newFormQuery,
    });

    if (!res.ok) {
      const errData = await res.json();
      return errData;

    } else {
      const tokenData = await res.json()
      const {access_token, bearer} = tokenData
      cookies().set('token', access_token);
      cookies().set('bearer', bearer)
      // will redirect/ revalidate to homepage, should modify using bind to redirect to the page the login was prompted
      revalidatePath('/dashboard');
      permanentRedirect('/dashboard');
    }
}