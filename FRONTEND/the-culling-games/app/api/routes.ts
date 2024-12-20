"use server"

import { revalidatePath } from "next/cache";
import { cookies } from "next/headers";
import { permanentRedirect, redirect } from "next/navigation";


export async function createUser(prevState: any, formData: FormData) {
  const rawFormData = Object.fromEntries(formData);
  // send to fastApi server
  const res = await fetch("http://localhost:8000/signup", {
    method: 'POST',
    body: JSON.stringify(rawFormData),
    headers: {
      'accept': 'application/json',
      'Content-Type': 'application/json',
    },
  });

  if (!res.ok) {
    const errData = await res.json();
    return errData;

  } else { // login in new user and store access token in cookie
    // get the username and password as formdata
    const loginFormData = new FormData();
    loginFormData.append("username", rawFormData.username);
    loginFormData.append("password", rawFormData.password);
    await login(prevState, loginFormData);
  }
}

export async function login(prevState: any, rawFormData: FormData) {
  // send login api call to fastapi
  // they have to be sent as form query format, because of the fastapi oauth
  const newFormQuery = new URLSearchParams();
  const password = rawFormData.get('password') as string;
  const username = rawFormData.get('username') as string;
  newFormQuery.append('username', username);
  newFormQuery.append('password', password);
  // send request to get token
  const res = await fetch("http://localhost:8000/login", {
    method: "POST",
    headers: {
      'accept': 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: newFormQuery,
  });

  if (!res.ok) {
    const errData = await res.json();
    return errData;

  } else {
    const tokenData = await res.json();
    const { access_token, bearer } = tokenData;
    (await cookies()).set('token', access_token);
    (await cookies()).set('bearer', bearer);
    // will redirect/ revalidate to homepage, should modify using bind to redirect to the page the login was prompted
    revalidatePath('/dashboard');
    permanentRedirect('/dashboard');
  }
}

export async function getUser() {
  const tokenCookie = (await cookies()).get('token');
  const res = await fetch('http://localhost:8000/users/me', {
    headers: {
      'accept': 'application/json',
      'Authorization': `Bearer ${tokenCookie?.value}`,
    },
    next: { revalidate: 30 }
  });

  if (!res.ok) {
    throw new Error(`Failed to get user: ${res.statusText}`);
  }

  return res.json();

}

export async function checkLogin() {
    const tokenExist = (await cookies()).get("token");
    if (tokenExist) {
        redirect('/dashboard');
    } else {
        redirect('/login');
    }
}
