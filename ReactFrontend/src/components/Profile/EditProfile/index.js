import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './style.css';

const EditProfile = () => {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [password2, setPassword2] = useState("");
    const [phone, setPhone] = useState("");
    const [avatar, setAvatar] = useState(null);
    const [errors, setErrors] = useState(null);
    const [token, setToken] = useState(null);

    const naviagate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('token');
        setToken(token);
    }, [])

    const submithandler = (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('username', username);
        formData.append('email', email);
        formData.append('password', password);
        formData.append('password2', password2);
        formData.append('phone', phone);
        formData.append('avatar', avatar);
        console.log(Object.fromEntries(formData));
        fetch(
            "http://127.0.0.1:8000/accounts/profile/edit/", {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
                body: formData,
            }
        )
        .then(response => {
            if (response.ok) {
                naviagate('/');
            }
            else {
                return response.json().then((data) => {
                    setErrors(data);
                })
            }
        });
    }

    return (
        <div className="container-fluid">
        <h2 className="text-center">Edit Profile</h2>
        <form onSubmit={submithandler}>
            <div className="form-group">
                <label htmlFor="avatar">Update jpg to change your avatar</label>
                <input type="file" className="form-control-file" id="avatar" onChange={e => setAvatar(e.target.files[0])}/>
            </div>
            <div className="form-group">
                <label htmlFor="username">Username</label>
                <input type="text" className="form-control" name="username" id="username" placeholder="Username" onChange={e => setUsername(e.target.value)}/>
            </div>
            {errors && errors.username && (
                <>
                    <br/><p style={{ color: 'red' }}>{errors.username}</p>
                </>
            )}
            <div className="form-group">
                <label htmlFor="password">Password</label>
                <input type="password" className="form-control" name="password" id="password" placeholder="New password" onChange={e => setPassword(e.target.value)}/>
            </div>
            {errors && errors.password && (
                <>
                    <p style={{ color: 'red' }}>{errors.password}</p>
                </>
            )}
            <div className="form-group">
                <label htmlFor="password2">Confirm Password</label>
                <input type="password" className="form-control" name="password2" id="password2" placeholder="New password" onChange={e => setPassword2(e.target.value)}/>
            </div>
            {errors && errors.password2 && (
                <>
                    <p style={{ color: 'red' }}>{errors.password2}</p>
                </>
            )}
            <div className="form-group">
                <label htmlFor="email">Email</label>
                <input type="email" className="form-control" name="email" id="email" placeholder="Enter Email" onChange={e => setEmail(e.target.value)}/>
            </div>
            {errors && errors.email && (
                <>
                    <br/><p style={{ color: 'red' }}>{errors.email}</p>
                </>
            )}
            <div className="form-group">
                <label htmlFor="phoneNumber">Phone Number</label>
                <input type="tel" className="form-control" name="phone" id="phoneNumber" placeholder="Enter Phone Number" onChange={e => setPhone(e.target.value)}/>
            </div>
            <div className="button-group">
                <button type="submit" className="button" >Save</button>
            </div>
        </form>
    </div>
    )
}

export default EditProfile;