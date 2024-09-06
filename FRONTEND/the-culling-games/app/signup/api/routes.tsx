// handles form actions for signup route
"use server"
import { login } from "@/app/login/api/routes";


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