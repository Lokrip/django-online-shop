import Axios from "./axios.js"

export default class Store {
    constructor() {
        this.axiosInstance = new Axios();
        this.setupEventListeners();
    }

    setupEventListeners() {
        const cardButton = document.querySelector('[data-cart-button]')
        if(cardButton) {
            cardButton.addEventListener('click', this.handleAddToCart.bind(this))
        }
    }

    view_cart_total_price(data) {
        document.querySelector('[data-total-price-cart]').textContent = data.total_price
    }

    view_cart_orderItems(data) {
        const cartContainer = document.querySelector('[data-list-cart-model="true"]')
        const { orderitem_set } = data;

        cartContainer.innerHTML = orderitem_set.map(item => `
            <li class="header-cart-item flex-w flex-t m-b-12">
                <div class="header-cart-item-img">
                    <img src="${item.product.image}" alt="IMG">
                </div>
                <div class="header-cart-item-txt p-t-8">
                    <a href="" class="header-cart-item-name m-b-18 hov-cl1 trans-04">
                        ${item.product.title}
                    </a>
                    <span class="header-cart-item-info">
                        ${item.quantity} x $${item.total_price}
                    </span>
                </div>
            </li>`
        )
    }

    async handleAddToCart(e) {
        e.preventDefault();

        const productId = this.getProductId()
        const productCount = this.getProductCount()

        if (!productId || !productCount) {
            console.warn("Product ID or Count is missing");
            return;
        }

        try {
            const data = await this.axiosInstance.post('/lk/api/v1/cart-add/', {
                method: 'add',
                productId: productId,
                productCount: productCount
            })
            this.view_cart_orderItems(data)
            this.view_cart_total_price(data)
            
        } catch(error) {
            console.error("Failed to add product to cart:", error);
        }

    }

    getProductId() {
        const productIdSelector = document.querySelector('[data-product-id]')
        return productIdSelector.getAttribute('data-product-id') || null
    }

    getProductCount() {
        const productCountSelector = document.querySelector('[data-count-product]')
        return productCountSelector.value
    }
}