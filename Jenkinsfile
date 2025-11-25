// Integrantes: Diego Henríquez y
// Sección: OCY1102


pipeline {
    agent any

    environment {
        IMAGE_NAME = "vulnerable-app"
        CONTAINER_NAME = "vulnerable-app-container"
        NETWORK_NAME = "red-ciberseguridad"
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
                    echo '🔨 Construyendo imagen (Forzando actualización de librerías)...'
                    sh "docker build --no-cache -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                    sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
                }
            }
        }

        stage('Despliegue (Deploy)') {
            steps {
                script {
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rm ${CONTAINER_NAME} || true"
                    
                    sh """
                        docker run -d \
                        --name ${CONTAINER_NAME} \
                        --network ${NETWORK_NAME} \
                        -p 5001:5000 \
                        ${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Pentesting (OWASP ZAP)') {
            steps {
                script {
                    echo '⏳ Esperando 10 segundos para que la app inicie...'
                    sleep 10
                    
                    // 1. Preparar carpeta en Jenkins para recibir el archivo
                    sh "rm -rf zap_reports"
                    sh "mkdir -p zap_reports"

                    // 2. Limpiar cualquier contenedor ZAP previo atascado
                    sh "docker rm -f zap-scanner || true"

                    echo '🔥 Ejecutando ZAP...'
                    // TRUCO: 
                    // - Usamos --name zap-scanner para poder referenciarlo después.
                    // - Usamos -v /zap/wrk (sin ruta host) para crear un volumen interno temporal donde ZAP pueda escribir.
                    // - NO usamos --rm, para que el contenedor exista lo suficiente para copiar el archivo.
                    sh """
                        docker run \
                        --name zap-scanner \
                        --network ${NETWORK_NAME} \
                        -u 0 \
                        -v /zap/wrk \
                        -t zaproxy/zap-stable \
                        /zap/zap-full-scan.py \
                        -t http://${CONTAINER_NAME}:5000 \
                        -r zap_report.html \
                        -I || true
                    """
                    
                    echo '📥 Extrayendo reporte del contenedor...'
                    // Copiamos el archivo desde dentro del contenedor hacia la carpeta de Jenkins
                    sh "docker cp zap-scanner:/zap/wrk/zap_report.html ./zap_reports/zap_report.html"
                    
                    // Ahora sí, borramos el contenedor de ZAP
                    sh "docker rm zap-scanner"
                }
            }
        }
    }

    post {
        always {
            echo '📄 Archivando reporte...'
            archiveArtifacts artifacts: 'zap_reports/zap_report.html', allowEmptyArchive: true
        }
    }
}