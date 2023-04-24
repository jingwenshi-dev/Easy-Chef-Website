import React, { useState, useEffect } from 'react';
import { Link, useNavigate, Outlet } from 'react-router-dom';
import Profile from '../Profile/ViewProfile';
import { Dropdown } from 'react-bootstrap';
import logo from '../../images/logo.png';
import blank from '../../images/blank-profile.png';
import './style.css'


const NavBar = () => {
    const [profile, setProfile] = useState(null);
    const [authenticated, setAuthenticated] = useState(false)
    const naviagate = useNavigate()
    useEffect(() => {
        const token = localStorage.getItem('token');
        fetch("http://127.0.0.1:8000/accounts/profile/details/", {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (response.ok) {
                setAuthenticated(true);
                return response.json().then((data) => {
                    setProfile(data)
                })
            }
            else {
                setAuthenticated(false);
            }
        })
        
        
    }, [])

    const logouthandler = () => {
        const token = localStorage.getItem('token');
        fetch("http://127.0.0.1:8000/accounts/logout/", {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(request => {
            if (request.ok) {
                localStorage.removeItem('token')
                window.location.reload();
            }
        })
    }

    return (
        <>
            <nav className="navbar navbar-expand-lg fixed-top bg-body-tertiary">
                <div className="container-fluid">
                    <img src={logo} style={{width: '80px', height: '80px'}}/>
                    <div className="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul className="navbar-nav me-auto mb-2 mb-lg-0">

                            <li className="nav-item">
                                <Link className="nav-link active" to="/">Home</Link>
                            </li>

                            <li className="nav-item">
                                <Link className="nav-link active" to="/my-recipe">My Recipe</Link>
                            </li>

                            <li className="nav-item">
                                <Link className="nav-link active" to="recipes/create-recipe">Add Recipe</Link>
                            </li>
                            <li className='nav-item'>
                                <Link className="nav-link active" to="/shopping-list">Shopping List</Link>
                            </li>
                        </ul>
                        {authenticated ? (
                            <>
                                {profile && profile.avatar && (<img src={profile.avatar} style={{width: '60px', height: '60px', borderRadius: '50%', marginRight: '20px'}}/>)}
                                {profile && !profile.avatar && (<img src={blank} style={{width: '60px', height: '60px', borderRadius: '50%', marginRight: '20px'}}/>)}
                                
                                {profile && profile.email && profile.phone && (    
                                    <Dropdown>
                                        <Dropdown.Toggle>
                                        User Info
                                        </Dropdown.Toggle>
                                        <Dropdown.Menu>
                                            <Profile email={profile.email} phone={profile.phone}/>
                                            <Link className="dropdown-item" to="/accounts/profile/edit">Edit Profile</Link>
                                            <Dropdown.Item onClick={logouthandler}>Log out</Dropdown.Item>
                                        </Dropdown.Menu>
                                    </Dropdown>
                                )}
                            </>
                        ) : (
                            <Link className='nav-item' to="/accounts/login">Log in</Link> 
                        )}
                    </div>
                </div>
            </nav>
            <Outlet/>
        </>
    )
}
export default NavBar;