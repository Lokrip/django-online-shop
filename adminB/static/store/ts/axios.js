export default class Axios{
    async post(url, datas) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,  // Добавляем CSRF-токен в заголовок
                },
                body: JSON.stringify(datas)
            })
            const data = await response.json();
            return data;
        } catch(error) {
            console.log(error.message)
        }
    }
}