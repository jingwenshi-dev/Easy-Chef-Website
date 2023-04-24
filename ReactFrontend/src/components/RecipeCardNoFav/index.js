import {React} from 'react';
import {useNavigate} from 'react-router-dom';

const RecipeCardNoFav = ({recipe}) => {
    const navigate = useNavigate();
    const handleCardClick = (e) => {
        e.preventDefault();
        navigate(`/recipes/${recipe.id}/details`);
    }
    return (
        <div className="card" onClick={handleCardClick}>
            <img className="card-img-top" src={recipe.picture} alt="Card image" style={{ width: '100%', height: '60%' }}/>
            <div className="card-body">
                <h4 className="card-title">{recipe.title}</h4>
                <p className="card-text">Cooking Time: {recipe.time} {recipe.time_unit}</p>
                <div className="row" style={{ paddingTop: '1em' }}>
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

export default RecipeCardNoFav;