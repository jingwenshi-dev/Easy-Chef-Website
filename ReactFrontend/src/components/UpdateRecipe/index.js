import React, { useState, useEffect } from "react";
import "./style.css";
import { useParams } from 'react-router-dom';

const UpdateRecipe = () => {
    let { recipeID } = useParams()

    let removedSteps = []

    const [title, setTitle] = useState("")
    const [description, setDescription] = useState("")
    const [picture, setPicture] = useState(null)
    const [cuisine, setCuisine] = useState('Other')
    const [diet, setDiet] = useState('Other')
    const [time, setTime] = useState('')
    const [time_unit, setTimeUnit] = useState('Mins')
    const [steps, setSteps] = useState([{id: -1,  number: 1, description: '', picture: null }])
    const [ingredients, setIngredients] = useState([{ iid: -1, name: '', amount: '', unit: 'gram' }])
    const [token, setToken] = useState(null)
    const [errorMessage, setErrorMessage] = useState({})

    const validateForm = () => {
        let errors = {}

        if (!title.trim()) {
            errors.title = 'Title cannot be empty.'
        }
        if (!description.trim()) {
            errors.description = 'Description cannot be empty.'
        }
        if (picture === null) {
            errors.picture = 'Picture cannot be empty.'
        }
        if (!cuisine.trim()) {
            errors.cuisine = 'Cuisine cannot be empty.'
        }
        if (!diet.trim()) {
            errors.diet = 'Diet cannot be empty.'
        }
        if (!time.trim()) {
            errors.time = 'Cook time cannot be empty.'
        }
        if (!time_unit.trim()) {
            errors.time_unit = 'Cook time unit cannot be empty.'
        }

        if (steps.length === 0) {
            errors.stepEmp = 'There must be at least one step.'
        } else {
            for (const [index, step] of steps.entries()) {
                if (!step.description.trim()) {
                    errors[`step${index}_description`] = `Description of step ${index + 1} cannot be empty.`
                }
                if (step.picture === null) {
                    errors[`step${index}_picture`] = `Picture of step ${index + 1} cannot be empty.`
                }
            }
        }

        if (ingredients.length === 0) {
            errors.ingredientEmp = 'There must be at least one ingredient.'
        } else {
            for (const [index, ingredient] of ingredients.entries()) {
                if (!ingredient.name.trim()) {
                    errors[`ingredient${index}_description`] = `Name of ingredient ${index + 1} cannot be empty.`
                }
                if (ingredient.amount === '') {
                    errors[`ingredient${index}_amount`] = `Amount of ingredient ${index + 1} cannot be empty.`;
                }
                if (!ingredient.unit.trim()) {
                    errors[`ingredient${index}_unit`] = `Unit of ingredient ${index + 1} cannot be empty.`;
                }
            }
        }

        setErrorMessage(errors)
        return Object.keys(errors).length === 0
    }

    useEffect(() => {
        const token = localStorage.getItem('token')
        setToken(token)

        console.log(token)

        const fillRecipe = async () => {
            const recipeResponse = await fetch(`http://127.0.0.1:8000/recipes/recipe=${recipeID}/fetch/`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })

            const recipeData = await recipeResponse.json()
            console.log(recipeData)

            if (!recipeResponse.ok) {
                if (recipeResponse.status === 401) {
                    alert("Please log in first before you edit a recipe!")
                    window.location.replace('/accounts/login')
                }
                else if (recipeResponse.status === 403) {
                    alert('Please log in first before you create a recipe!')
                    window.location.replace('/accounts/login')
                }
            }

            setTitle(recipeData.recipe.title)
            setDescription(recipeData.recipe.description)
            setPicture(recipeData.recipe.picture)
            setCuisine(recipeData.recipe.cuisine)
            setDiet(recipeData.recipe.diet)
            setTime(recipeData.recipe.time)
            setTimeUnit(recipeData.recipe.time_unit)

            const stepLst = recipeData.step.map(({ recipe, ...step }) => step)
            setSteps(stepLst)

            const ingredientLst = recipeData.recipe_ingredient.map(({ recipe, ingredient, ...ingredientData }) => ({
                ...ingredientData,
                iid: ingredient.id,
                name: ingredient.name,
            }))
            setIngredients(ingredientLst)

        }

        if (recipeID) {
            fillRecipe()
        } else {
            alert("Oops! This is not the webpage you are looking for.")
            console.log(recipeID)
        }

    }, [recipeID])

    const stepHandler = (index, field, value) => {
        const newSteps = [...steps]
        newSteps[index][field] = value
        setSteps(newSteps)
    }

    const removeStep = (index) => {
        removedSteps.push(steps[index].id)
        const newSteps = steps
            .filter((_, i) => i !== index)
            .map((step, i) => ({id: step.id, number: i + 1, description: step.description, picture: step.picture }))
        setSteps(newSteps)
    }

    const addStep = () => {
        setSteps([...steps, {id: -1, number: steps.length + 1, description: '', picture: null }])
    }

    const ingredientHandler = (index, field, value) => {
        const newIngredients = [...ingredients]
        newIngredients[index][field] = value
        setIngredients(newIngredients)
    }

    const removeIngredient = (index) => {
        const newIngredients = ingredients.filter((_, i) => i !== index)
        setIngredients(newIngredients)
    }

    const addIngredient = () => {
        setIngredients([...ingredients, { iid: -1, name: '', amount: '', unit: 'gram' }])
    }

    const submitHandler = async (e) => {
        e.preventDefault()

        if (!validateForm()) {
            return false
        }

        const formData = new FormData()
        formData.append('title', title)
        formData.append('description', description)
        formData.append('picture', picture)
        formData.append('time', time)
        formData.append('time_unit', time_unit)
        formData.append('cuisine', cuisine)
        formData.append('diet', diet)

        const response = await fetch(
            `http://127.0.0.1:8000/recipes/recipe=${recipeID}/RUD-recipe/`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
                body: formData
            }
        )

        const responseData = await response.json()
        console.log(responseData)

        if (!response.ok) {
            if (response.status === 401) {
                alert("Please log in first before you edit a recipe!")
                window.location.replace('/accounts/login')
            } else {
                alert(`Error ${response.status}: ${responseData}. An unexpected error occurred while updating the main body of the recipe.`)
                return;
            }
        }

        recipeID = responseData['id']

        for (const sid of removedSteps) {
            const delStepResponse = await fetch(
                `http://127.0.0.1:8000/recipes/recipe=${recipeID}&step=${sid}/RUD-step/`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    }
                }
            )

            const delStepData = await delStepResponse.json()

            if (!delStepResponse.ok) {
                if (delStepResponse.status === 401) {
                    alert("Please log in first before you edit a recipe!")
                    window.location.replace('/accounts/login')
                } else {
                    alert(`Error ${delStepResponse.status}: ${delStepData}. An unexpected error occurred while deleting a step.`)
                }
            }
        }

        for (const step of steps) {
            const stepData = new FormData()
            stepData.append('number', step.number)
            stepData.append('description', step.description)
            stepData.append('picture', step.picture)

            if (step.id !== -1) {
                const stepResponse = await fetch(`http://127.0.0.1:8000/recipes/recipe=${recipeID}&step=${step.id}/RUD-step/`, {
                    method: 'PUT',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    body: stepData
                })
                const stepResponseData = await stepResponse.json()
                console.log(stepResponseData)

                if (!stepResponse.ok) {
                    if (stepResponse.status === 401) {
                        alert("Please log in first before you edit a recipe!")
                        window.location.replace('/accounts/login')
                    } else {
                        alert(`Error ${stepResponse.status}: ${stepResponseData}. An unexpected error occurred while updating a step.`)
                        return;
                    }
                }

            } else {
                const stepResponse = await fetch(`http://127.0.0.1:8000/recipes/recipe=${recipeID}/create-step/`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    body: stepData
                })
                const stepResponseData = await stepResponse.json()
                console.log(stepResponseData)

                if (!stepResponse.ok) {
                    if (stepResponse.status === 401) {
                        alert("Please log in first before you edit a recipe!")
                        window.location.replace('/accounts/login')
                    } else {
                        alert(`Error ${stepResponse.status}: ${stepResponseData}. An unexpected error occurred while creating a step.`)
                        return;
                    }
                }
            }
        }

        for (const ingredient of ingredients) {

            const deleteIngredientResponse = await fetch(`http://127.0.0.1:8000/recipes/recipe=${recipeID}&ingredient=${ingredient.iid}/RUD-recipe-ingredient/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                }
            })

            let deletedData = await deleteIngredientResponse.json()
            console.log(deletedData)

            if (!deleteIngredientResponse.ok) {
                if (deleteIngredientResponse.status === 401) {
                    alert("Please log in first before you edit a recipe!")
                    window.location.replace('/accounts/login')
                }

                else if (deleteIngredientResponse.status !== 204) {
                    alert(`Error ${deleteIngredientResponse.status}: ${deletedData}. An unexpected error occurred while deleting an ingredient.`)
                    return;
                }
            }

            const getIngredientResponse = await fetch(
                `http://127.0.0.1:8000/recipes/find-ingredient/?ingredient=${ingredient.name}`
            )

            let ingredientData = await getIngredientResponse.json()
            let iid = ingredientData['id']

            if (!getIngredientResponse.ok) {
                if (getIngredientResponse.status === 401) {
                    alert("Please log in first before you edit a recipe!")
                    window.location.replace('/accounts/login')
                } else {
                    alert(`Error ${getIngredientResponse.status}: ${ingredientData}. An unexpected error occurred while retrieving an ingredient.`)
                    return;
                }
            }

            if (!iid) {
                const createIngredientResponse = await fetch(`http://127.0.0.1:8000/recipes/recipe=${recipeID}/create-ingredient/`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ name: ingredient.name })
                })

                ingredientData = await createIngredientResponse.json()
                console.log(ingredientData)

                if (!createIngredientResponse.ok) {
                    if (createIngredientResponse.status === 401) {
                        alert("Please log in first before you edit a recipe!")
                        window.location.replace('/accounts/login')
                    } else {
                        alert(`Error ${createIngredientResponse.status}: ${ingredientData}. An unexpected error occurred while creating an ingredient.`)
                        return;
                    }
                }
            }

            iid = ingredientData.id

            const createRecipeIngredientResponse= await fetch(`http://127.0.0.1:8000/recipes/recipe=${recipeID}&ingredient=${iid}/create-recipe-ingredient/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ amount: ingredient.amount, unit: ingredient.unit }),
            })

            const recipeIngredientData = await createRecipeIngredientResponse.json()
            console.log(recipeIngredientData)

            if (!createRecipeIngredientResponse.ok) {
                if (createRecipeIngredientResponse.status === 401) {
                    alert("Please log in first before you edit a recipe!")
                    window.location.replace('/accounts/login')
                } else {
                    alert(`Error ${createRecipeIngredientResponse.status}: ${recipeIngredientData}. An unexpected error occurred while creating an ingredient with amount and unit.`)
                    return;
                }
            }
        }
        alert('Your recipe has updated!')
        window.location.replace('/')
    }

    return (
        <form className="form-horizontal" style={{marginLeft: '30%', marginRight: '30%'}}>
            <h1 style={{marginBottom: '1em', marginTop: '1em', fontWeight: 700}}>Post your Recipe</h1>
            <h5 style={{marginBottom: '2em', fontWeight: 500}}>Sharing a personal recipe to your friends, family and the whole Easy Chef community!</h5>

            <div className="row">
                <div className="col" style={{marginRight: '1em'}}>
                    <div className="row">
                        <label htmlFor="recipeTitle" style={{textAlign: 'left', padding: 0, fontWeight: 700}}>Recipe
                            Title</label>
                        {errorMessage.title && <p className="error-message" style={{color: 'red', fontWeight: 700}}>{errorMessage.title}</p>}
                        <input type="text" className="form-control" id="recipeTitle" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Give a title to your recipe" required />
                    </div>

                    <div className="row">
                        <label htmlFor="recipeTitle"
                               style={{textAlign: 'left', padding: 0, fontWeight: 700}}>Description</label>
                        {errorMessage.description && <p className="error-message" style={{color: 'red', fontWeight: 700}}>{errorMessage.description}</p>}
                        <textarea className="form-control" id="recipeDescription" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Share the story behind your recipe!" required></textarea>
                    </div>
                </div>

                <div className="col uploadImg" style={{marginLeft: '1em'}}>
                    {errorMessage.picture && <p className="error-message" style={{color: 'red', fontWeight: 700}}>{errorMessage.picture}</p>}
                    <label htmlFor="uploadRecipeImages" style={{marginTop: '3em'}}>
                        <i className="fa-5x fa-solid fa-cloud-arrow-up"></i>
                        <br/>Upload Images</label>
                    <input type="file" className="form-control" id="uploadRecipeImages" onChange={(e) => setPicture(e.target.files[0])} style={{display: 'none'}} required />
                </div>

            </div>

            <hr/>

            <div className="row">

                <p style={{textAlign: 'left', padding: 0, fontWeight: 700}}>Ingredients</p>

                <p style={{textAlign: 'left', padding: 0, marginTop: '0.8em'}}>
                    Enter one ingredient per line. Include the quantity (i.e. cups, tablespoons) and any special preparation (i.e. sifted, softened, chopped).
                </p>

                {errorMessage.ingredientEmp && <p className="error-message" style={{color: 'red', fontWeight: 700}}>{errorMessage.ingredientEmp}</p>}

                {ingredients.map((ingredient, index) => (

                    <div key={index} className="row">

                        {errorMessage[`ingredient${index}_description`] && <p className="error-message" style={{color: 'red', fontWeight: 700}}>{errorMessage[`ingredient${index}_description`]}</p>}
                        {errorMessage[`ingredient${index}_amount`] && <p className="error-message" style={{color: 'red', fontWeight: 700}}>{errorMessage[`ingredient${index}_amount`]}</p>}
                        {errorMessage[`ingredient${index}_unit`] && <p className="error-message" style={{color: 'red', fontWeight: 700}}>{errorMessage[`ingredient${index}_unit`]}</p>}

                        <div className="col-auto" style={{width: '25%'}}>
                            <div className="row" style={{marginRight: '0.5em', marginLeft: '0.5em', padding: 0}}>
                                <label htmlFor={`ingredient-${index}`} style={{textAlign: 'left', padding: 0, fontWeight: 700}}>Ingredient</label>
                                <input type="text" className="form-control"
                                       id={`ingredient-${index}`}
                                       value={ingredient.name}
                                       onChange={(e) => ingredientHandler(index, 'name', e.target.value)} required/>
                            </div>
                        </div>

                        <div className="col-auto" style={{width: '25%'}}>
                            <div className="row" style={{marginRight: '0.5em', marginLeft: '0.5em', padding: 0}}>
                                <label htmlFor={`amount-${index}`} style={{textAlign: 'left', padding: 0, fontWeight: 700}}>Amount</label>
                                <input type="number" className="form-control" min='0'
                                       id={`amount-${index}`}
                                       value={ingredient.amount}
                                       onChange={(e) => ingredientHandler(index, 'amount', e.target.value)}
                                       required/>
                            </div>
                        </div>

                        <div className="col-auto" style={{width: '25%'}}>
                            <div className="row" style={{marginRight: '0.5em', marginLeft: '0.5em', padding: 0}}>
                                <label htmlFor={`unit-${index}`} style={{textAlign: 'left', padding: 0, fontWeight: 700}}>Unit</label>
                                <select className="form-control" id={`unit-${index}`}
                                        value={ingredient.unit}
                                        onChange={(e) => ingredientHandler(index, 'unit', e.target.value)} required>
                                    <option value="g">gram</option>
                                    <option value="ml">milliliter</option>
                                    <option value="kg">kilogram</option>
                                    <option value="L">liter</option>
                                    <option value="L">teaspoon</option>
                                </select>

                            </div>
                        </div>

                        <div className="col-2" style={{display: 'flex', alignItems: 'center'}}>
                            <button className="btn btn-warning" onClick={() => removeIngredient(index)} type="button">
                                <i className="fa-solid fa-trash-can"></i>
                                X
                            </button>
                        </div>

                    </div>

                ))}

                <div className="text-center">
                    <button className="btn btn-light" type="button" onClick={addIngredient} style={{width: '50%'}}>
                        <i className="fa-solid fa-plus"></i>
                        ADD INGREDIENT
                    </button>
                </div>

            </div>

            <hr/>

            <div className="row">

                <p style={{textAlign: 'left', padding: 0, fontWeight: 700}}>Directions</p>

                <p style={{textAlign: 'left', padding: 0, marginTop: '0.8em'}}>Explain how to make your recipe, including
                    oven temperatures, baking or cooking times, and pan sizes, etc.</p>

                {errorMessage.stepEmp && <p className="error-message" style={{color: 'red', fontWeight: 700}}>{errorMessage.stepEmp}</p>}

                <div className="col">

                    {steps.map((step, index) => (
                        <div key={index} className="row">

                            <label htmlFor={`step-${index}`}
                                   style={{textAlign: 'left', padding: 0, marginBottom: '0.7em', marginTop: '0.7em', fontWeight: 500}}>
                                Step {index + 1}:
                            </label>

                            {errorMessage[`step${index}_description`] && <p className="error-message" style={{color: 'red', fontWeight: 700}}>{errorMessage[`step${index}_description`]}</p>}
                            {errorMessage[`step${index}_picture`] && <p className="error-message" style={{color: 'red', fontWeight: 700}}>{errorMessage[`step${index}_picture`]}</p>}
                            {errorMessage[`step${index}_picture_type`] && <p className="error-message" style={{color: 'red', fontWeight: 700}}>{errorMessage[`step${index}_picture_type`]}</p>}

                            <div className={"col"}>
                                <textarea id={`step-${index}`}
                                          value={step.description}
                                          onChange={(e) => stepHandler(index, 'description', e.target.value)}
                                          className="form-control"
                                          placeholder="e.g. Prepare dipping with..."
                                          required>
                                </textarea>
                            </div>

                            <div className={"col-4"} style={{display: 'flex', alignItems: 'center'}}>
                                <input type={"file"} id={`step-image-${index}`}
                                       onChange={(e) => stepHandler(index, 'picture', e.target.files[0])}>
                                </input>
                            </div>

                            <div className={"col-2"} style={{display: 'flex', alignItems: 'center'}}>
                                <button className="btn btn-warning" onClick={() => removeStep(index)} type="button">
                                    X
                                    <i className="fa-solid fa-trash-can"></i>
                                </button>
                            </div>
                        </div>
                    ))}

                    <div className="text-center">
                        <button className="btn btn-light"
                                type="button"
                                style={{width: '50%'}}
                                onClick={addStep}>
                            <i className="fa-solid fa-plus"></i>
                            ADD STEP
                        </button>
                    </div>

                </div>

            </div>

            <hr/>

            <div className="row align-items-center">

                <div className="col d-flex">

                    <div className="col-auto" style={{width: '25%'}}>
                        <div className="row" style={{marginRight: '0.5em', marginLeft: '0.5em', padding: 0}}>
                            <label htmlFor="cooktime" style={{textAlign: 'left', padding: 0, fontWeight: 700}}>Cook Time</label>
                            <input type="number" className="form-control" id="cooktime" min="0" placeholder="time" value={time} onChange={(e) => setTime(e.target.value)} required/>
                        </div>
                    </div>

                    <div className="col-auto" style={{width: '25%'}}>
                        <div className="row" style={{marginRight: '0.5em', marginLeft: '0.5em', padding: 0}}>
                            <label htmlFor="cooktime" style={{textAlign: 'left', padding: 0, fontWeight: 700}}>Time Unit</label>
                            <select className="form-control" name="time_unit" id="time_unit" value={time_unit} onChange={(e) => setTimeUnit(e.target.value)} required>
                                <option value="Mins">Mins</option>
                                <option value="Hours">Hours</option>
                            </select>
                        </div>
                    </div>

                    <div className="col-auto" style={{width: '25%'}}>
                        <div className="row" style={{marginRight: '0.5em', marginLeft: '0.5em', padding: 0}}>
                            <label htmlFor="cuisine" style={{textAlign: 'left', padding: 0, fontWeight: 700}}>Cuisine</label>
                            <select className="form-control" name="cuisine" id="cuisine" value={cuisine} onChange={(e) => setCuisine(e.target.value)} required>
                                <option value="Other">Other</option>
                                <option value="American">American</option>
                                <option value="Chinese">Chinese</option>
                                <option value="Cajun">Cajun</option>
                                <option value="Caribbean">Caribbean</option>
                                <option value="French">French</option>
                                <option value="German">German</option>
                                <option value="Greek">Greek</option>
                                <option value="Hungarian">Hungarian</option>
                                <option value="Indian">Indian</option>
                                <option value="Italian">Italian</option>
                                <option value="Japanese">Japanese</option>
                                <option value="Lebanese">Lebanese</option>
                                <option value="Mediterranean">Mediterranean</option>
                                <option value="Mexican">Mexican</option>
                                <option value="Moroccan">Moroccan</option>
                                <option value="Russian">Russian</option>
                                <option value="Spanish">Spanish</option>
                                <option value="Thai">Thai</option>
                                <option value="Turkish">Turkish</option>
                            </select>
                        </div>
                    </div>

                    <div className="col-auto" style={{width: '25%'}}>
                        <div className="row" style={{marginRight: '0.5em', marginLeft: '0.5em', padding: 0}}>
                            <label htmlFor="diet" style={{textAlign: 'left', padding: 0, fontWeight: 700}}>Diet</label>
                            <select className="form-control" name="diet" id="diet" value={diet} onChange={(e) => setDiet(e.target.value)} required>
                                <option>Other</option>
                                <option>Intermittent Fasting</option>
                                <option>Mediterranean Diet</option>
                                <option>The Ketogenic Diet</option>
                                <option>If It Fits Your Macros</option>
                                <option>Veganism</option>
                                <option>Carnivore Diet</option>
                                <option>Paleo Diet</option>
                                <option>Dessert with Breakfast Diet</option>
                                <option>Sirtfood Diet</option>
                            </select>
                        </div>
                    </div>

                </div>

                {errorMessage.time && <p className="error-message" style={{color: 'red', fontWeight: 700}}>{errorMessage.time}</p>}
                {errorMessage.time_unit && <p className="error-message" style={{color: 'red', fontWeight: 700}}>{errorMessage.time_unit}</p>}
                {errorMessage.cuisine && <p className="error-message" style={{color: 'red', fontWeight: 700}}>{errorMessage.cuisine}</p>}
                {errorMessage.diet && <p className="error-message" style={{color: 'red', fontWeight: 700}}>{errorMessage.diet}</p>}

            </div>
            <div className="text-center">
                <button className="btn btn-success" type="submit" onClick={submitHandler} style={{width: '100%', marginBottom: '10em'}}>SAVE RECIPE <i className="fa-solid fa-paper-plane"></i></button>
            </div>
        </form>
        )
}

export default UpdateRecipe