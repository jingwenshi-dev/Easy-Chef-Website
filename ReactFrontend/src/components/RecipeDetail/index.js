import React, {useEffect, useState} from "react";
import "./style.css";
import {useParams} from "react-router-dom";

const RecipeDetail = () => {
    let { recipeID } = useParams()
    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

    const [title, setTitle] = useState("")
    const [description, setDescription] = useState("")
    const [picture, setPicture] = useState(null)
    const [cuisine, setCuisine] = useState('')
    const [diet, setDiet] = useState('')
    const [time, setTime] = useState('')
    const [time_unit, setTimeUnit] = useState('')
    const [createdDate, setCreatedDate] = useState('')
    const [likes, setLikes] = useState('')
    const [rating, setRating] = useState('')

    const [steps, setSteps] = useState([{id: -1,  number: 1, description: '', picture: null }])
    const [ingredients, setIngredients] = useState([{ iid: -1, name: '', amount: '', unit: '' }])
    const [comments, setComments] = useState([{username: '', message: '', file: '',  createdDate: ''}])

    const [userComment, setUserComment] = useState('')
    const [commentImg, setCommentImg] = useState(null)

    const [authenticated, setAuthenticated] = useState(false)
    const [shopping, setShopping] = useState({inShopping: false, shoppingID: null})

    const [token, setToken] = useState(null)

    useEffect(() => {
        const token = localStorage.getItem('token');
        setToken(token);

        const fillRecipe = async () => {
            const recipeResponse = await fetch(`http://127.0.0.1:8000/recipes/recipe=${recipeID}/details/`)

            const recipeData = await recipeResponse.json()
            console.log(recipeData)

            if (!recipeResponse.ok) {
                alert("An unexpected error has occurred.")
                window.location.replace('/')
            }

            setTitle(recipeData.recipe.title)
            setDescription(recipeData.recipe.description)
            setPicture(recipeData.recipe.picture)
            setCuisine(recipeData.recipe.cuisine)
            setDiet(recipeData.recipe.diet)
            setTime(recipeData.recipe.time)
            setTimeUnit(recipeData.recipe.time_unit)
            setCreatedDate(recipeData.recipe.createdDate)
            setLikes(recipeData.recipe.likes)
            setRating(recipeData.recipe.rating)

            const stepLst = recipeData.step.map(({ recipe, ...step }) => step)
            setSteps(stepLst)

            const ingredientLst = recipeData.recipe_ingredient.map(({ recipe, ingredient, ...ingredientData }) => ({
                ...ingredientData,
                iid: ingredient.id,
                name: ingredient.name,
            }))
            setIngredients(ingredientLst)

            const commentLst = recipeData.comment.map(({ user, ...comment }) => ({
                ...comment,
                username: user.username
            }))
            setComments(commentLst)
        }

        fetch(`http://127.0.0.1:8000/userdata/${recipeID}/in-shopping-list/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (response.ok) {
                setAuthenticated(true);
                return response.json().then((data) => {
                    setShopping({inShopping: data.inshopping, shoppingID: data.spid})
                })
            }
            else {
                setAuthenticated(false)
            }
        })

        if (recipeID) {
            fillRecipe()
        } else {
            alert("Oops! This is not the webpage you are looking for.")
            console.log(recipeID)
        }

    }, [recipeID])

    const submitComment = async () => {

        const formData = new FormData()
        formData.append('message', userComment)
        if (commentImg) {
            formData.append('file', commentImg)
        }

        const submitCommentResponse = await fetch(`http://127.0.0.1:8000/userdata/recipe=${recipeID}/create-comment/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
            body: formData
        })

        const submitCommentData = await submitCommentResponse.json()
        console.log(submitCommentData)

        if (!submitCommentResponse.ok) {
            if (submitCommentResponse.status === 401) {
                alert("Please log in before you post a comment.")
            } else {
                alert(`Error:${submitCommentResponse.status} ${submitCommentData}.An unexpected error has occurred.`)
            }
        }
    }

    const addtoshoppinglist = (e) => {
        e.preventDefault()
        fetch(`http://127.0.0.1:8000/userdata/recipe=${recipeID}/create-shopping-lst/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (response.ok) {
                return response.json().then((data) => {
                    setShopping({inShopping: true, shoppingID: data.id})
                })
            }
            else {
                return response.json().then((data) => {
                    console.log(data.detail)
                })
            }
        })
    }

    const removefromshoopinglist = (e) => {
        e.preventDefault()
        fetch(`http://127.0.0.1:8000/userdata/shopping-lst=${shopping.shoppingID}/RUD-shopping-lst/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (response.status === 204) {
                setShopping({inShopping: false, shoppingID: null})
            }
            else {
                return response.json().then((data) => {
                    console.log(data.detail)
                })
            }
        })
    }
    

    const ratingHandler = async (score) => {

        const formData = new FormData()
        formData.append('score', score)

        const createRatingResponse = await fetch(`http://127.0.0.1:8000/userdata/recipe=${recipeID}/create-rating/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
            body: formData
        })

        const createRatingData = await createRatingResponse.json()
        console.log(createRatingData)

        if (!createRatingResponse.ok) {
            if (createRatingResponse.status === 401) {
                alert("Please log in before you post a comment.")
            }

            else if (createRatingResponse.status === 400 && createRatingData.detail === "The current user has already rated this recipe.") {

                const updateRatingResponse = await fetch(`http://127.0.0.1:8000/userdata/rating=${recipeID}/RU-rating/`, {
                    method: 'PUT',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                    body: formData
                })

                const updateRatingData = await updateRatingResponse.json()
                console.log(updateRatingData)

                if (!updateRatingResponse.ok) {
                    alert("An unexpected error has occurred when updating your rating.")
                }

            }

            else {
                alert("An unexpected error has occurred while creating your rating.")
            }
        }

    }

    return (
        <>
        <div className="row align-items-center text-center" id="coverPage" style={{marginBottom: '3em'}}>
            <div className="col">
                <div className="row">
                    <div className="col">

                        <p style={{textAlign: 'right', paddingRight: '0.5em'}}>
                            Cuisine: {cuisine} | Diet: {diet}
                        </p>

                    </div>
                    <div className="col">

                        <p style={{textAlign: 'left', fontWeight: 700, paddingLeft: '0.5em'}}>
                            {months[parseInt(createdDate.slice(5, 7)) - 1]} {createdDate.slice(8, 10)} | {createdDate.slice(0, 4)}
                        </p>

                    </div>
                </div>

                <h1 style={{marginTop: '0.5em', marginBottom: '0.5em'}}>
                    {title}
                </h1>

                <p style={{marginTop: '0.5em', marginBottom: '0.5em'}}>
                    Cooking Time: {time} {time_unit}
                </p>

                <p>Rating: {rating} | Likes: {likes}<i className="fa-solid fa-star"></i><i className="fa-solid fa-star"></i><i
                    className="fa-solid fa-star"></i><i className="fa-solid fa-star"></i><i
                    className="fa-solid fa-star-half-stroke"></i></p>
            </div>
            <div className="col"
                 style={{height: '100vh', width: '100%', backgroundSize: 'cover', backgroundPosition: 'center',
                     backgroundImage: `url('http://127.0.0.1:8000${picture}')`}}>
            </div>
        </div>

        <div className="row align-items-center text-center" style={{marginLeft: '30em', marginRight: '30em'}}>
            <p style={{fontWeight: 500}}>
                {description}
            </p>

            <div className="row" id="Ingredients" style={{marginTop: '3em', textAlign: 'left'}}>
                <h1>Ingredients</h1>
                <hr/>
                {ingredients.map((ingredient, index) => (
                    <p key={index}>
                        {ingredient.name} - {ingredient.amount} {ingredient.unit}<br/>
                    </p>
                ))}
            </div>

            <div className="row" id="Directions" style={{marginTop: '3em', textAlign: 'left'}}>

                <h1>Directions</h1>
                <hr/>

                {steps.map((step, index) => (
                    <div className="row" key={index} style={{marginBottom: '1em'}}>
                        <h3>Step {step.number}</h3>
                        <p>
                            {step.description}
                            <br />
                            {step.picture && (<img src={`http://127.0.0.1:8000${picture}`} alt="Bootstrap"/>)}
                        </p>
                    </div>
                ))}

            </div>


            {authenticated && (<div className="row" style={{marginTop: '1em', marginBottom: '2em', textAlign: 'left'}}>
                {shopping.inShopping ? (<button className="btn btn-dark" onClick={removefromshoopinglist}>REMOVE FROM SHOPPING LIST</button>) : (<button className="btn btn-dark" onClick={addtoshoppinglist}>ADD TO SHOPPING LIST</button>)}
            </div>)}

            
            <div className="row" style={{marginTop: '1em', marginBottom: '2em', textAlign: 'left'}}>
                <hr/>
                <div className="row" style={{textAlign: 'center', color: 'darkgrey', marginBottom: '1em'}}>
                    <h5>How would you rate?</h5>

                    <div className="row" style={{ marginTop: '0.5em', display: 'flex', alignItems: 'center' }}>
                        <div className="col-auto" style={{width: '20%'}}>
                            <button className="btn btn-warning" onClick={() => ratingHandler(1)} type="button">
                                1
                            </button>
                        </div>
                        <div className="col-auto" style={{width: '20%'}}>
                            <button className="btn btn-warning" onClick={() => ratingHandler(2)} type="button">
                                2
                            </button>
                        </div>
                        <div className="col-auto" style={{width: '20%'}}>
                            <button className="btn btn-warning" onClick={() => ratingHandler(3)} type="button">
                                3
                            </button>
                        </div>
                        <div className="col-auto" style={{width: '20%'}}>
                            <button className="btn btn-warning" onClick={() => ratingHandler(4)} type="button">
                                4
                            </button>
                        </div>
                        <div className="col-auto" style={{width: '20%'}}>
                            <button className="btn btn-warning" onClick={() => ratingHandler(5)} type="button">
                                5
                            </button>
                        </div>
                    </div>

                </div>
                <hr/>

                <h3>Leave your comment</h3>

                <textarea className="form-control"
                          style={{marginTop: '0.2em', marginBottom: '1em'}}
                          placeholder="What do you think?"
                          value={userComment}
                          onChange={(e) => setUserComment(e.target.value)}
                />
                <input type="file" id="uploadCommentImg" onChange={(e) => setCommentImg(e.target.files[0])}/>
                <br />
                <br />
                <button type="submit" onClick={submitComment} className="btn btn-dark">COMMENT</button>
            </div>

            <div className="row" style={{textAlign: 'left'}}>

                <h2>Comments</h2>

                <div className="row" style={{marginBottom: '0.3em', marginTop: '0.3em'}}>

                    {comments.map((comment, index) => (
                        <React.Fragment key={index}>
                            <hr/>
                            <p style={{fontWeight: 500, marginBottom: '0.5em'}}>
                                {comment.message}
                                <br />
                                {comment.file && (<img src={`http://127.0.0.1:8000${comment.file}`} alt="Bootstrap"/>)}
                            </p>
                            <p>
                                <span>{comment.username}</span> •
                                <span> {months[parseInt(createdDate.slice(5, 7)) - 1]} {comment.createdDate.slice(8, 10)}, {comment.createdDate.slice(0, 4)}</span>
                            </p>
                        </React.Fragment>
                    ))}
                </div>
            </div>
        </div>
        </>
    )
}

export default RecipeDetail;