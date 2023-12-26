import React, {useEffect, useState} from "react";
import "./style.css";

const ShoppingList = () => {
    const [authenticated, setAuthenticated] = useState(false)
    const [shopping, setShopping] = useState([])
    const [ingredients, setIngredients] = useState(null)
    useEffect(() => {
        const token = localStorage.getItem('token')
        fetch('http://127.0.0.1:8000/userdata/all-shopping-list/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (response.ok) {
                setAuthenticated(true)
                return response.json().then(data => {
                    setShopping(data)
                    return fetch('http://127.0.0.1:8000/userfunction/shopping-list/', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    })
                    .then(response2 => {
                        if (response2.ok) {
                            return response2.json().then(data2 => {
                                setIngredients(data2)
                            })
                        }
                        else if (response.status === 401) {
                            setAuthenticated(false)
                        }
                        else {
                            console.log('unexpected error')
                        }
                    })
                })
            }
            else if (response.status === 401) {
                setAuthenticated(false)
            }
            else {
                console.log('unexpected error')
            }
        })
    }, [])

    const handleAdd = (shoppinglist) => {
        const token = localStorage.getItem('token')
        fetch(`http://127.0.0.1:8000/userdata/shopping-lst=${shoppinglist.id}/RUD-shopping-lst/?action=add`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            return fetch('http://127.0.0.1:8000/userdata/all-shopping-list/', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
        })
        .then(response => {
            if (response.ok) {
                setAuthenticated(true)
                return response.json().then(data => {
                    setShopping(data)
                    return fetch('http://127.0.0.1:8000/userfunction/shopping-list/', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    })
                    .then(response2 => {
                        if (response2.ok) {
                            return response2.json().then(data2 => {
                                setIngredients(data2)
                            })
                        }
                        else if (response.status === 401) {
                            setAuthenticated(false)
                        }
                        else {
                            console.log('unexpected error')
                        }
                    })
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

    const handleRemove = (shoppinglist) => {
        const token = localStorage.getItem('token')
        if (shoppinglist.number === 1) {
            fetch(`http://127.0.0.1:8000/userdata/shopping-lst=${shoppinglist.id}/RUD-shopping-lst/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                return fetch('http://127.0.0.1:8000/userdata/all-shopping-list/', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
            })
            .then(response => {
                if (response.ok) {
                    setAuthenticated(true)
                    return response.json().then(data => {
                        setShopping(data)
                        return fetch('http://127.0.0.1:8000/userfunction/shopping-list/', {
                            headers: {
                                'Authorization': `Bearer ${token}`
                            }
                        })
                        .then(response2 => {
                            if (response2.ok) {
                                return response2.json().then(data2 => {
                                    setIngredients(data2)
                                })
                            }
                            else if (response.status === 401) {
                                setAuthenticated(false)
                            }
                            else {
                                console.log('unexpected error')
                            }
                        })
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

        else {
            fetch(`http://127.0.0.1:8000/userdata/shopping-lst=${shoppinglist.id}/RUD-shopping-lst/?action=remove`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                return fetch('http://127.0.0.1:8000/userdata/all-shopping-list/', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
            })
            .then(response => {
                if (response.ok) {
                    setAuthenticated(true)
                    return response.json().then(data => {
                        setShopping(data)
                        return fetch('http://127.0.0.1:8000/userfunction/shopping-list/', {
                            headers: {
                                'Authorization': `Bearer ${token}`
                            }
                        })
                        .then(response2 => {
                            if (response2.ok) {
                                return response2.json().then(data2 => {
                                    setIngredients(data2)
                                })
                            }
                            else if (response.status === 401) {
                                setAuthenticated(false)
                            }
                            else {
                                console.log('unexpected error')
                            }
                        })
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
    }

    return (
        <>
        {authenticated ? (
        <div className="main-container">
            <div className="block">
                <h2>Recipe List</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Recipe Name</th>
                            <th>Servings</th>
                            <th></th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {shopping.map(shoppinglist => (
                            <tr key={shoppinglist.id}>
                                <td>{shoppinglist.recipe.title}</td>
                                <td>{shoppinglist.number}</td>
                                <td><button onClick={() => handleAdd(shoppinglist)}>+</button></td>
                                <td><button onClick={() => handleRemove(shoppinglist)}>-</button></td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <div className="block">
                <h2>Shopping List</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Ingredient</th>
                            <th>Amount</th>
                            <th>Unit</th>
                        </tr>
                    </thead>
                    <tbody>
                        {ingredients && Object.keys(ingredients).map(ingredient => (
                            <tr key={ingredient}>
                                <td>{ingredient}</td>
                                <td>{ingredients[ingredient].amount}</td>
                                <td>{ingredients[ingredient].unit}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
        
        ) : (
            <h1>You Are Not Logged in. Please Log to View This Page.</h1>
        )}
        </>
    )
}

export default ShoppingList