// The login page
import styles from '@/app/login/login.module.css';
import { lusitana } from '../layout';

export default function LoginPage() {
    return (
        <main className={`min-h-screen min-w-full backdrop-blur`}>
            <Form />
        </main>
            
    )
}

function Form() {
    return (
        <form action="" className='mx-auto w-fit mt-10 '>
            <h1 className={`font-bold text-lg ${lusitana.className}`}>Login</h1>
            <div className='flex flex-col md:flex-row p-3 rounded-md border'>
                <label htmlFor="username">
                    username
                    <input className='m-4 dark:text-black rounded p-1' title="username" type="text" id='userId' />
                </label>
                
                <label htmlFor="pwId">
                    password
                    <input className='m-4 dark:text-black rounded p-1' title="password" type="password" name="password" id="pwId" />
                </label>
                
            </div>
        </form>
    )
}