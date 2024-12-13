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
  const res = await fetch("/api/login", {
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
    const { access_token, bearer } = tokenData();
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

export const players = [
  {
    "name": "ibrahim",
    "gender": "male",
    "age": 30,
    "role": "string",
    "id": 1,
    "created": "2024-08-14",
    "cursed_technique": {
      "name": "string string string string string string string string string string string string string string string",
      "definition": "string",
      "id": 1,
      "applications": [
        {
          "application": "string",
          "number": 1
        },
        {
          "application": "string",
          "number": 2
        },
        {
          "application": "string",
          "number": 3
        },
        {
          "application": "string",
          "number": 4
        },
        {
          "application": "string",
          "number": 5
        }
      ]
    },
    "colony": {
      "country": "JP",
      "id": 1
    },
    "user": {
      "username": "crusader",
      "email": "user@example.com",
      "country": "AF",
      "id": 1,
      "created": "2024-08-14"
    }
  },
  {
    "name": "ixora",
    "gender": "female",
    "age": 25,
    "role": "string",
    "id": 2,
    "created": "2024-08-14",
    "cursed_technique": {
      "name": "string",
      "definition": "string",
      "id": 2,
      "applications": [
        {
          "application": "string",
          "number": 1
        },
        {
          "application": "string",
          "number": 2
        },
        {
          "application": "string",
          "number": 3
        },
        {
          "application": "string",
          "number": 4
        },
        {
          "application": "string",
          "number": 5
        }
      ]
    },
    "colony": {
      "country": "JP",
      "id": 1
    },
    "user": {
      "username": "sparrowking",
      "email": "user2@example.com",
      "country": "AF",
      "id": 2,
      "created": "2024-08-14"
    }
  },
  {
    "name": "string",
    "gender": "male",
    "age": 90,
    "role": "string",
    "id": 3,
    "created": "2024-08-14",
    "cursed_technique": {
      "name": "string",
      "definition": "string",
      "id": 3,
      "applications": [
        {
          "application": "string",
          "number": 1
        },
        {
          "application": "string",
          "number": 2
        },
        {
          "application": "string",
          "number": 3
        },
        {
          "application": "string",
          "number": 4
        },
        {
          "application": "string",
          "number": 5
        }
      ]
    },
    "colony": {
      "country": "JP",
      "id": 1
    },
    "user": {
      "username": "string",
      "email": "user3@example.com",
      "country": "AF",
      "id": 3,
      "created": "2024-08-14"
    }
  }
];

export async function checkLogin() {
    const tokenExist = (await cookies()).get("token");
    if (tokenExist) {
        redirect('/dashboard');
    } else {
        redirect('/login');
    }
}

