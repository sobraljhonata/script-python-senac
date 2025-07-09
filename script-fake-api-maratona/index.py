import os
import subprocess
import json

# Nome do projeto
project_name = "fake-restaurante-api"

# Cria a pasta do projeto
os.makedirs(project_name, exist_ok=True)
os.chdir(project_name)

# Inicializa o projeto Node.js
subprocess.run(["npm", "init", "-y"])

# Instala as dependências
subprocess.run(["npm", "install", "express", "@faker-js/faker", "swagger-ui-express", "cors"])

# Cria estrutura de diretórios
os.makedirs("routes", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Cria o arquivo index.js
with open("index.js", "w", encoding="utf-8") as f:
    f.write("""const express = require('express');
const cors = require('cors');
const app = express();
const pratosRoutes = require('./routes/pratos');
const swaggerUi = require('swagger-ui-express');
const swaggerDocument = require('./swagger.json');

app.use(cors());
app.use(express.json());

app.use('/pratos', pratosRoutes);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Servidor rodando na porta ${PORT}`));
""")

# Cria o arquivo de dados
with open("data/pratos.js", "w", encoding="utf-8") as f:
    f.write("module.exports = [];")

# Cria o arquivo de rotas
with open("routes/pratos.js", "w", encoding="utf-8") as f:
    f.write("""const express = require('express');
const router = express.Router();
const faker = require('@faker-js/faker').faker;
const pratos = require('../data/pratos');

// URLs de imagens por tipo de cozinha
const imagensPorCozinha = {
  Italiana: 'https://source.unsplash.com/featured/?italian-food',
  Japonesa: 'https://source.unsplash.com/featured/?japanese-food',
  Francesa: 'https://source.unsplash.com/featured/?french-food',
  Brasileira: 'https://source.unsplash.com/featured/?brazilian-food'
};

// Inicializa com 20 pratos
if (pratos.length === 0) {
  const cozinhas = Object.keys(imagensPorCozinha);
  for (let i = 0; i < 20; i++) {
    const cozinha = cozinhas[Math.floor(Math.random() * cozinhas.length)];
    pratos.push({
      id: i + 1,
      nome: faker.commerce.productName(),
      cozinha,
      descricao_resumida: faker.lorem.sentence(8).substring(0, 100),
      descricao_detalhada: faker.lorem.paragraph().substring(0, 200),
      imagem: imagensPorCozinha[cozinha],
      valor: parseFloat(faker.commerce.price({ min: 15, max: 120 }))
    });
  }
}

// Listar todos
router.get('/', (req, res) => {
  const { cozinha, page = 1, limit = 10 } = req.query;
  let results = pratos;
  if (cozinha) {
    results = results.filter(p => p.cozinha === cozinha);
  }
  const start = (page - 1) * limit;
  const end = start + parseInt(limit);
  res.json(results.slice(start, end).map(({ id, nome, cozinha, descricao_resumida, valor }) => ({
    id, nome, cozinha, descricao_resumida, valor
  })));
});

// Detalhe por ID
router.get('/:id', (req, res) => {
  const prato = pratos.find(p => p.id == req.params.id);
  if (!prato) return res.status(404).json({ erro: 'Prato não encontrado' });
  res.json(prato);
});

// Criar prato
router.post('/', (req, res) => {
  const { nome, cozinha, descricao_resumida, descricao_detalhada, valor } = req.body;
  const id = pratos.length ? pratos[pratos.length - 1].id + 1 : 1;
  const imagem = imagensPorCozinha[cozinha] || 'https://source.unsplash.com/featured/?food';
  const novo = { id, nome, cozinha, descricao_resumida, descricao_detalhada, imagem, valor };
  pratos.push(novo);
  res.status(201).json(novo);
});

// Atualizar prato
router.put('/:id', (req, res) => {
  const index = pratos.findIndex(p => p.id == req.params.id);
  if (index === -1) return res.status(404).json({ erro: 'Prato não encontrado' });
  const { nome, cozinha, descricao_resumida, descricao_detalhada, valor } = req.body;
  pratos[index] = { ...pratos[index], nome, cozinha, descricao_resumida, descricao_detalhada, valor };
  res.json(pratos[index]);
});

// Deletar prato
router.delete('/:id', (req, res) => {
  const index = pratos.findIndex(p => p.id == req.params.id);
  if (index === -1) return res.status(404).json({ erro: 'Prato não encontrado' });
  const deletado = pratos.splice(index, 1);
  res.json(deletado[0]);
});

module.exports = router;
""")

# Cria o arquivo swagger.json
swagger_json = {
  "openapi": "3.0.0",
  "info": {
    "title": "Fake Restaurante API",
    "version": "1.0.0",
    "description": "API fake de cardápio de restaurante"
  },
  "paths": {
    "/pratos": {
      "get": {
        "summary": "Listar pratos",
        "parameters": [
          { "name": "cozinha", "in": "query", "schema": { "type": "string" }},
          { "name": "page", "in": "query", "schema": { "type": "integer" }},
          { "name": "limit", "in": "query", "schema": { "type": "integer" }}
        ],
        "responses": {
          "200": {
            "description": "Lista de pratos"
          }
        }
      },
      "post": {
        "summary": "Criar prato",
        "requestBody": {
          "required": True,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "nome": {"type": "string"},
                  "cozinha": {"type": "string"},
                  "descricao_resumida": {"type": "string"},
                  "descricao_detalhada": {"type": "string"},
                  "valor": {"type": "number"}
                },
                "required": ["nome", "cozinha", "descricao_resumida", "descricao_detalhada", "valor"]
              }
            }
          }
        },
        "responses": {
          "201": { "description": "Prato criado" }
        }
      }
    },
    "/pratos/{id}": {
      "get": {
        "summary": "Obter detalhes de um prato",
        "parameters": [
          { "name": "id", "in": "path", "required": True, "schema": { "type": "integer" } }
        ],
        "responses": {
          "200": { "description": "Detalhes do prato" },
          "404": { "description": "Prato não encontrado" }
        }
      },
      "put": {
        "summary": "Atualizar prato",
        "parameters": [
          { "name": "id", "in": "path", "required": True, "schema": { "type": "integer" } }
        ],
        "requestBody": {
          "required": True,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "nome": {"type": "string"},
                  "cozinha": {"type": "string"},
                  "descricao_resumida": {"type": "string"},
                  "descricao_detalhada": {"type": "string"},
                  "valor": {"type": "number"}
                }
              }
            }
          }
        },
        "responses": {
          "200": { "description": "Prato atualizado" },
          "404": { "description": "Prato não encontrado" }
        }
      },
      "delete": {
        "summary": "Deletar prato",
        "parameters": [
          { "name": "id", "in": "path", "required": True, "schema": { "type": "integer" } }
        ],
        "responses": {
          "200": { "description": "Prato deletado" },
          "404": { "description": "Prato não encontrado" }
        }
      }
    }
  }
}

with open("swagger.json", "w", encoding="utf-8") as f:
    json.dump(swagger_json, f, indent=2)
    
# Adiciona o comando "start" no package.json
with open("package.json", "r+", encoding="utf-8") as f:
    package_data = json.load(f)
    if "scripts" not in package_data:
        package_data["scripts"] = {}
    package_data["scripts"]["start"] = "node index.js"
    f.seek(0)
    json.dump(package_data, f, indent=2, ensure_ascii=False)
    f.truncate()