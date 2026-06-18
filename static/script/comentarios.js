let valorEstrela

document.querySelectorAll('[name="star"]').forEach((input) => {
    input.addEventListener('input', () => {
        if (input.value > 0) valorEstrela = input.value
    })
})

const gerarEstrelas = (nota) => {
    let estrelas = ''
    for (let i = 1; i <= 5; i++) {
        estrelas += i <= nota ? '★' : '☆'
    }
    return estrelas
}

// Pega o id do pokemon da URL: /unitario/42
const idPokemon = window.location.pathname.split('/').pop()

const carregarComents = async () => {
    try {
        const resposta = await fetch(`/unitario/${idPokemon}/comentarios/get`)
        if (!resposta.ok) { alert('Erro na requisição'); return }

        const comentarios = await resposta.json()
        const container = document.querySelector('.reviews-container .lista-comentarios')

        if (comentarios.length === 0) {
            container.innerHTML = '<h2>Nenhum comentário ainda</h2>'
        } else {
            container.innerHTML = ''
            comentarios.forEach((c) => {
                const botaoExcluir = c.id_usuario === usuarioLogadoId
                    ? `<button class="btn-delete" data-id="${c.cod_comentario}">excluir</button>`
                    : ''

                container.innerHTML += `
<div class="review">
    <img src="https://images.icon-icons.com/851/PNG/512/Pokemon_Trainer_Boy_icon-icons.com_67516.png" class="avatar">
    <div class="review-content">
        <div class="top">
            <strong>${c.nome_usuario}</strong>
        </div>
        <div class="stars">${gerarEstrelas(c.nota)}</div>
        <p>${c.comentario}</p>
        ${botaoExcluir}
    </div>
</div>`
            })
        }

        document.querySelectorAll('.btn-delete').forEach((btn) => {
            btn.addEventListener('click', async () => {
                try {
                    const r = await fetch(`/unitario/${idPokemon}/comentarios/delete`, {
                        method: 'DELETE',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ codigo: btn.dataset.id })
                    })
                    if (!r.ok) alert('Erro ao deletar')
                    carregarComents()
                } catch (e) { console.error(e) }
            })
        })

    } catch (e) { console.error(e) }
}

window.onload = carregarComents

document.querySelector('.button_enviar').addEventListener('click', async () => {
    const comentario = document.querySelector('.avaliacao-form textarea').value
    const nota = valorEstrela

    if (!comentario || !nota) {
        alert('Preencha o comentário e selecione uma nota!')
        return
    }

    const resposta = await fetch(`/unitario/${idPokemon}/comentarios/post`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comentario, nota })
    })

    if (resposta.status === 401) {
        alert('Você precisa estar logado para comentar!')
        return
    }

    if (!resposta.ok) {
        alert('Erro ao enviar comentário')
        return
    }

    document.querySelector('.avaliacao-form textarea').value = ''
    valorEstrela = null
    carregarComents()
})