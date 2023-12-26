import {React, useEffect, useState} from 'react';
import RecipeCard from '../RecipeCard';
import './style.css';

const Home = () => {
    const count = 2;
    const [query, setQuery] = useState({
        recipes: [], page: 1
    });
    const [searchQuery, setSearchQuery] = useState({
        recipes: [], page: 1
    });
    const [search, setSearch] = useState(false);
    const [searchMode, setSearchMode] = useState('name');
    const [searchInput, setSearchInput] = useState('');
    const [cuisine, setCuisine] = useState('');
    const [diet, setDiet] = useState('');
    const [time, setTime] = useState('');
    const [unit, setUnit] = useState('');
    const [hasEnded, setHasEnded] = useState(true);
    const [firstPage, setFirstPage] = useState(true);
    const [searchUrl, setSearchUrl] = useState('http://127.0.0.1:8000/userfunction/search/');
    
    useEffect(() => {
        fetch(`http://127.0.0.1:8000/userfunction/popular-recipes/?count=${count}&page=${query.page}`)
        .then(response => response.json())
        .then(data => {
            setQuery({...query, recipes: data.results});
            setFirstPage(data.previous === null);
            setHasEnded(data.next === null);
        })
    }, [query.page]);

    const handleSearch = (e) => {
        e.preventDefault();
        setSearch(true);
        let url = 'http://127.0.0.1:8000/userfunction/search/';
        if (searchMode === 'name') {
            url += `name/?name=${searchInput}`;
        }
        if (searchMode === 'creator') {
            url += `creator/?creator=${searchInput}`;
        }
        if (searchMode === 'ingredient') {
            url += `ingredient/?ingredient=${searchInput}`
        }
        if (cuisine !== '') {
            url += `&cuisine=${cuisine}`
        }
        if (diet !== '') {
            url += `&diet=${diet}`
        }
        if (time !== '' && unit !== '') {
            url += `&time=${time}&unit=${unit}`
        }
        setSearchUrl(url)
        url += `&count=${count}&page=1`
        fetch(url)
        .then(response => response.json())
        .then(data => {
            setTimeout(() => {
                setSearchQuery({recipes: data.results, page: 1});
                setFirstPage(data.previous === null);
                setHasEnded(data.next === null);
            }, 0);
        })
    }

    const searchPrevPage = () => {
        console.log('before: ', searchQuery.page)
        let url = searchUrl 
        url += `&count=${count}&page=${searchQuery.page - 1}`
        fetch(url)
        .then(response => response.json())
        .then(data => {
            setTimeout(() => {
                setSearchQuery({recipes: data.results, page: searchQuery.page -1});
                setFirstPage(data.previous === null);
                setHasEnded(data.next === null);
            }, 0);
        })
        console.log('after: ', searchQuery.page)
    }

    const searchNextPage = () => {
        console.log('before: ', searchQuery.page)
        
        let url = searchUrl 
        url += `&count=${count}&page=${searchQuery.page + 1}`
        fetch(url)
        .then(response => response.json())
        .then(data => {
            setTimeout(() => {
                setSearchQuery({recipes: data.results, page: searchQuery.page + 1});
                setFirstPage(data.previous === null);
                setHasEnded(data.next === null);
            }, 0);
        })
        console.log('after: ', searchQuery.page)
    }

    return (
        <div className="main-container">
            <div className="search">
                <div className="col d-flex">
                    <div className="col-auto" style={{ width: '25%' }}>
                        <div className="row" style={{ marginRight: '0.5em', marginLeft: '0.5em', padding: '0' }}>
                            <label htmlFor="searchmode" style={{ textAlign: 'left', padding: '0', fontWeight: '700' }}>Search By</label>
                            <select className="form-control" id="searchmode" onChange={e => setSearchMode(e.target.value)}>
                                <option value="name">name</option>
                                <option value="creator">creator</option>
                                <option value="ingredient">ingredient</option>
                            </select>
                        </div>
                    </div>
                    <div className="col-auto" style={{ width: '75%' }}>
                        <div className="d-flex" style={{ marginTop: '24px' }}>
                        <div className="row" style={{ marginRight: '0.5em', marginLeft: '0.5em', padding: '0', width: '75%' }}>
                            <input id="search" className="form-control me-2" type="search" placeholder="Enter your search" aria-label="Search" onChange={e => setSearchInput(e.target.value)}/>
                        </div>
                        <button className="btn btn-outline-success" style={{marginRight: '0.5em', marginLeft: '0.5em', padding: '0', width: '25%'}} onClick={handleSearch}>Search</button>
                        </div>
                    </div>
                </div>
                <div className="col d-flex">
                    <div className="col-auto" style={{ width: '25%' }}>
                        <div className="row" style={{ marginRight: '0.5em', marginLeft: '0.5em', padding: '0' }}>
                            <label htmlFor="cooktime" style={{textAlign: 'left', padding: '0', fontWeight: '700'}}>Cook Time</label>
                            <input type="number" className="form-control" id="cooktime" min="0" placeholder="mins" onChange={e => setTime(e.target.value)}/>
                        </div>
                    </div>
                    <div className="col-auto" style={{ width: '25%' }}>
                        <div className="row" style={{ marginRight: '0.5em', marginLeft: '0.5em', padding: '0' }}>
                            <label htmlFor="unit" style={{textAlign: 'left', padding: '0', fontWeight: '700'}}>Time Unit</label>
                            <select className="form-control" id="unit" onChange={e => setUnit(e.target.value)}>
                                <option value="minute">minute</option>
                                <option value="hour">hour</option>
                            </select>
                        </div>
                    </div>
                    <div className="col-auto" style={{ width: '25%' }}>
                        <div className="row" style={{ marginRight: '0.5em', marginLeft: '0.5em', padding: '0' }}>
                            <label htmlFor="cuisine" style={{ textAlign: 'left', padding: '0', fontWeight: '700' }}>Cuisine</label>
                            <select className="form-control" id="cuisine" onChange={e => setCuisine(e.target.value)}>
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
                    <div className="col-auto" style={{ width: '25%' }}>
                        <div className="row" style={{ marginRight: '0.5em', marginLeft: '0.5em', padding: '0' }}>
                            <label htmlFor="diet" style={{ textAlign: 'left', padding: '0', fontWeight: '700' }}>Diet</label>
                            <select className="form-control" id="diet" onChange={e => setDiet(e.target.value)}>
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
            </div>
            <div className='recipes-container'>
                {search ? (searchQuery.recipes?.map(recipe => (
                    <RecipeCard key={recipe.id} className='recipe' recipe={recipe}/>
                ))) : (query.recipes?.map(recipe => (
                    <RecipeCard key={recipe.id} className='recipe' recipe={recipe}/>
                )))}
            </div>
            <div className='pagetraverse d-flex'>
                <button className='button' disabled={firstPage} style={{ marginLeft: '2em', marginRight: '2em' }} onClick={() => {search ? searchPrevPage() : setQuery({...query, page: query.page - 1})}}>prev</button>
                <button className='button' disabled={hasEnded} style={{ marginLeft: '2em', marginRight: '2em' }} onClick={() => {search ? searchNextPage() : setQuery({...query, page: query.page + 1})}}>next</button>
            </div>
        </div>
    )
}

export default Home;