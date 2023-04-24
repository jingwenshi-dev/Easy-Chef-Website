import {React, useEffect, useState} from 'react';
import RecipeCardNoFav from '../RecipeCardNoFav';
import './style.css'
import MyRecipeCard from '../MyRecipeCard';

const MyRecipes = () => {
    const count = 1
    const [authenticated, setAuthenticated] = useState(false)
    const [display, setDisplay] = useState('created')
    const [created, setCreated] = useState({recipes: [], page: 1})
    const [favorited, setFavorited] = useState({recipes: [], page: 1})
    const [interacted, setInteracted] = useState({recipes: [], page: 1})
    const [hasEnded, setHasEnded] = useState(true);
    const [firstPage, setFirstPage] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem('token')
        if (display === 'created') {
            fetch(`http://127.0.0.1:8000/userfunction/my-recipe/created/?count=${count}&page=${created.page}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                if (response.ok) {
                    setAuthenticated(true)
                    return response.json().then(data => {
                        setCreated({...created, recipes: data.results})
                        setFirstPage(data.previous === null);
                        setHasEnded(data.next === null);
                    })
                }
                else if (response.status === 401) {
                    setAuthenticated(false)
                }
                else {
                    console.log('unexpected error')
                }
            })
        }
        else if (display === 'favorited') {
            fetch(`http://127.0.0.1:8000/userfunction/my-recipe/favorited/?count=${count}&page=${favorited.page}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                if (response.ok) {
                    setAuthenticated(true)
                    return response.json().then(data => {
                        setFavorited({...favorited, recipes: data.results})
                        setFirstPage(data.previous === null);
                        setHasEnded(data.next === null);
                    })
                }
                else if (response.status === 401) {
                    setAuthenticated(false)
                }
                else {
                    console.log('unexpected error')
                }
            })
        }
        else if (display === 'interacted') {
            fetch(`http://127.0.0.1:8000/userfunction/my-recipe/interacted/?count=${count}&page=${interacted.page}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                if (response.ok) {
                    setAuthenticated(true)
                    return response.json().then(data => {
                        setInteracted({...interacted, recipes: data.results})
                        setFirstPage(data.previous === null);
                        setHasEnded(data.next === null);
                    })
                }
                else if (response.status === 401) {
                    setAuthenticated(false)
                }
                else {
                    console.log('unexpected error')
                }
            })
        }

    }, [display, created.page, favorited.page, interacted.page])

    const handlePrev = (e) => {
        e.preventDefault()
        if (display === 'created') {
            setCreated({...created, page: created.page - 1})
        }
        if (display === 'favorited') {
            setFavorited({...favorited, page: favorited.page - 1})
        }
        if (display === 'interacted') {
            setInteracted({...interacted, page: interacted.page - 1})
        }
    }

    const handleNext = (e) => {
        e.preventDefault()
        if (display === 'created') {
            setCreated({...created, page: created.page + 1})
        }
        if (display === 'favorited') {
            setFavorited({...favorited, page: favorited.page + 1})
        }
        if (display === 'interacted') {
            setInteracted({...interacted, page: interacted.page + 1})
        }
    }

    const switchtocreated = (e) => {
        e.preventDefault()
        setDisplay('created')
    }
    
    const switchtofavorited = (e) => {
        e.preventDefault()
        setDisplay('favorited')
    }
    
    const switchtointeracted = (e) => {
        e.preventDefault()
        setDisplay('interacted')
    }

    return (
        <>
            {authenticated ? (<div className="main-container">
                <div className='pagetraverse d-flex'>
                    {display === "created" ? <button className='btn btn-danger' style={{ marginLeft: '2em', marginRight: '2em' }} onClick={switchtocreated}>Recipes I Created</button> : <button className='btn btn-warning' style={{ marginLeft: '2em', marginRight: '2em' }} onClick={switchtocreated}>Recipes I Created</button>}
                    {display === "favorited" ? <button className='btn btn-danger' style={{ marginLeft: '2em', marginRight: '2em' }} onClick={switchtofavorited}>My Favorite Recipes</button> : <button className='btn btn-warning' style={{ marginLeft: '2em', marginRight: '2em' }} onClick={switchtofavorited}>My Favorite Recipes</button>}
                    {display === "interacted" ? <button className='btn btn-danger' style={{ marginLeft: '2em', marginRight: '2em' }} onClick={switchtointeracted}>Interacted Recipes</button> : <button className='btn btn-warning' style={{ marginLeft: '2em', marginRight: '2em' }} onClick={switchtointeracted}>Interacted Recipes</button>}
                </div>
                <div className='recipes-container'>
                    {display === 'created' && (created.recipes?.map(recipe => (
                        <MyRecipeCard key={recipe.id} className='recipe' recipe={recipe}/>
                    )))}
                    {display === 'favorited' && (favorited.recipes?.map(recipe => (
                        <RecipeCardNoFav key={recipe.id} className='recipe' recipe={recipe}/>
                    )))}
                    {display === 'interacted' && (interacted.recipes?.map(recipe => (
                        <RecipeCardNoFav key={recipe.id} className='recipe' recipe={recipe}/>
                    )))}
                </div>
                <div className='pagetraverse d-flex'>
                    <button className='button' disabled={firstPage} style={{ marginLeft: '2em', marginRight: '2em' }} onClick={handlePrev}>prev</button>
                    <button className='button' disabled={hasEnded} style={{ marginLeft: '2em', marginRight: '2em' }} onClick={handleNext}>next</button>
                </div>
            </div>) : (
                <h1>You Are Not Logged in. Please Log to View This Page.</h1>
            )}
        </>
    )
}

export default MyRecipes;