pipeline {
    agent any

    environment {
        // Nombre de la imagen que crearemos
        IMAGE_NAME = "vulnerable-app"
    }

    stages {
        stage('Inicio') {
            steps {
                // [cite: 5] Integrante: Diego Henríquez
                echo 'Iniciando el Pipeline de Evaluación de Ciberseguridad...'
            }
        }

        stage('Construcción (Build)') {
            steps {
                script {
                    echo 'Construyendo la imagen Docker...'
                    // Este comando usa el Docker del host para construir la imagen basada en tu Dockerfile
                    sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                }
            }
        }
        
        stage('Prueba Básica') {
            steps {
                echo 'Verificando que la imagen se creó...'
                sh "docker images | grep ${IMAGE_NAME}"
            }
        }
    }
}