import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './style.css';

const Login = () => {
    const [username, setUsername] = useState();
    const [password, setPassword] = useState();
    const [error, setError] = useState(null);

    const naviagate = useNavigate();

    const submithandler = (e) => {
        e.preventDefault();
        fetch (
            "http://127.0.0.1:8000/accounts/login/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'username': username,
                    'password': password
                })
            }
        )
        .then(response => {
            return response.json().then(data => {
                if (response.ok) {
                    const token = data.access;
                    localStorage.setItem('token', token);
                    console.log(localStorage);
                    naviagate('/');
                    window.location.reload();
                }
                else {
                    setError(data);
                }
            })
        });
    }

    return (
        <div className="container-fluid" onSubmit={submithandler}>
        <div className="row align-items-center g-0">
            <div className="col">
                <form className="form-horizontal">
                    <h2>Log in to your account</h2>
                    <h3>Welcome Back!</h3>
                    <div className="form-row">
                            <input type="text" className="form-control" name="username" id="Username" placeholder="&#xf0e0;   Username" style={{fontFamily: ['Open Sans', 'Font Awesome 5 Free']}} required onChange={e => setUsername(e.target.value)}/>
                    </div>
                    <div className="form-row">
                            <input type="password" className="form-control" name="password" id="Password1" placeholder="&#xf023;   Enter your password" style={{fontFamily: ['Open Sans', 'Font Awesome 5 Free']}} required onChange={e => setPassword(e.target.value)}/>
                    </div>
                    {error && error.detail && (
                        <>
                            <p style={{ color: 'red' }}>{error.detail}</p>
                        </>
                    )}
                    <p id="login">Not registered yet? <Link className="link" to="/accounts/signup">Sign up</Link></p>
                    <div className="form-row">
                        <button type="submit" className="Button">LOG IN</button>
                    </div>
                    <p id="agreement">By continuing, you agree to accept our <a className="link" href="">Privacy Police</a> & <a className="link" href="">Terms of Services</a>.</p>
                </form>
            </div>
            <div className="col" style={{height: '100vh', width: '100%', backgroundSize: 'cover', backgroundPosition: 'center', backgroundImage: "url('https://img.delicious.com.au/EEJ2ozkv/del/2020/10/green-tea-noodles-with-sticky-sweet-chilli-salmon-140868-2.jpg')"}}>
            </div>
        </div>
    </div>
    )
}

export default Login;