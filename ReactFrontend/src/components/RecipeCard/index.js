import {React, useEffect, useState} from 'react';
import {useNavigate} from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHeart as farHeart } from '@fortawesome/free-regular-svg-icons';
import { faHeart as fasHeart } from '@fortawesome/free-solid-svg-icons';
import './style.css';

const RecipeCard = ({recipe}) => {
    const [authenticated, setAuthenticated] = useState(false)
    const [favorite, setFavorite] = useState({favorited: false, favoriteid: null})
    const navigate = useNavigate();
    useEffect(() => {
        const token = localStorage.getItem('token');
        // fetch from isfavorited endpoint
        fetch(`http://127.0.0.1:8000/userdata/${recipe.id}/is-favorited/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (response.ok) {
                setAuthenticated(true);
                return response.json().then((data) => {
                    setFavorite({favorited: data.favorited, favoriteid: data.frid})
                })
            }
            else {
                setAuthenticated(false)
            }
        })
    }, [])

    const handleCardClick = (e) => {
        e.preventDefault();
        navigate(`/recipes/${recipe.id}/details`);
    }

    const handleFavClick = (e) => {
        e.preventDefault();
        e.stopPropagation();
        const token = localStorage.getItem('token');
        if (favorite.favorited) {
            fetch(`http://127.0.0.1:8000/userdata/favorited-recipe=${favorite.favoriteid}/RD-favorited-recipe/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                if (response.status === 204) {
                    setFavorite({favorited: false, favoriteid: null})
                }
                else {
                    return response.json().then((data) => {
                        console.log(data.detail)
                    })
                }
            })
        }
        else {
            fetch(`http://127.0.0.1:8000/userdata/recipe=${recipe.id}/create-favorited-recipe/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                if (response.ok) {
                    return response.json().then((data) => {
                        setFavorite({favorited: true, favoriteid: data.id})
                    })
                }
                else {
                    return response.json().then((data) => {
                        console.log(data.detail)
                    })
                }
            })
        }
    }

    return (
        <div className="card" onClick={handleCardClick}>
            <img className="card-img-top" src={recipe.picture} alt="Card image" style={{ width: '100%', height: '60%' }}/>
            <div className="card-body">
                <h4 className="card-title">{recipe.title}</h4>
                <p className="card-text">Cooking Time: {recipe.time} {recipe.time_unit}</p>
                
                <div className="row" style={{ paddingTop: '1em' }}>
                    {authenticated && <FontAwesomeIcon icon={favorite.favorited ? fasHeart : farHeart} onClick={handleFavClick}/>}
                    <div className="col-sm">
                        <p>Rating: {recipe.rating}</p>
                    </div>
                    <div className="col-sm">
                        <p>Likes: {recipe.likes}</p>
                    </div>
                </div>
            </div>
        </div>
    )
}
export default RecipeCard