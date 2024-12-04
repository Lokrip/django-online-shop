import Cart from "./cart.js";
import Store from "./shop.js";

const __init__ = () => {
    const body = document.body;
    if(body) {
        try {
            new Store();
            new Cart();
        } catch (error) {
            console.error(error)
            throw new Error(error)
        }
    } 
}


window.addEventListener('DOMContentLoaded', __init__)