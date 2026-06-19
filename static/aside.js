async function mostrar_carrinho(){
    const resposta = await fetch("/carrinho")

    if(resposta.ok){
        const dados = await resposta.json()

        const preco_total = document.querySelector(".cart__total")

        const carrinho = document.querySelector(".cart__items")
        carrinho.innerHTML="";
        let total = 0
        for (let item of dados) {
            let linha =`<div class="cart__item">
                                    <img src=${item.imagem}>
                                    <div class="container_info">
                                        <h1>${item.nome}</h1>
                                        <p>R$ ${item.preco}</p>
                                        <p>${item.quantidade}X</p>
                                        <button> <a href="/carrinho/delete/${item.id_pokemon}" class="remove_button">Remover Item <a></button>
                                    </div>
                                    
                                </div>`
            total = total + (item.preco*item.quantidade)
            carrinho.innerHTML += linha;
        }
        preco_total.textContent = `Total: R$ ${total}.00`
    };
}

mostrar_carrinho()
