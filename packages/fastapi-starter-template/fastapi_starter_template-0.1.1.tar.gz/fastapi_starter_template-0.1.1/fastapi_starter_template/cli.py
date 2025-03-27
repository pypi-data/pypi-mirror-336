import os
import sys
import click
from pathlib import Path

# Funções que criam diferentes estruturas de projeto


def create_aws_structure(base):
    # Função definida acima
    # (Insira o código da função create_aws_structure conforme mostrado)
    # Por conveniência, reutilize o código mostrado anteriormente.
    os.makedirs(os.path.join(base, "aws", "cfn"), exist_ok=True)
    os.makedirs(os.path.join(base, "aws", "sam"), exist_ok=True)
    os.makedirs(os.path.join(base, "src", "app"), exist_ok=True)
    os.makedirs(os.path.join(base, "tests"), exist_ok=True)

    with open(os.path.join(base, "aws", "cfn", "template.yaml"), "w") as f:
        f.write(
            "AWSTemplateFormatVersion: '2010-09-09'\n"
            "Description: Exemplo de template CloudFormation para FastAPI\n"
            "Resources:\n"
            "  FastAPILambda:\n"
            "    Type: AWS::Lambda::Function\n"
            "    Properties:\n"
            "      Handler: app.handler\n"
            "      Role: arn:aws:iam::123456789012:role/lambda-role\n"
            "      Code:\n"
            "        S3Bucket: your-code-bucket\n"
            "        S3Key: fastapi-app.zip\n"
            "      Runtime: python3.9\n"
        )

    with open(os.path.join(base, "aws", "sam", "template.yaml"), "w") as f:
        f.write(
            "AWSTemplateFormatVersion: '2010-09-09'\n"
            "Transform: AWS::Serverless-2016-10-31\n"
            "Description: Exemplo SAM para FastAPI\n"
            "Resources:\n"
            "  FastAPIApp:\n"
            "    Type: AWS::Serverless::Function\n"
            "    Properties:\n"
            "      Handler: app.handler\n"
            "      Runtime: python3.9\n"
            "      CodeUri: src/app/\n"
            "      Events:\n"
            "        ApiEvent:\n"
            "          Type: Api\n"
            "          Properties:\n"
            "            Path: /{proxy+}\n"
            "            Method: any\n"
        )

    with open(os.path.join(base, "src", "app", "main.py"), "w") as f:
        f.write(
            "from fastapi import FastAPI\n"
            "from app.aws_integration import list_s3_buckets\n\n"
            "app = FastAPI()\n\n"
            "@app.get('/')\n"
            "def read_root():\n"
            "    return {'message': 'Hello from AWS template'}\n\n"
            "@app.get('/buckets')\n"
            "def get_buckets():\n"
            "    buckets = list_s3_buckets()\n"
            "    return {'buckets': buckets}\n"
        )

    with open(os.path.join(base, "src", "app", "aws_integration.py"), "w") as f:
        f.write(
            "import boto3\n\n"
            "def list_s3_buckets():\n"
            "    s3 = boto3.client('s3')\n"
            "    response = s3.list_buckets()\n"
            "    buckets = [bucket['Name'] for bucket in response.get('Buckets', [])]\n"
            "    return buckets\n"
        )

    with open(os.path.join(base, "tests", "__init__.py"), "w") as f:
        f.write("# Testes para o template AWS\n")
    with open(os.path.join(base, "requirements.txt"), "w") as f:
        f.write("fastapi\nuvicorn\nboto3\nclick\n")
    with open(os.path.join(base, "Dockerfile"), "w") as f:
        f.write(
            "FROM python:3.9-slim\n"
            "WORKDIR /app\n"
            "COPY requirements.txt ./\n"
            "RUN pip install --no-cache-dir -r requirements.txt\n"
            "COPY src ./src\n"
            "EXPOSE 8000\n"
            "CMD [\"uvicorn\", \"src.app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n"
        )
    with open(os.path.join(base, "README.md"), "w") as f:
        f.write(
            f"# {os.path.basename(base)}\n\n"
            "Projeto FastAPI com integração AWS.\n\n"
            "## Como rodar\n"
            "1. Instale as dependências:\n"
            "   ```bash\n"
            "   pip install -r requirements.txt\n"
            "   ```\n"
            "2. Rode a aplicação:\n"
            "   ```bash\n"
            "   uvicorn src.app.main:app --reload\n"
            "   ```\n"
        )

# CLI com Click

def create_default_structure(base):
    """
    Template Default:
    Estrutura:
      default/
      ├── k8s/
      ├── src/
      │   ├── app/
      │   │   └── motor/
      │   │       └── __init__.py
      │   └── server.py
      ├── tests/
      │   └── __init__.py
      ├── requirements.txt
      ├── azure-pipelines.yaml
      ├── .dockerignore
      ├── .env
      ├── .gitignore
      ├── .gitmodules
      ├── compose.yaml
      ├── Dockerfile
      ├── jenkinsfile
      └── README.md
    """
    os.makedirs(os.path.join(base, "k8s"), exist_ok=True)
    os.makedirs(os.path.join(base, "src", "app", "motor"), exist_ok=True)
    os.makedirs(os.path.join(base, "tests"), exist_ok=True)

    with open(os.path.join(base, "src", "app", "motor", "__init__.py"), "w") as f:
        f.write("# Módulo motor do template Default\n")

    with open(os.path.join(base, "src", "server.py"), "w") as f:
        f.write(
            "from fastapi import FastAPI\n"
            "app = FastAPI()\n\n"
            "@app.get('/')\n"
            "def read_root():\n"
            "    return {'message': 'Hello from Default template'}\n"
        )

    with open(os.path.join(base, "tests", "__init__.py"), "w") as f:
        f.write("# Pacote de testes do Default template\n")

    with open(os.path.join(base, "requirements.txt"), "w") as f:
        f.write("fastapi\nuvicorn\n")
    with open(os.path.join(base, "azure-pipelines.yaml"), "w") as f:
        f.write("trigger:\n  - main\n")
    with open(os.path.join(base, ".dockerignore"), "w") as f:
        f.write("__pycache__/\n*.pyc\n")
    with open(os.path.join(base, ".env"), "w") as f:
        f.write("DEBUG=True\nPORT=8000\n")
    with open(os.path.join(base, ".gitignore"), "w") as f:
        f.write("venv/\n__pycache__/\n")
    with open(os.path.join(base, ".gitmodules"), "w") as f:
        f.write("# Configuração de submódulos\n")
    with open(os.path.join(base, "compose.yaml"), "w") as f:
        f.write("version: '3.8'\nservices:\n  web:\n    image: default_image\n")
    with open(os.path.join(base, "Dockerfile"), "w") as f:
        f.write(
            "FROM python:3.9-slim\n"
            "WORKDIR /app\n"
            "COPY requirements.txt ./\n"
            "RUN pip install --no-cache-dir -r requirements.txt\n"
            "COPY src ./src\n"
            "EXPOSE 8000\n"
            "CMD [\"uvicorn\", \"src.server:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n"
        )
    with open(os.path.join(base, "jenkinsfile"), "w") as f:
        f.write("pipeline { agent any; stages { stage('Build') { steps { echo 'Building Default template' } } } }\n")
    with open(os.path.join(base, "README.md"), "w") as f:
        f.write(f"# {os.path.basename(base)}\nProjeto Default template.\n")


def create_minimal_structure(base):
    """
    Template Minimal:
    Estrutura:
      minimal/
      ├── src/
      │   └── server.py
      ├── tests/
      │   └── __init__.py
      ├── requirements.txt
      └── README.md
    """
    os.makedirs(os.path.join(base, "src"), exist_ok=True)
    os.makedirs(os.path.join(base, "tests"), exist_ok=True)

    with open(os.path.join(base, "src", "server.py"), "w") as f:
        f.write(
            "from fastapi import FastAPI\n"
            "app = FastAPI()\n\n"
            "@app.get('/')\n"
            "def read_root():\n"
            "    return {'message': 'Hello from Minimal template'}\n"
            "\n"
            "@app.post('/items')\n"
            "def create_item(item: dict):\n"
            "    return {'item': item}\n"
        )
    with open(os.path.join(base, "tests", "__init__.py"), "w") as f:
        f.write("# Testes do Minimal template\n")
    with open(os.path.join(base, "requirements.txt"), "w") as f:
        f.write("fastapi\nuvicorn\n")
    with open(os.path.join(base, "README.md"), "w") as f:
        f.write(f"# {os.path.basename(base)}\nMinimal template project.\n")


def create_advanced_structure(base):
    """
    Template Advanced:
    Estrutura:
      advanced/
      ├── src/
      │   ├── app/
      │   │   ├── api/
      │   │   │   └── endpoints/
      │   │   │       └── example.py
      │   │   ├── core/
      │   │   │   └── config.py
      │   │   ├── models/
      │   │   └── schemas/
      │   └── server.py
      ├── tests/
      │   └── __init__.py
      ├── requirements.txt
      ├── Dockerfile
      └── README.md
    """
    os.makedirs(os.path.join(base, "src", "app", "api", "endpoints"), exist_ok=True)
    os.makedirs(os.path.join(base, "src", "app", "core"), exist_ok=True)
    os.makedirs(os.path.join(base, "src", "app", "models"), exist_ok=True)
    os.makedirs(os.path.join(base, "src", "app", "schemas"), exist_ok=True)
    os.makedirs(os.path.join(base, "tests"), exist_ok=True)

    with open(os.path.join(base, "src", "app", "api", "endpoints", "example.py"), "w") as f:
        f.write(
            "from fastapi import APIRouter\n"
            "router = APIRouter()\n\n"
            "@router.get('/example')\n"
            "def example():\n"
            "    return {'message': 'Hello from Advanced template endpoint'}\n"
        )
    with open(os.path.join(base, "src", "app", "core", "config.py"), "w") as f:
        f.write("APP_NAME = 'Advanced Project'\n")
    with open(os.path.join(base, "src", "server.py"), "w") as f:
        f.write(
            "from fastapi import FastAPI\n"
            "from app.api.endpoints.example import router as example_router\n"
            "app = FastAPI()\n\n"
            "app.include_router(example_router, prefix='/api/v1')\n"
            "\n"
            "@app.get('/')\n"
            "def read_root():\n"
            "    return {'message': 'Hello from Advanced template'}\n"
        )
    with open(os.path.join(base, "tests", "__init__.py"), "w") as f:
        f.write("# Advanced template tests\n")
    with open(os.path.join(base, "requirements.txt"), "w") as f:
        f.write("fastapi\nuvicorn\npydantic\n")
    with open(os.path.join(base, "Dockerfile"), "w") as f:
        f.write(
            "FROM python:3.9-slim\n"
            "WORKDIR /app\n"
            "COPY requirements.txt ./\n"
            "RUN pip install --no-cache-dir -r requirements.txt\n"
            "COPY src ./src\n"
            "EXPOSE 8000\n"
            "CMD [\"uvicorn\", \"src.server:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n"
        )
    with open(os.path.join(base, "README.md"), "w") as f:
        f.write(f"# {os.path.basename(base)}\nAdvanced template project.\n")


def create_enterprise_structure(base):
    """
    Template Enterprise:
    Estrutura:
      enterprise/
      ├── k8s/
      ├── docs/
      ├── src/
      │   ├── app/
      │   │   ├── api/
      │   │   ├── services/
      │   │   ├── repositories/
      │   │   └── config/
      │   │       └── settings.py
      │   └── server.py
      ├── tests/
      │   └── __init__.py
      ├── requirements.txt
      ├── Dockerfile
      └── README.md
    """
    os.makedirs(os.path.join(base, "k8s"), exist_ok=True)
    os.makedirs(os.path.join(base, "docs"), exist_ok=True)
    os.makedirs(os.path.join(base, "src", "app", "api"), exist_ok=True)
    os.makedirs(os.path.join(base, "src", "app", "services"), exist_ok=True)
    os.makedirs(os.path.join(base, "src", "app", "repositories"), exist_ok=True)
    os.makedirs(os.path.join(base, "src", "app", "config"), exist_ok=True)
    os.makedirs(os.path.join(base, "tests"), exist_ok=True)

    with open(os.path.join(base, "src", "app", "config", "settings.py"), "w") as f:
        f.write("DATABASE_URL = 'postgresql://user:pass@localhost/db'\n")
    with open(os.path.join(base, "src", "server.py"), "w") as f:
        f.write(
            "from fastapi import FastAPI\n"
            "app = FastAPI()\n\n"
            "@app.get('/')\n"
            "def read_root():\n"
            "    return {'message': 'Hello from Enterprise template'}\n"
        )
    with open(os.path.join(base, "tests", "__init__.py"), "w") as f:
        f.write("# Enterprise template tests\n")
    with open(os.path.join(base, "requirements.txt"), "w") as f:
        f.write("fastapi\nuvicorn\nsqlalchemy\npydantic\n")
    with open(os.path.join(base, "Dockerfile"), "w") as f:
        f.write(
            "FROM python:3.9-slim\n"
            "WORKDIR /app\n"
            "COPY requirements.txt ./\n"
            "RUN pip install --no-cache-dir -r requirements.txt\n"
            "COPY src ./src\n"
            "EXPOSE 8000\n"
            "CMD [\"uvicorn\", \"src.server:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n"
        )
    with open(os.path.join(base, "README.md"), "w") as f:
        f.write(f"# {os.path.basename(base)}\nEnterprise template project.\n")


def create_microservice_structure(base):
    """
    Template Microservice:
    Estrutura:
      microservice/
      ├── src/
      │   └── server.py
      ├── config/
      │   └── config.yaml
      ├── tests/
      │   └── __init__.py
      ├── requirements.txt
      ├── Dockerfile
      └── README.md
    """
    os.makedirs(os.path.join(base, "src"), exist_ok=True)
    os.makedirs(os.path.join(base, "config"), exist_ok=True)
    os.makedirs(os.path.join(base, "tests"), exist_ok=True)

    with open(os.path.join(base, "src", "server.py"), "w") as f:
        f.write(
            "from fastapi import FastAPI\n"
            "app = FastAPI()\n\n"
            "@app.get('/')\n"
            "def read_root():\n"
            "    return {'message': 'Hello from Microservice template'}\n"
        )
    with open(os.path.join(base, "config", "config.yaml"), "w") as f:
        f.write("service: microservice\nversion: 1.0\n")
    with open(os.path.join(base, "tests", "__init__.py"), "w") as f:
        f.write("# Microservice template tests\n")
    with open(os.path.join(base, "requirements.txt"), "w") as f:
        f.write("fastapi\nuvicorn\n")
    with open(os.path.join(base, "Dockerfile"), "w") as f:
        f.write(
            "FROM python:3.9-slim\n"
            "WORKDIR /app\n"
            "COPY requirements.txt ./\n"
            "RUN pip install --no-cache-dir -r requirements.txt\n"
            "COPY src ./src\n"
            "EXPOSE 8000\n"
            "CMD [\"uvicorn\", \"src.server:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n"
        )
    with open(os.path.join(base, "README.md"), "w") as f:
        f.write(f"# {os.path.basename(base)}\nMicroservice template project.\n")


def create_scalable_structure(base):
    """
    Template Scalable:
    Estrutura:
      scalable/
      ├── loadbalancer/
      │   └── lb_config.yaml
      ├── src/
      │   ├── app/
      │   │   ├── main.py
      │   │   └── modules/
      │   │       ├── users.py
      │   │       └── orders.py
      ├── workers/
      │   └── worker.py
      ├── tests/
      │   └── __init__.py
      ├── requirements.txt
      ├── Dockerfile
      └── README.md
    """
    os.makedirs(os.path.join(base, "loadbalancer"), exist_ok=True)
    os.makedirs(os.path.join(base, "src", "app", "modules"), exist_ok=True)
    os.makedirs(os.path.join(base, "workers"), exist_ok=True)
    os.makedirs(os.path.join(base, "tests"), exist_ok=True)

    # loadbalancer/lb_config.yaml
    with open(os.path.join(base, "loadbalancer", "lb_config.yaml"), "w") as f:
        f.write("strategy: round-robin\n")
    # src/app/main.py com rotas integradas
    os.makedirs(os.path.join(base, "src", "app"), exist_ok=True)
    with open(os.path.join(base, "src", "app", "main.py"), "w") as f:
        f.write(
            "from fastapi import FastAPI\n"
            "from app.modules import users, orders\n\n"
            "app = FastAPI()\n\n"
            "app.include_router(users.router, prefix='/users')\n"
            "app.include_router(orders.router, prefix='/orders')\n"
            "\n"
            "@app.get('/')\n"
            "def root():\n"
            "    return {'message': 'Hello from Scalable template'}\n"
        )
    # src/app/modules/users.py
    with open(os.path.join(base, "src", "app", "modules", "users.py"), "w") as f:
        f.write(
            "from fastapi import APIRouter\n"
            "router = APIRouter()\n\n"
            "@router.get('/')\n"
            "def get_users():\n"
            "    return {'users': []}\n"
        )
    # src/app/modules/orders.py
    with open(os.path.join(base, "src", "app", "modules", "orders.py"), "w") as f:
        f.write(
            "from fastapi import APIRouter\n"
            "router = APIRouter()\n\n"
            "@router.get('/')\n"
            "def get_orders():\n"
            "    return {'orders': []}\n"
        )
    # workers/worker.py
    with open(os.path.join(base, "workers", "worker.py"), "w") as f:
        f.write(
            "def run_worker():\n"
            "    print('Worker is running')\n"
        )
    with open(os.path.join(base, "tests", "__init__.py"), "w") as f:
        f.write("# Scalable template tests\n")
    with open(os.path.join(base, "requirements.txt"), "w") as f:
        f.write("fastapi\nuvicorn\n")
    with open(os.path.join(base, "Dockerfile"), "w") as f:
        f.write(
            "FROM python:3.9-slim\n"
            "WORKDIR /app\n"
            "COPY requirements.txt ./\n"
            "RUN pip install --no-cache-dir -r requirements.txt\n"
            "COPY . .\n"
            "EXPOSE 8000\n"
            "CMD [\"uvicorn\", \"src.app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n"
        )
    with open(os.path.join(base, "README.md"), "w") as f:
        f.write(f"# {os.path.basename(base)}\nScalable template project.\n")


def create_modular_structure(base):
    """
    Template Modular:
    Estrutura:
      modular/
      ├── src/
      │   ├── module1/
      │   │   ├── __init__.py
      │   │   └── endpoints.py
      │   ├── module2/
      │   │   ├── __init__.py
      │   │   └── endpoints.py
      │   └── server.py
      ├── tests/
      │   └── __init__.py
      ├── requirements.txt
      ├── Dockerfile
      └── README.md
    """
    os.makedirs(os.path.join(base, "src", "module1"), exist_ok=True)
    os.makedirs(os.path.join(base, "src", "module2"), exist_ok=True)
    os.makedirs(os.path.join(base, "tests"), exist_ok=True)

    # src/module1/__init__.py
    with open(os.path.join(base, "src", "module1", "__init__.py"), "w") as f:
        f.write("# Módulo 1\n")
    # src/module1/endpoints.py
    with open(os.path.join(base, "src", "module1", "endpoints.py"), "w") as f:
        f.write(
            "from fastapi import APIRouter\n"
            "router = APIRouter()\n\n"
            "@router.get('/module1')\n"
            "def get_module1():\n"
            "    return {'message': 'Hello from Module 1'}\n"
        )
    # src/module2/__init__.py
    with open(os.path.join(base, "src", "module2", "__init__.py"), "w") as f:
        f.write("# Módulo 2\n")
    # src/module2/endpoints.py
    with open(os.path.join(base, "src", "module2", "endpoints.py"), "w") as f:
        f.write(
            "from fastapi import APIRouter\n"
            "router = APIRouter()\n\n"
            "@router.get('/module2')\n"
            "def get_module2():\n"
            "    return {'message': 'Hello from Module 2'}\n"
        )
    # src/server.py que integra os módulos
    os.makedirs(os.path.join(base, "src"), exist_ok=True)
    with open(os.path.join(base, "src", "server.py"), "w") as f:
        f.write(
            "from fastapi import FastAPI\n"
            "from module1.endpoints import router as module1_router\n"
            "from module2.endpoints import router as module2_router\n\n"
            "app = FastAPI()\n\n"
            "app.include_router(module1_router, prefix='/m1')\n"
            "app.include_router(module2_router, prefix='/m2')\n"
            "\n"
            "@app.get('/')\n"
            "def read_root():\n"
            "    return {'message': 'Hello from Modular template'}\n"
        )
    with open(os.path.join(base, "tests", "__init__.py"), "w") as f:
        f.write("# Modular template tests\n")
    with open(os.path.join(base, "requirements.txt"), "w") as f:
        f.write("fastapi\nuvicorn\n")
    with open(os.path.join(base, "Dockerfile"), "w") as f:
        f.write(
            "FROM python:3.9-slim\n"
            "WORKDIR /app\n"
            "COPY requirements.txt ./\n"
            "RUN pip install --no-cache-dir -r requirements.txt\n"
            "COPY src ./src\n"
            "EXPOSE 8000\n"
            "CMD [\"uvicorn\", \"src.server:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n"
        )
    with open(os.path.join(base, "README.md"), "w") as f:
        f.write(f"# {os.path.basename(base)}\nModular template project.\n")


@click.group()
def cli():
    """CLI para inicializar projetos FastAPI com diferentes templates.
    
    Templates disponíveis: default, minimal, advanced, enterprise, microservice, scalable, modular, aws.
    """
    pass

@cli.command()
@click.argument('project_name')
@click.option('--template', default='default', help='Template a ser utilizado (default, minimal, advanced, enterprise, microservice, scalable, modular, aws)')
@click.option("--path", default=".", help="Diretório base onde o projeto será criado")
def init(project_name, template, path):
    """
    Cria a estrutura do projeto a partir do diretório informado usando o template selecionado.

    Exemplo:
      fastapi-starter init meu_projeto --template aws
    """
    try:
        project_path = os.path.join(path, project_name)
        if os.path.exists(project_path):
            click.echo(f"O diretório '{project_path}' já existe.")
            use_existing = click.confirm("Deseja usar esse diretório existente?", default=True)
            if not use_existing:
                click.echo("Operação cancelada.")
                sys.exit(1)
        else:
            create_new = click.confirm("O diretório não existe. Deseja criar um novo projeto?", default=True)
            if create_new:
                os.makedirs(project_path)
            else:
                click.echo("Operação cancelada.")
                sys.exit(1)

        if template == 'default':
            create_default_structure(project_path)
        elif template == 'minimal':
            create_minimal_structure(project_path)
        elif template == 'advanced':
            create_advanced_structure(project_path)
        elif template == 'enterprise':
            create_enterprise_structure(project_path)
        elif template == 'microservice':
            create_microservice_structure(project_path)
        elif template == 'scalable':
            create_scalable_structure(project_path)
        elif template == 'modular':
            create_modular_structure(project_path)
        elif template == 'aws':
            create_aws_structure(project_path)
        else:
            available = ['default', 'minimal', 'advanced', 'enterprise', 'microservice', 'scalable', 'modular', 'aws']
            click.echo(f"Template '{template}' não encontrado. Templates disponíveis: {', '.join(available)}")
            sys.exit(1)

        click.echo(f"Projeto '{project_name}' criado com sucesso usando o template '{template}' em {project_path}")

    except Exception as e:
        click.echo(f"Erro ao criar o projeto: {e}")
        sys.exit(1)

if __name__ == '__main__':
    cli()
