CREATE DATABASE PokeVault;
USE PokeVault;

CREATE TABLE Ataques (
    id_ataque INT NOT NULL auto_increment,
    nome VARCHAR(50),
    tipo VARCHAR(20),

    PRIMARY KEY (id_ataque)
);

CREATE TABLE Pokemons (
    id_pokemon INT NOT NULL,
    nome VARCHAR(80),
    descricao VARCHAR(300),
    imagem VARCHAR(150),
    preco DOUBLE,
    destaque BOOLEAN,

    PRIMARY KEY (id_pokemon)
);

CREATE TABLE tipos (
    id_tipo INT NOT NULL auto_increment,
    tipo VARCHAR(20),

    PRIMARY KEY (id_tipo)
);

CREATE TABLE usuarios (
    id_usuario INT NOT NULL auto_increment,
    email VARCHAR(100),
    nome VARCHAR(80),
    telefone VARCHAR(20),
    endereco VARCHAR(100),
    senha VARCHAR(50),

    PRIMARY KEY (id_usuario)
);

CREATE TABLE ataques_pokemons (
    id_pokemon INT NOT NULL,
    id_ataque INT NOT NULL,

    PRIMARY KEY (id_pokemon, id_ataque),

    FOREIGN KEY (id_pokemon)
        REFERENCES Pokemons(id_pokemon),

    FOREIGN KEY (id_ataque)
        REFERENCES Ataques(id_ataque)
);

CREATE TABLE carrinhos (
    id_carrinho INT NOT NULL,
    id_usuario INT NOT NULL,
    data DATE,
    finalizado BOOLEAN,

    PRIMARY KEY (id_carrinho),

    FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario)
);

CREATE TABLE Pokemons_tipos (
    id_tipo INT NOT NULL,
    id_pokemon INT NOT NULL,

    PRIMARY KEY (id_tipo, id_pokemon),

    FOREIGN KEY (id_tipo)
        REFERENCES tipos(id_tipo),

    FOREIGN KEY (id_pokemon)
        REFERENCES Pokemons(id_pokemon)
);

CREATE TABLE produtos_carrinho (
    id INT NOT NULL,
    id_pokemon INT NOT NULL,
    quantidade INT,
    id_carrinho INT NOT NULL,

    PRIMARY KEY (id),

    FOREIGN KEY (id_pokemon)
        REFERENCES Pokemons(id_pokemon),

    FOREIGN KEY (id_carrinho)
        REFERENCES carrinhos(id_carrinho)
);

CREATE TABLE comentario_unitario (
    cod_comentario INT PRIMARY KEY AUTO_INCREMENT,
    id_pokemon INT NOT NULL,
    nome_usuario VARCHAR(100) DEFAULT 'ANÔNIMO',
    comentario TEXT,
    nota INT DEFAULT 0,
    CONSTRAINT chk_nota_unitario CHECK (nota >= 0 AND nota <= 5),
    FOREIGN KEY (id_pokemon) REFERENCES Pokemons(id_pokemon)
);

ALTER TABLE comentario_unitario ADD COLUMN id_usuario INT NOT NULL;
ALTER TABLE comentario_unitario ADD FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario);