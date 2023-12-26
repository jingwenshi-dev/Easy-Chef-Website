import React, {  useState } from "react";
import { Link, useNavigate } from 'react-router-dom';
import './style.css';

const Signup = () => {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [password2, setPassword2] = useState("");
    const [errors, setErrors] = useState(null);

    const naviagate = useNavigate();

    const submithandler = (e) => {
        e.preventDefault();
        fetch (
            "http://127.0.0.1:8000/accounts/signup/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'username': username,
                    'email': email,
                    'password': password,
                    'password2': password2
                })
            }
        )
        .then(response => {
            if (response.ok) {
                naviagate('/accounts/login');
            }
            else if (response.status === 400) {
                return response.json().then((data) => {
                    setErrors(data);
                })
            }
        });
    }

    return (
        <div className="container-fluid">
            <div className="row align-items-center g-0">
                <div className="col">
                    <form className="form-horizontal" onSubmit={submithandler}>
                        <h3>Do you want to have a healthy meal in 10 mins?</h3>
                        <h2>Join us right now!</h2>
                        <div className="form-row">
                            <input type="text" className="form-control" name="username" id="Username" placeholder="&#xf0e0;   Username" style={{fontFamily: ['Open Sans', 'Font Awesome 5 Free']}} required onChange={e => setUsername(e.target.value)}/>
                        </div>
                        {errors && errors.username && (
                            <>
                                <br/><p style={{ color: 'red' }}>{errors.username}</p>
                            </>
                        )}
                        <div className="form-row">
                            <input type="email" className="form-control" name="email" id="Email" placeholder="&#xf0e0;   youremail@example.com" style={{fontFamily: ['Open Sans', 'Font Awesome 5 Free']}} required onChange={e => setEmail(e.target.value)}/>
                        </div>
                        {errors && errors.email && (
                            <>
                                <br/><p style={{ color: 'red' }}>{errors.email}</p>
                            </>
                        )}
                        <div className="form-row">
                            <input type="password" className="form-control" name="password" id="Password1" placeholder="&#xf023;   Enter your password" style={{fontFamily: ['Open Sans', 'Font Awesome 5 Free']}} required onChange={e => setPassword(e.target.value)}/>
                        </div>
                        {errors && errors.password && (
                            <>
                                <p style={{ color: 'red' }}>{errors.password}</p>
                            </>
                        )}
                        <div className="form-row">
                            <input type="password" className="form-control" name="password2" id="Password2" placeholder="&#xf023;   Re-enter your password" style={{fontFamily: ['Open Sans', 'Font Awesome 5 Free']}} required onChange={e => setPassword2(e.target.value)}/>
                        </div>
                        {errors && errors.password2 && (
                            <>
                                <p style={{ color: 'red' }}>{errors.password2}</p>
                            </>
                        )}
                        <p id="login">Already have an account? <Link className="link" to="/accounts/login">Log in</Link></p>
                        <div className="form-row">
                            <button type="submit" className="Button">SIGN UP</button>
                        </div>
                        <p id="agreement">By continuing, you agree to accept our <a className="link" href="">Privacy Police</a> & <a className="link" href="">Terms of Services</a>.</p>
                    </form>
                </div>
                <div className="col" style={{height: '100vh', width: '100%', backgroundSize: 'cover', backgroundPosition: 'center', backgroundImage: "url('https://static.onecms.io/wp-content/uploads/sites/44/2021/12/30/butternut-squash-and-black-bean-enchiladas.jpg')"}}>
                </div>
            </div>
        </div>
    )
}

export default Signup;