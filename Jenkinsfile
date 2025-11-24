pipeline {
    agent any

    environment {
        IMAGE_NAME = "vulnerable-app"
        CONTAINER_NAME = "vulnerable-app-container"
    }

    stages {
        stage('Inicio') {
            steps {
                // RECUERDA: Cambiar NOMBRE_INTEGRANTE por tu nombre real
                echo 'Iniciando Pipeline - Integrante: NOMBRE_INTEGRANTE' 
            }
        }

        stage('Construcción (Build)') {
            steps {
                script {
                    echo '🔨 Construyendo imagen Docker...'
                    sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                    sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
                }
            }
        }

        stage('Despliegue (Deploy)') {
            steps {
                script {
                    echo '🚀 Desplegando aplicación...'
                    
                    // 1. Detener y borrar el contenedor anterior si existe (para evitar errores de nombre duplicado)
                    // El '|| true' hace que no falle si el contenedor no existía antes
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rm ${CONTAINER_NAME} || true"
                    
                    // 2. Correr el nuevo contenedor
                    // --network red-ciberseguridad: IMPORTANTE para que Jenkins y ZAP lo vean
                    // -p 5001:5000: Mapeamos al puerto 5001 de tu PC (por si el 5000 está ocupado)
                    sh """
                        docker run -d \
                        --name ${CONTAINER_NAME} \
                        --network red-ciberseguridad \
                        -p 5001:5000 \
                        ${IMAGE_NAME}:latest
                    """
                }
            }
        }
        
        stage('Verificación') {
            steps {
                // Esperamos 5 segundos para que Flask arranque bien
                sleep 5
                echo '✅ Verificando que el contenedor está vivo...'
                sh "docker ps | grep ${CONTAINER_NAME}"
            }
        }
    }
}