import './App.css';
import NavBar from './components/NavBar';
import Login from './components/Login';
import Signup from './components/Signup';
import EditProfile from './components/Profile/EditProfile';
import Home from './components/Home';
import CreateRecipe from './components/CreateRecipe'
import UpdateRecipe from "./components/UpdateRecipe";
import RecipeDetail from "./components/RecipeDetail";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import ShoppingList from './components/ShoppingList';
import MyRecipes from './components/MyRecipes';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<NavBar/>}>
          <Route path="accounts/">
            <Route path="signup" element={<Signup/>}/>
            <Route path="login" element={<Login/>}/>
            <Route path="profile/edit" element={<EditProfile/>}/>
          </Route>
          <Route path="recipes/">
            <Route path="create-recipe" element={<CreateRecipe/>}/>
            <Route path=":recipeID/details" element={<RecipeDetail/>}/>
            <Route path=":recipeID/edit" element={<UpdateRecipe/>}/>
          </Route>
          <Route index element={<Home/>}/>
          <Route path="my-recipe" element={<MyRecipes/>}/>
          <Route path="shopping-list" element={<ShoppingList/>}/>
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App;
