// handles form actions for signup route
"use server"


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
    } else { // log in new user after
      return res.json();
    }   
}
