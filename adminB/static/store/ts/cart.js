import Axios from "./axios";

export default class Cart {
    constructor() {
        this.axiosInstance = new Axios();
        this.setupCartApp()
    }

    
}